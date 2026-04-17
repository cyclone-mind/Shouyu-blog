---
title: '柠檬水找零'
description: '柠檬水找零算法题解，使用贪心算法解决'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 贪心
  - 贪心算法
  - Leetcode
---

## 题目描述

在柠檬水摊上，每一杯柠檬水的售价为`5`美元。顾客排队购买你的产品，（按账单`bills`支付的顺序）一次购买一杯。

每位顾客只买一杯柠檬水，然后向你付`5`美元、`10`美元或`20`美元。你必须给每个顾客正确找零，也就是说净交易是每位顾客向你支付`5`美元。

注意，一开始你手头没有任何零钱。

给你一个整数数组`bills`，其中`bills[i]`是第`i`位顾客付的账。如果你能给每位顾客正确找零，返回`true`，否则返回`false`。

[题目链接](https://leetcode.cn/problems/lemonade-change)

[文章讲解](https://programmercarl.com/0860.%E6%9F%A0%E6%AA%AC%E6%B0%B4%E6%89%BE%E9%9B%B6.html)

## 思考

这道题需要我们维护三种钞票的数量，并在找零时，为了将来能更容易地找零，需要优先消耗10美元钞票，10美元没了再消耗5美元钞票。

这就是我们的贪心。

## 代码实现

```cpp
class Solution {
public:
    bool lemonadeChange(vector<int>& bills) {
        int five = 0, ten = 0, twenty = 0;
        for (int bill : bills) {
            // 情况一
            if (bill == 5) five++;
            // 情况二
            if (bill == 10) {
                if (five <= 0) return false;
                ten++;
                five--;
            }
            // 情况三
            if (bill == 20) {
                // 优先消耗10美元，因为5美元的找零用处更大，能多留着就多留着
                if (five > 0 && ten > 0) {
                    five--;
                    ten--;
                } else if (five >= 3) {
                    five -= 3;
                } else return false;
            }
        }
        return true;
    }
};
```