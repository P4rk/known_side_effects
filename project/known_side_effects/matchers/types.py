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


from abc import ABC

from hamcrest.core.matcher import Matcher


class Any(Matcher):
    def matches(self, item, mismatch_description=None):
        return True

    def describe_mismatch(self, item, mismatch_description):
        return f'Any Match should match {item}'

    def describe_to(self, description):
        description.append_text('Matches any item')


class NotNone(Matcher):
    def matches(self, item, mismatch_description=None):
        return item is not None

    def describe_mismatch(self, item, mismatch_description):
        return f'item: {item} is None, expected to not be'

    def describe_to(self, description):
        description.append_text('Matches any not None item')


class AnyX(Matcher, ABC):
    type_ = None

    def matches(self, item, mismatch_description=None):
        return isinstance(item, self.type_)

    def describe_mismatch(self, item, mismatch_description):
        return f'{item} is not of type {self.type_}, expected to not be'

    def describe_to(self, description):
        description.append_text(f'of type {self.type_}')


class AnyString(AnyX):
    type_ = str


class AnyTuple(AnyX):
    type_ = tuple


class AnyDict(AnyX):
    type_ = dict


class AnySet(AnyX):
    type_ = set


class AnyInt(AnyX):
    type_ = int


class AnyList(AnyX):
    type_ = list


class AnyObject(AnyX):
    type_ = object


class AnyBool(AnyX):
    type_ = bool
