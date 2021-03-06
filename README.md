# BDD Tool
Report on available BDD steps and usage within scripts
 
### Example:

```
bdd --counts
bdd --unused
```

## Dependencies

- Python3.8
- Pyenv
- zsh complete

## Installing

**Development**

```
pyenv local tools3 3.6.0
pip install -e .

py.test -vs
```
For intellij to enable execute test from editor with icon, set: default test runner to pytest

**Testing**

```
py.test -vs
# OR:
py.test --cov-report html --cov bdd.tests
open htmlcov/index.html
# OR:
tox
```