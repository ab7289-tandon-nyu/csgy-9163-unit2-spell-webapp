import pytest
from app.util import get_flash_msg


@pytest.mark.parametrize(
    ("error", "success", "value",),
    (
        ("error", None, ("error", "error"),),
        (None, "success", ("success", "success",),),
        ("error", "success", ("error", "error")),
        (None, None, None),
    ),
)
def test_utils(error, success, value):
    ret = get_flash_msg(error=error, success=success)
    print(f"return value: {ret}")
    assert get_flash_msg(error=error, success=success) == value
