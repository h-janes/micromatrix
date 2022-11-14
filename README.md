# MicroMatrix
**This is an old unfinished project which I plan to work on soon.**

MicroMatrix is a small Python module which adds a generalized `Matrix` class, supporting many operations with no external dependencies.

**MicroMatrix Supports:**
* Matrices of any size
* Complex Numbers
* Addition & Subtraction
* Multiplication & Division
* Integer Exponentiation
* Transposition
* Inverse & Determinant
* Assignment Operators
* And more!

## Usage
### Installation
Flask Sitemapper requires Python 3.10 or newer. The latest version can be installed from PyPi with pip as shown below.
```terminal
pip install micromatrix
```

Now you can import the `Matrix` class to use in your code.
```python
from micromatrix import Matrix

# Creating a 3x2 matrix
my_matrix = Matrix([1, 2, 3], [4, 5, 6])
```

### Matrix Operations
MicroMatrix supports many operations, including the standard Python mathematical operators and common matrix operations. These operations can be combined and used for complex calculations.

Keep in mind that some operations may not be possible depending on the dimension and elements of your matrices. In that case, you will see a `ValueError` with a description such as:
```terminal
ValueError: Operation requires a square matrix
```

#### Reversible Operations
* `Matrix + int | float | complex | Matrix`
* `Matrix - int | float | complex | Matrix`
* `Matrix * int | float | complex | Matrix`
* `Matrix / int | float | complex | Matrix`
* `Matrix == Any`
#### Non-Reversible Operations
* `Matrix ** int`
* `+ Matrix`
* `- Matrix`
* `~ Matrix`
* `abs(Matrix)`
* `len(Matrix)`
* `str(Matrix)`

#### Properties
* `Matrix.identity`
* `Matrix.transpose`
* `Matrix.determinant`
* `Matrix.invert`

#### Methods
* `Matrix.administer(function)`