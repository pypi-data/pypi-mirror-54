# Boar ML

[![Build Status](https://travis-ci.org/DobromirM/BoarML.svg?branch=master)](https://travis-ci.org/DobromirM/BoarML)

BOAR (Build Once And Run) ML is a library that allows you to build abstract machine
learning models and then compile them with popular ML platforms.

The library also implements additional modules for applying mutations to an architecture, support  for  writing  
architectures to a file and reading architectures from a file in a user readable format.

https://pypi.org/project/boarml/

## Installation

`pip install boarml`


## Building instructions

1) Building the package: `python setup.py sdist bdist_wheel`
2) Uploading to PyPi: `python -m twine upload  dist/*`
3) Uploading new versions: `twine upload --skip-existing dist/*`