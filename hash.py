# http://codeforces.com/problemset/problem/2/A

import sys
from random import randint
from typing import Tuple, List
from timeit import default_timer as timer

IS_LOCAL = False


class HashSet:
    _max_frac = 3.
    _min_size = 7

    def __init__(self):
        self._n = 0
        self._size = self._min_size
        self._a: List[List[int]] = [None] * self._size

    def __contains__(self, key) -> bool:
        _, key_exists = self._find(key)
        return key_exists

    @property
    def buckets(self):
        return [bucket or [] for bucket in self._a]

    def add(self, key) -> None:
        bucket, key_exists = self._find(key)

        if key_exists:
            return

        if not self._is_enough_space():
            self._extend()
            bucket, _ = self._find(key)

        if bucket:
            bucket.append(key)
        else:
            self._a[self._hash(key)] = [key]
        self._n += 1

    def _find(self, key) -> Tuple[List[int], bool]:
        bucket = self._find_bucket(key)
        key_exists = self._find_key(key, bucket) if bucket else False
        return bucket, key_exists

    def _find_bucket(self, key) -> List[int]:
        return self._a[self._hash(key)]

    def _find_key(self, key, bucket) -> bool:
        for k in bucket:
            if k == key:
                return True
        return False

    def _extend(self) -> None:
        a = self._a
        self._n = 0
        self._size = (self._size + 1) * 2 - 1
        self._a = [None] * self._size

        for bucket in a:
            if not bucket:
                continue
            for x in bucket:
                self.add(x)

    def _is_enough_space(self) -> bool:
        return self._n / self._size <= self._max_frac

    def _hash(self, x) -> int:
        if not isinstance(x, int):
            x = hash(x)
        return x % self._size


class HashTable:
    _max_frac = 2.
    _min_size = 7

    def __init__(self):
        self._n = 0
        self._size = self._min_size
        self._a: List[List[Tuple[int, object]]] = [None] * self._size

    @property
    def buckets(self):
        return [bucket or [] for bucket in self._a]

    def __iter__(self):
        for bucket in self._a:
            if not bucket:
                continue
            for p in bucket:
                yield p

    def __getitem__(self, key) -> object:
        bucket, index = self._find(key)
        return bucket[index][1]

    def __setitem__(self, key, value) -> None:
        self.set(key, value)

    def _is_enough_space(self) -> bool:
        return self._n / self._size <= self._max_frac

    def add(self, x) -> None:
        self.set(x, x)

    def set(self, key, value) -> None:
        bucket, index = self._find(key)

        # update value
        if index is not None:
            bucket[index] = (key, value)
            return

        # need to add new (key, value)
        if not self._is_enough_space():
            self._extend()
            bucket, index = self._find(key)

        if bucket:
            bucket.append((key, value))
        else:
            key_hash = self._hash(key)
            self._a[key_hash] = [(key, value)]
        self._n += 1

    def __contains__(self, key) -> bool:
        _, index = self._find(key)
        return index is not None

    def _extend(self) -> None:
        a = self._a
        self._n = 0
        self._size = ((self._size + 1) * 2 - 1)
        self._a = [None] * self._size

        for bucket in a:
            if not bucket:
                continue
            for p in bucket:
                self.set(p[0], p[1])

    def _find(self, key) -> Tuple[List[Tuple[int, object]], int]:
        bucket = self._find_bucket(key)
        index = self._find_index(key, bucket) if bucket else None
        return bucket, index

    def _find_bucket(self, key) -> List[Tuple[int, object]]:
        return self._a[self._hash(key)]

    def _find_index(self, key, bucket) -> int:
        for i, p in enumerate(bucket):
            if p[0] == key:
                return i

    def _hash(self, x) -> int:
        if not isinstance(x, int):
            x = hash(x)
        return x % self._size


def testHashSetPerf(container, a):
    print(f'{type(container).__name__}')
    addTime = timer()
    for x in a:
        container.add(x)
    print(f'add: {timer() - addTime}')

    readTime = timer()
    assert (not [x for x in a if x not in container])
    print(f'read: {timer() - readTime}')

    print('_______')


def testPerformance():
    a = [randint(1, 10**5) for _ in range(10**5)]
    s = set()
    testHashSetPerf(s, a)
    table = HashSet()
    testHashSetPerf(table, a)
    table3 = HashTable()
    testHashSetPerf(table3, a)

    print(len(table._a), len([x for bucket in table.buckets for x in bucket]))


def solve2A():
    def get_winner(cur_winner, p):
        return p if not cur_winner or p[1] > cur_winner[1] else cur_winner

    n = 3
    lines = ("""andrew 3
andrew 1
mike 5
andrew -2
andrew 4""").split('\n')

    if not IS_LOCAL:
        n = int(input())
        lines = []
        for _ in range(n):
            lines.append(input())

    info = HashTable()
    for i, line in enumerate(lines):
        name, score = line.split()
        score = int(score)
        if name not in info:
            info[name] = [(i, score)]
        else:
            info[name].append((i, score))

    winner = None
    for name, scores in info:
        max_score = sum([score for _, score in scores])
        t_score = 0
        for i, score in scores:
            t_score += score
            if t_score >= max_score:
                if not winner or max_score > winner[1] or (
                        max_score == winner[1] and i < winner[2]):
                    winner = (name, max_score, i)
                break

    print(winner[0])


def main():
    # solve2A()
    testPerformance()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'True':
        IS_LOCAL = True
    main()
