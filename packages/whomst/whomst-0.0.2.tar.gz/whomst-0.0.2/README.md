# whomst :owl:
[![Build Status](https://travis-ci.org/minelminel/whomst.svg?branch=master)](https://travis-ci.org/minelminel/whomst)
[![codecov](https://codecov.io/gh/minelminel/whomst/branch/master/graph/badge.svg)](https://codecov.io/gh/minelminel/whomst)
#### mystery dependency detective & missing `requirements.txt` creator
```
🦉 ~/whomst:$  whomst .
bar
foo
new
pytest
setuptools
whomst

🦉 ~/whomst:$  whomst . > requirements.txt

🦉 ~/whomst:$  whomst . > requirements.txt && cat requirements.txt
bar
foo
new
pytest
setuptools
whomst
```

---
### `/usr/bin`
```bash
git clone https://github.com/minelminel/whomst.git
cd whomst
./install
```

### `/site-packages/`
```bash
git clone https://github.com/minelminel/whomst.git
cd whomst
pip install -e .
```

### Uninstall
```bash
cd whomst && ./uninstall
```
