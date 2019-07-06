# Known Side Effects

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/393832636c36453eb382b56b4f6dcb0f)](https://www.codacy.com/app/P4rk/known_side_effects?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=P4rk/known_side_effects&amp;utm_campaign=Badge_Grade)
[![Coverage Badge](https://img.shields.io/badge/coverage-95%25-lgreen.svg)](https://shields.io/)
[![Python version badge](https://img.shields.io/badge/python-3.6+-blue.svg)](https://shields.io/)
[![Licence badge](https://img.shields.io/badge/license-MIT-green.svg)](https://shields.io/)


A test utility library to help write explict side effects for mocked objects.

Mocks side effects are manipulated by `when` and `then` functions.

```python
from known_side_effects import when
...
when(...).then(...)
```
You manipulate a specific mocks side effect by passing them to the first parameter in the when function.

```python
from known_side_effects import when
...
when(mock, ...).then(...)
```
## When

All parameters in the `when` function after the mock, are used to define the expected parameters for the side effect.

```python
from known_side_effects import when
...
when(mock, 'argument_one', arg='argument_two').then(...)
```
If the mock is called with parameters that don't match any of the specified parameter sets then an `UnmatchedArguments` exception is raised. The arguments have to match exactly.

E.g. Given `when(mock, 'argument_one', arg='argument_two').then(...)` when the mock is called with the parameters in the table below an `UnmatchedArguments` is either raised or not raised. 

| Parameters 									     | Raises |
|--------------------------------------------|--------|
| `mock('argument_one', arg='argument_two')` | False  |
| `mock(arg='argument_two')`                 | True   |
| `mock('argument_one')` 					     | True   | 


Multiple sets of parameters to match can be specified.

```python
from known_side_effects import when
...
when(mock, 'first_specified_argument').then(...)
when(mock, 'second_specified_argument').then(...)
when(mock, 'third_specified_argument').then(...)
```


## Then
The `then` function specifies what the known side effect should do when parameters are matched. By default it will just return what has been passed into the `then` function. 

```python
from unittest.mock import Mock
from known_side_effects import when, Any
...
response_one = Mock()
mock = Mock()

when(mock, ...).then(response_one)

assert mock(...) == response_one
```

However if the parameter is an instance of an exception then, when the known side effect is matched the exception will be raised instead of returned.s

```python
from unittest.mock import Mock
from known_side_effects import when, Any
...
exception = Exception()
mock = Mock()

when(mock, ...).then(exception)

mock(...)  # Raises the exception
```
You can also chain the `then` functions to return multiple different reponses.
Each response will be returned once until the last response. Once the last response is reached then that reponse will be the only thing returned.

```python
from unittest.mock import Mock
from known_side_effects import when, Any
...
exception = Exception()
response_one = Mock()
mock = Mock()

when(mock, ...).then(response_one).then(exception)

assert mock(...) == response_one
mock(...)  # Raises the exception
mock(...)  # Raises the exception
```

## Reset

You can reset the the known side effects on a mock by passing it the `reset` function.

```python
 
from unittest.mock import Mock
from known_side_effects import when, reset
...

mock = Mock()

when(mock, ...).then(...)

reset(mock)

mock(...)  # raises an UnmatchedArguments exception
```


## Gotcha
When calling the `mock` after specifying multiple known side effects, the first matched set of parameters will be executed. The order of matching is the order that the known side effects are defined in. If multiple arguments are specified where one matches a super set of the other (see Matchers) then the first matched will be executed. e.g.

```python
from unittest.mock import Mock
from known_side_effects import when, Any
...
response_one = Mock()
response_two = Mock()
argument_one = Mock()
argument_two = Mock()

when(mock, argument_one).then(response_one)
when(mock, Any()).then(response_two)
...
assert mock(argument_one) == response_one
assert mock(argument_two) == response_two

```
If the order of the known side effects were reversed, the mock would only ever return `response_two`. This is due to the fact that the `Any` matched will match all parameters, therefore never attempting to match `argument_one` as it has already found a match. e.g.

```python
from unittest.mock import Mock
from known_side_effects import when, Any
...
response_one = Mock()
response_two = Mock()
argument_one = Mock()
argument_two = Mock()

when(mock, Any()).then(response_two)        # These two lines have swapped
when(mock, argument_one).then(response_one) # These two lines have swapped

...
# This will raise an AssertionError as calling the mock with argument_one now
# returns response_two and not response_one
assert mock(argument_one) == response_one   
assert mock(argument_two) == response_two

```

## Matchers

Matchers can be passed to known side effects as parameters. They are implementations of [hamcrest matchers](https://github.com/hamcrest/PyHamcrest). Matchers will only match a single parameter.
