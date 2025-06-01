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
        print("\n\033[1;34mПостроение суффиксных и терминальных ссылок:\033[0m")
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

    def print_trie(self, node=None, level=0):
        if node is None:
            node = self.root
            print("\n\033[1;34mВизуализация бора:\033[0m")

        prefix = "    " * level
        char = node.char if node.char else "root"
        term = " [TERM]" if node.is_terminal else ""
        fail = f" (fail: '{node.fail.char if node.fail and node.fail.char else 'root'}')" if node.fail else ""
        out = f" [output: {node.output}]" if node.output else ""
        print(f"{prefix}└── {char}{term}{fail}{out}")

        for child in node.children.values():
            self.print_trie(child, level + 1)

    def find_matches(self, text):
        current_node = self.root
        results = []
        for pos, char in enumerate(text):
            while current_node != self.root and char not in current_node.children:
                current_node = current_node.fail
            if char in current_node.children:
                current_node = current_node.children[char]
            else:
                current_node = self.root
            for pattern_index in current_node.output:
                pattern = self.patterns[pattern_index]
                start_pos = pos - len(pattern) + 1
                results.append((start_pos, pattern_index))
        print(results)
        return results


def find_wildcard_matches(text, pattern, wildcard):
    print("\n\033[1;34mШаблон с джокерами\033[0m")
    print(f"Текст: '{text}'")
    print(f"Шаблон: '{pattern}' (джокер: '{wildcard}')")

    print("\n\033[1;34m1. Разбиение шаблона на подстроки:\033[0m")
    subpatterns, positions, current = [], [], []
    start_pos = 0

    for i, char in enumerate(pattern):
        if char == wildcard:
            if current:
                subpatterns.append(''.join(current))
                positions.append((start_pos, i - 1))
                print(f"Найдена подстрока: '{''.join(current)}' (позиции в шаблоне: {start_pos}-{i-1})")
                current = []
            start_pos = i + 1
        else:
            current.append(char)

    if current:
        subpatterns.append(''.join(current))
        positions.append((start_pos, len(pattern) - 1))
        print(f"Найдена подстрока: '{''.join(current)}' (позиции в шаблоне: {start_pos}-{len(pattern)-1})")

    if not subpatterns:
        print("Нет подстрок для поиска")
        return []

    print("\n\033[1;34m2. Построение автомата Ахо-Корасик:\033[0m", end="")
    aho = AhoCorasick(subpatterns)
    print(f"Добавлено подстрок: {len(subpatterns)}")

    aho.print_trie()

    print("\n\033[1;34m3. Поиск подстрок в тексте:\033[0m")
    matches = aho.find_matches(text)
    print(f"Найдено совпадений: {len(matches)}")

    print("\n\033[1;34m4. Подсчет возможных начал шаблона:\033[0m")
    C = [0] * (len(text) + len(pattern))
    for pos, pattern_idx in matches:
        possible_start = pos - positions[pattern_idx][0]
        C[pos - (positions[pattern_idx][0])] += 1
        print(f"Подстрока '{subpatterns[pattern_idx]}' на позиции {pos} → возможное начало шаблона: {possible_start} (C[{possible_start}] = {C[possible_start]})")

    required = len(subpatterns)
    possible_starts = [i for i in range(len(C)) if C[i] == required]

    valid_starts = []
    for start in possible_starts:
        if start + len(pattern) <= len(text):
            valid_starts.append(start + 1)
        else:
            print(f"Отброшена позиция {start} (выходит за границы текста)")

    print(f"\n\033[1;32mНайденные позиции: {sorted(valid_starts)}\033[0m")
    return sorted(valid_starts)


print("Введите текст:")
text = input()

print("Введите паттерн с джокерами:")
pattern = input()

print("Введите символ джокера:")
wildcard = input()

matches = find_wildcard_matches(text, pattern, wildcard)
for match in sorted(matches):
    print(match)
