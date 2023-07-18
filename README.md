# PSSE34to33
Convert PSSE formats from version 34 to grg-pssedata data structure (PSSE 33)

```python
import PSSE34to33
case33 = PSSE34to33.conversion_to_33(filename) # -> grg_pssedata.struct.Case
```
if you want to write a `.raw` file:
```python
import PSSE34to33
case33 = PSSE34to33.conversion_to_33(filename)

with open('case33.raw', 'w') as f:
  f.write(case33.to_psse())
```

## Installation
Clone the repository to a local machine:
```
git clone https://github.com/jbarberia/PSSE34to33
cd PSSE34to33
```
Install the dependencies:
```
pip install -r requirements.txt
```
Install the package:
```
python setup.py install
```