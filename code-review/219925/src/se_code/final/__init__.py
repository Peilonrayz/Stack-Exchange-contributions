import matplotlib.pyplot as plt
import numpy as np
import timeit


def random_numbers(limit):
    while True:
        yield from np.random.randint(limit, size=limit)


def simulate(size):
    boxes = np.array([0] * size)
    pair = None
    all_set = None
    for iteration, choice in enumerate(random_numbers(size), 1):
        boxes[choice] += 1
        if pair is None and boxes[choice] >= 2:
            pair = iteration
            if all_set is not None:
                break
        if all_set is None and all(boxes):
            all_set = iteration
            if pair is not None:
                break
    return pair, all_set


def birthday_problem(tests, boxes_limit):
    domain = range(10, boxes_limit + 1, 1)
    paired = [domain, []]
    all_set = [domain, []]
    for boxes in domain:
        pairs, all_sets = zip(*(simulate(boxes) for _ in range(tests)))
        paired[1].append(sum(pairs) / tests)
        all_set[1].append(sum(all_sets) / tests)
    return paired, all_set


def main():
    start = timeit.default_timer()
    number_of_tests = 1
    boxes_max_num = 1000
    birthday_paradox_graph, every_box_is_occupied_graph = birthday_problem(number_of_tests, boxes_max_num)
    print(timeit.default_timer() - start)
    plt.rcParams.update({'font.size': 15})
    plt.figure(1)
    plt.plot(birthday_paradox_graph[0], birthday_paradox_graph[1], 'ko')
    plt.title("Conajmniej jedna urna ma conajmniej dwie kule")
    plt.xlabel("Liczba urn")
    plt.ylabel("Średnia liczba kul potrzebna do spełnienia warunku")
    plt.figure(2)
    plt.title("Wszystkie urny są zapełnione")
    plt.xlabel("Liczba urn")
    plt.ylabel("Średnia liczba kul potrzebna do spełnienia warunku")
    plt.plot(
        every_box_is_occupied_graph[0],
        every_box_is_occupied_graph[1],
        'ko')
    plt.show()


if __name__ == '__main__':
    main()
