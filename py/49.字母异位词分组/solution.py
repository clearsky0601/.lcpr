#
# @lc app=leetcode.cn id=49 lang=python3
# @lcpr version=
#
# [49] 字母异位词分组
#


# @lcpr-template-start

# @lcpr-template-end
# @lc code=start
from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        字母异位词分组
        
        核心思路：字母异位词排序后相同
        例如："eat" 和 "tea" 排序后都是 "aet"
        
        方法1:排序法（推荐，最简单易懂）
        时间复杂度:O(n * k * log k),n是字符串数量，k是字符串平均长度
        空间复杂度:O(n * k)
        """
        # 使用 defaultdict 自动创建列表，避免判断 key 是否存在
        groups = defaultdict(list)
        
        for s in strs:
            # 关键：将字符串排序后作为 key
            # 字母异位词排序后会得到相同的字符串
            key = ''.join(sorted(s))
            groups[key].append(s)
        
        # 返回所有分组
        return list(groups.values())
        
        # 方法2：字符计数法（更高效，但代码更复杂）
        # 时间复杂度：O(n * k)
        # 空间复杂度：O(n * k)
        """
        groups = defaultdict(list)
        
        for s in strs:
            # 创建一个长度为26的计数数组(26个字母)
            count = [0] * 26
            for char in s:
                # 将字符映射到0-25的索引
                count[ord(char) - ord('a')] += 1
            
            # 将计数数组转换为元组作为 key
            # 例如：[1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0] 代表 "eat"
            key = tuple(count)
            groups[key].append(s)
        
        return list(groups.values())
        """
# @lc code=end



#
# @lcpr case=start
# ["eat", "tea", "tan", "ate", "nat", "bat"]\n
# @lcpr case=end

# @lcpr case=start
# [""]\n
# @lcpr case=end

# @lcpr case=start
# ["a"]\n
# @lcpr case=end

#

