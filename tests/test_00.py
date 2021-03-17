import pytest
from data import cases
from PSSE34to33 import conversion_to_33

@pytest.mark.parametrize('filename', cases)
def test_00(filename):
    conversion_to_33(filename)

