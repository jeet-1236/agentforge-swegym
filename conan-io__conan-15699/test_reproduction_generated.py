import pytest
from conan.tools.gnu.get_gnu_triplet import _get_gnu_triplet

def test_gnu_triplet_x86_on_linux_is_i686():
    """
    The GNU triplet for arch=x86 on Linux should use the "i686" machine name,
    not the suboptimal "x86". The expected triplet is "i686-linux-gnu".
    """
    result = _get_gnu_triplet("Linux", "x86")
    assert result == "i686-linux-gnu"  # current buggy code returns "x86-linux-gnu"
