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
from known_side_effects.argument_matcher import called_arguments_match, when_arguments_match
from known_side_effects.exceptions import UnmatchedArguments


class SideEffectFactory:
    def __init__(self):
        self._whens = []
        self._otherwise = None
        self._always = None

    def when(self, *arguments, **kwargs):
        # Attempt to match arguments and return that when rather
        # creating a new one
        for when in self._whens:
            if when_arguments_match(when, arguments, kwargs):
                return when

        when = When(self, arguments, kwargs)
        self._whens.append(when)
        return when

    def return_or_raise(self, response):
        should_raise, response = response
        if should_raise:
            raise response
        return response

    def __call__(self, *args, **kwargs):
        """
        side_effect
        """
        if self._always:
            return self.return_or_raise(self._always)
        for when in self._whens:
            if called_arguments_match(when, args, kwargs):
                response = when.get_response()
                return self.return_or_raise(response)

        if self._otherwise:
            return self.return_or_raise(self._otherwise)

        raise UnmatchedArguments(*args, **kwargs)


class When:
    def __init__(self, parent_side_effect, expected_arguments, expected_kwargs):
        self.expected_arguments = expected_arguments
        self.expected_kwargs = expected_kwargs
        self.parent_side_effect = parent_side_effect
        self._responses = []

    def then(self, response):
        self._responses.append((False, response))
        return self

    def then_raise(self, response):
        self._responses.append((True, response))
        return self

    def get_response(self):
        response = self._responses[0]
        if len(self._responses) > 1:
            response = self._responses.pop(0)
        return response

    def otherwise(self, response):
        self.parent_side_effect._otherwise = (False, response)

    def otherwise_raise(self, response):
        self.parent_side_effect._otherwise = (True, response)

    def always(self, response):
        self.parent_side_effect._always = (False, response)

    def always_raise(self, response):
        self.parent_side_effect._always = (True, response)
