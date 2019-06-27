import sys
import collections
import functools

sys.setrecursionlimit(10000000)

_Food = collections.namedtuple('Food', 'name carbs protein fat vitamins calories')


class Food(_Food):
    @property
    def nutrients(self):
        return sum(self[1:5])


def read_foods(foods):
    for food in foods:
        name, *other = food.split('/')
        yield Food(name, *[float(v) for v in other])


def tot_avg(food, attr):
    return (
        sum(f.calories * getattr(f, attr) for f in food)
        / sum(f.calories for f in food)
    )


def find_sp(total):
    try:
        nutrients = [
            tot_avg(total, 'carbs'),
            tot_avg(total, 'protein'),
            tot_avg(total, 'fat'),
            tot_avg(total, 'vitamins')
        ]
        balance = sum(nutrients) / 2 / max(nutrients)
    except ZeroDivisionError:
        return None
    return tot_avg(total, 'nutrients') * balance + 12


def find_combs(available, MAXCALORIES):
    all_combinations = []
    min_calories = min(a.calories for a in available)

    @functools.lru_cache(None)
    def inner(total):
        if sum(f.calories for f in total) + min_calories > MAXCALORIES:
            sp = find_sp(total)
            if sp is not None:
                all_combinations.append((sp, total))
        else:
            for food in available:
                total_calories = [f.calories for f in total]
                if sum(total_calories) + food.calories <= MAXCALORIES:
                    inner(total[:] + (food,))

    inner(())
    return max(all_combinations, key=lambda i: i[0])
