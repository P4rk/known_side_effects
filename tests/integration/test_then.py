from unittest import TestCase
from unittest.mock import Mock

from known_side_effects.matchers.types import Any
from known_side_effects.types import given


class TestReturnValues(TestCase):

    def setUp(self):
        self.mock = Mock()

    def test_returns_non_exception(self):
        response = Mock()
        given(self.mock).when(Any()).then(response)

        self.assertEqual(
            self.mock('1'),
            response
        )


class TestRaiseValues(TestCase):
    def setUp(self):
        self.mock = Mock()

    def test_raises_exception(self):
        response = Exception('Test Exception')
        given(self.mock).when(Any()).then(response)

        with self.assertRaises(Exception) as raised:
            self.mock('1')

        self.assertEqual(
            raised.exception,
            response
        )


class TestMultipleValues(TestCase):

    def setUp(self):
        self.mock = Mock()
        self.response_1 = Mock()
        self.response_2 = Mock()
        self.response_3 = Exception('test exception')
        given(self.mock).when(Any()).then(self.response_1).then(self.response_2).then(self.response_3)

    def test_multiple_then(self):
        argument = object()

        self.assertEqual(
            self.mock(argument),
            self.response_1,
        )
        self.assertEqual(
            self.mock(argument),
            self.response_2,
        )
        with self.assertRaises(Exception) as raised:
            self.mock(argument)

        self.assertEqual(
            raised.exception,
            self.response_3,
        )
