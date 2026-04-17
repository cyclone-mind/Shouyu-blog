---
title: '使用最小花费爬楼梯'
description: '使用最小花费爬楼梯算法题解，使用动态规划解决'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 爬楼梯
  - 基础DP
  - Leetcode
---

## 题目描述

给你一个整数数组`cost`，其中`cost[i]`是从楼梯第`i`个台阶向上爬需要支付的费用。一旦你支付此费用，即可选择向上爬一个或者两个台阶。

你可以选择从下标为`0`或下标为`1`的台阶开始爬楼梯。

请你计算并返回达到楼梯顶部的最低花费。

**示例 1：**

```python
输入：cost = [10,15,20]
输出：15
解释：你将从下标为 1 的台阶开始。
- 支付 15 ，向上爬两个台阶，到达楼梯顶部。
总花费为 15 。
```

[题目链接](https://leetcode.cn/problems/min-cost-climbing-stairs)

[文章讲解](https://programmercarl.com/0746.%E4%BD%BF%E7%94%A8%E6%9C%80%E5%B0%8F%E8%8A%B1%E8%B4%B9%E7%88%AC%E6%A5%BC%E6%A2%AF.html)

## 思路

以示例一为例：

到达楼梯顶部可以由i = 1或者i=2台阶往上爬到。

两种情况下的花费分别是 到达i=1台阶的最小花费加上cost[1]、到达i=2台阶的最小化非加上cost[2]。

这两者都有可能，但是要求是最低花费，因此我们选择这两种情况下花费最少的。

假设爬到第i阶，最少花费是dp[i]，dp[i]就是原问题，子问题包括：

```cpp
dp[i-1],dp[i-2],dp[i-3],...,dp[2],dp[1]
```

这种自下而上，由**最小子问题的解（初试状态）+ 父问题与子问题之间的关系 （状态转移方程）**不断向上循环，直到得到所求 问题的解。正式动态规划的体现

## 递归五部曲

### 1、确定dp数组以及下标的含义

爬到第`i`阶，最少花费是`dp[i]`

### 2、确定递推公式

```cpp
dp[i] = min(dp[i -1] +cost[i - 1],dp[i - 2]+cost[i-2])
```

### 3、dp 数组如何初始化

看一下递归公式，dp[i] 由dp[i - 1]，dp[i - 2]推出，那么只初始化dp[0]和dp[1]就够了。

题目描述中明确说了 “你可以选择从下标为 0 或下标为 1 的台阶开始爬楼梯。” 也就是说 到达 第 0 个台阶是不花费的，但从 第0 个台阶 往上跳的话，需要花费 cost[0]。所以初始化`dp[0] = 0; dp[1] = 0;`

### 4、确定遍历顺序

从前向后

### 5、举例推导dp数组

## 代码实现

```cpp
class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        vector<int> dp(cost.size() + 1);
        dp[0] = 0, dp[1] = 0;
        for (int i = 2; i < cost.size() + 1; i++) {
            dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2]);
        }
        return dp.back();
    }
};
```

## 优化空间复杂度

```cpp
class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        int dp0 = 0;
        int dp1 = 0;
        for (int i = 2; i <= cost.size(); i++) {
            int dpi = min(dp1 + cost[i - 1], dp0 + cost[i - 2]);
            dp0 = dp1; // 记录一下前两位
            dp1 = dpi;
        }
        return dp1;
    }
};
```