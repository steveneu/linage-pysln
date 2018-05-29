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

def main():
    assert matrix_multiplication([[5], [2]], [[5, 1]]) == [[25, 5], [10, 2]]
    assert matrix_multiplication([[5, 1]], [[5], [2]]) == [[27]]
    assert matrix_multiplication([[4]], [[3]]) == [[12]]
    assert matrix_multiplication([[2, 1, 8, 2, 1], [5, 6, 4, 2, 1]],
                                 [[1, 7, 2], [2, 6, 3], [3, 1, 1], [1, 20, 1], [7, 4, 16]]) == [[37, 72, 33],
                                                                                                [38, 119, 50]]

main()