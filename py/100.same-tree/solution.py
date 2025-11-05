#
# @lc app=leetcode.cn id=100 lang=python3
# @lcpr version=
#
# [100] 相同的树
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
        方法1：递归DFS（深度优先搜索）
        时间复杂度：O(min(m, n))，其中m和n分别是两棵树的节点数
        空间复杂度：O(min(m, n))，递归栈的深度
        
        思路：
        1. 如果两个节点都为空，返回True
        2. 如果只有一个节点为空，返回False
        3. 如果两个节点值不同，返回False
        4. 递归比较左子树和右子树
        """
        # 两个节点都为空
        if not p and not q:
            return True
        
        # 只有一个节点为空
        if not p or not q:
            return False
        
        # 节点值不同
        if p.val != q.val:
            return False
        
        # 递归比较左右子树
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        
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

