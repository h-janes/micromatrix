class Dimension:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def min(self) -> int:
        return min(self.x, self.y)

    @property
    def max(self) -> int:
        return max(self.x, self.y)

    @property
    def square(self) -> bool:
        return self.x == self.y

    def __eq__(self, other) -> bool:
        if isinstance(other, Dimension) and self.x == other.x and self.y == other.y:
            return True
        return False


# Types
class _Matrix:
    pass


NumberType = int | float | complex
MathType = int | float | complex | _Matrix


class Matrix(_Matrix):
    def __init__(self, *rows: list, precision: int = 5) -> None:
        if not all(len(row) == len(rows[0]) for row in rows):
            raise ValueError("Matrix rows must all have equal length")

        self.rows = rows
        self.columns = [list(i) for i in zip(*self.rows)]
        self.dimension = Dimension(len(self.rows), len(self.columns))
        self.precision = precision

    # Helper Methods
    def administer(self, func) -> _Matrix:
        """Applies the given function to all elements in the matrix"""
        rows = [[func(i) for i in row] for row in self.rows]
        return Matrix(*rows)

    def round(self, x: NumberType) -> NumberType:
        """Rounds any number, including complex"""
        try:
            return round(x, self.precision)
        except TypeError:
            return complex(round(x.real, self.precision), round(x.imag, self.precision))

    @staticmethod
    def minor(m: list, i: int, j: int) -> list:
        """Calculates matrix minor from list, returns list"""
        return [row[:j] + row[j + 1 :] for row in (m[:i] + m[i + 1 :])]

    # Matrix methods
    def identity(self) -> _Matrix:
        """Returns an identity matrix with the same dimensions"""
        rows = self.administer(lambda i: 0).rows
        for i in range(self.dimension.min):
            rows[i][i] = 1
        return Matrix(*rows)

    def transpose(self) -> _Matrix:
        """Returns the transposed matrix"""
        return Matrix(*self.columns)

    def determinant(self, rows: list = None) -> NumberType:
        """Returns the matrix determinant"""
        if not rows:
            if not self.dimension.square:
                raise ValueError("Operation requires a square matrix")
            rows = self.rows
        if len(rows) == 1:
            return rows[0][0]
        if len(rows) == 2:
            return rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]
        determinant = 0
        for i in range(len(rows)):
            minor = self.minor(rows, 0, i)
            determinant += ((-1) ** i) * rows[0][i] * self.determinant(minor)
        return determinant

    def invert(self) -> _Matrix:
        """Returns matrix inverse if it exists"""
        try:
            det = self.determinant()
            rows = self.rows
            if len(rows) == 1:
                return Matrix([1 / rows[0][0]])
            if len(rows) == 2:
                rows = [
                    [rows[1][1] / det, -1 * rows[0][1] / det],
                    [-1 * rows[1][0] / det, rows[0][0] / det],
                ]
                return Matrix(*rows)
            cofactors = []
            for i in range(len(rows)):
                cofactor_row = []
                for j in range(len(rows)):
                    minor = self.minor(rows, i, j)
                    cofactor_row.append(((-1) ** (i + j)) * self.determinant(rows=minor))
                cofactors.append(cofactor_row)
            cofactors = Matrix(*cofactors).transpose().rows
            for i in range(len(cofactors)):
                for j in range(len(cofactors)):
                    cofactors[i][j] = cofactors[i][j] / det
            return Matrix(*cofactors)
        except Exception:
            raise ValueError("Matrix cannot be inverted")

    # Magic methods
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

    def __pos__(self) -> _Matrix:
        return self

    def __neg__(self) -> _Matrix:
        return self.administer(lambda i: -i)

    def __abs__(self) -> _Matrix:
        return self.administer(lambda i: abs(i))

    def __eq__(self, other) -> bool:
        if isinstance(other, Matrix) and self.rows == other.rows:
            return True
        return False

    def __add__(self, other: MathType) -> _Matrix:
        if isinstance(other, NumberType):
            return self.administer(lambda i: i + other)
        if self.dimension != other.dimension:
            raise ValueError("Operation requires matrices of the same dimension")
        rows = [[a + b for a, b in zip(i, j)] for i, j in zip(self.rows, other.rows)]
        return Matrix(*rows)

    def __radd__(self, other: MathType) -> _Matrix:
        return self.__add__(other)

    def __sub__(self, other: MathType) -> _Matrix:
        return self.__add__(-other)

    def __rsub__(self, other: MathType) -> _Matrix:
        return (-self).__add__(other)

    def __mul__(self, other: MathType) -> _Matrix:
        if isinstance(other, NumberType):
            return self.administer(lambda i: i * other)
        if self.dimension.x != other.dimension.y:
            raise ValueError(
                "Operation requires number of rows in first matrix to equal number of columns in second matrix"
            )
        rows = [
            [sum(a * b for a, b in zip(row, column)) for column in other.columns]
            for row in self.rows
        ]
        return Matrix(*rows)

    def __rmul__(self, other: MathType) -> _Matrix:
        return self.__mul__(other)

    def __pow__(self, other: int) -> _Matrix:
        if not self.dimension.square:
            raise ValueError("Operation requires a square matrix")
        if other == 0:
            return self.identity()
        elif other < 0:
            return self.invert() ** abs(other)
        result = self
        for i in range(other - 1):
            result *= self
        return result

    def __truediv__(self, other: MathType) -> _Matrix:
        if isinstance(other, NumberType):
            return self.__mul__(1 / other)
        return self.__mul__(other.invert())

    def __rtruediv__(self, other: MathType) -> _Matrix:
        return self.invert().__mul__(other)

    # Aliases

    def det(self):
        return self.determinant()

    def T(self):
        return self.transpose()

    def __invert__(self):
        return self.invert()

    def inverse(self):
        return self.invert()
