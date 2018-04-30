from decimal import Decimal, getcontext
from line import Line
from vector import Vector

getcontext().prec = 30

class Plane(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 3

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()

    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0'] * self.dimension

            initial_index = Plane.first_nonzero_index(n)
            initial_coefficient = n.coordinates[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    @staticmethod
    def coincident(first, second):
        result = False
        if Plane.parallel(first, second):
            # test if basepoints are equal
            basepoints_equal = second.basepoint == first.basepoint
            if not basepoints_equal:
                # create a vector from the two basepoints on each plane
                test_vector = second.basepoint
                test_vector.minus(first.basepoint)

                # is the 1st planes' normal orthogonal the test vector?
                first_orthogonal = Vector.orthagonal(first.normal_vector, test_vector)
                # is the 2nd planes' normal orthogonal the test vector?
                second_orthogonal = Vector.orthagonal(second.normal_vector, test_vector)

                if first_orthogonal and second_orthogonal:
                    result = True   # vector formed by points on different planes is orthogonal to both planes' normals,
                                    # therefore planes are coincident
            else:
                result = True # planes share a common point and they are parallel, therefore coincident

        return result

    @staticmethod
    def parallel(first, second):
        # determine the angle between the 2 supplied planes' normal vectors.
        angle = Vector.angle_degrees(first.normal_vector, second.normal_vector)

        # if angle between normals is 0, return true, else false
        if angle == 0.0 or angle == 180:
            return True
        else:
            return False

    def __str__(self):

        num_decimal_places = 3

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

        n = self.normal_vector

        try:
            initial_index = Plane.first_nonzero_index(n)
            # todo: can't index Vector object n? seems to work for Line class.  trace thru that?
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
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable.coordinates):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Plane.NO_NONZERO_ELTS_FOUND_MSG)

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

# def main():
#     # lesson 3, #7 - coding functions for planes
#     plane_one = Plane(normal_vector = Vector(['-0.412', '3.806', '0.728']), constant_term = '-3.46')
#     plane_two = Plane(normal_vector = Vector(['1.03', '-9.515', '-1.82']), constant_term = '8.65')
#     message = '\n' + "p1" + " and " + "p2" + " are parallel? "
#     if Plane.parallel(plane_one, plane_two):
#         message += "yes"
#     else:
#         message += "no"
#
#     message += " coincident: "
#     if Plane.coincident(plane_one, plane_two):
#         message += " yes"
#     else:
#         message += " no"
#     print(message)
#
#     plane_three = Plane(normal_vector=Vector(['2.611', '5.528', '0.283']), constant_term='4.6')
#     plane_four = Plane(normal_vector=Vector(['7.715', '8.306', '5.342']), constant_term='3.76')
#     message = '\n' + "p3" + " and " + 'p4' + " are parallel? "
#     if Plane.parallel(plane_three, plane_four):
#         message += "yes"
#     else:
#         message += "no"
#
#     message += " coincident: "
#     if Plane.coincident(plane_three, plane_four):
#         message += " yes"
#     else:
#         message += " no"
#     print(message)
#
#     plane_five = Plane(normal_vector=Vector(['-7.926', '8.625', '-7.212']), constant_term='-7.952')
#     plane_six = Plane(normal_vector=Vector(['-2.642', '2.875', '-2.404']), constant_term='2.443')
#     message = '\n' + "p5" + " and " + 'p6' + " are parallel? "
#     if Plane.parallel(plane_five, plane_six):
#         message += "yes"
#     else:
#         message += "no"
#
#     message += " coincident: "
#     if Plane.coincident(plane_five, plane_six):
#         message += " yes"
#     else:
#         message += " no"
#     print(message)

    # lesson 3, #4 - coding functions for lines
    # A_one = Line([4.046, 2.836], 1.21)
    # A_two = Line([10.115, 7.09], 3.025)
    # printLineInfo(A_one, A_two)
    #
    # B_one = Line([7.204, 3.182], 8.68)
    # B_two = Line([8.172, 4.114], 9.883)
    # printLineInfo(B_one, B_two)
    #
    # C_one = Line([1.182, 5.562], 6.744)
    # C_two = Line([1.773, 8.343], 9.525)
    # printLineInfo(C_one, C_two)

    # test for lesson 2 #10
    # vone = Vector(['-7.579', '-7.88'])
    # vtwo = Vector(['-2.029', '9.97', '4.172'])
    # vthree = Vector(['-2.328', '-7.284', '-1.214'])
    # vfour = Vector(['2.118', '4.827'])

    # wone = Vector(['22.737', '23.64'])
    # wtwo = Vector(['-9.231', '-6.639', '-7.245'])
    # wthree = Vector(['-1.821', '1.072', '-2.94'])
    # wfour = Vector(['0','0'])

    # onep = Vector.parallel(vone, wone)
    # oneo = Vector.orthagonal(vone, wone)

    # twop = Vector.parallel(vtwo, wtwo)
    # twoo = Vector.orthagonal(vtwo, wtwo)

    # threep = Vector.parallel(vthree, wthree)
    # threeo = Vector.orthagonal(vthree, wthree)

    # fourp = Vector.parallel(vfour, wfour)
    # fouro = Vector.orthagonal(vfour, wfour)

    ## lesson 2 #12, projections
    # vone = Vector(['3.039', '1.879']);
    # bone = Vector(['0.825', '2.036']);

    # vtwo = Vector(['-9.88', '-3.264', '-8.159']);
    # btwo = Vector(['-2.155', '-9.353', '-9.473']);

    # vthree = Vector(['3.009', '-6.172', '3.692', '-2.51']);
    # bthree = Vector(['6.404', '-9.144', '2.759', '8.718']);

    # result1 = Vector.v_parallel(vone, bone);
    # result2 = Vector.v_perp(vtwo, btwo);

    # result3perp = Vector.v_parallel(vthree, bthree)
    # result3parallel = Vector.v_perp(vthree, bthree)

    # print(result1)
    # print(result2)
    # print(result3perp)
    # print(result3parallel)

    # lesson #2, Quiz: coding cross products
    # print ("#0, v cross w") # debug print template
    # v = Vector(['1.0', '0.0', '0.0'])
    # w = Vector(['0.0', '1.0', '0.0'])
    # Vector.cross(v,w).print()

    # print ("#1, v cross w") # debug print template
    # v = Vector(['8.462', '7.893', '-8.187'])
    # w = Vector(['6.984', '-5.975', '4.778'])
    # Vector.cross(v,w).print()

    # print ("#2 area of parallellogram spanned by v & w") # debug print template
    # v = Vector(['-8.987', '-9.838', '5.031'])
    # w = Vector(['-4.268', '-1.861', '-8.866'])
    # print (Vector.cross(v,w).magnitude())

    # print ("#3 area of triangle spanned by v & w") # debug print template
    # v = Vector(['1.5', '9.547', '3.691'])
    # w = Vector(['-6.007', '0.124', '5.772'])
    # print (Decimal(0.5) * Vector.cross(v,w).magnitude())

# lesson 2, #8
# onev = Vector([7.887, 4.138])
# onew = Vector([-8.802, 6.776])
# print(Vector.dot(onev, onew))

# twov = Vector([-5.955, -4.904, -1.874])
# twow = Vector([-4.496, -8.755, 7.103])
# print(Vector.dot(twov, twow))

# threev = Vector([3.183, -7.627])
# threew = Vector([-2.668, 5.319])
# print(Vector.angle_rads(threev, threew))

# fourv = Vector([7.35, 0.221, 5.188])
# fourw = Vector([2.751, 8.259, 3.985])
# print(Vector.angle_degrees(fourv, fourw))