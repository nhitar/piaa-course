import math
import copy

MAXIMUM = math.inf


class LittleSolver:
    def __init__(self, matrix):
        self.matrix = copy.deepcopy(matrix)
        self.record = math.inf
        self.arcs = {}
        print("Исходная матрица:")
        self.print_matrix(self.matrix)

    def print_matrix(self, matrix):
        for row in matrix:
            print(" ".join(str(x) if x != math.inf or x != -1 else "∞" for x in row))
        print()

    def subtract_min_from_matrix(self):
        subtracted_sum = 0

        for i in range(len(self.matrix)):
            mn = min([w for w in self.matrix[i] if w != -math.inf])
            if mn != 0 and mn != math.inf:
                print(f"Вычитаем минимум строки {i}: {mn}")
                subtracted_sum += mn
                for j in range(len(self.matrix)):
                    if self.matrix[i][j] != math.inf:
                        self.matrix[i][j] -= mn

        for i in range(len(self.matrix)):
            mn_column = min([row[i] for row in self.matrix])
            if mn_column != 0 and mn_column != math.inf:
                print(f"Вычитаем минимум столбца {i}: {mn_column}")
                subtracted_sum += mn_column
                for row in self.matrix:
                    row[i] -= mn_column
        print("Матрица после вычитания значений из строк и столбцов:")
        self.print_matrix(self.matrix)
        return subtracted_sum

    def coef_finder(self, row, column):
        mn_row = mn_column = MAXIMUM
        for i in range(len(self.matrix)):
            if i != row:
                mn_row = min(mn_row, self.matrix[i][column])
            if i != column:
                mn_column = min(mn_column, self.matrix[row][i])

        return mn_row + mn_column

    def find_zero_coefs(self):
        zeros = []
        coefs = []
        mx_coef = 0

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] == 0:
                    zeros.append([i, j])
                    coef = self.coef_finder(i, j)
                    coefs.append(coef)
                    mx_coef = max(mx_coef, coef)
                    print(f"Нулевая клетка ({i}, {j}), коэффициент: {coef}")

        for i in range(len(coefs)):
            if coefs[i] == mx_coef:
                print(f"\nВыбрана клетка ({zeros[i][0]}, {zeros[i][1]}) с макс. коэффициентом {mx_coef}")
                return zeros[i]
        exit(1)

    def find_longest_path(self, path: map, edge):
        start, end = edge
        end_path = []

        current = start
        while current in path.keys():
            end_path.append(path[current])
            current = path[current]

        current = start
        end_path.insert(0, current)
        while current in path.values():
            for k in path.keys():
                if path[k] == current:
                    current = k
            end_path.insert(0, current)
        return end_path

    def process_path(self, path, x_ind, y_ind):
        if len(path) < 2:
            return

        re_x = path[-1]
        re_y = path[0]

        if re_x - 1 in x_ind and re_y - 1 in y_ind:
            self.matrix[x_ind.index(re_x - 1)][y_ind.index(re_y - 1)] = math.inf
            print(f"Запрещаем переход ({re_x - 1} → {re_y - 1}) для избежания подцикла")

    def reduce_matrix(self, coordinate, path, x_ind, y_ind):
        re_x = x_ind[coordinate[0]]
        re_y = y_ind[coordinate[1]]

        path[re_x + 1] = re_y + 1
        print(f"Добавляем дугу: {re_x + 1} → {re_y + 1}")

        longest = self.find_longest_path(path, (re_x + 1, path[re_x + 1]))
        print(f"Текущий путь: {longest}")
        self.process_path(longest, x_ind, y_ind)

        x_ind.pop(coordinate[0])
        y_ind.pop(coordinate[1])
        self.matrix.pop(coordinate[0])
        for row in self.matrix:
            row.pop(coordinate[1])

        print("\nМатрица после удаления строки и столбца:")
        self.print_matrix(self.matrix)

    def check_solution(self, path, current_cost, x_ind, y_ind):
        flag = 0
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix)):
                if self.matrix[x][y] == math.inf:
                    path[x_ind[(x + 1) % 2] + 1] = y_ind[y] + 1
                    path[x_ind[x] + 1] = y_ind[(y + 1) % 2] + 1
                    self.arcs = path
                    self.record = current_cost
                    flag = 1
        if flag:
            print("\033[32mНайдено решение:\033[0m")
            print(f"Путь: {path}")
            print(f"Стоимость: {current_cost}")

    def solve(self, matrix, path, lower_limit, x_ind, y_ind, iteration=1):
        self.matrix = matrix
        print(f"\n\033[31mИтерация {iteration}\033[0m")
        print(f"Текущая нижняя граница: {lower_limit}")

        diff_cost = self.subtract_min_from_matrix()
        current_cost = diff_cost + lower_limit
        print(f"Текущая стоимость: {current_cost} (рекорд: {self.record})")

        if current_cost >= self.record:
            print("\033[31mОтсечение ветви\033[0m (стоимость >= рекорда)")
            return

        if len(matrix) == 2:
            self.check_solution(path, current_cost, x_ind, y_ind)
            return

        zeros = self.find_zero_coefs()
        new_path = copy.deepcopy(path)
        m1 = copy.deepcopy(matrix)
        new_x_ind = x_ind.copy()
        new_y_ind = y_ind.copy()

        self.matrix = m1
        print("\n\033[34mЛевая ветвь:\033[0m включаем дугу", zeros)
        self.reduce_matrix(zeros, new_path, new_x_ind, new_y_ind)
        self.solve(m1, new_path, current_cost, new_x_ind, new_y_ind, iteration + 1)

        matrix[zeros[0]][zeros[1]] = math.inf
        print("\n\033[34mПравая ветвь:\033[0m исключаем дугу", zeros)
        print("Матрица после запрета дуги:")
        self.print_matrix(matrix)
        self.solve(matrix, path, current_cost, x_ind.copy(), y_ind.copy(), iteration + 1)