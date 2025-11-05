# @lc app=leetcode.cn id=1 lang=python3
# @lcpr version=30204
#
# [1] 两数之和 - 多种解法对比
#
# 本文件展示了同一题目的多种解法，方便对比学习

# @lcpr-template-start

# @lcpr-template-end
# @lc code=start
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        方法选择说明：
        - 方法1（当前启用）：哈希表解法，时间复杂度 O(n)，空间复杂度 O(n)
        - 方法2（已注释）：暴力解法，时间复杂度 O(n²)，空间复杂度 O(1)
        - 方法3（已注释）：排序+双指针，但需要保留原索引，较复杂
        """
        
        # ========== 方法1：哈希表解法（推荐）==========
        # 时间复杂度：O(n)
        # 空间复杂度：O(n)
        # 思路：使用字典存储已遍历的数字及其索引
        num_dict = {}
        
        for i, num in enumerate(nums):
            complement = target - num
            
            if complement in num_dict:
                return [num_dict[complement], i]
            
            num_dict[num] = i
        
        return []
        
        # ========== 方法2：暴力解法 ==========
        # 时间复杂度：O(n²)
        # 空间复杂度：O(1)
        # 思路：双重循环遍历所有可能的组合
        # for i in range(len(nums)):
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] + nums[j] == target:
        #             return [i, j]
        # return []
        
        # ========== 方法3：排序+双指针（不推荐，因为需要返回索引）==========
        # 时间复杂度：O(n log n)
        # 空间复杂度：O(n)
        # 思路：先排序，再用双指针，但需要额外存储索引映射
        # indexed_nums = [(num, i) for i, num in enumerate(nums)]
        # indexed_nums.sort(key=lambda x: x[0])
        # 
        # left, right = 0, len(indexed_nums) - 1
        # while left < right:
        #     current_sum = indexed_nums[left][0] + indexed_nums[right][0]
        #     if current_sum == target:
        #         return [indexed_nums[left][1], indexed_nums[right][1]]
        #     elif current_sum < target:
        #         left += 1
        #     else:
        #         right -= 1
        # return []
        
# @lc code=end



#
# @lcpr case=start
# [2,7,11,15]\n9\n
# @lcpr case=end

# @lcpr case=start
# [3,2,4]\n6\n
# @lcpr case=end

# @lcpr case=start
# [3,3]\n6\n
# @lcpr case=end

# @lcpr case=start
# [0,4,3,0]\n0\n
# @lcpr case=end

# @lcpr case=start
# [-1,-2,-3,-4,-5]\n-8\n
# @lcpr case=end

#

