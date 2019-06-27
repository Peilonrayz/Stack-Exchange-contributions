from typing import List, Tuple


def test_orig(nums: List[int], target: int) -> List[int]:
    nums_d = {}

    for i in range(len(nums)):
        complement = target - nums[i]

        if nums_d.get(complement) != None: #Check None not True Value
            return [i, nums_d.get(complement)]
        nums_d[nums[i]] = i    #produce a map
    return []


def test_peil(nums: List[int], target: int) -> Tuple[int, ...]:
    lookup = {}
    for i, v in enumerate(nums):
        if target - v in lookup:
            return i, lookup[target - v]
        lookup[v] = i
    return ()


# Derived https://codereview.stackexchange.com/a/216057/42401
# By Alain T. - https://codereview.stackexchange.com/users/136599/alain-t
def test_alain_t(nums: List[int], target: int) -> Tuple[int, ...]:
    for i, n in enumerate(nums):
        if target - n in nums:
            return (i, nums.index(target - n))


# Derived https://codereview.stackexchange.com/a/216057/42401
# By Alain T. - https://codereview.stackexchange.com/users/136599/alain-t
def test_peil_alain(nums: List[int], target: int) -> Tuple[int, ...]:
    if len(nums) <= 100:
        for i, n in enumerate(nums):
            if target - n in nums:
                return i, nums.index(target - n)
    else:
        lookup = {}
        for i, v in enumerate(nums):
            if target - v in lookup:
                return i, lookup[target - v]
            lookup[v] = i
    return ()
