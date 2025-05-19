import math


def find(parent, node):
    while parent[node] != node:
        parent[node] = parent[parent[node]]
        node = parent[node]
    return node


class ADO_MOD:
    def __init__(self, matrix):
        self.matrix = matrix

    def kruskal_mod(self):
        print("\033[31mПостроение минимального остовного дерева (Краскал)\033[0m")
        edges = []
        n = len(self.matrix)

        # Вес ребра, текущая вершина, соединяемая вершина
        for u in range(n):
            for v in range(u + 1, n):
                if self.matrix[u][v] != -1 and self.matrix[u][v] != math.inf:
                    edges.append((self.matrix[u][v], u, v))
                    print(f"Добавлено ребро: {u} -> {v}, вес = {self.matrix[u][v]}")

        edges.sort()  # Сортировка по весу
        print("\n\033[31mОтсортированные рёбра:\033[0m", edges)

        parent = list(range(n))
        mst = [[] for _ in range(n)]

        print("\n\033[31mПостроение MST:\033[0m")
        for weight, u, v in edges:
            u_root, v_root = find(parent, u), find(parent, v)
            if u_root != v_root:
                mst[u].append(v)
                mst[v].append(u)
                parent[v_root] = u_root
                print(f"Добавлено ребро в MST: {u} — {v} (вес: {weight})")
                continue

        mst_map = {}
        for i, v in enumerate(mst):
            mst_map[i] = v
        print("\033[32mМинимальное остовное дерево (MST):\033[0m", mst_map)
        return mst

    def dfs(self, node, adjacent, visited, path):
        visited.add(node)
        path.append(node)
        print(f"\033[34mПосещена вершина: {node}\033[0m")
        print(f"Текущий путь: {path}")

        for v in sorted(adjacent[node], key=lambda x: self.matrix[node][x]):
            if v not in visited:
                print(f"Переход из {node} в {v} (вес: {self.matrix[node][v]})")
                self.dfs(v, adjacent, visited, path)

    def solve(self, start):
        mst = self.kruskal_mod()
        path = []
        print("\n\033[31mОбход MST в глубину (DFS)\033[0m")
        self.dfs(start, mst, set(), path)

        path.append(start)
        print(f"\n\033[31mПолный путь после DFS:\033[0m {path}")

        total_cost = round(sum(self.matrix[path[i]][path[i + 1]] for i in range(len(path) - 1)), 2)
        print(f"\033[1;32mОбщая стоимость пути: {total_cost}\033[0m")
        print("\033[1;32mИтоговый путь:\033[0m", " → ".join(map(str, path)))

        return path
