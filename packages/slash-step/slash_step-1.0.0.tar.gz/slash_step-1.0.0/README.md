slash-step
==========

|                       |                                                                                     |
|-----------------------|-------------------------------------------------------------------------------------|
| Build Status          | ![Build Status](https://secure.travis-ci.org/getslash/slash-step.png?branch=master) |
| Supported Versions    | ![Supported Versions](https://img.shields.io/pypi/pyversions/slash-step.svg)        |
| Latest Version        | ![Latest Version](https://img.shields.io/pypi/v/slash-step.svg)                     |

Create a more granular sub `STEP` for `Slash` tests.

Some scenarios can be long and complex, but you still want to have them as a single logical test.
Steps allow to document subsections of a test, and also provide some handy hooks to perform actions inside a test (such as validations).

To continue the microwave example from `Slash`'s [docs](https://slash.readthedocs.org/en/latest/index.html):

```python
from slash import g
from slash_step import STEP, hooks

@hooks.step_end.register
def measure_temperature():
    if g.microwave.temperature > 180:
        logger.warn("Microwave is over heating!")
    
def test_cook_chicken():
    with STEP("Defrost chicken"):
        # ...
    with STEP("Cook"):
        # ...
    with STEP("Eat"):
        # Yum...
        assert g.chicken.is_cooked()
```

