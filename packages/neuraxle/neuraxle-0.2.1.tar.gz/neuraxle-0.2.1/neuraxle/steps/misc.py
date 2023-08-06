"""
Miscelaneous Pipeline Steps
====================================
You can find here misc. pipeline steps, for example, callbacks useful for debugging, and a step cloner.

..
    Copyright 2019, Neuraxio Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

import hashlib
import time
from abc import ABC, abstractmethod

from neuraxle.pipeline import Pipeline

VALUE_CACHING = 'value_caching'
from typing import List, Any

from neuraxle.base import BaseStep, NonFittableMixin, NonTransformableMixin, DataContainer


class BaseCallbackStep(BaseStep, ABC):
    """Base class for callback steps."""

    def __init__(self, callback_function, more_arguments: List = tuple(),
                 hyperparams=None, fit_callback_function=None, transform_function=None):
        """
        Create the callback step with a function and extra arguments to send to the function

        :param callback_function: The function that will be called on events.
        :param more_arguments: Extra arguments that will be sent to the callback after the processed data (optional).
        """
        BaseStep.__init__(self, hyperparams=hyperparams)
        self.transform_function = transform_function
        self.callback_function = callback_function
        self.fit_callback_function = fit_callback_function
        self.more_arguments = more_arguments

    def _fit_callback(self, data_inputs, expected_outputs):
        """
        Will call the self.fit_callback_function() with the data being processed and the extra arguments specified.
        It has no other effect.

        :param data_inputs: data inputs to fit
        :param expected_outputs: expected outputs to fit

        :return: self
        """
        self.fit_callback_function((data_inputs, expected_outputs), *self.more_arguments)

    def _callback(self, data):
        """
        Will call the self.callback_function() with the data being processed and the extra arguments specified.
        It has no other effect.

        :param data_inputs: the data to process
        :return: None
        """
        self.callback_function(data, *self.more_arguments)


class FitCallbackStep(NonTransformableMixin, BaseCallbackStep):
    """Call a callback method on fit."""

    def fit(self, data_inputs, expected_outputs=None) -> 'FitCallbackStep':
        """
        Will call the self._callback() with the data being processed and the extra arguments specified.
        Note that here, the data to process is packed into a tuple of (data_inputs, expected_outputs).
        It has no other effect.

        :param data_inputs: the data to process
        :param expected_outputs: the data to process
        :return: self
        """
        self._callback((data_inputs, expected_outputs))
        return self


class TransformCallbackStep(NonFittableMixin, BaseCallbackStep):
    """Call a callback method on transform and inverse transform."""

    def fit_transform(self, data_inputs, expected_outputs=None) -> ('BaseStep', Any):
        self._callback(data_inputs)

        if self.transform_function is not None:
            return self, self.transform_function(data_inputs)
        return self, data_inputs

    def transform(self, data_inputs):
        """
        Will call the self._callback() with the data being processed and the extra arguments specified.
        It has no other effect.

        :param data_inputs: the data to process
        :return: the same data as input, unchanged (like the Identity class).
        """
        self._callback(data_inputs)
        if self.transform_function is not None:
            return self.transform_function(data_inputs)

        return data_inputs

    def inverse_transform(self, processed_outputs):
        """
        Will call the self._callback() with the data being processed and the extra arguments specified.
        It has no other effect.

        :param processed_outputs: the data to process
        :return: the same data as input, unchanged (like the Identity class).
        """
        self._callback(processed_outputs)
        return processed_outputs


class FitTransformCallbackStep(BaseStep):
    def __init__(self, transform_callback_function, fit_callback_function, more_arguments: List = tuple(),
                 transform_function=None,
                 hyperparams=None):
        BaseStep.__init__(self, hyperparams)
        self.transform_function = transform_function
        self.more_arguments = more_arguments
        self.fit_callback_function = fit_callback_function
        self.transform_callback_function = transform_callback_function

    def fit(self, data_inputs, expected_outputs=None):
        self.fit_callback_function((data_inputs, expected_outputs), *self.more_arguments)
        return self

    def transform(self, data_inputs):
        self.transform_callback_function(data_inputs, *self.more_arguments)
        if self.transform_function is not None:
            return self.transform_function(data_inputs)
        return data_inputs

    def fit_transform(self, data_inputs, expected_outputs=None) -> ('BaseStep', Any):
        self.fit_callback_function((data_inputs, expected_outputs), *self.more_arguments)
        self.transform_callback_function(data_inputs, *self.more_arguments)
        if self.transform_function is not None:
            return self, self.transform_function(data_inputs)

        return self, data_inputs


class TapeCallbackFunction:
    """This class's purpose is to be sent to the callback to accumulate information.

    Example usage:

    .. code-block:: python

        expected_tape = ["1", "2", "3", "a", "b", "4"]
        tape = TapeCallbackFunction()

        p = Pipeline([
            Identity(),
            TransformCallbackStep(tape.callback, ["1"]),
            TransformCallbackStep(tape.callback, ["2"]),
            TransformCallbackStep(tape.callback, ["3"]),
            AddFeatures([
                TransformCallbackStep(tape.callback, ["a"]),
                TransformCallbackStep(tape.callback, ["b"]),
            ]),
            TransformCallbackStep(tape.callback, ["4"]),
            Identity()
        ])
        p.fit_transform(np.ones((1, 1)))

        assert expected_tape == tape.get_name_tape()

    """

    def __init__(self):
        """Initialize the tape (cache lists)."""
        self.data: List = []
        self.name_tape: List[str] = []

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)

    def callback(self, data, name: str = ""):
        """
        Will stick the data and name to the tape.

        :param data: data to save
        :param name: name to save (string)
        :return: None
        """
        self.data.append(data)
        self.name_tape.append(name)

    def get_data(self) -> List:
        """
        Get the data tape

        :return: The list of data.
        """
        return self.data

    def get_name_tape(self) -> List[str]:
        """
        Get the data tape

        :return: The list of names.
        """
        return self.name_tape

class Sleep(NonFittableMixin, BaseStep):
    def __init__(self, sleep_time=0.1, hyperparams=None, hyperparams_space=None):
        BaseStep.__init__(self, hyperparams=hyperparams, hyperparams_space=hyperparams_space)
        self.sleep_time = sleep_time

    def transform(self, data_inputs):
        time.sleep(self.sleep_time)
        return data_inputs


class DataShuffler:
    pass  # TODO.

    def load(self, pipeline: 'Pipeline', data_container: DataContainer) -> 'Pipeline':
        return pipeline


class BaseValueHasher(ABC):
    @abstractmethod
    def hash(self, data_input):
        raise NotImplementedError()


class Md5Hasher(BaseValueHasher):
    def hash(self, data_input):
        m = hashlib.md5()
        m.update(str.encode(str(data_input)))

        return m.hexdigest()


