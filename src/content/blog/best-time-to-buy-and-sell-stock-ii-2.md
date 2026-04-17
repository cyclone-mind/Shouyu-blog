---
title: '买卖股票的最佳时机II'
description: '贪心算法解决股票买卖问题，多次交易获取最大利润。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 贪心算法
  - 股票问题
  - 动态规划
  - Leetcode
---

## 题目描述

给定一个数组，它的第  i 个元素是一支给定股票第 i 天的价格。

设计一个算法来计算你所能获取的最大利润。你可以尽可能地完成更多的交易（多次买卖一支股票）。

注意你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。

[题目链接](<https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/>)

[文章讲解](<https://programmercarl.com/0122.%E4%B9%B0%E5%8D%96%E8%82%A1%E7%A5%A8%E7%9A%84%E6%9C%80%E4%BD%B3%E6%97%B6%E6%9C%BAII.html>)

## 思考

### 贪心解法

图形化的方式很好理解

对于股票走势图，汇总出来所有上升的值即可。

贪心的思路理解的话就是，体现在短视，只在乎一天的利益，一张股票在手里只待一天。

这意味着，只要明天这只股票是涨的，我今天就买，明天就卖，而不管后天如何变化，后天如果涨，那我明天卖了再买呗，如果后天跌了，正好明天我卖了后就不再买了。

## 代码实现

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int result = 0;
        for (int i = 1; i < prices.size(); i++) {
            result += max(prices[i] - prices[i - 1], 0);
        }
        return result;
    }
};
```