---
title: '零钱兑换'
description: '计算凑成总金额所需的最少硬币个数，完全背包问题的应用'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 完全背包
---

## 题目描述

给你一个整数数组`coins`，表示不同面额的硬币；以及一个整数`amount`，表示总金额。

计算并返回可以凑成总金额所需的**最少的硬币个数**。如果没有任何一种硬币组合能组成总金额，返回`-1`。

你可以认为每种硬币的数量是无限的。

**示例 1：**

```text
输入：coins = [1, 2, 5], amount = 11
输出：3 
解释：11 = 5 + 5 + 1
```

[题目链接](https://leetcode.cn/problems/coin-change)

[文章讲解](https://programmercarl.com/0322.%E9%9B%B6%E9%92%B1%E5%85%91%E6%8D%A2.html)

## 思路

和**零钱兑换II**相似，依然是用硬币凑成总金额。单类硬币无限，完全背包。不过那道题是求凑成总金额有多少种方案，多少种组合。而这道题求的是所需要的**最少硬币个数**即最少需要多少物品

## 递归五部曲

### 1、dp数组及下标含义

**dp[j]：凑足总额为j所需钱币的最少个数为dp[j]**

### 2、递推公式

在【0，i】coins 中考虑，凑足总额为 j 钱币最少时有两种情况：

情况1、总金额 j 小于 i，这时 i 根本放不进背包，溢出了。意味着`[0,i] 时dp[j] == [0,i-1]时dp[j]`

情况2、总金额 j 大于等于 i，这时考虑 i 在不在其中。

```text
- 情况2.1 在，那么`dp[j] = dp[j-coins[i]]+1`。这里需要注意，如果`dp[j-coins[i]]`是初始值，意味着`j-coins[i]`金额无法被凑出，既然子问题无解，那么父问题自然不存在，即 j 金额也无法被凑出。这时需要跳过循环，跳过考虑 `coins[i]`
- 情况2.2 不在，那么`dp[j] = dp[j]`，和第一种情况相同
- 情况2.1和2.2之间选个小的
```

### 3、dp数组初始化

从递推公式上看需要设置`dp[0] = 0;`，因为有min函数，因此其他位置取最大的数即可。

### 4、确定遍历顺序

因为并非组合或排列，而是最小个数。所以**钱币有顺序和没有顺序都可以，都不影响钱币的最小个数**。

本题就是**外层for循环遍历物品，内层for遍历背包或者外层for遍历背包，内层for循环遍历物品都是可以的！**

又完全背包，内层循环正序。

### 5、举例推导

coins = [1, 2, 5], amount = 5为例

## 代码实现

```cpp
#include <cstdint>
#include <vector>
using namespace std;

int coinChange(vector<int> &coins, int amount) {
    vector<int> dp(amount + 1, INT32_MAX);
    dp[0] = 0;
    for (int i = 0; i < coins.size(); i++) {
        for (int j = coins[i]; j <= amount; j++) {
            if(dp[j - coins[i]] == INT32_MAX) continue;
            dp[j] = std::min(dp[j], dp[j - coins[i]] + 1);
        }
    }
    if (dp[amount] == INT32_MAX)
        return -1;
    return dp[amount];
}
int main() {}
```