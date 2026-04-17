---
title: 'N皇后'
description: '回溯算法解决N皇后问题，在n×n棋盘上放置n个皇后且彼此不能相互攻击。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 回溯算法
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

## 题目描述

按照国际象棋的规则，皇后可以攻击与之处在同一行或同一列或同一斜线上的棋子。

**n 皇后问题**研究的是如何将`n`个皇后放置在`n×n`的棋盘上，并且使皇后彼此之间不能相互攻击。

给你一个整数`n`，返回所有不同的**n 皇后问题**的解决方案。

每一种解法包含一个不同的**n 皇后问题**的棋子放置方案，该方案中`'Q'`和`'.'`分别代表了皇后和空位。

## 思考

一次一次的放，保证后一个和前一个不打架。每次都在下一行选择。

回溯函数`backtrack(row)`，它的任务是“在第`row`行，给皇后找个合适的位置”。

## 回溯三部曲

**回溯函数的参数**

* 当前要处理哪一行 (`int row`): 给第 row 行找个位置”。

* 棋盘长啥样了 (`vector<string>& board`): 这个参数记录了之前的决策。它就像一张草稿纸，上面画着0到 row-1 行的皇后都放在了哪儿。

* 最终结果集 (`vector<vector<string>>& result`): 收集所有符合条件的棋盘布局。这个也可以设置为全局变量，都可以

**终止条件**

当`row`增加到`n`的时候，意味着第 0, 1, 2, ...,`n-1`行已经全部成功地、互不冲突地放上了皇后。

**这不就找到了一个完整的、可行的解决方案吗！**

所以，终止条件就是`row == n`。一旦满足这个条件，说明大功告成，把当前的`board`放进result`

**单层搜索逻辑**

在**当前**`**row**`**这一行**，一个固定的工作流程：**“遍历选择 -> 判断 -> 做决定 -> 交给下一行 -> 撤销决定”**。

1. 遍历所有可能的选择: 在第 row 行，我们需要一个 for 循环来遍历所有列。

2. 判断选择是否有效（剪枝）: 对于 for 循环中的每一个 col，我们都得判断皇后放在 (row, col) 这个位置，是否会与（0到 row-1 行的皇后）冲突。写一个辅助函数 `isValid(row, col, board)` 判断。

3. 执行“选择-前进-撤销”循环: 如果 isValid 判断通过，说明 (row, col) 是一个当前看来可行的选择，正式进入“小三步”：

处理节点（做出选择）: 在棋盘的 (row, col) 位置放上皇后。 `board[row][col] = 'Q';`

递归（前进）: 既然这一行搞定了，那就把剩下的任务交给下一行。调用自身，去处理 row + 1 行。 backtrack(n, row + 1, board, result);

回溯（撤销选择）: 当上面那句 backtrack(row + 1, ...) 执行完毕返回时，意味着基于 (row, col) 这个位置所能引发的所有后续可能性都已经被探索完了。我们必须把棋盘恢复原状，也就是把刚刚放在 (row, col) 的皇后拿走，这样 for 循环在下一次迭代（col + 1）时，才能在一个干净的棋盘上尝试新的选择。 `board[row][col] = '.';`

## 代码实现

```cpp
class Solution {
public:
    vector<vector<string>> result;

    bool isValid(int row, int col, vector<string> chessboard, int n) {
        // 检查列
        for (int i = 0; i < row; i++) {
            if (chessboard[i][col] == 'Q') {
                return false;
            }
        }
        // 检查 45度角是否有皇后
        for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
            if (chessboard[i][j] == 'Q') {
                return false;
            }
        }
        // 检查 135度角是否有皇后
        for (int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++) {
            if (chessboard[i][j] == 'Q') {
                return false;
            }
        }
        return true;
    }

    void backtracking(int n, int row, vector<string>& chessboard) {
        if (row == n) {
            result.push_back(chessboard);
            return;
        }
        for (int col = 0; col < n; col++) {
            if (isValid(row, col, chessboard, n)) {
                chessboard[row][col] = 'Q';
                backtracking(n, row + 1, chessboard);
                chessboard[row][col] = '.';
            }
        }
    }

    vector<vector<string>> solveNQueens(int n) {
        result.clear();
        vector<string> chessboard(n, string(n, '.'));
        backtracking(n, 0, chessboard);
        return result;
    }
};
```
