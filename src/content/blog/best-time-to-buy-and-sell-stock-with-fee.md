---
title: '买卖股票的最佳时机含手续费'
description: '动态规划解决含手续费的股票买卖最大利润问题。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 股票问题
  - 贪心算法
  - Leetcode
---

## 题目描述

给定一个整数数组`prices`，其中`prices[i]`表示第`i`天的股票价格 ；整数`fee`代表了交易股票的手续费用。

你可以无限次地完成交易，但是你每笔交易都需要付手续费。如果你已经购买了一个股票，在卖出它之前你就不能再继续购买股票了。

返回获得利润的最大值。

**注意**这里的一笔交易指买入持有并卖出股票的整个过程，每笔交易你只需要为支付一次手续费。

**示例 1：**

```cpp
输入：prices = [1, 3, 2, 8, 4, 9], fee = 2
输出：8
解释：能够达到的最大利润:  
在此处买入 prices[0] = 1
在此处卖出 prices[3] = 8
在此处买入 prices[4] = 4
在此处卖出 prices[5] = 9
总利润: ((8 - 1) - 2) + ((9 - 4) - 2) = 8
```

[题目链接](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/)

[文章讲解](https://programmercarl.com/0714.%E4%B9%B0%E5%8D%96%E8%82%A1%E7%A5%A8%E7%9A%84%E6%9C%80%E4%BD%B3%E6%97%B6%E6%9C%BA%E5%90%AB%E6%89%8B%E7%BB%AD%E8%B4%B9%EF%BC%88%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92%EF%BC%89.html)

## 思路

贪心的解法已经讲过，找到正向的利润区间，直到利润区间的利润大于手续费，才收获利润。一旦发现能收获就立马收获。

这个思路不好理解。或者说好理解但不好写出来。

我这里贴出来

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices, int fee) {
        int result = 0;
        int minPrice = prices[0]; // 记录最低价格
        for (int i = 1; i < prices.size(); i++) {
            // 情况二：不断记录当前最小价格，相当于买入
            if (prices[i] < minPrice) minPrice = prices[i];

            // 情况三：此时利润区间是正的，但是还不足以抵扣手续费，因此需要继续观望。
            if (prices[i] >= minPrice && prices[i] <= minPrice + fee) {
                continue;
            }

            // 当利润区间可以抵扣手续费，就收获利润。然后重置
            if (prices[i] > minPrice + fee) {
                result += prices[i] - minPrice - fee;
                minPrice = prices[i] - fee; // 情况一，这一步很关键，避免了在价格连续上涨的时候重复扣手续费。
            }
        }
        return result;
    }
};
```

如果上面关键一步不理解，可以参考下面这个例子：

* 假设prices = [1, 3, 4, 8], fee=2

* 第一次卖出在4时：利润=(4-1)-2=1

* 调整后minPrice=4-2=2

* 这样后续价格是8，8-2-2 = 4。收获利润是5。

* 思想是既然贪心是只要利润合适就收获，必然会导致在4到8这段连续上涨中被多次扣费。那么我就提前把最小价格压低一个手续费。以抵消多次扣费。

## 动规解法

相对于贪心算法：122.买卖股票的最佳时机II 的动态规划解法中，只需要在计算卖出操作的时候减去手续费就可以了，代码几乎是一样的。

```cpp
int maxProfit(vector<int>& prices, int fee) {
    int n = prices.size();
    vector<vector<int>> dp(n, vector<int>(2, 0));
    dp[0][0] -= prices[0]; // 持股票
    for (int i = 1; i < n; i++) {
        dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] - prices[i]);
        dp[i][1] = max(dp[i - 1][1], dp[i - 1][0] + prices[i] - fee); // 仅这一点不同
    }
    return max(dp[n - 1][0], dp[n - 1][1]);
}
```