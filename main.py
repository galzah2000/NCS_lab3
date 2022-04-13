# Галацин Захар ІО-82 Варіант 6
from math import log, factorial
from termcolor import cprint


def P_calculate_system(matrix_of_coherence, P):
    """лаб 2. Обрахунок надійності системи за вхідним графом і ймовірність безвідновної роботи"""
    cprint(
        "Лаб 2.Результат роботи функції обрахунку надійності системи за вхідним графом і ймовірностями безвідн. роботи. єл.",
        "blue")
    cprint("Ймовірність безвідмовної роботи", "blue")
    cprint(P, "blue")

    first_one = []
    for i in range(len(matrix_of_coherence)):
        for j in range(len(matrix_of_coherence[i])):
            if matrix_of_coherence[i][j] == 1:
                first_one.append(j)
                break
            if j == len(matrix_of_coherence[i]) - 1:
                first_one.append("")

    start_nodes = []
    finish_nodes = []
    min = len(matrix_of_coherence[0])
    for i in range(len(first_one)):
        if first_one[i] == "":
            finish_nodes.append(i)
        else:
            if first_one[i] <= min:
                min = first_one[i]
                start_nodes.append(i)

    path = []
    visit = []

    def func(start, set):
        set.append(start)
        if sum(matrix_of_coherence[start]) == 0:
            path.append(set.copy())
            set.pop()
            return 0
        for i in range(len(matrix_of_coherence[start])):
            if matrix_of_coherence[start][i] == 1:
                func(i, set)
        set.pop()
        return 0

    for i in start_nodes:
        func(i, [])

    cprint("Усі можливі шляхи", "blue")
    for i in path:
        cprint(i, "blue")

    all_sets = []

    line_str = "{:0>" + str(len(matrix_of_coherence)) + "}"
    for i in range(2 ** (len(matrix_of_coherence))):
        line = line_str.format((str(bin(i)[2:])))
        all_sets.append([])
        for j in line:
            all_sets[i].append(int(j))

    work_sets = []
    check = False
    for i in all_sets:
        for j in path:
            for k in j:
                if i[k] == 0:
                    check = False
                    break
                check = True
            if check:
                work_sets.append(i)
                check = False
                break

    cprint("Таблиця працездатних станів системи і ймовірність безвідмовної роботи", "blue")
    P_sets = []
    for i in work_sets:
        cprint(i, "blue", end=" ")
        S = 1
        for j in range(len(P)):
            if i[j] == 0:
                S *= (1 - P[j])
            if i[j] == 1:
                S *= P[j]
        cprint("{:f}".format(S), "blue")
        P_sets.append(S)
        S = 1
    P_system = sum(P_sets)
    cprint("P = {}".format(P_system), "blue")
    return P_system


def reserve(matrix_of_coherence: list, P: list, t: int, K: int, local: bool, loaded: bool):
    """Загальне / позподілене навантажене / ненавантажене резервування"""
    if not local:
        local_or_global = "global"
    else:
        local_or_global = "local"

    # ймовірність безвідмовної роботи на час t годин без резервування
    P_system = P_calculate_system(matrix_of_coherence, P)
    print("P_system = {}".format(P_system))

    # Обрахуемо ймовірність відмови на час t годин без резервування
    Q_system = 1 - P_system
    print("Q_system = {}".format(Q_system))

    # середній наробіток до відмови системи без резервуванння
    T_system = -t / log(P_system)
    print("T_system = {}".format(T_system))

    if not local:
        # Обрахуємо ймовірність відмови на час t годин системи з загальним навант./ не навант. резервуванням з кратністю K:
        if not loaded:
            Q_reserve_system = (1 / factorial(K + 1)) * Q_system
        else:
            Q_reserve_system = Q_system ** (K + 1)
        P_reserve_system = 1 - Q_reserve_system
    else:
        # Обрахуємо ймовірність відмови на час t годин системи з розподіл. навант./ не навант. резервуванням з кратністю K:
        def P_reserve_elements_system(P, K):
            if not loaded:
                return 1 - (1 / factorial(K + 1)) * (1 - P)
            if loaded:
                return 1 - (1 - P) ** (K + 1)

        P_local_system_elements = []
        for i in range(len(P)):
            P_reserve_system_elements = P_reserve_elements_system(P[i], K)
            P_local_system_elements.append(P_reserve_system_elements)
            print("Для {} елемента: P_local_reserved{} = {:<6f}, Q_local_reserved{} = {:<6f}".format(i + 1, i + 1,
                                                                                                     P_reserve_system_elements,
                                                                                                     i + 1,
                                                                                                     1 - P_reserve_system_elements))
        # системи при його навантаженому резервуванні з кратністю K за формулою 2.4:

        P_reserve_system = P_calculate_system(matrix_of_coherence, P_local_system_elements)
        Q_reserve_system = 1 - P_reserve_system

    # ймовірності безвідмовної роботи системи з резервуванням
    print("P_{}_reserved_system = {}".format(local_or_global, P_reserve_system))

    # ймовірності відмови роботи системи з резервуванням
    print("Q_{}_reserved_system = {}".format(local_or_global, Q_reserve_system))

    # середній наробіток до відмови системи без резервування на час t
    T_reserve_system = -t / log(P_reserve_system)
    print("T_{}_reserve system = {}".format(local_or_global, T_reserve_system))

    # виграш надійності протягом часу t за ймовірністю відмов:
    G_q = Q_reserve_system / (1 - P_system)
    print("Gq_{} ({}) = {}".format(local_or_global, t, G_q))

    # виграш надійності протягом часу t за ймовірністю безвідмовної роботи:
    G_p = P_reserve_system / P_system
    print("Gp_{} ({}) = {}".format(local_or_global, t, G_p))

    # виграш надійності за середнім часом безвідмовної роботи:
    T_system = -t / log(P_system)
    G_t = T_reserve_system / T_system
    print("Gt_{} ({}) = {}".format(local_or_global, t, G_t))


