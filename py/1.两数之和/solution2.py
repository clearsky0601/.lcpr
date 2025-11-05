#
# @lc app=leetcode.cn id=1 lang=python3
# @lcpr version=30204
#
# [1] 两数之和
#


# @lcpr-template-start

# @lcpr-template-end
# @lc code=start
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # 哈希表解法：时间复杂度 O(n)，空间复杂度 O(n)
        # 使用字典存储：key = 数值，value = 索引
        num_dict = {}
        
        # 遍历数组
        for i, num in enumerate(nums):
            # 计算需要的补数
            complement = target - num
            
            # 如果补数已经在字典中，说明找到了
            if complement in num_dict:
                return [num_dict[complement], i]
            
            # 否则将当前数字和索引存入字典
            num_dict[num] = i
        
        # 理论上不会到这里（题目保证有解）
        return []
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

#

