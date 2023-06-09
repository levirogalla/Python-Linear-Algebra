import time


class Vector(list):
    def __init__(self, *args):
        self.space = len(args)
        super().__init__(args)

    def __add__(self, other):
        if len(self) == len(other):
            return Vector(*tuple(map(lambda x1, x2: x1 + x2, self, other)))
        else:
            return ValueError("Vectors exist in different dimensions.")

    def __sub__(self, other):
        if len(self) == len(other):
            return Vector(*tuple(map(lambda x1, x2: x1 - x2, self, other)))
        else:
            return ValueError("Vectors exist in different dimensions.")

    def __mul__(self, other):
        if isinstance(other, Vector) and isinstance(self, Vector):
            if len(self) == len(other):
                return sum(tuple(map(lambda x1, x2: x1 * x2, self, other)))
            else:
                return ValueError("Vectors exist in different dimensions.")
        else:
            return Vector(*tuple(map(lambda x1: x1 * other, self)))

    def __abs__(self):
        return pow(sum(tuple(map(lambda x: pow(x, 2), self))), 0.5)

    def projOn(self, direction):
        return (direction) * ((self * direction) / pow(abs(direction), 2))

    def perpTo(self, direction):
        return self - self.projOn(direction)

    def crossWith(self, other):
        if len(self) == 3 and len(other) == 3:
            return Vector(
                (self[1] * other[2] - other[1] * self[2]),
                (-1 * (self[0] * other[2] - other[0] * self[2])),
                (self[0] * other[1] - other[0] * self[1]),
            )
        else:
            return ValueError("Vectors are not in the third dimension.")