# матриця згідно варінату 6
matrix_of_coherence = [[0, 0, 1, 1, 0, 0, 0],  # 1
                       [0, 0, 1, 0, 1, 0, 1],  # 2
                       [0, 0, 0, 1, 1, 0, 1],  # 3
                       [0, 0, 0, 0, 1, 1, 0],  # 4
                       [0, 0, 0, 0, 0, 1, 1],  # 5
                       [0, 0, 0, 0, 0, 0, 0],  # 6
                       [0, 0, 0, 0, 0, 0, 0]]  # 7

P = [0.32, 0.82, 0.15, 0.24, 0.66, 0.99, 0.93]
t = 1390

local1 = False # загальне або роздільне навантаження. True = роздільне, False = загальне
loaded1 = True  # навантажена / не навантажена система. True = навантажена, False = не навантажена
K1 = 3 # кратність резервування першої системи


local2 = True # загальне або роздільне навантаження. True = роздільне, False = загальне
loaded2 = False  # навантажена / не навантажена система. True = навантажена, False = не навантажена
K2 = 3 # кратність резервування другої системи

"""
# Вхідні данні згідно прикладу для перевірки роботи програми
matrix_of_coherence = [[0, 1, 1, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 1, 0, 0, 0],
                       [0, 0, 0, 1, 0, 1, 0, 1],
                       [0, 0, 0, 0, 1, 1, 0, 1],
                       [0, 0, 0, 0, 0, 1, 1, 0],
                       [0, 0, 0, 0, 0, 0, 1, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]]

P = [0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.92, 0.94]
t = 1000

local1 = False # загальне або роздільне навантаження. True = роздільне, False = загальне
loaded1 = False  # навантажена / не навантажена система. True = навантажена, False = не навантажена
K1 = 1 # кратність резервування першої системи


local2 = True # загальне або роздільне навантаження. True = роздільне, False = загальне
loaded2 = True  # навантажена / не навантажена система. True = навантажена, False = не навантажена
K2 = 1 # кратність резервування другої системи
"""

local = [local1, local2]
loaded = [loaded1, loaded2]
K = [K1, K2]

cprint("Умова", "green")
for i in range(len(local)):
    cprint("Матриця зв’язності", "green")
    for j in matrix_of_coherence:
        cprint(j, 'green')
    cprint("P = {}".format(P), "green")
    cprint("Система {}:".format(i+1), "green", end=" ")
    if not local[i]:
        cprint("загальне", "green", end=" ")
    else:
        cprint("роздільне", "green", end=" ")

    if not loaded[i]:
        cprint("ненавантажене", "green", end=" ")
    else:
        cprint("навантажене", "green", end=" ")

    cprint("резервування з кратністю {}".format(K1), "green")

    cprint("t = {}".format(t), 'green')

    reserve(matrix_of_coherence, P, t, K1, local[i], loaded[i])
