import numpy as np


def multMatrix(matrixA, matrixB):
    return matrixA @ matrixB


def multMatrVect(matrix, vector):
    return matrix @ vector


def calcSysEqu(coef, frMem):
    return np.linalg.solve(coef, frMem)


def calcDetMat(matrix):
    return round(np.linalg.det(matrix))


def inverseMat(matrix):
    return np.linalg.inv(matrix)


def transposMat(matrix):
    return matrix.T


matrixA = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])
matrixB = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
print(multMatrix(matrixA, matrixB))

print()

matrixC = np.array([[1, 2, 3], [6, 7, 8], [11, 12, 13], [16, 17, 18], [21, 22, 23]])
vector = np.array([1, 2, 3])
print(multMatrVect(matrixC, vector))

print()

#  1x1 + 5x2 = 11
#  2x1 + 3x2 = 8
coef = np.array([[1, 5], [2, 3]])
frMem = np.array([11, 8])
print(calcSysEqu(coef, frMem))

print()

matrixD = np.array([[1, 2], [3, 4]])
print(calcDetMat(matrixD))

print()

matrixE = np.array([[1, 2], [3, 4]])
print(inverseMat(matrixE))

print()

matrixF = np.array([[1, 2], [3, 4]])
print(transposMat(matrixF))

print()

matrixF = np.array([[1, 2, 3, 4, 5], [0, 6, 7, 8, 9], [0, 0, 10, 11, 12], [0, 0, 0, 13, 14], [0, 0, 0, 0, 15]])
print(calcDetMat(matrixF))

res = 1
for i in range(0, 5):
    res *= matrixF[i][i]
print(res)