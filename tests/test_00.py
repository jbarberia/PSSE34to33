import os
import pytest
import grg_pssedata as pd
from data import cases
from PSSE34to33 import conversion_to_33

@pytest.mark.parametrize('filename', cases)
def test_00(filename):
    conversion_to_33(filename)

@pytest.mark.parametrize('filename', cases)
def test_01(filename):
    case33 = conversion_to_33(filename)
    name, ext = os.path.splitext(filename)
    with open('tmp'+ext, 'w') as f:
        f.write(case33.to_psse())
    pd.io.parse_psse_case_file('tmp'+ext)
    os.remove('tmp'+ext)
