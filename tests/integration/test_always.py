from unittest import TestCase
from unittest.mock import Mock


class AlwaysTestCase(TestCase):

    def setUp(self):
        self.mock = Mock()
        self.argument = Mock()
        self.exception = Exception()
        self.response = Mock()

    def test_always(self):
        self.mock.when(self.argument).then(Mock())
        self.mock.when().always(self.response)

        self.assertEqual(
            self.mock(self.argument),
            self.response,
        )

    def test_always_raise(self):
        self.mock.when(self.argument).then(Mock())
        self.mock.when().always_raise(self.exception)

        with self.assertRaises(Exception) as raised:
            self.mock(self.argument)

        self.assertEqual(
            raised.exception,
            self.exception,
        )
