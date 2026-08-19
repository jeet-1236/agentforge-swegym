import pytest
from hydra.errors import InstantiationException
from hydra._internal.instantiate._instantiate2 import instantiate


def test_instantiate_error_message_includes_chained_exception():
    cfg = {"_target_": "non.existent.Class"}
    with pytest.raises(InstantiationException) as excinfo:
        instantiate(cfg)
    # The error message should surface the original exception (e.g., ModuleNotFoundError)
    msg = str(excinfo.value)
    assert "ModuleNotFoundError" in msg or "No module named" in msg
