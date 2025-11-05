# 100. 相同的树

## 题目链接

https://leetcode.cn/problems/same-tree/

## 难度

Easy

## 题目描述

给你两棵二叉树的根节点 `p` 和 `q` ，编写一个函数来检验这两棵树是否相同。

如果两个树在结构上相同，并且节点具有相同的值，则认为它们是相同的。

## 解法

### 方法1：递归DFS（推荐⭐）

- 文件：`solution.py`
- 时间复杂度：O(min(m, n))，其中m和n分别是两棵树的节点数
- 空间复杂度：O(min(m, n))，递归栈的深度
- 思路：
  - 递归遍历两棵树，同时比较对应节点
  - 如果两个节点都为空，返回True
  - 如果只有一个节点为空，返回False
  - 如果节点值不同，返回False
  - 递归比较左右子树

**优点**：
- 代码简洁清晰
- 最容易理解和实现
- 时间复杂度最优

**代码要点**：
```python
if not p and not q:
    return True
if not p or not q:
    return False
if p.val != q.val:
    return False
return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
```

### 方法2：迭代DFS（使用栈）

- 文件：`solution2-iterative-dfs.py`
- 时间复杂度：O(min(m, n))
- 空间复杂度：O(min(m, n))
- 思路：
  - 使用栈模拟递归过程
  - 同时遍历两棵树，比较对应节点
  - 将左右子节点入栈（先右后左，因为栈是LIFO）

**优点**：
- 避免了递归栈溢出的风险
- 适合深度很大的树

**缺点**：
- 代码相对复杂
- 需要手动管理栈

### 方法3：迭代BFS（使用队列）

- 文件：`solution3-iterative-bfs.py`
- 时间复杂度：O(min(m, n))
- 空间复杂度：O(min(m, n))
- 思路：
  - 使用队列进行层序遍历
  - 每次从队列中取出两个对应节点进行比较
  - 如果所有节点都相同，返回True

**优点**：
- 层序遍历，可以提前发现不同
- 适合宽度很大的树

**缺点**：
- 代码相对复杂
- 需要手动管理队列

### 方法4：序列化比较

- 文件：`solution4-serialize.py`
- 时间复杂度：O(min(m, n))
- 空间复杂度：O(min(m, n))
- 思路：
  - 将两棵树序列化为字符串
  - 比较序列化后的字符串是否相同

**优点**：
- 思路新颖有趣
- 代码简洁

**缺点**：
- 需要额外的字符串空间
- 字符串比较可能较慢（虽然复杂度相同）

## 总结

- **最佳解法**：方法1（递归DFS）
  - 代码最简洁
  - 最容易理解
  - 性能最优

- **适用场景**：
  - 递归DFS：一般情况下首选
  - 迭代DFS：树很深时使用
  - 迭代BFS：树很宽时使用
  - 序列化：需要序列化树时使用

- **相关题目**：
  - [101. 对称二叉树](https://leetcode.cn/problems/symmetric-tree/)
  - [226. 翻转二叉树](https://leetcode.cn/problems/invert-binary-tree/)
  - [572. 另一棵树的子树](https://leetcode.cn/problems/subtree-of-another-tree/)

## 复杂度对比

| 方法 | 时间复杂度 | 空间复杂度 | 代码复杂度 |
|------|-----------|-----------|-----------|
| 递归DFS | O(min(m,n)) | O(min(m,n)) | ⭐⭐ |
| 迭代DFS | O(min(m,n)) | O(min(m,n)) | ⭐⭐⭐ |
| 迭代BFS | O(min(m,n)) | O(min(m,n)) | ⭐⭐⭐ |
| 序列化 | O(min(m,n)) | O(min(m,n)) | ⭐⭐ |

## 测试用例

```
输入：p = [1,2,3], q = [1,2,3]
输出：true

输入：p = [1,2], q = [1,null,2]
输出：false

输入：p = [1,2,1], q = [1,1,2]
输出：false
```