# enter rows
# assumes columns, rows, and aug is all correctly sized
# can only take vector as aug
class Matrix(list):
    def __init__(self, *args, aug: "Matrix" = None):
        super().__init__(args)
        self.rows = []
        self.columns = []
        self.aug = aug
        if aug:
            self.aug = aug
        if args:
            for row in self:
                self.rows.append(Vector(*row))
            for column in range(len(args[0])):
                self.columns.append(
                    Vector(*(args[row][column] for row in range(len(args))))
                )

    def __getitem__(self, index) -> Vector | float:
        return self.rows[index]

    def __setitem__(self, index, value) -> None:
        if isinstance(index, tuple):
            row, col = index
            self[row][col] = value
            self.columns[col][row] = value
            self.rows[row][col] = value
        else:
            super().__setitem__(index, value)
            self.rows[index] = Vector(*value)
            if len(self.columns) > 0:
                for row in range(len(self)):
                    self.columns[row][index] = self.rows[index][row]

    def __repr__(self):
        rows = []
        for row in self.rows:
            row_str = " ".join([str(elem) for elem in row])
            rows.append(row_str)
        return "\n".join(rows)

    # __str__ function mainly created by chatgpt
    def __str__(self) -> str:
        # Initialize the string that will hold the matrix representation
        matrix_str = "\n"

        # Determine the maximum width of each column
        column_widths = [
            max([len("{:.3f}".format(self.rows[i][j])) for i in range(len(self.rows))])
            for j in range(len(self.rows[0]))
        ]

        # Loop through each row of the matrix
        for i, row in enumerate(self.rows):
            # Format each column of the row
            formatted_row = ["|"]
            for j in range(len(row)):
                formatted_row.append("{:.3f}".format(row[j]).rjust(column_widths[j]))

            # My additions
            formatted_row.append("|")

            if self.aug:
                formatted_row.append(str(self.aug[i]))
                formatted_row.append("|")

            # Append the formatted row to the matrix string
            matrix_str += " ".join(formatted_row) + "\n"

        # Return the final matrix string
        return matrix_str

    def __mul__(self, other):
        new = []

        # vector matrix multipication
        if isinstance(other, Vector):
            temp = []
            try:
                if other.space != len(self.columns):
                    raise TypeError("Vector space does not match matrix space")
                for i, col in enumerate(self.columns):
                    temp.append(Vector(*col) * other[i])
                temp = Matrix(*temp).T()
                for i, row in enumerate(temp):
                    new.append(sum(row))
                return Vector(*new)
            except Exception as e:
                print(e)

        # matrix vector multiplication
        elif isinstance(other, Matrix):
            if len(self.columns) == len(other.rows):
                for col in other.columns:
                    new.append(self * col)
            return Matrix(*new).T()

    def cof(self, rowI, colI) -> "Matrix":
        new = []
        for i, row in enumerate(self.rows):
            if i != rowI:
                r = []
                for x, num in enumerate(row):
                    if x != colI:
                        r.append(num)
                new.append(r)
        return Matrix(*new)

    # shows all the determinats
    def detS(self) -> float:
        if len(self.rows) == 2:
            return (self[0][0] * self[1][1]) - (self[1][0] * self[0][1])
        else:
            result = []
            for col, num in enumerate(self.rows[0]):
                print(f"{num} * determinant of: {self.cof(0,col)}")
                val = self.cof(0, col).detS()
                if col % 2:
                    val = val * -1
                print(f"The sum was: {num*val}")

                result.append(num * val)

            return sum(result)

    def det(self) -> float:
        if len(self.rows) == 2:
            return (self[0][0] * self[1][1]) - (self[1][0] * self[0][1])
        else:
            result = []
            for col, num in enumerate(self.rows[0]):
                val = self.cof(0, col).det()
                if col % 2:
                    val = val * -1
                result.append(num * val)
            return sum(result)

    def rref(self) -> "Matrix":
        new = [*self.rows]
        newAug = self.aug

        # case where the matrix is 1x1
        if len(new) == 1 and len(new[0]) == 1:
            if new[0][0] != 0:
                newAug[0, 0] = newAug[0][0] / new[0][0]
                new[0][0] = 1
            return Matrix(*new, aug=newAug)

        # finds smallest dimension, may make a funtion to do this
        for rowIndex in range(
            self.rows[0].space
            if self.rows[0].space < self.columns[0].space
            else self.columns[0].space
        ):
            # rotates rows until the val at nn is not 0 won't rotate rows above n
            rotations = 0
            columnNormalizable = True
            while new[rowIndex][rowIndex] == 0:
                rotations += 1

                # apply to matrix
                lastRow = new.pop(-1)
                new.insert(rowIndex, lastRow)

                # apply to augmented matrix if there is one
                if newAug:
                    lastRowAug = newAug.pop(-1)
                    newAug.insert(rowIndex, lastRowAug)

                # breaks out of loop if max rotations have been done
                if rotations == len(self.rows) - rowIndex:
                    columnNormalizable = False
                    break

            # if a column has all 0s it will skip to the next column
            if columnNormalizable == False:
                continue

            leadingOneFactor = 1 / new[rowIndex][rowIndex]

            new[rowIndex] = new[rowIndex] * (leadingOneFactor)

            if newAug:
                newAug[rowIndex] = newAug[rowIndex] * (leadingOneFactor)

            # subtracts row with leading 1 from all other rows to make everything else in the column 0
            for i, row in enumerate(new):
                if rowIndex != i:
                    zeroingFactor = row[rowIndex]
                    new[i] = row - (new[rowIndex] * zeroingFactor)

                    if newAug:
                        newAug[i] = newAug[i] - (newAug[rowIndex] * zeroingFactor)

        return Matrix(*new, aug=newAug)

    def inverse(self) -> "Matrix":
        "Returns either the appropriate (left, right, square) inverse or false if matrix is not invertable"

        # checks the matrix is square
        if len(self.rows) == len(self.columns):
            # creates identity matrix
            newAug = Matrix(
                *[
                    [1 if col == row else 0 for col in range(len(self.rows))]
                    for row in range(len(self.rows))
                ]
            )

            inverse = Matrix(*self.rows, aug=newAug).rref().aug

            return inverse

        # checks to see if right inverse is appropriate
        if len(self.rows) < len(self.columns):
            transpose = self.T()

            # multiply the matrix by its transpose to make it square
            square = self * transpose

            squareInvers = square.inverse()
            # reverses the "squaring" action done above
            inverse = transpose * squareInvers

            return inverse

        # checks to see if left inverse is appropriate
        if len(self.rows) > len(self.columns):
            transpose = self.T()

            # multiply the matrix by its transpose to make it square
            square = transpose * self

            # reverses the "squaring" action done above
            inverse = square.inverse() * transpose

            return inverse

        return False

    def rank(self) -> int:
        rref = self.rref()
        rank = 1

        minSize = min(len(rref.columns), len(rref.rows))

        for val in range(minSize):
            if val == 1:
                rank += 1

        return rank

    def T(self):
        rows = self.columns
        return Matrix(*rows)
