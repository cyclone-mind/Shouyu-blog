---
title: '不相交的线'
description: '不相交的线：最长公共子序列问题'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 最长公共子序列
  - Leetcode
---

## 题目描述

在两条独立的水平线上按给定的顺序写下 nums1 和 nums2 中的整数。

现在，可以绘制一些连接两个数字 nums1[i] 和 nums2[j] 的直线，这些直线需要同时满足：

* nums1[i] == nums2[j]

* 且绘制的直线不与任何其他连线（非水平线）相交。

请注意，连线即使在端点也不能相交：每个数字只能属于一条连线。

以这种方法绘制线条，并返回可以绘制的最大连线数。

[题目链接](https://leetcode.cn/problems/uncrossed-lines/)

[文章讲解](https://programmercarl.com/1035.%E4%B8%8D%E7%9B%B8%E4%BA%A4%E7%9A%84%E7%BA%BF.html)

## 思路

绘制线段说明要找到相同的两个元素，而直线不能相交就是要找子序列，子序列不能改变相对顺序。

**本质上是求两个字符串的最长公共子序列**

## 代码实现

```cpp
int maxUncrossedLines(vector<int> &nums1, vector<int> &nums2) {
    int m = nums1.size(), n = nums2.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    for (int i = 1; i < m + 1; i++) {
        for (int j = 1; j < n + 1; j++) {
            if (nums1[i - 1] == nums2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = max(dp[i][j - 1], dp[i - 1][j]);
            }
        }
    }
    return dp[m][n];
}
```