import sys


def read_data():
    n, m = list(map(int, sys.stdin.readline().split()))
    yield n

    for _ in range(m):
        yield next(read_query())


def read_query():
    score_a, score_b = list(map(int, sys.stdin.readline().split()))
    players = list(map(int, sys.stdin.readline().split()))
    yield score_a, score_b, players


def get_number_of_elements_less_than(array, value):
    return sum(map(lambda x: x > value, array))


def solve():
    data_generator = read_data()
    n = next(data_generator)
    array = [0] * n

    for (score_a, score_b, players) in data_generator:
        for score, player_id in zip([score_a] * 5 + [score_b] * 5, players):
            array[player_id] += score

        yield get_number_of_elements_less_than(array, array[0])


if __name__ == '__main__':
    for solution in solve():
        print(solution)
