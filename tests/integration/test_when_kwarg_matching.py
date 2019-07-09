from unittest import TestCase
from unittest.mock import Mock

from parameterized import parameterized

from known_side_effects import UnmatchedArguments
from known_side_effects import AnyArg, NotNone
from known_side_effects import when


class TestBasicKwargs(TestCase):

    def setUp(self):
        self.mock = Mock()

    @parameterized.expand([
        ({'arg': 'string'}, Mock()),
        ({'arg': tuple([1])}, Mock()),
        ({'arg': {'1': 1}}, Mock()),
        ({'arg': {1}}, Mock()),
        ({'arg': 1}, Mock()),
        ({'arg': [1]}, Mock()),
        ({'arg': object()}, Mock()),
        ((
            {
                'arg': 'string',
                'arg1': tuple([1]),
                'arg2': {'1': 1},
                'arg3': {1},
                'arg4': 1,
                'arg5': [1],
                'arg6': object(),
            }
        ), Mock()),
    ])
    def test_kwargs(self, kwargs, response):
        when(self.mock, **kwargs).then(response)
        self.assertEqual(self.mock(**kwargs), response)

    def test_order_does_not_breaks_matching_kwargs(self):
        """
        Re arranging kwargs should have no effect
        """
        response = Mock()
        when(self.mock, arg_1='2', arg_2=1).then(response)

        self.assertEqual(
            self.mock(arg_2=1, arg_1='2'),
            response,
        )

    def test_error_raised_on_no_match_same_keyword(self):
        when(self.mock, arg_1=Mock()).then(Mock())

        with self.assertRaises(UnmatchedArguments) as raised:
            argument = Mock()
            self.mock(arg_1=argument)
            self.assertEqual(
                raised.exception.args[0],
                UnmatchedArguments.ERROR_MSG.format(
                    args=tuple(),
                    kwargs={'arg_1': argument},
                ),
            )

    def test_error_raised_on_no_match_different_keyword(self):
        when(self.mock, arg_1=Mock()).then(Mock())

        with self.assertRaises(UnmatchedArguments) as raised:
            argument = Mock()
            self.mock(arg_2=argument)
            self.assertEqual(
                raised.exception.args[0],
                UnmatchedArguments.ERROR_MSG.format(
                    args=tuple(),
                    kwargs={'arg_2': argument},
                ),
            )

    def test_error_raised_on_argument_length_mismatch_args(self):
        argument = Mock()
        when(self.mock, arg=argument).then(Mock())

        with self.assertRaises(UnmatchedArguments) as raised:
            self.mock(arg=argument, arg1='1')
            self.assertEqual(
                raised.exception.args[0],
                UnmatchedArguments.ERROR_MSG.format(
                    args=tuple(),
                    kwargs={'arg': argument, 'arg1': '1'},
                ),
            )


class TestMatcherKwargs(TestCase):
    def setUp(self):
        self.mock = Mock()

    def test_single_matcher_kwarg(self):
        response = Mock()

        when(self.mock, arg=AnyArg()).then(response)

        self.assertEqual(
            self.mock(arg=object()),
            response,
        )

    def test_matcher_kwarg_and_basic_kwargs(self):
        response = Mock()
        argument_1 = Mock()
        when(self.mock, arg=argument_1, arg1=AnyArg()).then(response)

        self.assertEqual(
            self.mock(arg=argument_1, arg1=object()),
            response,
        )

    def test_order_does_non_breaks_matching_kwargs(self):
        response = Mock()
        argument_1 = Mock()

        when(self.mock, arg=argument_1, arg1=AnyArg()).then(response)

        self.assertEqual(
            self.mock(arg1=object(), arg=argument_1),
            response,
        )

    def test_error_raised_on_no_match_kwargs(self):
        when(self.mock, arg=NotNone()).then(Mock())

        with self.assertRaises(UnmatchedArguments) as raised:
            argument = None
            self.mock(arg=argument)

        self.assertEqual(
            raised.exception.args[0],
            UnmatchedArguments.ERROR_MSG.format(
                args=tuple(),
                kwargs={'arg': argument},
            ),
        )
