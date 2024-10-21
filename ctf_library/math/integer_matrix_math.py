# file: integer_matrix_math.py

# Matrix Modular Inverse
# Ref: https://www.andreaminini.net/math/modular-inverse-of-a-matrix
# Ref: https://stackoverflow.com/questions/4287721/easiest-way-to-perform-modular-matrix-inversion-with-python
# Ref: https://math.stackexchange.com/questions/2686150/inverse-of-a-modular-matrix
# Ref: https://www.geeksforgeeks.org/compute-the-inverse-of-a-matrix-using-numpy/
#
# Matrix Cofactor
# Ref: https://www.geeksforgeeks.org/how-to-find-cofactor-of-a-matrix-using-numpy/
# Ref: https://stackoverflow.com/questions/6527641/speed-up-python-code-for-computing-matrix-cofactors
#
# Adjugate
# Ref: https://stackoverflow.com/questions/51010662/getting-the-adjugate-of-matrix-in-python/75566371#75566371
#
# Matrix Determinant
# Ref: https://en.wikipedia.org/wiki/Determinant
# Ref: https://byjus.com/maths/determinant-of-a-matrix/

import numpy as np

class IntegerMatrixMath:

    # Return the minor matrix by removing row i and column j from the given matrix.
    @staticmethod
    def matrix_minor(matrix, i, j):
        top = matrix[:i,:]
        bottom = matrix[i+1:,:]
        minor_step_1 = np.concatenate((top, bottom), axis=0)
        left = minor_step_1[:,:j]
        right = minor_step_1[:,j+1:]
        result = np.concatenate((left, right), axis=1)
        return result

    # Return the cofactor matrix of the given matrix.
    @staticmethod
    def matrix_cofactor(matrix):
        result = np.zeros_like(matrix)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                minor = IntegerMatrixMath.matrix_minor(matrix, i, j)
                result[i][j] = IntegerMatrixMath.matrix_det(minor) * pow(-1, (i+j))
        return result
    
    # Return the Adjucate of the given matrix.
    @staticmethod
    def matrix_adjucate(matrix):
        matrix_cofactor = IntegerMatrixMath.matrix_cofactor(matrix)
        return matrix_cofactor.transpose()
    
    # Return the modulo of the given matrix.
    @staticmethod
    def matrix_modulo(matrix, modulo):
        return matrix % modulo
    
    # Return the modular inverse of the given matrix.
    #
    # (TODO: Do those check? Or just catch ValueError?)
    # Modular inverse does not exist if
    #   (a) determinant is zero
    #   (b) determinant and module are not co-prime.
    @staticmethod
    def matrix_modular_inverse(matrix, modulo):
        matrix_cofactor = IntegerMatrixMath.matrix_cofactor(matrix)
        matrix_adjucate = matrix_cofactor.transpose()
        det_modular_inverse = pow(IntegerMatrixMath.matrix_det(matrix), -1, modulo)
        matrix_inverse = (matrix_adjucate * det_modular_inverse) % modulo
        return matrix_inverse
    
    # Return the determinant of the matrix, in integer
    @staticmethod
    def matrix_det(matrix):
        return int(round(np.linalg.det(matrix)))
    
    # --- Reference implementation. Do not use.
    
    @staticmethod
    def matrix_cofactor_ref(matrix):
        # This is a reference implementation that will give a non-integer answer.
        cofactor_matrix = np.linalg.inv(matrix).transpose() * np.linalg.det(matrix)
        return cofactor_matrix
    
    @staticmethod
    def matrix_adjucate_ref(matrix):
        # This is a reference implementation that will give a non-integer answer,
        # because of the non-integer answer from matrix_cofactor_ref().
        cofactor_matrix = IntegerMatrixMath.matrix_cofactor_ref(matrix)
        adjucate_matrix = cofactor_matrix.transpose()
        return adjucate_matrix
    
    @staticmethod
    def matrix_modular_inverse_ref(matrix, modulo):
        # This is a reference implementation that will give a non-integer answer,
        # because of the non-integer answer from matrix_cofactor_ref().
        cofactor_matrix = IntegerMatrixMath.matrix_cofactor_ref(matrix)
        adjucate_matrix = cofactor_matrix.transpose()
        det_modular_inverse = pow(int(np.linalg.det(matrix)), -1, modulo)
        inverse_matrix = (adjucate_matrix * det_modular_inverse) % modulo
        return inverse_matrix

# --- end of file --- #
