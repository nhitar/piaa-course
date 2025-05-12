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
        edges = []
        n = len(self.matrix)

        # Вес ребра, текущая вершина, соединяемая вершина
        for u in range(n):
            for v in range(u + 1, n):
                if self.matrix[u][v] != -1 or self.matrix[u][v] != math.inf:
                    edges.append((self.matrix[u][v], u, v))

        edges.sort()  # Сортировка по весу
        parent = list(range(n))

        mst = [[] for _ in range(n)]
        for _, u, v in edges:
            u_root, v_root = find(parent, u), find(parent, v)
            if u_root != v_root:
                mst[u].append(v)  # Удвоение рёбер
                mst[v].append(u)
                parent[v_root] = u_root

        return mst

    def dfs(self, node, adjacent, visited, path):
        visited.add(node)
        path.append(node)
        for v in sorted(adjacent[node], key=lambda x: self.matrix[node][x]):
            if v not in visited:
                self.dfs(v, adjacent, visited, path)

    def solve(self, start):
        mst = self.kruskal_mod()

        path = []
        self.dfs(start, mst, set(), path)
        path.append(start)

        print(round(sum(self.matrix[path[i]][path[i + 1]] for i in range(len(path) - 1)), 2))
        print(*path)
        return path
