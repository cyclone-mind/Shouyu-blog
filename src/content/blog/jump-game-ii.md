---
title: '跳跃游戏II'
description: '给定一个非负整数数组，你最初位于数组的第一个位置。你的目标是使用最少的跳跃次数到达数组的最后一个位置。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 贪心
  - 数组
  - 动态规划
  - Leetcode
---

## 题目描述

给定一个非负整数数组，你最初位于数组的第一个位置。

数组中的每个元素代表你在该位置可以跳跃的最大长度。

你的目标是使用最少的跳跃次数到达数组的最后一个位置。

示例:

* 输入: [2,3,1,1,4]

* 输出: 2

* 解释: 跳到最后一个位置的最小跳跃数是 2。从下标为 0 跳到下标为 1 的位置，跳  1 步，然后跳  3 步到达数组的最后一个位置。

说明: 假设你总是可以到达数组的最后一个位置。

[题目链接](https://leetcode.cn/problems/jump-game-ii/)

[文章讲解](https://programmercarl.com/0045.%E8%B7%B3%E8%B7%83%E6%B8%B8%E6%88%8FII.html)

## 思考

### 贪心解法

其实这道题更好理解，当前这一步要跳多远，应该取决于下一跳能跳多源。

以示例：[2,3,1,1,4]说明，从位置0跳到位置1，其下一跳覆盖范围能达到位置4，而从位置0跳到位置2，其下一跳覆盖范围是位置3。

那么我们应该选择下一跳覆盖范围更大的位置跳。

其实这道题我们既没有贪心也在贪心。为什么这么说？

当前这一跳我们其实并没有尽可能地往远跳，我们的目光没有短视，没有只限于这一步。反而是放得长远，放在了下一步上，我们还是尽可能地让下一跳更好，更优，本质还是贪心的思想，只不过贪的不是当前跳，而是下一跳。

## 代码实现

```cpp
int jump(vector<int>& nums){
    if(nums.size() == 1) return 1;
    int ans = 0;
    int curdistance = 0;
    int nextdistance = 0;
    for(int i = 0;i < nums.size();i++){
        nextdistance = nextdistance > (nums[i] + i)? nextdistance : (nums[i] + i);
        if(i == curdistance){
            ans ++;
            curdistance = nextdistance;
            if(nextdistance >= nums.size()-1) break;
        }
    }
    return ans;
}
```