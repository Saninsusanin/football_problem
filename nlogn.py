import sys

from math import inf


def read_data():
    n, m = list(map(int, sys.stdin.readline().split()))
    yield n

    for _ in range(m):
        yield next(read_query())


def read_query():
    score_a, score_b = list(map(int, sys.stdin.readline().split()))
    players = list(map(int, sys.stdin.readline().split()))
    yield score_a, score_b, players


class SegmentTree:
    def __init__(self, array):
        n = len(array) - 1
        n |= n >> 1
        n |= n >> 2
        n |= n >> 4
        n |= n >> 8
        n |= n >> 16
        n += 1
        self.arr_len = n
        self.tree = [0] * (n - 1) + array + [0] * (n - len(array))
        self.number_of_elements = [0] * (n - 1) + [1] * len(array) + [0] * (n - len(array))

        for i in range(n - 2, -1, -1):
            self.tree[i] = max(self.tree[i * 2 + 1: i * 2 + 3])
            self.number_of_elements[i] = sum(self.number_of_elements[i * 2 + 1: i * 2 + 3])

    def get_max(self, l, r):
        l += self.arr_len - 1
        r += self.arr_len - 2
        maximal = -inf

        while (l <= r):
            if ((l % 2) == 0):
                left_max = self.tree[l]
                l = (l + 1 - 1) // 2
            else:
                left_max = -inf
                l = (l - 1) // 2

            if ((r % 2) == 1):
                right_max = self.tree[r]
                r = (r - 1 - 2) // 2
            else:
                right_max = -inf
                r = (r - 2) // 2

            maximal = max(maximal, left_max, right_max)

        return maximal

    def update(self, i, value):
        node = self.arr_len - 1 + i
        self.tree[node] += value

        while node > 0:
            node = (node - 1) // 2
            left_child = node * 2 + 1
            right_child = node * 2 + 2
            self.tree[node] = max(self.tree[left_child], self.tree[right_child])

    def get_number_of_elements_less_than(self, value):
        stack = [0]
        number_of_elements = 0

        while stack:
            curr_node_index = stack.pop()
            curr_max_value = self.tree[curr_node_index]

            if curr_max_value < value:
                number_of_elements += self.number_of_elements[curr_node_index]
            else:
                stack.extend(filter(lambda x: x < len(self.tree),
                                    (2 * curr_node_index + 1, 2 * curr_node_index + 2)))

        return number_of_elements


def solve():
    data_generator = read_data()
    n = next(data_generator)
    segment_tree = SegmentTree([0] * n)

    for (score_a, score_b, players) in data_generator:
        [segment_tree.update(player_id, score) for score, player_id in zip([score_a] * 5 + [score_b] * 5, players)]
        yield segment_tree.get_number_of_elements_less_than(segment_tree.tree[segment_tree.arr_len - 1])


if __name__ == '__main__':
    for solution in solve():
        print(solution)
