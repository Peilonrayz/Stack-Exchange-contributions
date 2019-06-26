class Solution:
    def twoSum(self, nums, target) -> List[int]:
        """
        :type nums: List[int]
        :type target: int
        """
        nums_d = {}

        for i in range(len(nums)):
            complement = target - nums[i]

            if nums_d.get(complement) != None: #Check None not True Value
                return [i, nums_d.get(complement)]
            nums_d[nums[i]] = i    #produce a map
        return []