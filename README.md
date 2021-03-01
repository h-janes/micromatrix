# MicroMatrix
MicroMatrix is a small Python3 package which adds a generalised `Matrix` class for matrix maths with no external dependancies.

MicroMatrix supports complex numbers; standard arithmatic such as addition, subtraction, absolute value and scalar multiplication; and matrix operations such as transpose, invert, multiplication, division, exponentiation and more.

You can create matrices of any size: `1x1`, `2x4`, `3x3`, or whatever you want.
The `Matrix` class takes any number of lists as parameters which will form the horizontal rows of the matrix.

```python
from micromatrix import Matrix

my_matrix = Matrix([1, 2, 3], [4, 5, 6]) # Creating a 3x2 matrix

# Do stuff with my_matrix...
```

## Matrix Operations
MicroMatrix supports many operations, including all of the standard mathematical operators.

All operations can be reversed, combined, whatever - although keep in mind that matrices are weird. Some operations may not be possible depending on the dimension and elements of your matrices. In that case, you will see an AssertionError with a description, such as:
```terminal
AssertionError: Matrix cannot be inverted
```

Most supported methods are below, but more can be found in the source code.

```python
# Applies function to all elements in matrix, returns a new matrix
my_matrix.administer(function)

# Returns a nice multiline padded string representation of the matrix
str(my_matrix)

# Returns the total number of elements in the matrix
len(my_matrix)

# Calculates absolute value of each element, returns a new matrix
abs(my_matrix)

# Returns True if both matrices have same elements, else returns False
my_matrix == another_matrix

# Returns the identity matrix with the same dimensions as my_matrix
my_matrix.identity()

# Returns the transpose of my_matrix
my_matrix.transpose()

# Returns the determinant of my_matrix
my_matrix.determinant()

# Returns the inverse of my_matrix (if possible)
my_matrix.invert()

# Mathematical operation examples
my_matrix + 30
my_matrix - 16
2 - my_matrix
my_matrix + another_matrix
my_matrix - another_matrix
my_matrix * 40
my_matrix * another_matrix
my_matrix / 3
6 / my_matrix
my_matrix / another_matrix
my_matrix ** -1
my_matrix ** 4

# Assignment statements can also be used
my_matrix += 7
my_matrix -= another_matrix
my_matrix *= another_matrix
my_matrix /= 420
```
