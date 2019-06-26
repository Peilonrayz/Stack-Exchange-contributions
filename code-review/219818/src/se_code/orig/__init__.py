item_no = [5, 6, 7, 8, 8]
max_no = 0
for i in item_no:
    if i > max_no:
        max_no = i
        high = [i]
    elif i == max_no:
        high.append(i)
