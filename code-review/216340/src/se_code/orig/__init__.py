from typing import List


def parse_message(string) -> List:
    i, j, ids_map, n, ids = 0, 0, dict(), len(string), ''

    while i < n:
        if string[i] in ('I', 'A') or i == n - 1:
            if ids:
                if i == n - 1:
                    ids_map[ids] = ids_map.get(ids, 0) + int(string[j:])
                else:
                    ids_map[ids] = ids_map.get(ids, 0) + int(string[j:i])
            j = i + 4 if string[i] == 'I' else i + 3
            ids = string[i:j]
            i = j - 1
        i += 1
    res = []
    while any(i > 0 for i in ids_map.values()):
        for k, v in ids_map.items():
            if v > 0:
                res.append(k)
                ids_map[k] -= 1
    return res