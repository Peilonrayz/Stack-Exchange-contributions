[A One-Pass Hash Table Solution to twoSum](https://codereview.stackexchange.com/q/216025/42401) - [Alice](https://codereview.stackexchange.com/users/195806)

---

1. Don't leave white space at the end of lines.
2. [Use `enumerate`][1].
3. When comparing with `None` use `is` and `is not`.
4. It'd be cleaner to just use `in` rather than `get`.
5. If you want to use `nums_d.get` then you should use it outside the `if` so you don't have to use it a _second_ time when you enter the `if`.  
    This however makes the code messy for not much of a benefit IMO.
6. Unless the site forces you to return lists returning a tuple would be more Pythonic.
7. Your comments aren't helpful, if anything they make the code harder to read for me.
8. The variable name `nums` is easier to read then `nums_d`, the `_d` is useless.
9. When returning it would be better to either:

    - Raise an exception, as the lookup failed.
    - Return a tuple where both values are `None`. This is so you can tuple unpack without errors.

Getting the code:

    def test_peil(nums: List[int], target: int) -> Tuple[int, ...]:
        lookup = {}
        for i, v in enumerate(nums):
            if target - v in lookup:
                return i, lookup[target - v]
            lookup[v] = i
        raise ValueError('Two sums target not in list.')

You can further improve performance [by including Alain T.'s change for small numbers.][2]

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
        raise ValueError('Two sums target not in list.')

And has a performance improvement: (the graph is volatile due to only using one input sample)

[![enter image description here][3]][3]


  [1]: https://codereview.stackexchange.com/a/215985
  [2]: https://codereview.stackexchange.com/a/216057
  [3]: https://i.stack.imgur.com/0srBa.png