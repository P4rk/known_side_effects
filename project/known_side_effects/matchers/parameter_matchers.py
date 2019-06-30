from typing import List, Any, Dict

from hamcrest.core.matcher import Matcher

__all__ = [
    'match_arguments',
    'match_kwarg',
]


def _check_hamcrest_matcher(matcher: Matcher, item: Any) -> bool:
    # Add mismatch description
    if matcher.matches(item):
        return True
    else:
        # call mismatch description
        # TODO log mismatch
        return False


def match_arguments(expected_args: List[Any], actual_args: List[Any]) -> bool:
    expected_args_length = len(expected_args)
    actual_args_length = len(actual_args)
    if expected_args_length != actual_args_length:
        # TODO log mismatch
        return False

    zero_args = expected_args_length == 0 and actual_args_length == 0
    match = True if zero_args else False

    for index, arg_to_match in enumerate(expected_args):
        arg = actual_args[index]
        if isinstance(arg_to_match, Matcher):
            match = _check_hamcrest_matcher(arg_to_match, arg)
            if match:
                continue
            else:
                break
        else:
            match = arg_to_match == arg
            if match:
                continue
            else:
                break

    return match


def match_kwarg(expected_kwargs: Dict[str, Any], actual_kwars: Dict[str, Any]):
    expected_items = expected_kwargs.items()
    actual_items = actual_kwars.items()

    if len(expected_items) != len(actual_items):
        # TODO log mismatch
        return False

    for expected_key, expected_value in expected_items:
        matched = False
        for actual_key, actual_value in actual_items:
            matched_expected_key = expected_key == actual_key

            if matched_expected_key:
                matched = match_arguments([expected_value], [actual_value])
            if matched:
                # TODO consider removing the matched item
                break

        if not matched:
            # TODO log mismatch
            return False

    return True


