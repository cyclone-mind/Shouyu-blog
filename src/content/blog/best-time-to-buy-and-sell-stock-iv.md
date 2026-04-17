---
title: '买卖股票的最佳时机IV'
description: '动态规划解决最多K笔交易的股票问题。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 股票问题
  - 状态机
  - Leetcode
---

## 题目描述

给你一个整数数组`prices`和一个整数`k`，其中`prices[i]`是某支给定的股票在第`i`天的价格。

设计一个算法来计算你所能获取的最大利润。你最多可以完成`k`笔交易。也就是说，你最多可以买`k`次，卖`k`次。

**注意**你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。

**示例 1：**

```text
输入：k = 2, prices = [2,4,1]
输出：2
解释：在第 1 天 (股票价格 = 2) 的时候买入，在第 2 天 (股票价格 = 4) 的时候卖出，这笔交易所能获得利润 = 4-2 = 2 。
```

[题目链接](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iv
)
[文章讲解](https://programmercarl.com/0188.%E4%B9%B0%E5%8D%96%E8%82%A1%E7%A5%A8%E7%9A%84%E6%9C%80%E4%BD%B3%E6%97%B6%E6%9C%BAIV.html
)

## 思路

与上一题相比，将交易的次数从2次改为了 k 次。

我们就依然需要划分 一天的状态 是在交易的哪个阶段。

## 递归五部曲

### 1、dp数组及下标含义

二维dp数组。`dp[i][j]`：第 i 天的状态是 j ，所剩下的最大现金是`dp[i][j]`

j的状态：

0 - 不操作

1 - 第一次买入

2 - 第一次卖出

3- 第二次买入

4 -第二次卖出

...

我们发现除0外，奇数 j 都是买入，偶数 j 卖出。买入和卖出的次数最终要相等。那么 k 笔交易对应 k 次买入和卖出。所以 j 的范围应该 0~2*k。

```cpp
vector<vector<int>> dp(prices.size(),vector<int>(2*k+1,0));
```

### 2、递推公式

`dp[i][1]`有两种情况：

* 操作一：第i天买入股票了，那么`dp[i][1] = dp[i - 1][0] - prices[i]`

* 操作二：第i天没有操作，而是沿用前一天买入的状态，即：`dp[i][1] = dp[i - 1][1]`

`dp[i][2]`也有两个操作：

* 操作一：第i天卖出股票了，那么`dp[i][2] = dp[i - 1][1] + prices[i]`

* 操作二：第i天没有操作，沿用前一天卖出股票的状态，即：`dp[i][2] = dp[i - 1][2]`

所以`dp[i][2] = max(dp[i - 1][1] + prices[i], dp[i - 1][2])`

那么`dp[i][3]`呢？

公式仍是一样的

* 操作一：第 i 天第二次买入股票了，那么，前一天不持有股票。 `dp[i][3] = dp[i - 1][2] - prices[i]`

* 操作二：第i天没有操作，而是沿用前一天第二次买入的状态，即：`dp[i][3] = dp[i - 1][3]`

总结出 j 是奇数时规律：

`dp[i][j] = max(dp[i-1][j], dp[i-1][j-1]-prices[i])`。

同理 j 是偶数时规律：

`dp[i][j] = max(dp[i-1][j], dp[i-1][j-1]+prices[i])`。

这个定义不清淅，遍历 j ，j 可能奇数也可能偶数。每次循环里还要判断奇偶。

我们可以让 j 从0开始，每次跳两格，这时，j+1就是奇数，j +2 就是偶数。改进后

```cpp
for(int j = 0;j < 2*k +1 ;j+=2){
    dp[i][j + 1] = max(dp[i - 1][j + 1], dp[i - 1][j] - prices[i]);
    dp[i][j + 2] = max(dp[i - 1][j + 2], dp[i - 1][j + 1] + prices[i]);
}
```

### 3、dp数组初始化

j 奇数 初始化为`-peicrs[0]`。其余初始化为0。

### 4、确定遍历顺序

正序，按时间流逝排序

### 5、举例推导

输入`[1,2,3,4,5]`，k=2为例。

最后一次卖出，一定是利润最大的，`dp[prices.size() - 1][2 * k]`即红色部分就是最后求解。

## 代码实现

```cpp
int maxProfit(int k, vector<int>& prices) {
    vector<vector<int>> dp(prices.size(),vector<int>(2 * k + 1, 0));
    for(int j = 1;j < 2 * k;j+=2){
        dp[0][j] = -prices[0];
    }
    for(int i = 1;i< prices.size();i++){
        for(int j = 0;j < 2*k-1;j+=2){
            dp[i][j+1] = max(dp[i - 1][j+1], dp[i - 1][j] - prices[i]);
            dp[i][j+2] = max(dp[i - 1][j+2], dp[i - 1][j+1] + prices[i]);
        }
    }
    return dp[prices.size() - 1][2 * k];
}
```