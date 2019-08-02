from unittest import TestCase
import known_side_effects

from unittest.mock import Mock

from known_side_effects import UnmatchedArguments
from known_side_effects import reset


known_side_effects.extend(Mock)


class ResettingMocksTestCase(TestCase):

    def test_resetting_mock(self):
        self.mock = Mock()
        argument = Mock()
        response = Mock()

        self.mock.when(argument).then(response)

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
