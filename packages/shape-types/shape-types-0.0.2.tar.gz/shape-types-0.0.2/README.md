# shape-types

## Shape-Types
Shape-Types is a program that statically analyzes linear algebra in python. Currently it only works with some numpy functions.

Writing large amounts of maintainable linear algebra code is tricky. Shapes are always in the back of ones mind, so there might as well be a means with which one can annotate the shape of an array and additionally verify that the shape returned from a particular function is what one expects.

This repository has:
- A mypy plugin (that is slightly hacky and needs work, I think) to statically analyze the shapes type of the variables returned by functions such as matmul, sum, prod, etc.
- A git submodule which tracks numpy-stubs

### Getting Started

#### Requirements
 - I've only really developed against python 3.6, but might work for 3.5+

#### Install
1. Install from pypi with `pip install shape-types`

#### Running
Just run `mypy` on your code.

## Developing
I would love any contributions via pull requests. Also, feel free to report any bugs. In terms of a roadmap for this software, it would be interesting to understand a path towards making such code a possibility in numpy itself. Additionally, it would be interesting to extend this software to work with tensorflow and pytorch.

#### Tests
- Run ```tox```
