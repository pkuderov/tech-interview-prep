# http://codeforces.com/problemset/problem/1092/B

import sys
from random import randint

IS_LOCAL = False

# ------------ INSERTION SORT ------------


def _swap(a, i, j):
    t = a[i]
    a[i] = a[j]
    a[j] = t


def insertionSort(n, a):
    a = a.copy()
    for i in range(n):
        min_i = i
        for j in range(i, n):
            if a[j] < a[min_i]:
                min_i = j
        _swap(a, i, min_i)

    return a


# --------- MERGE SORT --------------


def mergeSort(n, a):
    if n == 1:
        return a

    la = mergeSort(n//2, a[:n//2])
    ra = mergeSort(n - n//2, a[n//2:])
    return _merge(n, la, ra)


def _merge(n, a, b):
    res = [None]*n
    i, ia, ib = 0, 0, 0
    while i < n:
        is_a = ia < len(a)
        is_b = ib < len(b)
        if not is_b or (is_a and is_b and a[ia] <= b[ib]):
            res[i] = a[ia]
            ia += 1
        else:
            res[i] = b[ib]
            ib += 1
        i += 1
    return res


# --------- RADIX SORT --------------


def radixSort(n, a, base=100):
    a = list(zip(a, a))

    is_sorted = False
    while not is_sorted:
        backets = [[] for i in range(base)]
        for t, x in a:
            backets[t % base].append((t//base, x))

        a = [x for backet in backets for x in backet]
        is_sorted = all([p[0] == 0 for p in a])

    return [p[1] for p in a]


# --------- THE PROBLEM -------------


def countProblemsToSolve(n, a):
    r = 0
    for i in range(0, n, 2):
        r += a[i+1] - a[i]
    return r


def readInput():
    n = int(input())
    a = list(map(int, input().split()))
    return n, a


def writeResult(r):
    print(r)


def main():
    # n, a = (6, [5, 10, 2, 3, 14, 5]) if IS_LOCAL else readInput()
    n, a = (10000, [randint(1, 100) for _ in range(10000)])

    if not IS_LOCAL:
        n, a = readInput()

    sorted_a = radixSort(n, a)
    # sorted_a = insertionSort(n, a)
    # sorted_a = mergeSort(n, a)
    sorted_a2 = sorted(a)
    if sorted_a != sorted_a2:
        print("Sort mistake")
        pass

    r = countProblemsToSolve(n, sorted_a)
    writeResult(r)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'True':
        IS_LOCAL = True
    main()
