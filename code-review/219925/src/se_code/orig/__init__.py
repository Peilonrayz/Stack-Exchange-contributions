import numpy as np
import matplotlib.pyplot as plt
import timeit


def check_every_box_is_occupied(boxes):
    for box in boxes:
        if box == 0:
            return False
    return True


def check_birthday_paradox(boxes):
    for box in boxes:
        if box >= 2:
            return True
    return False


def main():
    start = timeit.default_timer()
    number_of_tests = 20
    birthday_paradox_graph = [[], []]
    every_box_is_occupied_graph = [[], []]
    boxes_max_num = 200
    for number_of_boxes in range(10, boxes_max_num + 1, 1):
        # print(number_of_boxes)
        average_frequency_birthday_paradox = 0
        average_frequency_every_box_is_occupied = 0
        for index in range(number_of_tests):
            number_of_balls = 1
            boxes = np.array([0] * number_of_boxes)
            while True:
                boxes[np.random.randint(number_of_boxes)] += 1
                if check_birthday_paradox(boxes):
                    average_frequency_birthday_paradox += number_of_balls
                    break
                number_of_balls += 1
            number_of_balls = number_of_boxes
            boxes = np.array([0] * number_of_boxes)
            while True:
                boxes[np.random.randint(number_of_boxes)] += 1
                if check_every_box_is_occupied(boxes):
                    average_frequency_every_box_is_occupied += number_of_balls
                    break
                number_of_balls += 1

        plt.rcParams.update({'font.size': 15})
        birthday_paradox_graph[0].append(number_of_boxes)
        birthday_paradox_graph[1].append(average_frequency_birthday_paradox / number_of_tests)
        every_box_is_occupied_graph[0].append(number_of_boxes)
        every_box_is_occupied_graph[1].append(average_frequency_every_box_is_occupied / number_of_tests)

    print(timeit.default_timer() - start)
    plt.figure(1)
    plt.plot(birthday_paradox_graph[0], birthday_paradox_graph[1], 'ko')
    plt.title("Conajmniej jedna urna ma conajmniej dwie kule")
    plt.xlabel("Liczba urn")
    plt.ylabel("Średnia liczba kul potrzebna do spełnienia warunku")
    plt.figure(2)
    plt.title("Wszystkie urny są zapełnione")
    plt.xlabel("Liczba urn")
    plt.ylabel("Średnia liczba kul potrzebna do spełnienia warunku")
    plt.plot(every_box_is_occupied_graph[0], every_box_is_occupied_graph[1], 'ko')
    plt.show()

if __name__ == '__main__':
    main()