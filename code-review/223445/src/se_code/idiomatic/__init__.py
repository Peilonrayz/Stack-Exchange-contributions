def ground_cost(weight):
    if weight > 10:
        cost = weight * 4.75
    elif weight > 6:
        cost = weight * 4
    elif weight > 2:
        cost = weight * 3
    else:
        cost = weight * 1.5
    cost += 20
    return cost


def drone_cost(weight):
    if weight > 10:
        cost = weight * 14.25
    elif weight > 6:
        cost = weight * 12
    elif weight > 2:
        cost = weight * 9
    else:
        cost = weight * 4.5
    return cost


def cost_calc(weight):
    g = ground_cost(weight)
    p = 125
    d = drone_cost(weight)
    g_s = "Ground Shipping"
    p_s = "Premium Ground Shipping"
    d_s = "Drone Shipping"
    if d == g or d == p or g == p:
        if d == g and d == p:
            print("All shipping methods cost $125 according to your items weight")
            return
        if d == g:
            same1 = d_s
            same2 = g_s
            cost = d
        elif d == p:
            same1 = d_s
            same2 = p_s
            cost = d
        else:
            same1 = g_s
            same2 = p_s
            cost = g
        print("You're cheapest shipping method is " + same1 + " and " + same2 + " as they both cost $" + str(cost))
        return
    elif (g < d) and g < p:
        cheap_meth = g_s
        cost = g
    elif (p < d) and p < g:
        cheap_meth = p_s
        cost = p
    elif (d < g) and d < p:
        cheap_meth = d_s
        cost = d
    print("Youre cheapest shipping method is " + cheap_meth + " costing $" + str(cost))
    return


if __name__ == '__main__':
    cost_calc(int(input()))
