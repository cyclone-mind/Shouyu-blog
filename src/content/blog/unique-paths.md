---
title: '不同路径'
description: '不同路径：动态规划路径问题'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 路径问题
  - 组合数学
  - Leetcode
---

## 题目描述

一个机器人位于一个`m x n`网格的左上角 （起始点在下图中标记为 “Start” ）。

机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为 “Finish” ）。

问总共有多少条不同的路径？

**示例 1：**

```cpp
输入：m = 3, n = 7
输出：28
```

**示例 2：**

```python
输入：m = 3, n = 2
输出：3
解释：
从左上角开始，总共有 3 条路径可以到达右下角。
1. 向右 -> 向下 -> 向下
2. 向下 -> 向下 -> 向右
3. 向下 -> 向右 -> 向下
```

[题目链接](https://leetcode.cn/problems/unique-paths)

[文章讲解](https://programmercarl.com/0062.%E4%B8%8D%E5%90%8C%E8%B7%AF%E5%BE%84.html)

## 思路

直观的想法是图论里面的深搜，每次向下或者向右，每次分叉作为二叉树的一个节点。叶子节点就是终点，有多少条不同的路径到达叶子节点，就是结果。

举例的话就是

节点或者说位置是 i，j，终点是m，n

情况1是到达终点，情况2是超出边界，情况3就是其余位置，需要继续移动。当然也可以从二叉树的角度，终止条件是情况1、2，递归逻辑是情况3其余位置。遍历顺序是后序遍历，因为

dfs函数的含义是从位置i，j到终点有多少种路径。

```cpp
int uniquePaths(int m, int n){
    return dfs(1,1,m,n);
}
int dfs(int i,int j, int m,int n){
    // 基础情况1: 到达终点
    if (i == m && j == n) {
        return 1;  // 找到一条有效路径
    }
    // 基础情况2: 超出边界
    if (i > m || j > n) {
        return 0;  // 无效路径
    }
    // 递归情况: 向下 + 向右
    int down = dfs(i + 1, j, m, n);    // 向下移动
    int right = dfs(i, j + 1, m, n);   // 向右移动
    
    return down + right;  // 返回所有可能的路径数
}
```

动规思路

讨论我们是如何到达 (i,j) 的：

* 如果是从(i−1,j)过来，那么问题变成从起点 (0,0) 走到 (i−1,j) 的路径数，即 dfs(i−1,j)。

* 如果是从(i,j−1)过来，那么问题变成从起点 (0,0) 走到 (i,j−1) 的路径数，即 dfs(i,j−1)。
这两种情况互斥，根据加法原理，有

```cpp
dfs(i,j)=dfs(i−1,j)+dfs(i,j−1)
```

## 动态规划五部曲

### 1、确定dp数组以及下标的含义

`dp[i][j]`：表示从（0 ，0）出发，到 (i, j) 有`dp[i][j]`条不同的路径。

### 2、确定递推公式

到达 i，j 位置无非是从上面过来或者左边过来。很自然，`dp[i][j] = dp[i - 1][j] + dp[i][j - 1]`，

### 3、dp 数组如何初始化

因为遍历 i 要从1开始，因此需要确定i j 等于0 的情况，即边界情况，那么到达边界上的任何点都是只有一种方案，一条路径。

初始化边界：

```cpp
for (int i = 0; i < m; i++) dp[i][0] = 1;
for (int j = 0; j < n; j++) dp[0][j] = 1;
```

### 4、确定遍历顺序

递推公式`dp[i][j] = dp[i - 1][j] + dp[i][j - 1]`，`dp[i][j]`都是从其上方和左方推导而来，那么从左到右一层一层遍历就可以了。

### 5、举例推导dp数组

把dp数组画出来就很好理解

## 代码实现

```cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<vector<int>> dp(m, vector<int>(n, 0));
        for (int i = 0; i < m; i++) dp[i][0] = 1;
        for (int j = 0; j < n; j++) dp[0][j] = 1;
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
            }
        }
        return dp[m - 1][n - 1];
    }
};
```

## 优化空间复杂度

```cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<int> dp(n);
        for (int i = 0; i < n; i++) dp[i] = 1;
        for (int j = 1; j < m; j++) {
            for (int i = 1; i < n; i++) {
                dp[i] += dp[i - 1];
            }
        }
        return dp[n - 1];
    }
};
```