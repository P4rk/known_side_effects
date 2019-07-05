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
from typing import List, Any, Dict

from hamcrest.core.matcher import Matcher

__all__ = [
    'match_arguments',
    'match_kwarg',
]


def _check_hamcrest_matcher(matcher: Matcher, item: Any) -> bool:
    # Add mismatch description
    if matcher.matches(item):
        return True
    else:
        # call mismatch description
        # TODO log mismatch
        return False


def match_arguments(expected_args: List[Any], actual_args: List[Any]) -> bool:
    expected_args_length = len(expected_args)
    actual_args_length = len(actual_args)
    if expected_args_length != actual_args_length:
        # TODO log mismatch
        return False

    zero_args = expected_args_length == 0 and actual_args_length == 0
    match = True if zero_args else False

    for index, arg_to_match in enumerate(expected_args):
        arg = actual_args[index]
        if isinstance(arg_to_match, Matcher):
            match = _check_hamcrest_matcher(arg_to_match, arg)
            if match:
                continue
            else:
                break
        else:
            match = arg_to_match == arg
            if match:
                continue
            else:
                break

    return match


def match_kwarg(expected_kwargs: Dict[str, Any], actual_kwars: Dict[str, Any]):
    expected_items = expected_kwargs.items()
    actual_items = actual_kwars.items()

    if len(expected_items) != len(actual_items):
        # TODO log mismatch
        return False

    for expected_key, expected_value in expected_items:
        matched = False
        for actual_key, actual_value in actual_items:
            matched_expected_key = expected_key == actual_key

            if matched_expected_key:
                matched = match_arguments([expected_value], [actual_value])
            if matched:
                # TODO consider removing the matched item
                break

        if not matched:
            # TODO log mismatch
            return False

    return True


