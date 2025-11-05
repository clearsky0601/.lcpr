// @lcpr-before-debug-begin




// @lcpr-before-debug-end

/*
 * @lc app=leetcode.cn id=3238 lang=cpp
 * @lcpr version=30204
 *
 * [3238] 求出胜利玩家的数目
 */


// @lcpr-template-start
using namespace std;
#include <algorithm>
#include <array>
#include <bitset>
#include <climits>
#include <deque>
#include <functional>
#include <iostream>
#include <list>
#include <queue>
#include <stack>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>
// @lcpr-template-end
// @lc code=start
class Solution {
public:
    int winningPlayerCount(int n, vector<vector<int>>& pick) {
        
        // 使用哈希表记录每个玩家获得的每种颜色球的数量
        unordered_map<int, unordered_map<int, int>> playerBalls;
        
            // 遍历所有的 pick 记录
            for (auto& p : pick) {
                int player = p[0];
                int color = p[1];
                // 增加对应玩家对应颜色球的数量
                playerBalls[player][color]++;
            }
        
        // 计数胜利玩家的数量
        int count = 0;
        for (int i = 0; i < n; ++i) {
            // 检查玩家 i 是否是胜利玩家
            bool isWinner = false;
            for (auto& colorCount : playerBalls[i]) {
                if (colorCount.second > i) {
                    isWinner = true;
                    break;
                }
            }
            // 如果玩家 i 是胜利玩家，增加计数
            if (isWinner) {
                ++count;
            }
        }
        
        return count;
        
    }
};
// @lc code=end


// @lcpr-div-debug-arg-start
// funName=demo
// paramTypes= ["number","number[][]"]
// @lcpr-div-debug-arg-end




/*
// @lcpr case=start
// 4\n[[0,0],[1,0],[1,0],[2,1],[2,1],[2,0]]\n
// @lcpr case=end

// @lcpr case=start
// 5\n[[1,1],[1,2],[1,3],[1,4]]\n
// @lcpr case=end

// @lcpr case=start
// 5\n[[1,1],[2,4],[2,4],[2,4]]\n
// @lcpr case=end

 */

