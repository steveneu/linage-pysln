from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30

class Matrix(object):
    def __init__(self, vals_in): # input is a list of lists (each inner list is a row).
        # single column matrix is [ [x1], [x2], [x3] ]
        self.rows = len(vals_in)
        self.cols = len(vals_in[0])
        self.vals = vals_in
        self.element_count = len(vals_in)

    #def print(self):

def get_column(matrix_in, column_number):
    column = []
    for i in range(len(matrix_in)):
        column.append(matrix_in[i][column_number])
    return column

def dot_product(vector_one, vector_two):
    assert (len(vector_one) == len(vector_two))

    result = sum([vector_one[i] * vector_two[i] for i in range(len(vector_one))])
    return result

def matrix_multiplication(matrixA, matrixB):
    # a.cols should match b.rows
    assert ( len(matrixA[0]) == len(matrixB) )

    m_rows = len(matrixA)
    p_columns = len(matrixB[0])

    # empty list that will hold the product of AxB
    result = []

    for r in range(m_rows):
        result_row = []
        for c in range(p_columns):
            cell = dot_product(matrixA[r], get_column(matrixB, c))
            result_row.append(cell)
        result.append(result_row)

    return result

# given a matrix, return its transpose
def transpose(matrix_in):
    rows = len(matrix_in)
    cols = len(matrix_in[0])
    matrix_transpose = []

    # iterate columns.  construct row from iteration and append to result matrix
    for c in range(cols):
        result_row = []
        for r in range(rows):
            result_row.append(matrix_in[r][c])
        matrix_transpose.append(result_row)

    return matrix_transpose

# given a size, return identity matrix as a list of lists
def identity_matrix(n):
    identity = []

    for r in range(n):
        # make row of zeds:
        row_of_zeds = []
        for c in range(n):
            row_of_zeds.append(0)
        identity.append(row_of_zeds)

    for ones in range(n):
        identity[ones][ones] = 1

    return identity

# return inverse of supplied matrix if dimension is 2 or less
def inverse_matrix2x2(matrix):
    inverse = []

    if len(matrix) != len(matrix[0]):
        raise ValueError('The matrix must be square')

    ## TODO: Check if matrix is larger than 2x2.
    ## If matrix is too large, then raise an error
    if (len(matrix)>2):
        raise ValueError('the supplied matrix must be dimension 2 or less to compute inverse')

    if len(matrix) == 1:
        if matrix[0][0] != 0:
            inverse.append([1/matrix[0][0]])
        else:
            raise ValueError('matrix does not have an inverse')
    elif len(matrix) == 2:
        inverse = [ [0, 0], [0, 0] ]
        a = matrix[0][0]
        b = matrix[0][1]
        c = matrix[1][0]
        d = matrix[1][1]

        det = (a*d - b*c)
        if det == 0:
            raise ValueError('no inverse exists for supplied matrix')
        det = det ** -1

        inverse[0][0] = d * det
        inverse[0][1] = -b * det
        inverse[1][0] = -c * det
        inverse[1][1] = a * det

    return inverse

def main():
    # assert transpose([[5, 4, 1, 7], [2, 1, 3, 5]]) == [[5, 2], [4, 1], [1, 3], [7, 5]]
    # assert transpose([[5]]) == [[5]]
    # assert transpose([[5, 3, 2], [7, 1, 4], [1, 1, 2], [8, 9, 1]]) == [[5, 7, 1, 8], [3, 1, 1, 9], [2, 4, 2, 1]]

    inverse_matrix2x2([[4, 5], [7, 1]])

    # assert matrix_multiplication([[5], [2]], [[5, 1]]) == [[25, 5], [10, 2]]
    # assert matrix_multiplication([[5, 1]], [[5], [2]]) == [[27]]
    # assert matrix_multiplication([[4]], [[3]]) == [[12]]
    # assert matrix_multiplication([[2, 1, 8, 2, 1], [5, 6, 4, 2, 1]],
    #                              [[1, 7, 2], [2, 6, 3], [3, 1, 1], [1, 20, 1], [7, 4, 16]]) == [[37, 72, 33],
    #                                                                                             [38, 119, 50]]

main()