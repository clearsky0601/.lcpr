# @lcpr-before-debug-begin
from python3problem9 import *
from typing import *
# @lcpr-before-debug-end

#
# @lc app=leetcode.cn id=9 lang=python3
# @lcpr version=30204
#
# [9] 回文数
#
# https://leetcode.cn/problems/palindrome-number/description/
#
# algorithms
# Easy (56.24%)
# Likes:    3041
# Dislikes: 0
# Total Accepted:    1.8M
# Total Submissions: 3.3M
# Testcase Example:  '121'
#
# 给你一个整数 x ，如果 x 是一个回文整数，返回 true ；否则，返回 false 。
# 
# 回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。
# 
# 
# 例如，121 是回文，而 123 不是。
# 
# 
# 
# 
# 示例 1：
# 
# 输入：x = 121
# 输出：true
# 
# 
# 示例 2：
# 
# 输入：x = -121
# 输出：false
# 解释：从左向右读, 为 -121 。 从右向左读, 为 121- 。因此它不是一个回文数。
# 
# 
# 示例 3：
# 
# 输入：x = 10
# 输出：false
# 解释：从右向左读, 为 01 。因此它不是一个回文数。
# 
# 
# 
# 
# 提示：
# 
# 
# -2^31 <= x <= 2^31 - 1
# 
# 
# 
# 
# 进阶：你能不将整数转为字符串来解决这个问题吗？
# 
#


# @lcpr-template-start

# @lcpr-template-end
# @lc code=start
class Solution:
    def isPalindrome(self, x: int) -> bool:
        # 负数和以0结尾的正数（除了0）都不是回文数
        if x < 0 or (x % 10 == 0 and x != 0):
            return False
        
        reversed_half = 0
        while x > reversed_half:
            reversed_half = reversed_half * 10 + x % 10
            x //= 10
        
        # x == reversed_half: 偶数位数的情况
        # x == reversed_half // 10: 奇数位数的情况（去掉中间数字）
        return x == reversed_half or x == reversed_half // 10

# @lc code=end



#
# @lcpr case=start
# 121\n
# @lcpr case=end

# @lcpr case=start
# -121\n
# @lcpr case=end

# @lcpr case=start
# 10\n
# @lcpr case=end

#

