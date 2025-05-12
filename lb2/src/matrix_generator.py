import math
import random


class MatrixGenerator:
    def __init__(self) -> None:
        pass

    def generate_normal_matrix(self, n):
        matrix = []
        for i in range(n):
            row = [round(random.uniform(1, 100), 2) for _ in range(n)]
            row[i] = math.inf
            matrix.append(row)
        return matrix

    def generate_symmetrical_matrix(self, n):
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                a = round(random.uniform(1, 100), 2)
                matrix[i][j] = a
                matrix[j][i] = a
                if i == j:
                    matrix[i][j] = math.inf
        return matrix

    def generate_euclidean_matrix(self, n, dimensions=2):
        points = [[round(random.uniform(0, 100), 2) for _ in range(dimensions)] for _ in range(n)]
        matrix = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i == j:
                    matrix[i][j] = math.inf
                else:
                    distance = math.sqrt(sum((points[i][k] - points[j][k]) ** 2 for k in range(dimensions)))
                    matrix[i][j] = int(distance)
                    matrix[j][i] = int(distance)
        return matrix
