from __future__ import annotations

# Error Messages
error = {
    1: "Matrix parameters must be of type array (list, tuple)",
    2: "Matrix rows must all have equal length",
    3: "Operation requires a square matrix",
    4: "Parameter must be of type math (Matrix, int, float, complex)",
    5: "Operation requires matrices of equal dimension",
    6: "Number of rows in M1 must equal number of columns in M2",
    7: "Matrix exponent must be of type int",
    8: "Matrix cannot be inverted",
}

# Type Groupings
array = (list, tuple)
number = (int, float, complex)
math = number


class Dimension:
    def __init__(self, width: array, height: array) -> None:
        self.x = len(width)
        self.y = len(height)
        self.min = min(self.x, self.y)
        self.max = max(self.x, self.y)
        self.square = self.x == self.y

    def __eq__(self, other) -> bool:
        if isinstance(other, Dimension) and self.x == other.x and self.y == other.y:
            return True
        return False


class Matrix:
    def __init__(self, *rows: array, precision: int = 5) -> None:
        assert all(isinstance(row, array) for row in rows), error[1]
        assert all(len(row) == len(rows[0]) for row in rows), error[2]

        global math
        math = (Matrix, int, float, complex)

        self.rows = [list(i) for i in rows]
        self.columns = [list(i) for i in zip(*self.rows)]
        self.dimension = Dimension(self.rows, self.columns)
        self.precision = int(precision)

    # Helper Methods

    def administer(self, func) -> Matrix:
        """ Applies the given function to all elements in the matrix """
        rows = [[func(i) for i in row] for row in self.rows]
        return Matrix(*rows)

    def round(self, x: number) -> number:
        """ Rounds any number, including complex """
        try:
            return round(x, self.precision)
        except TypeError:
            return complex(round(x.real, self.precision), round(x.imag, self.precision))

    @staticmethod
    def minor(m: list, i: int, j: int) -> list:
        """ Calculates matrix minor from list, returns list """
        return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

    # Basic and Miscellaneous Methods

    def __str__(self) -> str:
        s = [[str(self.round(i)) for i in row] for row in self.rows]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = "[ " + "   ".join("{{:{}}}".format(x) for x in lens) + " ]"
        table = [fmt.format(*row) for row in s]
        return "\n".join(table)

    def __len__(self) -> int:
        length = 0
        for row in self.rows:
            length += len(row)
        return length

    def __pos__(self) -> Matrix:
        return self

    def __neg__(self) -> Matrix:
        return self.administer(lambda i: -i)

    def __abs__(self) -> Matrix:
        return self.administer(lambda i: abs(i))

    # Boolean and Comparison Methods

    def __eq__(self, other) -> bool:
        if isinstance(other, Matrix) and self.rows == other.rows:
            return True
        return False

    # Callables

    def identity(self) -> Matrix:
        """ Returns an identity matrix with the same dimensions """
        rows = self.administer(lambda i: 0).rows
        for i in range(self.dimension.min):
            rows[i][i] = 1
        return Matrix(*rows)

    def transpose(self) -> Matrix:
        """ Returns the transposed matrix """
        return Matrix(*self.columns)

    def determinant(self, rows: list = None) -> number:
        """ Returns the matrix determinant """
        if not rows:
            assert self.dimension.square, error[3]
            rows = self.rows
        if len(rows) == 1:
            return rows[0][0]
        if len(rows) == 2:
            return rows[0][0]*rows[1][1]-rows[0][1]*rows[1][0]
        determinant = 0
        for i in range(len(rows)):
            minor = self.minor(rows, 0, i)
            determinant += ((-1)**i)*rows[0][i]*self.determinant(minor)
        return determinant

    def invert(self) -> Matrix:
        """ Returns matrix invert if it exists """
        try:
            det = self.determinant()
            rows = self.rows
            if len(rows) == 1:
                return Matrix([1/rows[0][0]])
            if len(rows) == 2:
                rows = [[rows[1][1]/det, -1*rows[0][1]/det],
                        [-1*rows[1][0]/det, rows[0][0]/det]]
                return Matrix(*rows)
            cofactors = []
            for i in range(len(rows)):
                cofactor_row = []
                for j in range(len(rows)):
                    minor = self.minor(rows, i, j)
                    cofactor_row.append(((-1)**(i+j)) * self.determinant(rows=minor))
                cofactors.append(cofactor_row)
            cofactors = Matrix(*cofactors).transpose().rows
            for i in range(len(cofactors)):
                for j in range(len(cofactors)):
                    cofactors[i][j] = cofactors[i][j]/det
            return Matrix(*cofactors)
        except Exception:
            assert False, error[8]

    # Maths Methods

    def __add__(self, other: math) -> Matrix:
        assert isinstance(other, math), error[4]
        if isinstance(other, number):
            return self.administer(lambda i: i + other)
        assert self.dimension == other.dimension, error[5]
        rows = [[a + b for a, b in zip(i, j)] for i, j in zip(self.rows, other.rows)]
        return Matrix(*rows)

    def __radd__(self, other: math) -> Matrix:
        return self.__add__(other)

    def __sub__(self, other: math) -> Matrix:
        return self.__add__(-other)

    def __rsub__(self, other: math) -> Matrix:
        return (-self).__add__(other)

    def __mul__(self, other: math) -> Matrix:
        assert isinstance(other, math), error[4]
        if isinstance(other, number):
            return self.administer(lambda i: i * other)
        assert self.dimension.x == other.dimension.y, error[6]
        rows = [[sum(a*b for a, b in zip(row, column))
                for column in other.columns]
                for row in self.rows]
        return Matrix(*rows)

    def __rmul__(self, other: math) -> Matrix:
        return self.__mul__(other)

    def __pow__(self, other: int) -> Matrix:
        assert isinstance(other, int), error[7]
        assert self.dimension.square, error[3]
        if other == 0:
            return self.identity()
        elif other < 0:
            return self.invert() ** abs(other)
        result = self
        for i in range(other-1):
            result *= self
        return result

    def __truediv__(self, other: math) -> Matrix:
        assert isinstance(other, math), error[4]
        if isinstance(other, number):
            return self.__mul__(1/other)
        return self.__mul__(other.invert())

    def __rtruediv__(self, other: math) -> Matrix:
        return self.invert().__mul__(other)

    # Method aliases

    def det(self):
        return self.determinant()

    def T(self):
        return self.transpose()

    def __invert__(self):
        return self.invert()

    def inverse(self):
        return self.invert()
    
