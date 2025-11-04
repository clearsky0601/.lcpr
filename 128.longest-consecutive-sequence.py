#
# @lc app=leetcode.cn id=128 lang=python3
# @lcpr version=
#
# [128] 最长连续序列
#
"""
解题思路：
1. 使用集合（set）存储所有数字，实现O(1)的查找
2. 遍历数组，对于每个数字，如果它是某个连续序列的起始点
    （即num-1不在集合中），则从这个数字开始向后查找连续序列的长度
3. 更新最大长度 

时间复杂度：O(n) - 每个数字最多被访问两次
空间复杂度：O(n) - 哈希集合存储所有数字

示例：[100,4,200,1,3,2]
- 100是起始点（99不在集合中），向后查找：100 -> 长度1
- 4不是起始点（3在集合中，4-1=3也在集合中）
- 1是起始点（0不在集合中），向后查找：1->2->3->4，长度4
"""

# @lcpr-template-start

# @lcpr-template-end
# @lc code=start
from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:

        # 边界情况：空数组返回0
        if not nums:
            return 0
        
        # 将数组转换为集合，去重并实现O(1)查找
        num_set = set[int](nums)
        max_length = 0
        
        # 遍历集合中的每个数字
        for num in num_set:
            # 关键：只有当num是某个连续序列的起始点时才处理
            # 如果num-1在集合中，说明num不是起始点，跳过（避免重复计算）
            if num - 1 not in num_set:
                # num是起始点，开始向后查找连续序列
                current_num = num
                current_length = 1
                
                # 向后查找连续的数字
                while current_num + 1 in num_set:
                    current_num += 1
                    current_length += 1
                
                # 更新最大长度
                max_length = max(max_length, current_length)
        
        return max_length
# @lc code=end



#
# @lcpr case=start
# [100,4,200,1,3,2]\n
# @lcpr case=end

# @lcpr case=start
# [0,3,7,2,5,8,4,6,0,1]\n
# @lcpr case=end

# @lcpr case=start
# [1,0,1,2]\n
# @lcpr case=end

#

