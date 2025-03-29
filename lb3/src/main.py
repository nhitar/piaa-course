from levenshtein import *


def get_costs(is_special):
    try:
        costs = list(map(int, input().split()))
        if is_special:
            if len(costs) != 2:
                raise ValueError
        else:
            if len(costs) != 3:
                raise ValueError

        return costs
    except:
        print("Стоимости некорректны")
        exit(1)


def main():
    print("Введи стоимость замены, вставки и удаления символов")
    costs = Costs(*get_costs(0))

    print("\nВведи первую строку")
    s1 = input()

    print("\nВведи вторую строку")
    s2 = input()
    print()

    print("Добавить особо заменяемый и добавляемый символы? y")
    if input() == 'y':
        print("Введи цены, затем символы")
        special_costs = Special_Costs(*get_costs(1), *input().split())

        d = get_distance_matrix(s1, s2, costs, special_costs)
        solution = traceback_operations(d, s1, s2, costs, special_costs)
    else:
        d = get_distance_matrix(s1, s2, costs)
        solution = traceback_operations(d, s1, s2, costs)

    check_solution(s1, s2, solution)

    print('    ', *[c for c in s2], sep='  ')
    for i, column in enumerate(d):
        if i == 0:
            print(' ', end='  ')
        else:
            print(s1[i - 1], end='  ')

        for j in column:
            if j >= 10:
                print(j, end=' ')
                continue
            print(j, end='  ')
        print()
    print()

    print("Расстояние Левенштейна =", d[len(s1)][len(s2)])
    print(solution, s1, s2, sep='\n')


if __name__ == "__main__":
    main()
