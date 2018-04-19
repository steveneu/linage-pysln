from decimal import Decimal, getcontext
from vector import Vector

getcontext().prec = 30

class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)
        self.set_basepoint()

    # instructor implementation for coincident
    # def __eq__(self, ell):
    #     if not self.is_parallel_to(ell):
    #         return False
    #     x0 = self.basepoint
    #     y0 = ell.basepoint
    #     basepoint_difference = x0.minus

    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/Decimal(initial_coefficient)
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    # return a point on line as a vector when x=1 and y=1
    def get_point_on_line(self):
        # solve for y when x=1
        y = (self.constant_term - Decimal(self.normal_vector[0]))/Decimal(self.normal_vector[1])
        return [1, y]

    def __str__(self):
        num_decimal_places = 3
        n = self.normal_vector

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output
        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                        for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    @staticmethod
    def parallel(first, second):
        v1 = Vector(first.normal_vector)
        v2 = Vector(second.normal_vector)
        return Vector.parallel(v1, v2)

    @staticmethod # return true if supplied lines are coincident (parallel & overlapping)
    def coincident(first, second):
        result = False
        parallel_lines = Line.parallel(first, second)
        if parallel_lines:
            # todo: handle lines that are vertical or horizontal (A=0 or B=0)
            ptline1 = first.get_point_on_line()
            ptline2 = second.get_point_on_line()
            if ptline1[0] == ptline2[0] and ptline1[1] == ptline2[1]:
                result = True
            else:
                v0 = Vector( [ptline2[0]-ptline1[0], ptline2[1]-ptline1[1]] )
                v1 = Vector(first.normal_vector)
                v2 = Vector(second.normal_vector)
                first_orthogonal = Vector.orthagonal(v0, v1)
                second_orthogonal = Vector.orthagonal(v0, v2)
                if first_orthogonal and second_orthogonal:
                    result = True
        else:
            result = parallel_lines
        return result

    @staticmethod
    def intersection(first, second):
        if not Line.parallel(first, second):
            A = Decimal(first.normal_vector[0])
            B = Decimal(first.normal_vector[1])
            k1 = first.constant_term
            C = Decimal(second.normal_vector[0])
            D = Decimal(second.normal_vector[1])
            k2 = second.constant_term
            x = (D*k1-B*k2)/(A*D-B*C)
            y = (-C*k1 + A*k2)/(A*D-B*C)
            return tuple([Decimal(x), Decimal(y)])
        else:
            return False

    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

    ## ..............................................................

def printLineInfo(one, two):
    message = "line one: " + str(one) + " and line two: " + str(two)
    if Line.parallel(one, two):
        if Line.coincident(one, two):
            message += " are coincident"
        else:
            message += " are parallel"
    else:
        result = Line.intersection(one, two)
        if result == False:
            message += " do not intersect"
        else:
            message += " intersect at: " + str(result)
    print(message)

