# MicroMatrix
MicroMatrix is a small Python3 package which adds a generalised `Matrix` class for matrix maths with no external dependancies.

You can create matrices of any size: `1x1`, `2x4`, `3x3`, or whatever you want.
The `Matrix` class takes any number of lists as parameters which will form the horizontal rows of the matrix.

```python
from micromatrix import Matrix

my_matrix = Matrix([1, 2, 3], [4, 5, 6]) # Creating a 3x2 matrix

# Do stuff with my_matrix...
```

## Matrix Operations
MicroMatrix supports many operations, including all of the standard mathematical operators.
Some examples are below, but more can be found in the source code.

```python
my_matrix.transpose()

# i actually cba to write more rn
```
