"""
MIT License

Copyright (c) 2019 Luke Park

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from known_side_effects.exceptions import UnmatchedArguments
from known_side_effects.matchers.parameter_matchers import (
    match_arguments,
    match_kwarg,
)


class SideEffectGenerator:
    def __init__(self):
        self.whens = []

    def when(self, *arguments, **kwargs):
        when = When(self, arguments, kwargs)
        self.whens.append(when)
        return when

    def __call__(self, *args, **kwargs):
        """
        side_effect
        """
        for when in self.whens:
            if when.arguments_match(args, kwargs):
                return when.get_response()
        raise UnmatchedArguments(*args, **kwargs)


class When:
    def __init__(self, parent_side_effect, expected_arguments, expected_kwargs):
        self.expected_arguments = expected_arguments
        self.expected_kwargs = expected_kwargs
        self.parent_side_effect = parent_side_effect
        self._responses = []

    def arguments_match(self, arguments, kwargs):
        args_match = match_arguments(self.expected_arguments, arguments)
        kwargs_match = match_kwarg(self.expected_kwargs, kwargs)
        return args_match and kwargs_match

    def then(self, response):
        self._responses.append(response)
        return self

    def get_response(self):
        response = self._responses[0]
        if len(self._responses) > 1:
            response = self._responses.pop(0)

        if isinstance(response, Exception):
            raise response
        return response
