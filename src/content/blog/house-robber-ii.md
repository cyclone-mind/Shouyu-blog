---
title: '打家劫舍II'
description: '环形房屋的偷窃问题，相邻房屋不能同时偷窃'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 环形DP
---

## 题目描述

你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，**如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警**。

你是一个专业的小偷，计划偷窃沿街的房屋，每间房内都藏有一定的现金。这个地方所有的房屋都**围成一圈**，这意味着第一个房屋和最后一个房屋是紧挨着的。同时，相邻的房屋装有相互连通的防盗系统，**如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警**。

给定一个代表每个房屋存放金额的非负整数数组，计算你**在不触动警报装置的情况下**，今晚能够偷窃到的最高金额。

**示例 1：**

```python
输入：nums = [2,3,2]
输出：3
解释：你不能先偷窃 1 号房屋（金额 = 2），然后偷窃 3 号房屋（金额 = 2）, 因为他们是相邻的。
```

[题目链接](https://leetcode.cn/problems/house-robber-ii/)

[文章讲解](https://programmercarl.com/0213.%E6%89%93%E5%AE%B6%E5%8A%AB%E8%88%8DII.html)

## 思路

这道题房屋成环了，成环对我们的约束就是第一间和最后一间不能同时被偷了，仅这一个区别。

所以整体上看：

情况1：我们在偷的时候压根不看首尾房间，不纳入考虑范围

情况2：把首房间纳入考虑范围，不考虑尾房间

情况3：把尾房间纳入考虑范围，不考虑首房间

三种情况选最大，**而情况二 和 情况三 都包含了情况一了，所以只考虑情况二和情况三就可以了**。

每一种情况都对应一个完整版的198.打家劫舍 的代码。

有人可能疑惑为什么不是根据偷没偷首尾房间来分情况讨论呢？ 注意这道题一开始我们就是把`[0,i]`视作考虑范围的。我们从来没有决定过某个房间偷还是不偷，而是从结果上讨论偷了还是没偷。

## 代码实现

```cpp
int rob198(vector<int> &nums, int start, int end) {
    vector<int> dp(nums.size(), 0);
    if (start == end)
        return nums[start];
    dp[start] = nums[start];
    dp[start + 1] = max(nums[start], nums[start + 1]);
    for (int i = start + 2; i <= end; i++) {
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i]);
    }
    return dp[end];
}
int rob(vector<int> &nums) {
    if (nums.size() == 1)
        return nums[0];
    int result1 = rob198(nums, 0, nums.size() - 2);
    int result2 = rob198(nums, 1, nums.size() - 1);
    int result = max(result1, result2);
    return result;
}
```