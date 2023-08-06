# VVar-Python

## Description

Simple python module to save and load user-persistent strings, that will stay after application stop. Note that the variables will be stored unencrypted.

## Usage

```python
import vvar

# Store
vvar.example_var = "Example String"

# Read
print(vvar.example_var)
# Output: Example String

# Delete
del vvar.example_var
```

## Installation
```
pip install vvar
```