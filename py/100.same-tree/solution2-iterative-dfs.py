# @lc app=leetcode.cn id=100 lang=python3
# @lcpr version=
#
# [100] 相同的树 - 方法2：迭代DFS
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
        方法2：迭代DFS（使用栈）
        时间复杂度：O(min(m, n))
        空间复杂度：O(min(m, n))
        
        思路：
        1. 使用栈模拟递归过程
        2. 同时遍历两棵树，比较对应节点
        3. 如果所有节点都相同，返回True
        """
        stack = [(p, q)]
        
        while stack:
            node1, node2 = stack.pop()
            
            # 两个节点都为空，继续
            if not node1 and not node2:
                continue
            
            # 只有一个节点为空
            if not node1 or not node2:
                return False
            
            # 节点值不同
            if node1.val != node2.val:
                return False
            
            # 将左右子节点入栈（注意顺序：先右后左，因为栈是LIFO）
            stack.append((node1.right, node2.right))
            stack.append((node1.left, node2.left))
        
        return True
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

