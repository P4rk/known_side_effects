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
