import known_side_effects
from unittest import TestCase
from unittest.mock import Mock


known_side_effects.extend(Mock)


class TestBasicArgumentsAndBasicKwargs(TestCase):
    pass


class TestMatcherArgumentsAndBasicKwargs(TestCase):
    pass


class TestBasicArgumentsAndMatcherKwargs(TestCase):
    pass


class TestMatcherArgumentsAndMatcherKwargs(TestCase):
    pass

