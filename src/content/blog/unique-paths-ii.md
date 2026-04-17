---
title: '不同路径II'
description: '不同路径II：带障碍物的路径问题'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 路径问题
  - 障碍物
  - Leetcode
---

## 题目描述

给定一个`m x n`的整数数组`grid`。一个机器人初始位于**左上角**（即`grid[0][0]`）。机器人尝试移动到**右下角**（即`grid[m - 1][n - 1]`）。机器人每次只能向下或者向右移动一步。

网格中的障碍物和空位置分别用`1`和`0`来表示。机器人的移动路径中不能包含**任何**有障碍物的方格。

返回机器人能够到达右下角的不同路径数量。

测试用例保证答案小于等于`2 * 109`。

**示例 1：**

```text
输入：obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
输出：2
解释：3x3 网格的正中间有一个障碍物。
从左上角到右下角一共有 2 条不同的路径：
1. 向右 -> 向右 -> 向下 -> 向下
2. 向下 -> 向下 -> 向右 -> 向右
```

[题目链接](https://leetcode.cn/problems/unique-paths-ii)

[文章讲解](https://programmercarl.com/0063.%E4%B8%8D%E5%90%8C%E8%B7%AF%E5%BE%84II.html)

## 思路

这道题与上一道题版本不同的是有了障碍物。那么，从dp数组的角度就可以考虑有障碍物的 dp 值为 0。

## 递归五部曲

### 1、dp数组及下标含义

`dp[i][j]`表示从`(0, 0)`出发到达`(i,j)`位置有`dp[i][j]`条不同的路径。

### 2、递归公式

`dp[i][j] = dp[i-1][j]+dp[i][j-1]`

如果左边和上边是障碍，那么这个公式仍然成立。也就是路径数加0。

如果 (i,j) 是障碍，那么我们就不用计算`dp[i][j]`。直接将`dp[i][j]`设置为0，或者保持0不变

### 3、dp数组初始化

初始任何位置都为0。然后边界任何位置都为1，但是有特殊情况就是边界如果有障碍，那么障碍以后包括障碍也都是0了

所以

```cpp
vector<vector<int>> dp(m, ector<int>(n,0));
for (int i = 0; i < m && obstacleGrid[i][0] == 0; i++) dp[i][0] = 1;
for (int j = 0; j < n && obstacleGrid[0][j] == 0; j++) dp[0][j] = 1;
```

### 4、确定遍历顺序

从递推公式看依然是从上到下，从左到右，所以从左向右一层一层遍历即可

这样保证推导`dp[i][j]`的时候，`dp[i - 1][j]`和`dp[i][j - 1]`一定是有数值。

### 5、举例推导

## 代码实现

```cpp
class Solution {
public:
    int uniquePathsWithObstacles(vector<vector<int>>& obstacleGrid) {
        int m = obstacleGrid.size(), n = obstacleGrid[0].size();
        vector<vector<int>> dp(m, vector<int>(n, 0));
        // 如果起点就是障碍物，则无法移动，返回 0
        if (obstacleGrid[0][0] == 1 || obstacleGrid[m - 1][n - 1] == 1) {
            return 0;
        }
        for (int i = 0; i < n && obstacleGrid[0][i] != 1; i++) {
            dp[0][i] = 1;
        }
        for (int i = 0; i < m && obstacleGrid[i][0] != 1; i++) {
            dp[i][0] = 1;
        }
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                if (obstacleGrid[i][j] != 1) {
                    dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
                }
            }
        }
        return dp[m - 1][n - 1];
    }
};
```

#### 空间优化

```cpp
// 优化版：使用一维数组
int uniquePathsWithObstaclesOptimized(vector<vector<int>> &obstacleGrid) {
    int m = obstacleGrid.size();
    int n = obstacleGrid[0].size();

    // 如果起点就是障碍物，则无法移动，返回 0
    if (obstacleGrid[0][0] == 1) {
        return 0;
    }

    // dp[j] 表示到达当前行第 j 列的路径数
    // 初始化 dp 数组，所有元素为 0
    vector<int> dp(n, 0);

    // 初始化第一行
    // dp[0] 只能从起点到达，如果起点不是障碍物，则 dp[0] 为 1
    dp[0] = 1;
    for (int j = 1; j < n; ++j) {
        // 如果当前位置是障碍物，或者左边的位置不可达，则当前位置不可达
        if (obstacleGrid[0][j] == 1 || dp[j - 1] == 0) {
            dp[j] = 0;
        } else {
            dp[j] = 1;
        }
    }

    // 从第二行开始遍历
    for (int i = 1; i < m; ++i) {
        // 处理当前行的第一列 (dp[0])
        // 如果当前位置 (i, 0) 是障碍物，则 dp[0] 变为 0
        // 否则，dp[0] 保持不变 (即继承上一行 dp[0] 的值，如果上一行 dp[0] 是
        // 0，则当前 dp[0] 也会是 0)
        if (obstacleGrid[i][0] == 1) {
            dp[0] = 0;
        }

        // 遍历当前行的其他列
        for (int j = 1; j < n; ++j) {
            if (obstacleGrid[i][j] == 1) {
                // 如果当前位置是障碍物，则路径数为 0
                dp[j] = 0;
            } else {
                // 路径数 = 从上方来的路径数 (dp[j]) + 从左方来的路径数
                // (dp[j-1])
                dp[j] = dp[j] + dp[j - 1];
            }
        }
    }

    // 返回右下角的路径数
    return dp[n - 1];
}
```