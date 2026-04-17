---
title: '解数独'
description: '回溯算法解决数独问题，填充空格使数独满足规则。'
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

编写一个程序，通过填充空格来解决数独问题。

数独的解法需**遵循如下规则**：

1. 数字 1-9 在每一行只能出现一次。

1. 数字 1-9 在每一列只能出现一次。

1. 数字 1-9 在每一个以粗实线分隔的 3x3 宫内只能出现一次。（请参考示例图）

数独部分空格内已填入了数字，空白格用`'.'`表示。

[题目链接]51

[文章讲解]51

## 思考

## 回溯三部曲

**回溯函数的参数**及返回值

* 棋盘本身 (vector<vector<char>>& board): 引用传递（&），保证所有修改都是全局可见的。

* bool 返回值。返回true说明当填的数字是正确的，后续基于这个数字能得出正确的解。返回false说明当前数字填不上，或者当前填没问题，但是后续基于这个数字推导的结果是错误解。

**终止条件**

什么时候填充完毕？当然是棋盘上所有的格子都填满了数字，再也找不到一个`'.'`的时候。

所以，在`backtrack`函数的一开始，我们就应该先去找下一个需要填的空格。如果我们把整个棋盘从头到尾扫了一遍，都**没找到**空格，那说明数独已经完成了。找到了一个解！

然后收工，返回true。

```cpp
// 在 backtrack 函数内部
for (int i = 0; i < 9; ++i) {
    for (int j = 0; j < 9; ++j) {
        if (board[i][j] == '.') {
            // 找到了空格，还没结束，继续下面的单层逻辑
            // ...
        }
    }
}

// 如果两个循环跑完了都没找到'.', 说明大功告成！
return true; // 终止条件达成
```

**单层搜索逻辑**

当我们找到了一个需要填写的空格，比如在`(row, col)`位置，我们要做什么。

**1. 有哪些选择？**这个空格，可以尝试填入数字 '1' 到 '9'。

**2. 判断选择是否有效**在尝试填入数字`k`之前，必须检查一下，在`(row, col)`这个位置放`k`是否违反数独规则？也就是：

* 第 row 行，已经有 k 了吗？

* 第 col 列，已经有 k 了吗？

* (row, col) 所在的 3x3 小方块里，已经有 k 了吗？

这三个检查但凡有一个不通过，就不能填`k`，继续试下一个数字。

**3. “尝试-深入-撤销”的小循环**如果 k 有效，就开始“回溯小三步”：

* **做出尝试 **: 在 1board[row][col]1 填上 k。 1board[row][col] = k;1

* 深入探索: 基于这个尝试，继续再调用一次 1backtrack(board)1 就行！它会自然地去寻找下一个空格，并重复上面的过程。 1if (backtrack(board)) return true;1 如果深层的调用返回了 true，说明它已经找到了一个完整的解。就没必要再尝试别的数字了，立刻把这个 true 继续向上传递，层层返回，结束整个搜索。

* 撤销尝试 (Undo): 如果深层的调用返回了 false，那说明刚才把 k 放在 (row, col) 这个决定是错误的，它导致了后面的路走不通。我们必须回溯，把这个位置恢复原样，好在下一次 for 循环中尝试 k+1。 1board[row][col] = '.';1

如果`for`循环把 '1' 到 '9' 全都试完了，（要么是自身不合法，要么是导致的后续的路都是死路），那么说明在当前棋盘状态下，`(row, col)`这个格子无解。函数只能无奈地返回`false`，告诉上一层：“你给我的这个局面是个烂摊子，我解决不了。”

## 代码实现

```cpp
class Solution {
public:
    void solveSudoku(vector<vector<char>>& board) {
        backtrack(board);
    }

private:
    // 回溯主函数
    bool backtrack(vector<vector<char>>& board) {
        for (int i = 0; i < 9; ++i) {        // 遍历行
            for (int j = 0; j < 9; ++j) {    // 遍历列
                // 如果当前格子是空的，才需要我们处理
                if (board[i][j] == '.') {
                    // === 这是我们的“单层搜索逻辑” ===
                    for (char k = '1'; k <= '9'; ++k) { // 尝试填入1-9
                        if (isValid(i, j, k, board)) { // 如果这个数字合法
                            // 1. 做出选择
                            board[i][j] = k;
                            // 2. 深入下一层
                            if (backtrack(board)) {
                                return true; // 如果下一层成功了，直接返回true
                            }
                            // 3. 撤销选择
                            board[i][j] = '.';
                        }
                    }
                    // 如果1-9都试过了还不行，说明上一步错了，返回false
                    return false; 
                }
            }
        }
        // === 这是我们的“终止条件” ===
        // 如果遍历完整个棋盘都没找到空格，说明解题成功！
        return true;
    }

    // 检查在 (row, col) 位置放数字 k 是否合法
    bool isValid(int row, int col, char k, vector<vector<char>>& board) {
        // 检查行
        for (int i = 0; i < 9; ++i) {
            if (board[row][i] == k) return false;
        }
        // 检查列
        for (int i = 0; i < 9; ++i) {
            if (board[i][col] == k) return false;
        }
        // 检查 3x3 小方块
        int startRow = (row / 3) * 3;
        int startCol = (col / 3) * 3;
        for (int i = startRow; i < startRow + 3; ++i) {
            for (int j = startCol; j < startCol + 3; ++j) {
                if (board[i][j] == k) return false;
            }
        }
        return true;
    }
};
```