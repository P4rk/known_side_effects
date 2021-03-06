from unittest import TestCase
import known_side_effects

from unittest.mock import Mock
from parameterized import parameterized

from known_side_effects import UnmatchedArguments
from known_side_effects import AnyArg, NotNone


known_side_effects.extend(Mock)


class TestBasicArguments(TestCase):

    def setUp(self):
        self.mock = Mock()

    @parameterized.expand([
        (('string',), Mock()),
        ((tuple([1]),), Mock()),
        (({'1': 1},), Mock()),
        (({1},), Mock()),
        ((1,), Mock()),
        (([1],), Mock()),
        ((object(),), Mock()),
        (
            (
                'string',
                tuple([1]),
                {'1': 1},
                {1},
                1,
                [1],
                object(),
            ),
            Mock(),
        ),
    ])
    def test_args(self, arguments, response):
        self.mock.when(*arguments).then(response)
        self.assertEqual(self.mock(*arguments), response)

    def test_order_breaks_matching_args(self):
        self.mock.when('2', 1).then(Mock())

        with self.assertRaises(UnmatchedArguments) as raised:
            self.mock(1, '2')

        self.assertEqual(
            raised.exception.args[0],
            UnmatchedArguments.ERROR_MSG.format(
                args=(1, '2'),
                kwargs={},
            ),
        )

    def test_error_raised_on_no_match_args(self):
        self.mock.when(Mock()).then(Mock())

        with self.assertRaises(UnmatchedArguments) as raised:
            argument = Mock()
            self.mock(argument)
            self.assertEqual(
                raised.exception.args[0],
                UnmatchedArguments.ERROR_MSG.format(
                    args=(argument,),
                    kwargs={},
                ),
            )

    def test_error_raised_on_argument_length_mismatch_args(self):
        argument = Mock()
        self.mock.when(argument).then(Mock())

        with self.assertRaises(UnmatchedArguments) as raised:
            self.mock(argument, '1')
            self.assertEqual(
                raised.exception.args[0],
                UnmatchedArguments.ERROR_MSG.format(
                    args=(argument, '1'),
                    kwargs={},
                ),
            )


class TestMatcherArguments(TestCase):
    def setUp(self):
        self.mock = Mock()

    def test_single_matcher_argument_args(self):
        response = Mock()

        self.mock.when(AnyArg()).then(response)

        self.assertEqual(
            self.mock(object()),
            response,
        )

    def test_matcher_argument_and_basic_argument_args(self):
        response = Mock()
        argument_1 = Mock()
        self.mock.when(argument_1, AnyArg()).then(response)

        self.assertEqual(
            self.mock(argument_1, object()),
            response,
        )

    def test_order_breaks_matching_args(self):
        response = Mock()
        argument_1 = Mock()

        self.mock.when(argument_1, AnyArg()).then(response)

        bad_argument_1 = object()
        with self.assertRaises(UnmatchedArguments) as raised:
            self.mock(bad_argument_1, argument_1)

        self.assertEqual(
            raised.exception.args[0],
            UnmatchedArguments.ERROR_MSG.format(
                args=(bad_argument_1, argument_1),
                kwargs={},
            ),
        )

    def test_error_raised_on_no_match_args(self):
        self.mock.when(NotNone()).then(Mock())

        with self.assertRaises(UnmatchedArguments) as raised:
            argument = None
            self.mock(argument)

        self.assertEqual(
            raised.exception.args[0],
            UnmatchedArguments.ERROR_MSG.format(
                args=(argument,),
                kwargs={},
            ),
        )
