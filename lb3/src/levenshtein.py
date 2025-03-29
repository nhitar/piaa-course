class Costs:
    def __init__(self, replacement_cost, insertion_cost, deletion_cost):
        self.replacement_cost = replacement_cost
        self.insertion_cost = insertion_cost
        self.deletion_cost = deletion_cost
    

class Special_Costs:
    def __init__(self, replacement_cost, insertion_cost, replacement_symbol, insertion_symbol):
        self.replacement_cost = replacement_cost
        self.insertion_cost = insertion_cost
        self.replacement_symbol = replacement_symbol
        self.insertion_symbol = insertion_symbol


def decide_costs(symbol_1, symbol_2, costs, special_costs = None):
    if special_costs and symbol_1 == special_costs.replacement_symbol:
        replacement_cost = special_costs.replacement_cost
    else:
        replacement_cost = costs.replacement_cost

    if special_costs and symbol_2 == special_costs.insertion_symbol:
        insertion_cost = special_costs.insertion_cost
    else:
        insertion_cost = costs.insertion_cost
    return replacement_cost, insertion_cost


def get_distance_matrix(s1, s2, costs, special_costs = None):
    m, n = len(s1), len(s2)

    d = [[-1] * (n+1) for _ in range(m+1)]
    d[0][0] = 0

    for j in range(1, n + 1):
        if special_costs and s2[j - 1] == special_costs.insertion_symbol:
            d[0][j] = d[0][j - 1] + special_costs.insertion_cost
            continue    
        d[0][j] = d[0][j - 1] + costs.insertion_cost

    for i in range(1, m + 1):
        d[i][0] = d[i - 1][0] + costs.deletion_cost
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                d[i][j] = d[i - 1][j - 1]
                continue

            replacement_cost, insertion_cost = decide_costs(s1[i - 1], s2[j - 1], costs, special_costs)

            d[i][j] = min(
                d[i - 1][j - 1] + replacement_cost,
                d[i][j - 1] + insertion_cost,
                d[i - 1][j] + costs.deletion_cost
            )
    return d


def traceback_operations(d, s1, s2, costs, special_costs = None):
    m, n = len(s1), len(s2)
    solution = ''
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            solution += "M"
            i -= 1
            j -= 1
            continue
        
        replacement_cost, insertion_cost = decide_costs(s1[i - 1], s2[j - 1], costs, special_costs)

        if i > 0 and j > 0 and d[i - 1][j - 1] + replacement_cost == d[i][j]:
            solution += 'R'
            i -= 1
            j -= 1
        elif j > 0 and d[i][j - 1] + insertion_cost == d[i][j]:
            solution += 'I'
            j -= 1
        elif i > 0 and d[i - 1][j] + costs.deletion_cost == d[i][j]:
            solution += 'D'
            i -= 1
    return solution[::-1]


def check_solution(s1, s2, solution):
    s = list(s1)
    ptr = 0
    for option in solution:
        print(''.join(s), option, ptr)
        if option == 'R':
            s[ptr] = s2[ptr]
        elif option == 'I':
            s.insert(ptr, s2[ptr])
        elif option == 'D':
            del s[ptr]
            ptr -= 1
        ptr += 1
        print(''.join(s), option, ptr, "\n")

    print("Изменённая s1 по сравнению с s2")
    print(''.join(s))
    print(s2)
    if ''.join(s) == s2:
        print("Совпадение\n")
