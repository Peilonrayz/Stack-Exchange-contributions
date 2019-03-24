from .changes import test_peil, available
from pprint import pprint


def main():
    ret = sorted((test_peil(available, i, 10) for i in range(0, 3001, 10)), key=lambda i: i[0], reverse=True)
    ret = [(sum(f.calories for f in item[1]),) + item for item in ret]
    pprint(ret)


if __name__ == '__main__':
    main()
