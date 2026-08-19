import pytest
from hydra._internal.instantiate._instantiate2 import instantiate


class A:
    class B:
        def __init__(self):
            self.value = 42


def test_instantiate_nested_class_returns_instance():
    # Should instantiate the nested class A.B without raising an ImportError
    obj = instantiate({}, _target_=A.B)
    assert isinstance(obj, A.B)
    assert obj.value == 42
