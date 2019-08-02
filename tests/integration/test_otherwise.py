import known_side_effects

from unittest import TestCase
from unittest.mock import Mock

known_side_effects.extend(Mock)


class OtherwiseTestCase(TestCase):

    def setUp(self):
        self.mock = Mock()
        self.response = Mock()
        self.exception = Exception()

    def test_otherwise(self):
        self.mock.when(Mock()).then(Mock()).otherwise(self.response)

        self.assertEqual(
            self.mock(Mock()),
            self.response,
        )

    def test_not_otherwise(self):
        expected_arg = 'arg1'
        self.mock.when(Mock()).then(Mock()).otherwise(Mock())
        self.mock.when(expected_arg).then(self.response)

        self.assertEqual(
            self.mock(expected_arg),
            self.response,
        )

    def test_just_otherwise(self):
        self.mock.when().otherwise(self.response)

        self.assertEqual(
            self.mock(Mock()),
            self.response,
        )

    def test_otherwise_raise(self):
        self.mock.when(Mock()).then(Mock()).otherwise_raise(
            self.exception,
        )

        with self.assertRaises(Exception) as raised:
            self.mock(Mock)

        self.assertEqual(
            raised.exception,
            self.exception,
        )


