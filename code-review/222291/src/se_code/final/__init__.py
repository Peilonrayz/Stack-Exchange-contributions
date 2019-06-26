import numpy as np


def pos_diff_cum_sum(flow_in: np.ndarray, flow_out: np.ndarray) -> np.ndarray:
    sums = []
    cum_sum = 0
    diff = list(flow_in - flow_out)

    for dd in diff:
        cum_sum += dd
        if cum_sum < 0:
            cum_sum = 0

        sums.append(cum_sum)

    return np.array(sums)


def pos_diff_cum_sum_peil(flow_in, flow_out):
    delta = np.cumsum(flow_in - flow_out)
    return delta - np.minimum.accumulate(np.append([0], delta))[1:]


def _extend(*arrays):
    array = np.array([])
    for arr in arrays:
        array = np.append(array, arr)
    return array


def fn(in_, out):
    print(f'>>> fn({in_}, {out})')
    delta = np.cumsum(np.array(in_) - np.array(out))
    print(delta)
    output = delta - np.minimum.accumulate(np.append([0], delta))[1:]
    print(np.minimum.accumulate(np.append([0], delta))[1:])
    print(output)


if __name__ == '__main__':
    steps = 9

    fn([1, 1, 1, 1, 1], [0, 0, 0, 0, 0])
    fn([1, 0, 0, 0, 0], [0, 1, 1, 0, 0])
    fn([1, 0, 0, 1, 1], [0, 1, 1, 0, 0])
    fn([1, 0, 0, 0, 0], [0, 1, 1, 1, 1])
    fn([1, 0, 0, 0, 1], [0, 1, 1, 1, 0])
