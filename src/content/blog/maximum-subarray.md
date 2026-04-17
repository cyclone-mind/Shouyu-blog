---
title: '最大子序和'
description: '给定一个整数数组 nums，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 贪心算法
  - 线性DP
  - Leetcode
---


## 题目描述

给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

示例:

* 输入: [-2,1,-3,4,-1,2,1,-5,4]

* 输出: 6

* 解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。

[题目链接](https://leetcode.cn/problems/maximum-subarray/)

[文章讲解](https://programmercarl.com/0053.%E6%9C%80%E5%A4%A7%E5%AD%90%E5%BA%8F%E5%92%8C%EF%BC%88%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92%EF%BC%89.html)

## 思路

这道题之前是使用贪心做的，连续子数组最大和。其实用贪心很不好想。这次使用动态规划的思想。

为什么想到动态规划？因为观察到连续子数组和的增加是依赖在后面增加一个元素。这样增加前和增加后就有了状态之间的关系。

## 递归五部曲

### 1、dp 数组及下标含义

**dp[i]：包括下标i（以nums[i]为结尾）的最大连续子序列和为dp[i]**。

### 2、递推公式

`dp[i]`有两者情况：

* 情况1：前者是一个最大连续子序列，i 在其后面使其和增加，此时dp[i] = dp[i - 1] + nums[i]

* 情况2：i 是一个 新的连续子序列，是一个新的开始，此时dp[i] = nums[i]

两者可能的情况中取最大值

`dp[i] = max(dp[i - 1] + nums[i], nums[i]);`

### 3、初始化

初始化dp[0]=nums[0]

### 4、确定遍历顺序

从前往后

### 5、举例推导

输入：nums = [-2,1,-3,4,-1,2,1,-5,4]，对应的dp状态如下：

**注意最后的结果可不是dp[nums.size() - 1]！**，而是dp[6]。 找每一个i为终点的连续最大子序列。

## 代码实现

```cpp
int maxSubArray(vector<int>& nums) {
    vector<int> dp(nums.size());
    dp[0] = nums[0];
    int result = nums[0];
    for(int i = 1;i < nums.size();i++){
        dp[i] = max(dp[i - 1] + nums[i],nums[i]);
        if(dp[i] > result) result = dp[i];
    }
    return result;
}
```