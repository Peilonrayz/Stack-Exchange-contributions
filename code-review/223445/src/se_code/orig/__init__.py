def groundCost(weight):
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

def droneCost(weight):
  if weight > 10:
    cost = weight * 14.25
  elif weight > 6:
    cost = weight * 12
  elif weight > 2:
    cost = weight * 9
  else:
    cost = weight * 4.5
  return cost

def costCalc(weight):
  g = groundCost(weight)
  p = 125
  d = droneCost(weight)
  gS = "Ground Shipping"
  pS = "Premium Ground Shipping"
  dS = "Drone Shipping"
  if d == g or d == p or g == p:
    if d == g and d == p:
      print("All shipping methods cost $125 according to your items weight")
      return
    if d == g:
      same1 = dS
      same2 = gS
      cost = d
    if d == p:
      same1 = dS
      same2 = pS
      cost = d
    if g == p:
      same1 = gS
      same2 = pS
      cost = g
    print("Youre cheapest shipping method is "+same1+" and "+same2+" as they both cost $"+str(cost))
    return
  elif (g < d) and g < p:
    cheapMeth = gS
    cost = g
  elif (p < d) and p < g:
    cheapMeth = pS
    cost = p
  elif (d < g) and d < p:
    cheapMeth = dS
    cost = d
  print("Youre cheapest shipping method is "+cheapMeth+" costing $"+str(cost))
  return
weight = int(input())
costCalc(weight)