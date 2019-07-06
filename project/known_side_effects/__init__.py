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
from unittest.mock import Mock

from known_side_effects.exceptions import UnmatchedArguments
from known_side_effects.types import SideEffectGenerator
from known_side_effects.matchers.types import (
    Any,
    NotNone,
    AnyX,
    AnyString,
    AnyTuple,
    AnyDict,
    AnySet,
    AnyInt,
    AnyList,
    AnyObject,
    AnyBool,
)

__all__ = [
    'reset',
    'when',
    'UnmatchedArguments',
    'Any',
    'NotNone',
    'AnyX',
    'AnyString',
    'AnyTuple',
    'AnyDict',
    'AnySet',
    'AnyInt',
    'AnyList',
    'AnyObject',
    'AnyBool',
]


mock_to_seg = dict()


def _given(mock: Mock):
    global mock_to_seg
    seg = mock_to_seg.get(mock, SideEffectGenerator())
    mock.side_effect = seg
    mock_to_seg[mock] = seg
    return seg


def reset(mock: Mock):
    global mock_to_seg
    seg = mock_to_seg[mock]
    seg.whens = []


def when(mock: Mock, *args, **kwargs):
    if not isinstance(mock, Mock):
        raise AssertionError(
            f'First argument to when is expected to be a Mock. It was {mock}'
        )
    return _given(mock).when(*args, **kwargs)
