import sys
import collections


sys.setrecursionlimit(10000000)

_Food = collections.namedtuple('Food', 'name carbs protein fat vitamins calories')

__all__ = [
    'available',
    'test_orig',
    'test_early_leaf',
    'test_peil'
]


class Food(_Food):
    @property
    def nutrients(self):
        return sum(self[1:5])


def tot_avg(food, attr):
    return (
        sum(f.calories * getattr(f, attr) for f in food)
        / sum(f.calories for f in food)
    )


def ratio_transform(attrs):
    largest = max(attrs[1:5])
    if largest == 0:
        return 0, 0, 0, 0
    return tuple(100 * a / largest for a in attrs[1:5])


def bulid_ratios(food_ratios, delta_step):
    def _ratios(attrs, delta):
        wanted = []
        for *ratio, food in food_ratios:
            if all((a - delta) <= r <= (a + delta) for r, a in zip(ratio, attrs)):
                wanted.append(food)
        return wanted

    def ratios(attrs, calories):
        ratios = ratio_transform(attrs)
        ratios = tuple(100 - int(round(r)) for r in ratios)
        delta = delta_step
        while delta <= 100:
            rets = _ratios(ratios, delta)
            rets = [f for f in rets if f.calories <= calories]
            if rets:
                return rets
            delta += delta_step
    return ratios


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


def test_orig(available, MAXCALORIES):
    all_combinations = []

    def inner(total):
        for food in available:
            total_calories = [f.calories for f in total]
            if sum(total_calories) + food.calories <= MAXCALORIES:
                inner(total[:] + [food])
            else:
                sp = find_sp(total)
                if sp is not None:
                    all_combinations.append((sp, total))

    inner([])
    return max(all_combinations, key=lambda i: i[0])


def test_early_leaf(available, MAXCALORIES):
    all_combinations = []
    min_calories = min(a.calories for a in available)

    def inner(total):
        if sum(f.calories for f in total) + min_calories > MAXCALORIES:
            sp = find_sp(total)
            if sp is not None:
                all_combinations.append((sp, total))
        else:
            for food in available:
                total_calories = [f.calories for f in total]
                if sum(total_calories) + food.calories <= MAXCALORIES:
                    inner(total[:] + [food])

    inner([])
    return max(all_combinations, key=lambda i: i[0])


def test_peil(available, max_calories, delta_step=10):
    available = list(sorted(available, key=lambda f: f.nutrients, reverse=True))

    food_ratios = [
        ratio_transform(food[1:5]) + (food,)
        for food in available
    ]

    ratios = bulid_ratios(food_ratios, delta_step)
    largest = (0, ())
    for food in available:
        if food.calories > max_calories:
            continue
        if food.nutrients * 2 <= largest[0] - 12:
            break
        foods = [food]
        calories = food.calories
        attrs = [a * food.calories for a in food[1:5]]
        while True:
            new_foods = ratios(attrs, max_calories - calories)
            if not new_foods:
                break
            new_food = new_foods[0]
            foods.append(new_food)
            calories += new_food.calories
            attrs = [a + b * new_food.calories for a, b in zip(attrs, new_food[1:5])]
        sp = find_sp(foods)
        if sp > largest[0]:
            largest = sp, tuple(foods)
    return largest


def read_foods(foods):
    for food in foods:
        name, *other = food.split('/')
        yield Food(name, *[float(v) for v in other])


available = [
    "Fiddleheads/3/1/0/3/80",
    "Fireweed Shoots/3/0/0/4/150",
    "Prickly Pear Fruit/2/1/1/3/190",
    "Huckleberries/2/0/0/6/80",
    "Rice/7/1/0/0/90",
    "Camas Bulb/1/2/5/0/120",
    "Beans/1/4/3/0/120",
    "Wheat/6/2/0/0/130",
    "Crimini Mushrooms/3/3/1/1/200",
    "Corn/5/2/0/1/230",
    "Beet/3/1/1/3/230",
    "Tomato/4/1/0/3/240",
    "Raw Fish/0/3/7/0/200",
    "Raw Meat/0/7/3/0/250",
    "Tallow/0/0/8/0/200",
    "Scrap Meat/0/5/5/0/50",
    "Prepared Meat/0/4/6/0/600",
    "Raw Roast/0/6/5/0/800",
    "Raw Sausage/0/4/8/0/500",
    "Raw Bacon/0/3/9/0/600",
    "Prime Cut/0/9/4/0/600",
    "Cereal Germ/5/0/7/3/20",  # test
    "Bean Paste/3/5/7/0/40",
    "Flour/15/0/0/0/50",
    "Sugar/15/0/0/0/50",
    "Camas Paste/3/2/10/0/60",
    "Cornmeal/9/3/3/0/60",
    "Huckleberry Extract/0/0/0/15/60",
    "Yeast/0/8/0/7/60",  # test
    "Oil/0/0/15/0/120",
    "Infused Oil/0/0/12/3/120",
    "Simple Syrup/12/0/3/0/400",
    "Rice Sludge/10/1/0/2/450",
    "Charred Beet/3/0/3/7/470",
    "Camas Mash/1/2/9/1/500",
    "Campfire Beans/1/9/3/0/500",
    "Wilted Fiddleheads/4/1/0/8/500",
    "Boiled Shoots/3/0/1/9/510",
    "Charred Camas Bulb/2/3/7/1/510",
    "Charred Tomato/8/1/0/4/510",
    "Charred Corn/8/1/0/4/530",
    "Charred Fish/0/9/4/0/550",
    "Charred Meat/0/10/10/0/550",
    "Wheat Porridge/10/4/0/10/510",
    "Charred Sausage/0/11/15/0/500",
    "Fried Tomatoes/12/3/9/2/560",
    "Bannock/15/3/8/0/600",
    "Fiddlehead Salad/6/6/0/14/970",
    "Campfire Roast/0/16/12/0/1000",
    "Campfire Stew/5/12/9/4/1200",
    "Wild Stew/8/5/5/12/1200",
    "Fruit Salad/8/2/2/10/900",
    "Meat Stock/5/8/9/3/700",
    "Vegetable Stock/11/1/2/11/700",
    "Camas Bulb Bake/12/7/5/4/400",
    "Flatbread/17/8/3/0/500",
    "Huckleberry Muffin/10/5/4/11/450",
    "Baked Meat/0/13/17/0/600",
    "Baked Roast/4/13/8/7/900",
    "Huckleberry Pie/9/5/4/16/1300",
    "Meat Pie/7/11/11/5/1300",
    "Basic Salad/13/6/6/13/800",
    "Simmered Meat/6/18/13/5/900",
    # "Vegetable Medley/9/5/8/20/900", outdated values
    "Vegetable Medley/8/4/7/17/900",
    "Vegetable Soup/12/4/7/19/1200",
    "Crispy Bacon/0/18/26/0/600",
    "Stuffed Turkey/9/16/12/7/1500",
]
available = list(read_foods(available))
