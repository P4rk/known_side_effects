# Known Side Effects

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/393832636c36453eb382b56b4f6dcb0f)](https://www.codacy.com/app/P4rk/known_side_effects?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=P4rk/known_side_effects&amp;utm_campaign=Badge_Grade)

A test utility library to help write explict sideffects for mocked objects.

## Basic example
```python
from unittest.mock import Mock
from known_side_effects.types import given

mock = Mock()
response = Mock()

given(mock).when('argument', kw='arg').then(response)
rsp = mock('argument', kw='arg')

assert rsp == response
```

## Matches
TODO
