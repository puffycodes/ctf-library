# file: integer_matrix_math.py

# Matrix Inverse Modulo
# Ref: https://www.andreaminini.net/math/modular-inverse-of-a-matrix
# Ref: https://stackoverflow.com/questions/4287721/easiest-way-to-perform-modular-matrix-inversion-with-python
# Matrix Inverse and Cofactor
# Ref: https://www.geeksforgeeks.org/compute-the-inverse-of-a-matrix-using-numpy/
# Ref: https://www.geeksforgeeks.org/how-to-find-cofactor-of-a-matrix-using-numpy/
# Adjugate
# Ref: https://stackoverflow.com/questions/51010662/getting-the-adjugate-of-matrix-in-python/75566371#75566371

import numpy as np

class IntegerMatrixMath:

    # Ref: https://www.geeksforgeeks.org/how-to-find-cofactor-of-a-matrix-using-numpy/
    # Ref: https://stackoverflow.com/questions/4287721/easiest-way-to-perform-modular-matrix-inversion-with-python
    # Ref: https://math.stackexchange.com/questions/2686150/inverse-of-a-modular-matrix
    @staticmethod
    def matrix_modular_inverse(matrix, modulo):
        # TODO: The function linalg.inv() is causing the rounding issue?
        matrix_cofactor = np.linalg.inv(matrix).transpose() * np.linalg.det(matrix)
        matrix_adjucate = matrix_cofactor.transpose()
        # TODO: There is some rounding issue here?
        matrix_inverse = (matrix_adjucate * pow(int(np.linalg.det(matrix)), -1, modulo)) % modulo
        # TODO: This function needs to return intergers
        return matrix_inverse
    
    @staticmethod
    def cofactor(matrix):
        det = np.linalg.det(matrix)
        if det == 0:
            return None
        cofactor_matrix = np.linalg.inv(matrix).transpose() * det
        return cofactor_matrix
    
    @staticmethod
    def cofactor_ref(matrix):
        # TODO: This will cause rounding issues?
        cofactor_matrix = np.linalg.inv(matrix).transpose() * np.linalg.det(matrix)
        return cofactor_matrix
    
    @staticmethod
    def adjucate_ref(matrix):
        cofactor_matrix = IntegerMatrixMath.cofactor_ref(matrix)
        adjucate_matrix = cofactor_matrix.transpose()
        return adjucate_matrix
    
    @staticmethod
    def modular_inverse_ref(matrix, modulo):
        adjucate_matrix = IntegerMatrixMath.adjucate_ref(matrix)
        # TODO: There is some rounding issue here?
        inverse_matrix = (adjucate_matrix * pow(int(np.linalg.det(matrix)), -1, modulo)) % modulo
        return inverse_matrix

# --- end of file --- #
