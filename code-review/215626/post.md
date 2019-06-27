# Readability is #1

1. Global variables are bad. Don’t use them. I have to spend a long while looking at your code to tell what uses them and when. When your code becomes hundreds of lines long this is tedious and unmaintainable.

   If you need to use recursion and add to something not in the recursive function use a closure.

1. You should load `available` into an object, rather than extract the information from it each and every time you use it.

1. Using the above you can simplify all your `totalNames`, `totalCarbs` into one list.

1. Rather than using `AllSP` and `AllNames` you can add a tuple to one list.

1. You should put all your code into a `main` so that you reduce the amount of variables in the global scope. This goes hand in hand with (1).

1. Rather than copying and pasting the same line multiple times you can create a function.

All this gets the following. Which should be easier for you to increase the performance from:

```
import collections
import sys
import time

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


def main(available):
    for MAXCALORIES in range(100, 3000, 10):
        start = time.time()
        all_ = find_combs(available, MAXCALORIES)
        amount, foods = max(all_, key=lambda i: i[0])
        print(amount, '  ', [f.name for f in foods])
        print('Calories:', amount, '>>> Time:', time.time()-start)


if __name__ == '__main__':
    available = ['Fiddleheads/3/1/0/3/80', 'Fireweed Shoots/3/0/0/4/150', 'Prickly Pear Fruit/2/1/1/3/190', 'Huckleberries/2/0/0/6/80', 'Rice/7/1/0/0/90', 'Camas Bulb/1/2/5/0/120', 'Beans/1/4/3/0/120', 'Wheat/6/2/0/0/130', 'Crimini Mushrooms/3/3/1/1/200', 'Corn/5/2/0/1/230', 'Beet/3/1/1/3/230', 'Tomato/4/1/0/3/240', 'Raw Fish/0/3/7/0/200', 'Raw Meat/0/7/3/0/250', 'Tallow/0/0/8/0/200', 'Scrap Meat/0/5/5/0/50', 'Prepared Meat/0/4/6/0/600', 'Raw Roast/0/6/5/0/800', 'Raw Sausage/0/4/8/0/500', 'Raw Bacon/0/3/9/0/600', 'Prime Cut/0/9/4/0/600', 'Cereal Germ/5/0/7/3/20', 'Bean Paste/3/5/7/0/40', 'Flour/15/0/0/0/50', 'Sugar/15/0/0/0/50', 'Camas Paste/3/2/10/0/60', 'Cornmeal/9/3/3/0/60', 'Huckleberry Extract/0/0/0/15/60', 'Yeast/0/8/0/7/60', 'Oil/0/0/15/0/120', 'Infused Oil/0/0/12/3/120', 'Simple Syrup/12/0/3/0/400', 'Rice Sludge/10/1/0/2/450', 'Charred Beet/3/0/3/7/470', 'Camas Mash/1/2/9/1/500', 'Campfire Beans/1/9/3/0/500', 'Wilted Fiddleheads/4/1/0/8/500', 'Boiled Shoots/3/0/1/9/510', 'Charred Camas Bulb/2/3/7/1/510', 'Charred Tomato/8/1/0/4/510', 'Charred Corn/8/1/0/4/530', 'Charred Fish/0/9/4/0/550', 'Charred Meat/0/10/10/0/550', 'Wheat Porridge/10/4/0/10/510', 'Charred Sausage/0/11/15/0/500', 'Fried Tomatoes/12/3/9/2/560', 'Bannock/15/3/8/0/600', 'Fiddlehead Salad/6/6/0/14/970', 'Campfire Roast/0/16/12/0/1000', 'Campfire Stew/5/12/9/4/1200', 'Wild Stew/8/5/5/12/1200', 'Fruit Salad/8/2/2/10/900', 'Meat Stock/5/8/9/3/700', 'Vegetable Stock/11/1/2/11/700', 'Camas Bulb Bake/12/7/5/4/400', 'Flatbread/17/8/3/0/500', 'Huckleberry Muffin/10/5/4/11/450', 'Baked Meat/0/13/17/0/600', 'Baked Roast/4/13/8/7/900', 'Huckleberry Pie/9/5/4/16/1300', 'Meat Pie/7/11/11/5/1300', 'Basic Salad/13/6/6/13/800', 'Simmered Meat/6/18/13/5/900', 'Vegetable Medley/9/5/8/20/900', 'Vegetable Soup/12/4/7/19/1200', 'Crispy Bacon/0/18/26/0/600', 'Stuffed Turkey/9/16/12/7/1500']
    main(list(read_foods(available)))
```

