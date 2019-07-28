# Known Side Effects

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/393832636c36453eb382b56b4f6dcb0f)](https://www.codacy.com/app/P4rk/known_side_effects?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=P4rk/known_side_effects&amp;utm_campaign=Badge_Grade)
[![Coverage Badge](https://img.shields.io/badge/coverage-97%25-lgreen.svg)](https://shields.io/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/known-side-effects.svg)](https://pypi.python.org/pypi/known-side-effects/)
[![PyPI version fury.io](https://badge.fury.io/py/known-side-effects.svg)](https://pypi.python.org/pypi/known-side-effects/)
[![PyPI license](https://img.shields.io/pypi/l/known-side-effects.svg)](https://pypi.python.org/pypi/known-side-effects/)





A test utility library to help write explict side effects for mocked objects.

Mocks side effects are manipulated by `when` and `then` functions.

```python
mock.when(...).then(...)
```
## When

All parameters in the `when` function are used to define the expected parameters for the side effect.

```python
mock.when('argument_one', arg='argument_two').then(...)
```
If the mock is called with parameters that don't match any of the specified parameter sets then an `UnmatchedArguments` exception is raised. The arguments have to match exactly.

E.g. Given `mock.when('argument_one', arg='argument_two').then(...)` when the mock is called with the parameters in the table below an `UnmatchedArguments` is either raised or not raised. 

| Parameters 									     | Raises |
|--------------------------------------------|--------|
| `mock('argument_one', arg='argument_two')` | False  |
| `mock(arg='argument_two')`                 | True   |
| `mock('argument_one')` 					     | True   | 


Multiple sets of parameters to match can be specified.

```python
mock.when('first_specified_argument').then(...)
mock.when('second_specified_argument').then(...)
mock.when('third_specified_argument').then(...)
```

#### Chaining
Calling the when function with exactly the same arguments will allow you to append to the responses.

```python
mock.when('arg').then('response_one')
mock.when('arg').then('response_two')
```
is the same as
```python
mock.when('arg').then('response_one').then('response_two')
```

## Then
The `then` function specifies what the known side effect should do when parameters are matched. By default it will just return what has been passed into the `then` function. 

```python
from unittest.mock import Mock
...
response_one = Mock()
mock = Mock()

mock.when(...).then(response_one)

assert mock(...) == response_one
```

To raise an exception rather that return a value call `then_raise` rather than `then`. An exception will be raised instead of returned.

```python
from unittest.mock import Mock
...
exception = Exception()
mock = Mock()

mock.when(...).then_raise(exception)

mock(...)  # Raises the exception
```
You can also chain the `then` functions to return multiple different reponses.
Each response will be returned once until the last response. Once the last response is reached then that reponse will be the only thing returned.

```python
from unittest.mock import Mock
...
exception = Exception()
response_one = Mock()
mock = Mock()

mock.when(...).then(response_one).then_raise(exception)

assert mock(...) == response_one
mock(...)  # Raises the exception
mock(...)  # Raises the exception
```

## Otherwise

You can specify default return values on a mock by calling otherwise. If the mock is called without 
matching any arguments then the otherwise value will returned.
```python
mock.when('arg').then(...).otherwise('otherwise')

assert mock('not arg') == 'otherwise'
```
You can also raise an exception by default
```python
mock.when(...).then(...).otherwise_raise(Exception())
```


## Always

You can specify the mock to always return the same response regardless of what arguments it is called with.
```python
mock.when().always('response')

assert mock(...) == 'response'
```
You can also raise an exception
```python
mock.when().always_raise(Exception())
```


## Reset

You can reset the the known side effects on a mock by passing it the `reset` function.

```python
 
from unittest.mock import Mock
from known_side_effects import reset
...

mock = Mock()

mock.when(...).then(...)

reset(mock)

mock(...)  # raises an UnmatchedArguments exception
```


## Gotcha
When calling the `mock` after specifying multiple known side effects, the first matched set of parameters will be executed. The order of matching is the order that the known side effects are defined in. If multiple arguments are specified where one matches a super set of the other (see Matchers) then the first matched will be executed. e.g.

```python
from unittest.mock import Mock
from known_side_effects import AnyArg
...
response_one = Mock()
response_two = Mock()
argument_one = Mock()
argument_two = Mock()

mock.when(argument_one).then(response_one)
mock.when(AnyArg()).then(response_two)
...
assert mock(argument_one) == response_one
assert mock(argument_two) == response_two

```
If the order of the known side effects were reversed, the mock would only ever return `response_two`. This is due to the fact that the `Any` matched will match all parameters, therefore never attempting to match `argument_one` as it has already found a match. e.g.

```python
from unittest.mock import Mock
from known_side_effects import AnyArg
...
response_one = Mock()
response_two = Mock()
argument_one = Mock()
argument_two = Mock()

mock.when(AnyArg()).then(response_two)        # These two lines have swapped
mock.when(argument_one).then(response_one) # These two lines have swapped

...
# This will raise an AssertionError as calling the mock with argument_one now
# returns response_two and not response_one
assert mock(argument_one) == response_one   
assert mock(argument_two) == response_two

```

## Matchers

Matchers can be passed to known side effects as parameters. They are implementations of [hamcrest matchers](https://github.com/hamcrest/PyHamcrest). Matchers will only match a single parameter.
