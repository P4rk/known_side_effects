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
from known_side_effects.matchers.parameter_matchers import (
    match_arguments,
    match_kwarg,
)


def called_arguments_match(when, arguments, kwargs):
    """
    Used to match arguments against the when call to invoke the response
    """
    args_match = match_arguments(when.expected_arguments, arguments)
    kwargs_match = match_kwarg(when.expected_kwargs, kwargs)
    return args_match and kwargs_match


def when_arguments_match(when, arguments, kwargs):
    """
    Used to match if the _same_ when function has been called, so that
    it is possible to chain multiple returns.
    Not used to match arguments against the when call that invoke the
    response
    """
    arg_match = when.expected_arguments == arguments
    kwargs_match = when.expected_kwargs == kwargs
    return arg_match and kwargs_match
