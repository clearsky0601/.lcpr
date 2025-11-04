# @lcpr-before-debug-begin
from python3problem560 import *
from typing import *
# @lcpr-before-debug-end

#
# @lc app=leetcode.cn id=560 lang=python3
# @lcpr version=
#
# [560] 和为 K 的子数组
#
"""
解题思路：
1. 使用前缀和 + 哈希表
2. 遍历数组，维护当前前缀和 prefix_sum
3. 对于每个位置，查找 prefix_sum - k 是否在哈希表中出现过
    如果出现过，说明存在子数组的和为 k
4. 更新哈希表，记录当前前缀和出现的次数

时间复杂度：O(n)
空间复杂度：O(n)

示例：nums = [1,1,1], k = 2
- i=0: prefix_sum=1, 查找 1-2=-1 (不存在), count=0, 哈希表{1:1}
- i=1: prefix_sum=2, 查找 2-2=0 (不存在), count=0, 哈希表{1:1, 2:1}
- i=2: prefix_sum=3, 查找 3-2=1 (存在，出现1次), count=1, 哈希表{1:1, 2:1, 3:1}
- 最后检查 prefix_sum==k 的情况：如果k=2，在i=1时 prefix_sum=2，满足条件
"""

# @lcpr-template-start

# @lcpr-template-end
# @lc code=start
from typing import List
from collections import defaultdict

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # 哈希表：存储 前缀和 -> 出现次数
        prefix_sum_count = defaultdict(int)
        # 初始化：前缀和为0的情况（空数组），出现1次
        # 这样当 prefix_sum == k 时，可以正确计数
        prefix_sum_count[0] = 1
        
        prefix_sum = 0  # 当前前缀和
        count = 0       # 结果计数器
        
        # 🔍 调试技巧：在这里设置断点，然后点击 @lcpr case 的 debug 按钮
        # 如果调试器停在插件代码中，点击"继续"（F5）或"运行到断点"（F5）
        # 调试器会自动跳到你设置的断点位置
        for num in nums:
            # 🔍 调试技巧：在这里设置断点，可以看到每次循环的变量值
            # 更新当前前缀和
            prefix_sum += num
            
            # 🔍 调试技巧：在这里设置断点，可以查看：
            # - nums: 输入数组
            # - k: 目标和
            # - prefix_sum: 当前前缀和
            # - prefix_sum - k: 需要查找的目标值
            # - prefix_sum_count: 哈希表内容
            # - count: 当前计数
            
            # 查找是否存在 prefix_sum - k 的前缀和
            # 如果存在，说明从那个位置到当前位置的子数组和为 k
            if prefix_sum - k in prefix_sum_count:
                count += prefix_sum_count[prefix_sum - k]
            
            # 将当前前缀和加入哈希表
            prefix_sum_count[prefix_sum] += 1
        
        return count
# @lc code=end



#
# @lcpr case=start
# [1,1,1]\n2\n
# @lcpr case=end

# @lcpr case=start
# [1,2,3]\n3\n
# @lcpr case=end

#

