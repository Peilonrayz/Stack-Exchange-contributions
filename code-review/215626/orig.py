import itertools
import sys
import time

sys.setrecursionlimit(10000000)

#["Name/Carbs/Protein/Fat/Vitamins/Calories"]
available = ['Fiddleheads/3/1/0/3/80', 'Fireweed Shoots/3/0/0/4/150', 'Prickly Pear Fruit/2/1/1/3/190', 'Huckleberries/2/0/0/6/80', 'Rice/7/1/0/0/90', 'Camas Bulb/1/2/5/0/120', 'Beans/1/4/3/0/120', 'Wheat/6/2/0/0/130', 'Crimini Mushrooms/3/3/1/1/200', 'Corn/5/2/0/1/230', 'Beet/3/1/1/3/230', 'Tomato/4/1/0/3/240', 'Raw Fish/0/3/7/0/200', 'Raw Meat/0/7/3/0/250', 'Tallow/0/0/8/0/200', 'Scrap Meat/0/5/5/0/50', 'Prepared Meat/0/4/6/0/600', 'Raw Roast/0/6/5/0/800', 'Raw Sausage/0/4/8/0/500', 'Raw Bacon/0/3/9/0/600', 'Prime Cut/0/9/4/0/600', 'Cereal Germ/5/0/7/3/20', 'Bean Paste/3/5/7/0/40', 'Flour/15/0/0/0/50', 'Sugar/15/0/0/0/50', 'Camas Paste/3/2/10/0/60', 'Cornmeal/9/3/3/0/60', 'Huckleberry Extract/0/0/0/15/60', 'Yeast/0/8/0/7/60', 'Oil/0/0/15/0/120', 'Infused Oil/0/0/12/3/120', 'Simple Syrup/12/0/3/0/400', 'Rice Sludge/10/1/0/2/450', 'Charred Beet/3/0/3/7/470', 'Camas Mash/1/2/9/1/500', 'Campfire Beans/1/9/3/0/500', 'Wilted Fiddleheads/4/1/0/8/500', 'Boiled Shoots/3/0/1/9/510', 'Charred Camas Bulb/2/3/7/1/510', 'Charred Tomato/8/1/0/4/510', 'Charred Corn/8/1/0/4/530', 'Charred Fish/0/9/4/0/550', 'Charred Meat/0/10/10/0/550', 'Wheat Porridge/10/4/0/10/510', 'Charred Sausage/0/11/15/0/500', 'Fried Tomatoes/12/3/9/2/560', 'Bannock/15/3/8/0/600', 'Fiddlehead Salad/6/6/0/14/970', 'Campfire Roast/0/16/12/0/1000', 'Campfire Stew/5/12/9/4/1200', 'Wild Stew/8/5/5/12/1200', 'Fruit Salad/8/2/2/10/900', 'Meat Stock/5/8/9/3/700', 'Vegetable Stock/11/1/2/11/700', 'Camas Bulb Bake/12/7/5/4/400', 'Flatbread/17/8/3/0/500', 'Huckleberry Muffin/10/5/4/11/450', 'Baked Meat/0/13/17/0/600', 'Baked Roast/4/13/8/7/900', 'Huckleberry Pie/9/5/4/16/1300', 'Meat Pie/7/11/11/5/1300', 'Basic Salad/13/6/6/13/800', 'Simmered Meat/6/18/13/5/900', 'Vegetable Medley/9/5/8/20/900', 'Vegetable Soup/12/4/7/19/1200', 'Crispy Bacon/0/18/26/0/600', 'Stuffed Turkey/9/16/12/7/1500']

global AllSP, AllNames
AllSP = []
AllNames = []

def findcombs(totalNames, totalCarbs, totalProtein, totalFat, totalVitamins, totalNutrients, totalCalories, MAXCALORIES):
    doneit = False
    for each in available:
        each = each.split("/")
        name = each[0]
        carbs = float(each[1])
        protein = float(each[2])
        fat = float(each[3])
        vitamins = float(each[4])
        nutrients = carbs+protein+fat+vitamins
        calories = float(each[5])
#        print(totalNames, totalCalories, calories, each)
        if sum(totalCalories)+calories <= MAXCALORIES:
            doneit = True
            totalNames2 = totalNames[::]
            totalCarbs2 = totalCarbs[::]
            totalProtein2 = totalProtein[::]
            totalFat2 = totalFat[::]
            totalVitamins2 = totalVitamins[::]
            totalCalories2 = totalCalories[::]
            totalNutrients2 = totalNutrients[::]

            totalNames2.append(name)
            totalCarbs2.append(carbs)
            totalProtein2.append(protein)
            totalFat2.append(fat)
            totalVitamins2.append(vitamins)
            totalCalories2.append(calories)
            totalNutrients2.append(nutrients)
#            print("    ", totalNames2, totalCarbs2, totalProtein2, totalFat2, totalVitamins2, totalNutrients2, totalCalories2)
            findcombs(totalNames2, totalCarbs2, totalProtein2, totalFat2, totalVitamins2, totalNutrients2, totalCalories2, MAXCALORIES)
        else:
            #find SP
            try:
                carbs    = sum([x * y for x, y in zip(totalCalories, totalCarbs)])    / sum(totalCalories)
                protein  = sum([x * y for x, y in zip(totalCalories, totalProtein)])  / sum(totalCalories)
                fat      = sum([x * y for x, y in zip(totalCalories, totalFat)])      / sum(totalCalories)
                vitamins = sum([x * y for x, y in zip(totalCalories, totalVitamins)]) / sum(totalCalories)
                balance  = (carbs+protein+fat+vitamins)/(2*max([carbs,protein,fat,vitamins]))
                thisSP   = sum([x * y for x, y in zip(totalCalories, totalNutrients)]) / sum(totalCalories) * balance + 12
            except:
                thisSP = 0
            #add SP and names to two lists
            AllSP.append(thisSP)
            AllNames.append(totalNames)

def main(MAXCALORIES):
    findcombs([], [], [], [], [], [], [], MAXCALORIES)
    index = AllSP.index(max(AllSP))
    print()
    print(AllSP[index], "  ", AllNames[index])

for i in range(100, 3000, 10):
    start = time.time()
    main(i)
    print("Calories:", i, ">>> Time:", time.time()-start)