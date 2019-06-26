import itertools

class LuhnBase:
    @staticmethod
    def calculate_lut_overkill(input_):
        """Calculate the check digit using Luhn's algorithm"""
        sum_ = 0
        for i, digit in enumerate(reversed(input_)):
            digit = int(digit)
            if i % 2 == 0:
                digit *= 2
                if digit > 9:
                    digit -= 9
            sum_ += digit
        return str(10 - sum_ % 10)


class LuhnOverkill:

    DOUBLE_LUT = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
    # CHECK_DIGIT_LUT = tuple(str(10 - i) for i in range(10))
    CHECK_DIGIT_LUT = ("0", "9", "8", "7", "6", "5", "4", "3", "2", "1")
    # STR_TO_INT_LUT = {str(i): i for i in range(10)}
    STR_TO_INT_LUT = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }
    SUM_MOD10_LUT = {
        i: {str(j): (i + j) % 10 for j in range(10)}
        for i in range(10)
    }
    SUM_DOUBLE_MOD10_LUT = {
        i: {str(j): (i + (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)[j]) % 10 for j in range(10)}
        for i in range(10)
    }

    @classmethod
    def calculate_lut_overkill(cls, input_):
        """Calculate the check digit using Luhn's algorithm"""
        sum_ = 0
        for i, digit in enumerate(reversed(input_)):
            if i % 2:
                sum_ = cls.SUM_MOD10_LUT[sum_][digit]
            else:
                sum_ = cls.SUM_DOUBLE_MOD10_LUT[sum_][digit]
        return cls.CHECK_DIGIT_LUT[sum_]


class LuhnPeilList:
    DOUBLE_LUT = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
    # CHECK_DIGIT_LUT = tuple(str(10 - i) for i in range(10))
    CHECK_DIGIT_LUT = ("0", "9", "8", "7", "6", "5", "4", "3", "2", "1")
    # STR_TO_INT_LUT = {str(i): i for i in range(10)}
    STR_TO_INT_LUT = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }
    SUM_MOD10_LUT = [
        {str(j): (i + j) % 10 for j in range(10)}
        for i in range(10)
    ]
    SUM_DOUBLE_MOD10_LUT = [
        {str(j): (i + (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)[j]) % 10 for j in range(10)}
        for i in range(10)
    ]

    @classmethod
    def calculate_lut_overkill(cls, input_):
        """Calculate the check digit using Luhn's algorithm"""
        sum_ = 0
        for i, digit in enumerate(reversed(input_)):
            if i % 2:
                sum_ = cls.SUM_MOD10_LUT[sum_][digit]
            else:
                sum_ = cls.SUM_DOUBLE_MOD10_LUT[sum_][digit]
        return cls.CHECK_DIGIT_LUT[sum_]


