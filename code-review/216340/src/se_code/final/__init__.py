from typing import List, Iterator, Tuple, Sequence, TypeVar
import itertools


MESSAGE_LENGTH = {
    'I': 3,
    'A': 2
}

TValue = TypeVar('TValue')


def roundrobin(*iterables: Tuple[Sequence[TValue], ...]) -> Iterator[TValue]:
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = itertools.cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = itertools.cycle(itertools.islice(nexts, num_active))


def extract_messages(input: Iterator[str]) -> Iterator[Tuple[str, int]]:
    input = iter(input)
    message_type = next(input)
    while True:
        length = MESSAGE_LENGTH[message_type]
        message = ''.join([message_type] + list(itertools.islice(input, length)))
        message_type = next(input)
        number = []
        try:
            while message_type not in MESSAGE_LENGTH:
                number += [message_type]
                message_type = next(input)
        except StopIteration:
            break
        finally:
            yield message, int(''.join(number))


def parse_message(string: str) -> List[str]:
    message_counts = {}
    for message, amount in extract_messages(string):
        message_counts.setdefault(message, 0)
        message_counts[message] += amount

    return list(roundrobin(*(
        itertools.repeat(key, amount)
        for key, amount in message_counts.items()
    )))


if __name__ == '__main__':
    print(parse_message('Akb2IAld3'))
    print(parse_message('Aqp1Iasd2Aqp4IAbd1'))
    print(parse_message('Aqp1Iasd2Aqp4IAbd10'))