# I want speed and I want it now!

To speed up your program you can return early. Knowing `if sum(total_calories) + food.calories <= MAXCALORIES:` then you should return if the inverse is true when `food` is the food with the lowest amount of calories.

```
def find_combs(available, MAXCALORIES):
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
```

I added another function that performs naive memoization via an LRU cache with an unbound size. However it seemed to slow the process.The function that runs in roughly linear time is described below.

![image](static/figs/all_plots.svg)

# How to optimizing the algorithm

Firstly the equations are:

$$
g(f, a) = \frac{\Sigma(f_{a_i} \times f_{\text{calories}_i})}{\Sigma(f_{\text{calories}_i})}
$$

$$
n = \{g(f, \text{carbs}), g(f, \text{protein}), g(f, \text{fat}), g(f, \text{vitimins})\}
$$

$$
\text{SP} = g(f, \text{nutrients}) \times \frac{\Sigma n}{2\max(n)} + \text{Base gain}
$$

From here we have to find the maximums.

1. What’s the maximum and minimum that $\frac{\Sigma n}{2\max(n)}$ can be?

   $$
   \frac{n + n + n + n}{2 \times n} = \frac{4n}{2n} = 2
   $$

   $$
   \frac{n + 0 + 0 + 0}{2 \times n} = \frac{n}{2n} = 0.5
   $$

   This means all we need to do is ensure the calorie average of all the different nutrients are the same. It doesn’t matter what value this average is, only that all have the same.

1. What’s the maximum that $g(f, \text{nutrients})$ can be?

   Firstly taking into account:

   $$
   \frac{\Sigma(a_i \times b_i)}{\Sigma(b_i)} = \Sigma(a_i \times \frac{b_i}{\Sigma(b_i)})
   $$

   We know that these are the calorie average of the foods nutritional value. To maximize this you just want the foods with the highest nutritional value.

Lets work through an example lets say we have the following five foods:

* a/10/0/0/0/1

* b/0/10/0/0/1

* c/0/0/10/0/1

* d/0/0/0/10/1

* e/1/1/1/1/4

What’s the way to maximize SP?

Eating 1 e would give you $4 \times 2 = 8$.Eating 4 a would give you $10 \times 0.5 = 5$.Eating 1 a, b, c and d would give you $10 \times 2 = 20$.And so from here we have deduced eating a, b, c and d in ratios of 1:1:1:1 give the most SP.

This means the rough solution is to find the foods that have the same calorie average for their individual nutrients where you select foods with a bias for ones with high total nutrients.

```
import sys
import collections


sys.setrecursionlimit(10000000)

_Food = collections.namedtuple('Food', 'name carbs protein fat vitamins calories')

__all__ = [
    'available',
    'find_combs',
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


def find_combs(available, max_calories, delta_step=10):
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
```

Which runs fairly quickly across the board:



![image](static/figs/final.svg)

Output is also what you’d expect:

<!-- from se_code.final import find_combs, available -->
```
>>> find_combs(available, 2000)
(79.65454545454546, (Food(name='Simmered Meat', carbs=6.0, protein=18.0, fat=13.0, vitamins=5.0, calories=900.0), Food(name='Vegetable Medley', carbs=8.0, protein=4.0, fat=7.0, vitamins=17.0, calories=900.0), Food(name='Flour', carbs=15.0, protein=0.0, fat=0.0, vitamins=0.0, calories=50.0), Food(name='Flour', carbs=15.0, protein=0.0, fat=0.0, vitamins=0.0, calories=50.0), Food(name='Flour', carbs=15.0, protein=0.0, fat=0.0, vitamins=0.0, calories=50.0), Food(name='Flour', carbs=15.0, protein=0.0, fat=0.0, vitamins=0.0, calories=50.0)))
```