class LuhnPeilTables:
    DOUBLE_LUT = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
    # CHECK_DIGIT_LUT = tuple(str(10 - i) for i in range(10))
    CHECK_DIGIT_LUT = ("0", "9", "8", "7", "6", "5", "4", "3", "2", "1")
    # STR_TO_INT_LUT = {str(i): i for i in range(10)}
    STR_TO_INT_LUT = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }
    SUM_MOD10_LUT = [
        {str(j): (i + j) % 10 for j in range(10)}
        for i in range(10)
    ]
    SUM_DOUBLE_MOD10_LUT = [
        {str(j): (i + (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)[j]) % 10 for j in range(10)}
        for i in range(10)
    ]

    @classmethod
    def calculate_lut_overkill(cls, input_):
        """Calculate the check digit using Luhn's algorithm"""
        tables = [cls.SUM_DOUBLE_MOD10_LUT, cls.SUM_MOD10_LUT] * ((len(input_) + 1) // 2)
        sum_ = 0
        for table, digit in zip(tables, reversed(input_)):
            sum_ = table[sum_][digit]
        return cls.CHECK_DIGIT_LUT[sum_]


class LuhnPeilAltTables:
    DOUBLE_LUT = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
    # CHECK_DIGIT_LUT = tuple(str(10 - i) for i in range(10))
    CHECK_DIGIT_LUT = ("0", "9", "8", "7", "6", "5", "4", "3", "2", "1")
    # STR_TO_INT_LUT = {str(i): i for i in range(10)}
    STR_TO_INT_LUT = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }
    SUM_MOD10_LUT = [
        {str(j): (i + j) % 10 for j in range(10)}
        for i in range(10)
    ]
    SUM_DOUBLE_MOD10_LUT = [
        {str(j): (i + (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)[j]) % 10 for j in range(10)}
        for i in range(10)
    ]

    @classmethod
    def calculate_lut_overkill(cls, input_):
        """Calculate the check digit using Luhn's algorithm"""
        tables = [cls.SUM_DOUBLE_MOD10_LUT, cls.SUM_MOD10_LUT] * ((len(input_) + 1) // 2)
        sum_ = 0
        for digit, table in zip(reversed(input_), tables):
            sum_ = table[sum_][digit]
        return cls.CHECK_DIGIT_LUT[sum_]


class LuhnPeilItertools:
    DOUBLE_LUT = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
    # CHECK_DIGIT_LUT = tuple(str(10 - i) for i in range(10))
    CHECK_DIGIT_LUT = ("0", "9", "8", "7", "6", "5", "4", "3", "2", "1")
    # STR_TO_INT_LUT = {str(i): i for i in range(10)}
    STR_TO_INT_LUT = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }
    SUM_MOD10_LUT = [
        {str(j): (i + j) % 10 for j in range(10)}
        for i in range(10)
    ]
    SUM_DOUBLE_MOD10_LUT = [
        {str(j): (i + (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)[j]) % 10 for j in range(10)}
        for i in range(10)
    ]

    @classmethod
    def calculate_lut_overkill(cls, input_):
        """Calculate the check digit using Luhn's algorithm"""
        sum_ = 0
        for table, digit in zip(itertools.cycle([cls.SUM_DOUBLE_MOD10_LUT, cls.SUM_MOD10_LUT]), reversed(input_)):
            sum_ = table[sum_][digit]
        return cls.CHECK_DIGIT_LUT[sum_]


class LuhnPeilAltItertools:
    DOUBLE_LUT = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
    # CHECK_DIGIT_LUT = tuple(str(10 - i) for i in range(10))
    CHECK_DIGIT_LUT = ("0", "9", "8", "7", "6", "5", "4", "3", "2", "1")
    # STR_TO_INT_LUT = {str(i): i for i in range(10)}
    STR_TO_INT_LUT = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }
    SUM_MOD10_LUT = [
        {str(j): (i + j) % 10 for j in range(10)}
        for i in range(10)
    ]
    SUM_DOUBLE_MOD10_LUT = [
        {str(j): (i + (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)[j]) % 10 for j in range(10)}
        for i in range(10)
    ]

    @classmethod
    def calculate_lut_overkill(cls, input_):
        """Calculate the check digit using Luhn's algorithm"""
        sum_ = 0
        for digit, table in zip(reversed(input_), itertools.cycle([cls.SUM_DOUBLE_MOD10_LUT, cls.SUM_MOD10_LUT])):
            sum_ = table[sum_][digit]
        return cls.CHECK_DIGIT_LUT[sum_]


class Luhn:
    CHECK_DIGIT_LUT = ("0", "9", "8", "7", "6", "5", "4", "3", "2", "1")
    SUM_MOD10_LUT = [
        {str(j): (i + j) % 10 for j in range(10)}
        for i in range(10)
    ]
    SUM_DOUBLE_MOD10_LUT = [
        {str(j): (i + (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)[j]) % 10 for j in range(10)}
        for i in range(10)
    ]

    @classmethod
    def calculate_lut_overkill(cls, input_):
        """Calculate the check digit using Luhn's algorithm"""
        sum_ = 0
        for digit, table in zip(
            reversed(input_),
            itertools.cycle([
                cls.SUM_DOUBLE_MOD10_LUT,
                cls.SUM_MOD10_LUT,
            ]),
        ):
            sum_ = table[sum_][digit]
        return cls.CHECK_DIGIT_LUT[sum_]


