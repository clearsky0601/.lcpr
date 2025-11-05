#
# @lc app=leetcode.cn id=2177 lang=python3
# @lcpr version=
#
# [2177] 找到和为给定整数的三个连续整数
#


# @lcpr-template-start

# @lcpr-template-end
# @lc code=start
class Solution:
    def sumOfThree(self, num: int) -> List[int]:
        if (num/3)%1 == 0:
            return [num//3-1,num//3,num//3+1]
        else:
            return []
# @lc code=end



#
# @lcpr case=start
# 33\n
# @lcpr case=end

# @lcpr case=start
# 4\n
# @lcpr case=end

#

