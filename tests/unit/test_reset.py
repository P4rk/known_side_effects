from unittest import TestCase
from unittest.mock import Mock

from known_side_effects.exceptions import UnmatchedArguments
from known_side_effects.types import given, reset


class ResettingMocksTestCase(TestCase):

    def test_resetting_mock(self):
        self.mock = Mock()
        argument = Mock()
        response = Mock()

        given(self.mock).when(argument).then(response)

        self.assertEqual(
            self.mock(argument),
            response
        )

        reset(self.mock)

        with self.assertRaises(UnmatchedArguments) as raised:
            self.mock(argument)

        self.assertEqual(
            raised.exception.args[0],
            UnmatchedArguments.ERROR_MSG.format(
                args=(argument,),
                kwargs={},
            ),
        )