class LuhnPeilWithoutIf:
    DOUBLE_LUT = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
    # CHECK_DIGIT_LUT = tuple(str(10 - i) for i in range(10))
    CHECK_DIGIT_LUT = ("0", "9", "8", "7", "6", "5", "4", "3", "2", "1")
    # STR_TO_INT_LUT = {str(i): i for i in range(10)}
    STR_TO_INT_LUT = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }
    SUM_MOD10_LUT = [
        {str(j): (i + j) % 10 for j in range(10)}
        for i in range(10)
    ]
    SUM_DOUBLE_MOD10_LUT = [
        {str(j): (i + (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)[j]) % 10 for j in range(10)}
        for i in range(10)
    ]

    @classmethod
    def calculate_lut_overkill(cls, input_):
        """Calculate the check digit using Luhn's algorithm"""
        tables = [cls.SUM_DOUBLE_MOD10_LUT, cls.SUM_MOD10_LUT]
        sum_ = 0
        for i, digit in enumerate(reversed(input_)):
            sum_ = tables[i % 2][sum_][digit]
        return cls.CHECK_DIGIT_LUT[sum_]


class LuhnPeilWithoutIfMod:
    DOUBLE_LUT = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
    # CHECK_DIGIT_LUT = tuple(str(10 - i) for i in range(10))
    CHECK_DIGIT_LUT = ("0", "9", "8", "7", "6", "5", "4", "3", "2", "1")
    # STR_TO_INT_LUT = {str(i): i for i in range(10)}
    STR_TO_INT_LUT = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }
    SUM_MOD10_LUT = [
        {str(j): (i + j) % 10 for j in range(10)}
        for i in range(10)
    ]
    SUM_DOUBLE_MOD10_LUT = [
        {str(j): (i + (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)[j]) % 10 for j in range(10)}
        for i in range(10)
    ]

    @classmethod
    def calculate_lut_overkill(cls, input_):
        """Calculate the check digit using Luhn's algorithm"""
        tables = [cls.SUM_DOUBLE_MOD10_LUT, cls.SUM_MOD10_LUT] * ((len(input_) + 1) // 2)
        sum_ = 0
        for i, digit in enumerate(reversed(input_)):
            sum_ = tables[i][sum_][digit]
        return cls.CHECK_DIGIT_LUT[sum_]


class LuhnPeilWithoutIfModEnumerate:
    CHECK_DIGIT_LUT = ("0", "9", "8", "7", "6", "5", "4", "3", "2", "1")
    SUM_MOD10_LUT = [
        {str(j): (i + j) % 10 for j in range(10)}
        for i in range(10)
    ]
    SUM_DOUBLE_MOD10_LUT = [
        {str(j): (i + (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)[j]) % 10 for j in range(10)}
        for i in range(10)
    ]

    @classmethod
    def calculate_lut_overkill(cls, input_):
        """Calculate the check digit using Luhn's algorithm"""
        tables = [cls.SUM_DOUBLE_MOD10_LUT, cls.SUM_MOD10_LUT] * ((len(input_) + 1) // 2)
        sum_ = 0
        for digit, table in zip(reversed(input_), tables):
            sum_ = table[sum_][digit]
        return cls.CHECK_DIGIT_LUT[sum_]


class LuhnPeilWithoutIfEnumerate:
    DOUBLE_LUT = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
    # CHECK_DIGIT_LUT = tuple(str(10 - i) for i in range(10))
    CHECK_DIGIT_LUT = ("0", "9", "8", "7", "6", "5", "4", "3", "2", "1")
    # STR_TO_INT_LUT = {str(i): i for i in range(10)}
    STR_TO_INT_LUT = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }
    SUM_MOD10_LUT = [
        {str(j): (i + j) % 10 for j in range(10)}
        for i in range(10)
    ]
    SUM_DOUBLE_MOD10_LUT = [
        {str(j): (i + (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)[j]) % 10 for j in range(10)}
        for i in range(10)
    ]

    @classmethod
    def calculate_lut_overkill(cls, input_):
        """Calculate the check digit using Luhn's algorithm"""
        tables = [cls.SUM_DOUBLE_MOD10_LUT, cls.SUM_MOD10_LUT]
        sum_ = 0
        for digit, i in zip(reversed(input_), range(len(input_))):
            sum_ = tables[i % 2][sum_][digit]
        return cls.CHECK_DIGIT_LUT[sum_]


if __name__ == '__main__':
    from timeit import timeit

    statement = 'Luhn.calculate_lut_overkill("630490001774029244")'
    luhns = [LuhnBase, LuhnPeilTables,
             LuhnPeilAltTables, LuhnPeilItertools, LuhnPeilAltItertools,

             LuhnOverkill, LuhnPeilList, LuhnPeilWithoutIf,
             LuhnPeilWithoutIfEnumerate,
             LuhnPeilWithoutIfMod,
             LuhnPeilWithoutIfModEnumerate,
             Luhn,
             ]

    timings = [[] for _ in range(len(luhns))]
    for _ in range(10):
        for i, luhn in enumerate(luhns):
            timings[i].append(timeit(statement, globals={'Luhn': luhn}, number=100000))

    for luhn, timing in zip(luhns, timings):
        print(luhn.__name__, round(min(timing), 3))


def luhn_peil_list(cls, input_):
    sum_ = 0
    for i, digit in enumerate(reversed(input_)):
        if i % 2:
            sum_ = cls.SUM_MOD10_LUT[sum_][digit]
        else:
            sum_ = cls.SUM_DOUBLE_MOD10_LUT[sum_][digit]
    return cls.CHECK_DIGIT_LUT[sum_]


def luhn_peil_without_if(cls, input_):
    tables = [cls.SUM_DOUBLE_MOD10_LUT, cls.SUM_MOD10_LUT]
    sum_ = 0
    for i, digit in enumerate(reversed(input_)):
        sum_ = tables[i % 2][sum_][digit]
    return cls.CHECK_DIGIT_LUT[sum_]


def luhn_peil_without_if_enumerate(cls, input_):
    tables = [cls.SUM_DOUBLE_MOD10_LUT, cls.SUM_MOD10_LUT]
    sum_ = 0
    for digit, i in zip(reversed(input_), range(len(input_))):
        sum_ = tables[i % 2][sum_][digit]
    return cls.CHECK_DIGIT_LUT[sum_]


def luhn_peil_without_if_mod(cls, input_):
    tables = [cls.SUM_DOUBLE_MOD10_LUT, cls.SUM_MOD10_LUT] * ((len(input_) + 1) // 2)
    sum_ = 0
    for i, digit in enumerate(reversed(input_)):
        sum_ = tables[i][sum_][digit]
    return cls.CHECK_DIGIT_LUT[sum_]


def luhn_peil_without_if_mod_enumerate(cls, input_):
    tables = [cls.SUM_DOUBLE_MOD10_LUT, cls.SUM_MOD10_LUT] * ((len(input_) + 1) // 2)
    sum_ = 0
    for digit, table in zip(reversed(input_), tables):
        sum_ = table[sum_][digit]
    return cls.CHECK_DIGIT_LUT[sum_]


def luhn(cls, input_):
    sum_ = 0
    for digit, table in zip(
        reversed(input_),
        itertools.cycle([
            cls.SUM_DOUBLE_MOD10_LUT,
            cls.SUM_MOD10_LUT,
        ]),
    ):
        sum_ = table[sum_][digit]
    return cls.CHECK_DIGIT_LUT[sum_]
