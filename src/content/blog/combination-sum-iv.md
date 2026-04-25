---
title: '组合总和IV'
description: '完全背包求排列数的问题，计算目标和为target的元素组合个数'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 完全背包
  - 排列组合
---

## 题目描述

给你一个由**不同**整数组成的数组`nums`，和一个目标整数`target`。请你从`nums`中找出并返回总和为`target`的元素组合的个数。

题目数据保证答案符合 32 位整数范围。

**示例 1：**

```cpp
输入：nums = [1,2,3], target = 4
输出：7
解释：
所有可能的组合为：
(1, 1, 1, 1)
(1, 1, 2)
(1, 2, 1)
(1, 3)
(2, 1, 1)
(2, 2)
(3, 1)
请注意，顺序不同的序列被视作不同的组合。
```

[题目链接](https://leetcode.cn/problems/combination-sum-iv/)

[文章讲解](https://programmercarl.com/0377.%E7%BB%84%E5%90%88%E6%80%BB%E5%92%8C%E2%85%A3.html)

## 思路

示例1中也别注释了 “顺序不同的序列被视作不同的组合”  摆明了这不是组合而是排列，让我们求排列数。

本质求的是排列总和，而且仅仅是求排列总和的个数，并不是把所有的排列都列出来。因此用不着回溯暴搜把所有排列求出来。

类比成完全背包：target为背包容量，不同整数无限使用为单类物品无限次放入，组合个数为装满有多少种方法，

## 递归五部曲

### 1、dp数组及下标含义

**dp[i]: 凑成目标正整数为i的排列个数为dp[i]**，注意这里并非是只考虑前i个元素，而是0到target所有可能目标金额

### 2.、递推公式

* dp[i] += dp[i - nums[j]]

* 对于每个金额i，遍历所有nums中的数，如果i >= nums[j]，则dp[i] += dp[i-nums[j]]

* 这表示当前组合数等于所有减去当前物品值后的组合数之和

### 3、dp数组初始化

* dp[0] = 1：凑成金额0的组合数为1（即什么都不选）

* 其他位置初始化为0，这样不会影响dp[i]累加所有的dp[i - nums[j]]。

### 4、确定遍历顺序

纯完全背包求最大价值，for循环嵌套的顺序没有要求

**零钱兑换II**完全背包求得是恰好装满得组合数；

而这道题 完全背包求得是恰好装满得排列数；

一个规律是:

**如果求组合数就是外层for循环遍历物品，内层for遍历背包**。

举个例子，先物品后背包，计算dp[4] 的时候，结果集只能是1，3，不会有3，1。因为3在1后面，计算dp[4] 只会考虑前面**一个**元素

**如果求排列数就是外层for遍历背包，内层for循环遍历物品**。

### 5、举例推导

示例中的例子推导一下：

```cpp
容量 0 1 2 3 4 
物品0 1 1 0 0 0 
物品1 1 1 2 0 0 
物品2 1 1 2 4 0 
物品3 1 1 2 4 7
```

## 代码实现

```cpp
#include <cstdint>
#include <vector>
#include <iostream>
using namespace std;
class Solution {
public:
    int combinationSum4(vector<int>& nums, int target) {
        vector<uint64_t> dp(target + 1, 0);
        dp[0] = 1;
        for (int i = 0; i <= target; i++) { // 遍历背包
            for (int j = 0; j < nums.size(); j++) { // 遍历物品
                if (i - nums[j] >= 0 ) {
                    dp[i] += dp[i - nums[j]];
                }
            }
        }
        return dp[target];
    }
};

int main(){
    Solution so;
    vector<int> nums = {1,2,3};
    int target = 4;
    std::cout << "ans::" << so.combinationSum4(nums,target);
}
```