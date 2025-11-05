# @lc app=leetcode.cn id=100 lang=python3
# @lcpr version=
#
# [100] 相同的树 - 方法4：序列化比较
#

# @lcpr-template-start

# @lcpr-template-end
# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import Optional

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        方法4：序列化比较
        时间复杂度：O(min(m, n))
        空间复杂度：O(min(m, n))
        
        思路：
        1. 将两棵树序列化为字符串
        2. 比较序列化后的字符串是否相同
        3. 这是一种"作弊"方法，但思路很有趣
        """
        def serialize(root: Optional[TreeNode]) -> str:
            """序列化树为字符串"""
            if not root:
                return "null"
            return f"{root.val},{serialize(root.left)},{serialize(root.right)}"
        
        return serialize(p) == serialize(q)
        
        # 或者使用更简洁的版本：
        # def serialize(root):
        #     if not root:
        #         return "null"
        #     return f"{root.val},{serialize(root.left)},{serialize(root.right)}"
        # return serialize(p) == serialize(q)
# @lc code=end



#
# @lcpr case=start
# [1,2,3]\n[1,2,3]\n
# @lcpr case=end

# @lcpr case=start
# [1,2]\n[1,null,2]\n
# @lcpr case=end

# @lcpr case=start
# [1,2,1]\n[1,1,2]\n
# @lcpr case=end

#

