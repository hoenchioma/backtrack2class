from typing import Any


def set_intersection(a: list, b: list) -> list:
    i, j = 0, 0
    res = []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            i += 1
        elif b[j] < a[i]:
            j += 1
        else:
            res.append(b[j])
            j += 1
            i += 1
    return res


def set_union(a: list, b: list) -> list:
    i, j = 0, 0
    m, n = len(a), len(b)
    res = []
    while i < m and j < n:
        if a[i] < b[j]:
            res.append(a[i])
            i += 1
        elif b[j] < a[i]:
            res.append(b[j])
            j += 1
        else:
            res.append(b[j])
            j += 1
            i += 1
    while i < m:
        res.append(a[i])
        i += 1
    while j < n:
        res.append(b[j])
        j += 1
    return res


def update_dict(dict_to_update: dict, key: Any, del_val: Any):
    if key not in dict_to_update:
        dict_to_update[key] = 0
    dict_to_update[key] += del_val
    if dict_to_update[key] == 0:
        dict_to_update.pop(key)
