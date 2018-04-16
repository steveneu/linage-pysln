import sys
from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    ATTEMPTED_ZERO_DIVIDE = 'An attempt was made to divide by zero'
    ATTEMPTED_CROSS_PRODUCT_WO3DINPUTS = 'Cannot perform cross product without 3D input vectors'

    def __init__(self, coordinates):
        try: 
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')
    
    ## print coordinates
    def print(self):
        print ('coordinates: ')
        for x in self.coordinates:
            print(x)

    ## +, -, scalar multiply
    def plus(self, v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    ## magnitude, normalization
    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return Decimal(sqrt(sum(coordinates_squared)))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0')/magnitude)

        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
    
    def zero(self):
        return self.magnitude() == 0

    ## dot/inner product, get angle between 2 vectors (radians, degrees)
    @staticmethod
    def dot(first, second):
        result = 0
        if first.zero() or second.zero():
            result = 0
        else:
            #products = [one * two for one,two in zip(first.coordinates, second.coordinates)]
            #result = sum(products)
            result = sum([x*y for x,y in zip(first.coordinates, second.coordinates)])
        return result

    @staticmethod
    def angle_rads(first, second):
        try:
            #numerator = Vector.dot(first, second)
            #denominator = first.magnitude() * second.magnitude()
            u1 = first.normalized()
            u2 = second.normalized()
            dotted = Vector.dot(u1, u2)
            if (dotted <-1):
                error = abs(dotted-(-1))
                if (error < 0.00001):
                    dotted = -1
            elif (dotted > 1):
                error = dotted-1
                if error < 0.00001:
                    dotted = 1

            result = acos(dotted)

            #arg = numerator/denominator
            #result = acos(arg)
        except ZeroDivisionError:
            raise Exception(Vector.ATTEMPTED_ZERO_DIVIDE + ' in angle_rads()')
        return result
    
    @staticmethod
    def angle_degrees(first, second, tolerance=1e-10):
        result = Vector.angle_rads(first, second)
        return result * 180/pi # convert to degrees and return

    @staticmethod
    def orthagonal(first, second, tolerance=1e-10):
        result = False
        if first.zero() or second.zero():
            result = True
        else:
            result = abs(Vector.dot(first, second)) < tolerance
        return result
    
    @staticmethod
    def parallel(first, second): # return true if supplied vectors are parallel
        parallel = False
        if first.zero() or second.zero():
            parallel = True
        else:
            angle = Vector.angle_degrees(first, second)
            parallel = angle == 0 or angle == 180

        return parallel

    # projection functions
    @staticmethod 
    def v_parallel(self, v, b): # return the (2D?) projection of v onto b a.k.a. v"
        try:
            b_normalized = b.normalized()
            u = Vector.dot(v, b_normalized)
            return b_normalized.times_scalar(u)
        except Exception as e:
            if str(e) == self.CANNON_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLELL_COMPONENT_MSG)
            else:
                raise e

    @staticmethod
    def v_perp(self, v, b): # return the vector orthagonal to v"
        try:
            vee = v
            return vee.minus(Vector.v_parallel(v, b))
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLELL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGANAL_COMPONENT_MSG)
            else:
                raise e

    # cross product, area of parallelogram defined by 2 vectors, area of triangle defined by 2 vectors
    @staticmethod
    def cross(v, w):
        # todo: assert v.dimension == 3 && w.dimension == 3
        a1 = v.coordinates[0]
        a2 = v.coordinates[1]
        a3 = v.coordinates[2]
        b1 = w.coordinates[0]
        b2 = w.coordinates[1]
        b3 = w.coordinates[2]
        x = a2 * b3 - a3 * b2
        y = a3 * b1 - a1 * b3
        z = a1 * b2 - a2 * b1
        return Vector([x,y,z])
    
    @staticmethod
    def area_of_parallellogram(v, w):
        return Vector.cross(v,w).magnitude()

    @staticmethod
    def area_of_triangle_with(v,w):
        return Vector.area_of_parallellogram()/Decimal ('2.0')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates


    