import math
import copy
import time

from matrix_generator import MatrixGenerator
from little_alg import LittleSolver
from ado_mod_alg import ADO_MOD
from visualization import visualize_mst


def print_matrix(matrix):
    print()
    for i in matrix:
        print(i)
    print()


class Handler:
    def __init__(self):
        self.matrix_generator = MatrixGenerator()
        self.matrix = []

    def generate_matrix(self, matrix_type):
        print("Введи количество городов (размер матрицы)")
        n = int(input())

        if matrix_type == "normal":
            self.matrix = self.matrix_generator.generate_normal_matrix(n)
        elif matrix_type == "symmetrical":
            self.matrix = self.matrix_generator.generate_symmetrical_matrix(n)
        elif matrix_type == "euclidean":
            self.matrix = self.matrix_generator.generate_euclidean_matrix(n)

        if n <= 15:
            print_matrix(self.matrix)

    def load_matrix(self):
        file = open("text.txt", 'r')
        self.matrix = []
        for row in file:
            current = []
            for i in row.split():
                if i == "inf" or i == "math.inf":
                    current.append(math.inf)
                else:
                    current.append(float(i))
            self.matrix.append(current)
        if len(self.matrix) <= 15:
            print_matrix(self.matrix)

        file.close()

    def save_matrix(self):
        if self.matrix is []:
            print("Матрица пустая\n")
            return

        file = open("text.txt", 'w')

        for row in self.matrix:
            file.write(' '.join(str(i) for i in row) + '\n')

        file.close()

    def little_init(self):
        if self.matrix is []:
            self.generate_matrix("normal")

        copy_matrix = copy.deepcopy(self.matrix)

        for i in range(len(copy_matrix[0])):
            for j in range(len(copy_matrix[0])):
                if i != j:
                    copy_matrix[i][j] = int(copy_matrix[i][j])
                else:
                    copy_matrix[i][j] = math.inf

        l = LittleSolver(copy_matrix)

        x_ind = [x for x in range(len(copy_matrix))]
        y_ind = [y for y in range(len(copy_matrix))]
        s = time.perf_counter()
        l.solve(copy_matrix, {}, 0, x_ind, y_ind, 0)
        e = time.perf_counter()
        print("Затраченное время:", e - s)

        nxt = l.arcs[1]
        res = [0]
        while nxt != 1:
            res.append(nxt - 1)
            nxt = l.arcs[nxt]
        print(*res, sep=" ")

        # print("best path:", l.arcs)
        print(l.record / 1)

    def ado_mod_init(self):
        if self.matrix is []:
            self.generate_matrix("normal")

        print("Введи начальную вершину")
        start = int(input())
        if start >= len(self.matrix[0]):
            print("Неправильная нумерация\n")
            return

        matrix = copy.deepcopy(self.matrix)
        s = time.perf_counter()
        path = ADO_MOD(matrix).solve(start)
        e = time.perf_counter()
        print("Затраченное время:", e - s)

        if len(path) <= 15:
            visualize_mst(self.matrix, path)

    def start(self):
        print("Доступные команды:")
        while True:
            print("1 Сгенерировать обычную матрицу\n"
                  "2 Сгенерировать симметричную матрицу\n"
                  "3 Сгенерировать евклидову матрицу\n"
                  "4 Загрузить матрицу\n"
                  "5 Сохранить матрицу\n"
                  "6 Метод Литтла\n"
                  "7 Метод АДО МОД\n"
                  "8 Выход")
            choice = input()
            print()

            if choice == '1':
                self.generate_matrix("normal")
            elif choice == '2':
                self.generate_matrix("symmetrical")
            elif choice == '3':
                self.generate_matrix("euclidean")
            elif choice == '4':
                self.load_matrix()
            elif choice == '5':
                self.save_matrix()
            elif choice == '6':
                self.little_init()
            elif choice == '7':
                self.ado_mod_init()
            elif choice == '8':
                return


if __name__ == "__main__":
    handler = Handler()
    handler.start()
