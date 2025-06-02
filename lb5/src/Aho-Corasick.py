from collections import deque


class TrieNode:
    def __init__(self, char=None):
        self.char = char
        self.parent = None
        self.children = {}
        self.fail = None
        self.output = set()
        self.is_terminal = False


class AhoCorasick:
    def __init__(self, patterns):
        self.root = TrieNode()
        self.patterns = patterns
        self.build_trie()
        self.build_links()

    def build_trie(self):
        print("\033[1;34m1. Построение бора:\033[0m")
        for index, pattern in enumerate(self.patterns):
            print(f"\nДобавление образца #{index + 1}: '{pattern}'")
            node = self.root
            for i, char in enumerate(pattern):
                if char not in node.children:
                    print(f"  Создание узла для символа '{char}' (позиция {i + 1})")
                    node.children[char] = TrieNode(char)
                    node.children[char].parent = node
                else:
                    print(f"  Символ '{char}' уже существует в боре (позиция {i + 1})")
                node = node.children[char]
            node.output.add(index)
            node.is_terminal = True
            print(f"  Образец '{pattern}' добавлен (терминальный узел)")

    def build_links(self):
        print("\n\033[1;34m2. Построение суффиксных и терминальных ссылок:\033[0m")
        queue = deque()
        self.root.fail = self.root
        print("Установка fail-ссылок для детей корня:")
        for char, child in self.root.children.items():
            child.fail = self.root
            queue.append(child)
            print(f"  Узел '{char}': fail → корень")

        while queue:
            current_node = queue.popleft()
            print(f"\nОбработка узла '{current_node.char}' (родитель: '{"root" if current_node.parent.char is None else current_node.parent.char}')")

            for char, child in current_node.children.items():
                fail_node = current_node.fail
                print(f"  Обработка дочернего узла '{char}':")

                while fail_node != self.root and char not in fail_node.children:
                    print(f"    Переход по fail: '{fail_node.char}' → '{fail_node.fail.char}'")
                    fail_node = fail_node.fail

                if char in fail_node.children:
                    child.fail = fail_node.children[char]
                    print(f"    Установка fail: '{char}' → '{child.fail.char}'")
                else:
                    child.fail = self.root
                    print("    Установка fail: → root")
                child.output.update(child.fail.output)
                if child.fail.output:
                    print(f"    Добавлены output из fail-ссылки: {child.fail.output}")

                queue.append(child)

    def print_trie(self, node=None, level=0, prefix=''):
        if node is None:
            node = self.root
            print("\n\033[1;34m3. Визуализация бора:\033[0m")
            print("root [fail → self]")
            level = 1

        children = list(node.children.values())

        for i, child in enumerate(children):
            is_last = i == len(children) - 1
            new_prefix = prefix + ("    " if is_last else "│   ")

            node_info = f"{child.char}"
            node_info += " [TERM]" if child.is_terminal else ""
            node_info += f" [output: {child.output}]" if child.output else ""

            if child.fail:
                if child.fail == self.root:
                    fail_info = "root"
                else:
                    fail_path = []
                    fail_node = child.fail
                    while fail_node != self.root:
                        fail_path.append(fail_node.char)
                        fail_node = fail_node.parent
                    fail_path.reverse()
                    fail_info = "'" + ''.join(fail_path) + "'"

                node_info += f" [fail → {fail_info}]"

            branch = "└── " if is_last else "├── "
            print(prefix + branch + node_info)

            self.print_trie(child, level + 1, new_prefix)

    def search(self, text):
        print(f"\n\033[1;34m4. Поиск в тексте '{text}':\033[0m")
        current_node = self.root
        results = []

        for pos, char in enumerate(text):
            print(f"\nСимвол '{char}' (позиция {pos + 1}):")

            while current_node != self.root and char not in current_node.children:
                print(f"  Нет перехода по '{char}', переход по fail: '{current_node.char}' → '{current_node.fail.char}'")
                current_node = current_node.fail

            if char in current_node.children:
                current_node = current_node.children[char]
                print(f"  Переход в узел '{current_node.char}'")
                if current_node.fail != self.root and current_node.fail.output:
                    print(f"  Узел '{current_node.char}' унаследовал output через fail-ссылку: {current_node.fail.output}")
            else:
                current_node = self.root
                print("  Возврат в корень")

            if current_node.output:
                print(f"  Найдены подстроки {current_node.output} через терминальные ссылки")
                for pattern_index in current_node.output:
                    pattern = self.patterns[pattern_index]
                    start = pos - len(pattern) + 2
                    results.append((start, pattern_index + 1, pattern))
                    print(f"    Образец #{pattern_index + 1} '{pattern}' начинается на позиции {start}")

        return results

    def analyze_patterns(self, results, text):
        total_nodes = count_nodes(self.root)
        print(f"\n\033[1;35mАнализ результатов:\033[0m")
        print(f"Всего вершин в автомате: {total_nodes}")

        overlapping = []
        results_sorted = sorted(results, key=lambda x: x[0])

        for i in range(len(results_sorted)):
            start_i, _, pattern_i = results_sorted[i]
            end_i = start_i + len(pattern_i) - 1

            for j in range(i + 1, len(results_sorted)):
                start_j, _, pattern_j = results_sorted[j]
                end_j = start_j + len(pattern_j) - 1

                if start_j <= end_i:
                    overlapping.append((pattern_i, pattern_j, (start_i, end_i), (start_j, end_j)))
                else:
                    break

        if overlapping:
            print("\nПересекающиеся образцы:")
            for pattern1, pattern2, pos1, pos2 in overlapping:
                print(f"  '{pattern1}' {pos1} пересекается с '{pattern2}' {pos2}")

                overlap_start = max(pos1[0], pos2[0])
                overlap_end = min(pos1[1], pos2[1])
                overlap_text = text[overlap_start - 1:overlap_end]
                print(f"    Область пересечения: '{overlap_text}' (позиции {overlap_start}-{overlap_end})")
        else:
            print("\nПересекающихся образцов не найдено")

        return total_nodes, overlapping


def count_nodes(node):
    count = 1
    for child in node.children.values():
        count += count_nodes(child)
    return count


print("Введите текст:")
text = input()

print("Введите паттерны:")
patterns = input().split()

print("\033[1;34mАлгоритм Ахо-Корасик\033[0m")
print(f"Текст для поиска: '{text}'")
print(f"Образцы для поиска: {patterns}\n")

aho = AhoCorasick(patterns)
aho.print_trie()

results = aho.search(text)

print("\n\033[1;34mРезультаты поиска\033[0m")
for start_pos, pattern_idx, pattern in sorted(results):
    print(f"На позиции {start_pos} найден образец #{pattern_idx} '{pattern}'")

aho.analyze_patterns(results, text)
