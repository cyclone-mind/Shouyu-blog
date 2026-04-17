---
title: '最长连续递增序列'
description: '最长连续递增序列算法题解，使用动态规划解决'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 数组
  - Leetcode
---

## 题目描述

给定一个未经排序的整数数组，找到最长且**连续递增的子序列**，并返回该序列的长度。

**连续递增的子序列**可以由两个下标`l`和`r`（`l < r`）确定，如果对于每个`l <= i < r`，都有`nums[i] < nums[i + 1]`，那么子序列`[nums[l], nums[l + 1], ..., nums[r - 1], nums[r]]`就是连续递增子序列。

**示例 1：**

```text
输入：nums = [1,3,5,4,7]
输出：3
解释：最长连续递增序列是 [1,3,5], 长度为3。
尽管 [1,3,5,7] 也是升序的子序列, 但它不是连续的，因为 5 和 7 在原数组里被 4 隔开。
```

[题目链接](https://leetcode.cn/problems/longest-continuous-increasing-subsequence)

[文章讲解](https://programmercarl.com/0674.%E6%9C%80%E9%95%BF%E8%BF%9E%E7%BB%AD%E9%80%92%E5%A2%9E%E5%BA%8F%E5%88%97.html)

## 思路

与上一题的区别在于连续。上一题我们在递推出`dp[i]`的时候我们要找到 [0，i-1] 之间的 所有 dp 值，找出最长的那个 +1。

这道题有了连续，示例中，计算`dp[4]`时，它的最长连续递增序列是 [4,7]，并不能以原本定义中的 dp[0] dp[1] dp[2] 得出，因为这三者都经历了 nums[3] 这个数导致子序列没有严格递增。

所以，要想得到dp[4] 就必须确定前一个元素是连续递增序列的末尾元素才可以。此时dp[0] dp[1] dp[2] 就没必要计算了。 这里就是**和****动态规划：300.最长递增子序列 ****的区别！**

## 递归五部曲

### 1、dp数组及下标含义

**dp[i]表示i之前包括i的以nums[i]结尾的最长连续递增子序列的长度**

### 2、递推公式

`nums[i] > nums[i - 1]`时`dp[i] = dp[i-1] + 1;`

### 4、确定遍历顺序

从前向后遍历

### 5、举例推导

输入nums = [1,3,5,4,7]为例，dp数组状态如下：

**注意这里依然要要取所有**`**dp[i]**`**里的最大值，即**`**dp[2]**`

## 代码实现

```cpp
int findLengthOfLCIS(vector<int> &nums) {
    if (nums.size() <= 1)
        return 1;
    vector<int> dp(nums.size(), 1);
    int result = 0;
    for (int i = 1; i < nums.size(); i++) {
            if (nums[i] > nums[i - 1])
                dp[i] = dp[i - 1] + 1;
        if (dp[i] > result) result = dp[i];
    }
    return result;
}
```