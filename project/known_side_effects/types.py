from unittest.mock import Mock

from known_side_effects.exceptions import UnmatchedArguments
from known_side_effects.matchers.parameter_matchers import match_arguments, match_kwarg

mock_to_seg = dict()


def given(mock: Mock):
    global mock_to_seg
    seg = mock_to_seg.get(mock, SideEffectGenerator())
    mock.side_effect = seg
    mock_to_seg[mock] = seg
    return seg


def reset(mock: Mock):
    global mock_to_seg
    seg = mock_to_seg[mock]
    seg.whens = []


class SideEffectGenerator:
    def __init__(self):
        self.whens = []

    def when(self, *arguments, **kwargs):
        when = When(self, arguments, kwargs)
        self.whens.append(when)
        return when

    def __call__(self, *args, **kwargs):
        """
        side_effect
        """
        for when in self.whens:
            if when.arguments_match(args, kwargs):
                return when.get_response()
        raise UnmatchedArguments(*args, **kwargs)


class When:
    def __init__(self, parent_side_effect, expected_arguments, expected_kwargs):
        self.expected_arguments = expected_arguments
        self.expected_kwargs = expected_kwargs
        self.parent_side_effect = parent_side_effect
        self._responses = []

    def arguments_match(self, arguments, kwargs):
        args_match = match_arguments(self.expected_arguments, arguments)
        kwargs_match = match_kwarg(self.expected_kwargs, kwargs)
        return args_match and kwargs_match

    def then(self, response):
        self._responses.append(response)
        return self

    def get_response(self):
        response = self._responses[0]
        if len(self._responses) > 1:
            response = self._responses.pop(0)

        if isinstance(response, Exception):
            raise response
        return response
