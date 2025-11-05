# LCPR 插件快速参考

## 🚀 快速开始

### 基本文件格式

```python
# @lc app=leetcode.cn id=题目编号 lang=python3
# @lcpr version=

# @lc code=start
class Solution:
    def yourFunction(self, ...):
        # 你的代码
        pass
# @lc code=end

# @lcpr case=start
# 输入参数1\n输入参数2\n...
# @lcpr case=end
```

---

## 📝 用不同方法刷题的5种方式

### 方式1：同一文件，注释多个解法（推荐⭐）

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # ========== 方法1：当前使用 ==========
        # 哈希表解法
        num_dict = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_dict:
                return [num_dict[complement], i]
            num_dict[num] = i
        return []
        
        # ========== 方法2：已注释 ==========
        # 暴力解法
        # for i in range(len(nums)):
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] + nums[j] == target:
        #             return [i, j]
        # return []
```

**优点**：方便对比，保留历史思路

---

### 方式2：创建多个文件（不同语言）

```
1.two-sum.py      # Python版本
1.two-sum.cpp     # C++版本
1.two-sum.java    # Java版本
```

**优点**：练习不同语言

---

### 方式3：创建多个文件（不同算法）

```
560.subarray-sum-equals-k.brute-force.py
560.subarray-sum-equals-k.prefix-sum.py
560.subarray-sum-equals-k.sliding-window.py
```

**优点**：每个文件专注一种算法

---

### 方式4：添加多个测试用例

```python
# @lcpr case=start
# [1,1,1]\n2\n
# @lcpr case=end

# @lcpr case=start
# [1]\n1\n          # 边界情况
# @lcpr case=end

# @lcpr case=start
# [1,-1,0]\n0\n     # 包含负数
# @lcpr case=end
```

**优点**：测试不同场景

---

### 方式5：使用Jupyter Notebook

```
syntax/py/1.two-sum.ipynb
```

**优点**：逐步执行，可视化结果

---

## 🎯 工作流程

### 1. 创建新题目

```bash
# 插件会自动生成文件，或手动创建：
touch 560.subarray-sum-equals-k.py
```

### 2. 编写代码

```python
# @lc app=leetcode.cn id=560 lang=python3
# @lcpr version=

# @lc code=start
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # 你的代码
        pass
# @lc code=end

# @lcpr case=start
# [1,1,1]\n2\n
# @lcpr case=end
```

### 3. 测试代码

- 点击 `@lcpr case` 上方的 **"Run"** 按钮
- 或点击 **"Debug"** 按钮进行调试

### 4. 调试代码

1. 设置断点（点击行号左侧）
2. 点击 **"Debug"** 按钮
3. 如果停在插件代码，按 **F5** 继续
4. 查看变量值（左侧面板或悬停）

---

## 🔍 核心原理（简化版）

```
你的代码文件
    ↓
插件解析 @lc 和 @lcpr 标记
    ↓
提取函数定义和测试用例
    ↓
生成临时测试文件
    ↓
执行测试并显示结果
```

---

## 📁 重要文件说明

| 文件/目录 | 说明 |
|---------|------|
| `leetcode/cache/*.json` | 题目元数据（描述、模板等） |
| `.lcpr_data/bricks.json` | 刷题进度（间隔重复） |
| `leetcode/stat.json` | 统计信息 |
| `*.py` | 你的代码文件 |

---

## 💡 最佳实践

1. ✅ **保留多种解法**：用注释保留历史解法
2. ✅ **添加详细注释**：说明时间/空间复杂度
3. ✅ **测试边界情况**：添加多个测试用例
4. ✅ **记录思路**：在文件顶部记录解题思路
5. ✅ **定期复习**：使用插件的间隔重复功能

---

## 🛠️ 常用命令

```bash
# 导出题目为Markdown
python3 export_lcpr_markdown.py --filter "560"

# 批量获取题目
python3 fetch_all_cache_json.py

# 批量导出Markdown
python3 fetch_all_markdown.py
```

---

## ❓ 常见问题

**Q: 如何切换解法？**
A: 注释掉当前解法，取消注释另一个解法

**Q: 如何添加自定义测试用例？**
A: 添加新的 `@lcpr case=start/end` 块

**Q: 如何调试？**
A: 设置断点 → 点击Debug → 按F5跳过插件代码

**Q: 进度如何跟踪？**
A: 插件自动更新 `bricks.json`，使用间隔重复算法

---

## 📚 更多信息

- 详细原理：查看 `LCPR插件原理详解.md`
- 调试指南：查看 `LCPR_调试指南.md`
- 示例文件：查看 `1.two-sum-multiple-solutions.py`


