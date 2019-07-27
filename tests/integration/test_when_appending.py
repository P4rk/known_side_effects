from unittest import TestCase
from unittest.mock import Mock

from known_side_effects import AnyArg


class WhenAppendingTestCase(TestCase):
    def setUp(self):
        self.mock = Mock()
        self.response = Mock()
        self.argument = Mock()
        self.exception = Exception()

    def test_adding_matching_when(self):
        self.mock.when(AnyArg()).then(self.response)
        self.mock.when(self.argument).then_raise(self.exception)

        self.assertEqual(
            len(self.mock.side_effect._whens),
            2,
        )

    def test_adding_the_same_when(self):
        self.mock.when(self.argument).then_raise(self.exception)
        self.mock.when(self.argument).then(self.response)

        self.assertEqual(
            len(self.mock.side_effect._whens),
            1,
        )
