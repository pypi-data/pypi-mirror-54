import argparse
import dataclasses
import shlex
from dataclasses import dataclass, field
from typing import *

import pytest

from .testutils import TestSetup
from simple_parsing import (Formatter, InconsistentArgumentError,
                            ParseableFromCommandLine)

    
# call a test function multiple times passing in different arguments in turn.
# argvalues generally needs to be a list of values if argnames specifies only one name or a list of tuples of values if argnames specifies multiple names.
# Example: @parametrize('arg1', [1,2]) would lead to two calls of the decorated test function,
# one with arg1=1 and another with arg1=2.see https://docs.pytest.org/en/latest/parametrize.html for more info and examples.


@dataclass()
class ClassA(ParseableFromCommandLine):
    a: int = 1


@dataclass()
class ClassB(ParseableFromCommandLine):
    b: int = 2


@dataclass()
class ClassC(ParseableFromCommandLine):
    c: int = 3


@dataclass()
class Container1(ParseableFromCommandLine, TestSetup):
    v1: int = 0
    class_a: ClassA = ClassA()
    class_b: ClassB = ClassB()


@dataclass()
class Container2(ParseableFromCommandLine, TestSetup):
    list_of_class_c: List[ClassC] = field(default_factory=list)


def test_nesting_no_args():
    args = Container1.setup("")
    c1 = Container1.from_args(args)
    assert c1.v1 == 0
    assert c1.class_a.a == 1
    assert c1.class_b.b == 2

@pytest.mark.xfail(reason="TODO: make sure this is how people would want to use this feature.")
def test_nesting_with_args():
    args = Container1.setup("--a 123 --b 456 --v1 3")
    c1 = Container1.from_args(args)
    assert c1.v1 == 3
    assert c1.class_a.a == 123
    assert c1.class_b.b == 456