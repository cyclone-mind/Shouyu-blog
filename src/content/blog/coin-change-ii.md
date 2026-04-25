---
title: '零钱兑换II'
description: '完全背包问题变形，计算凑成总金额的硬币组合数'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 完全背包
  - 组合问题
---

## 题目描述

给你一个整数数组`coins`表示不同面额的硬币，另给一个整数`amount`表示总金额。

请你计算并返回可以凑成总金额的硬币组合数。如果任何硬币组合都无法凑出总金额，返回`0`。

假设每一种面额的硬币有无限个。

题目数据保证结果符合 32 位带符号整数。

[题目链接](https://leetcode.cn/problems/coin-change-ii)

[文章讲解](https://programmercarl.com/0518.%E9%9B%B6%E9%92%B1%E5%85%91%E6%8D%A2II.html)

## 思路

总金额为背包容量，不同面额硬币代表物品，无限个代表完全背包，问的是凑成背包的组合数。

并非求凑成背包最大价值。

这道题类似于**目标和**那道题也是问组合数。不过那道题每类物品只有一个属于01背包。

## 递归五部曲

### 1、dp数组及下标含义

定义二维dp数值`dp[i][j]`：使用 下标为`[0, i]`的`coins[i]`能够凑满 j（包括j）这么大容量的包，有`dp[i][j]`种组合方法。

### 2.、递推公式

01背包中二维DP数组的递推公式为：

```cpp
dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - weight[i]] + value[i])
```

完全背包二维DP数组的递推公式为：

```cpp
dp[i][j] = max(dp[i - 1][j], dp[i][j - weight[i]] + value[i])
```

区别在于完全背包是但类物品无限，因此状态 i j 用了本层 i 来推导

**目标和**装满背包的组合数 递推公式：`dp[i][j] = dp[i - 1][j] + dp[i - 1][j - nums[i]]`

本题`dp[i][j] = dp[i-1][j] + dp[i][j - nums[i]]`

### 3、dp数组初始化

第一层，`dp[0][j]`如果 j 可以整除 物品0，那么装满背包就有1种组合方法。

```cpp
for (int j = 0; j <= bagSize; j++) {
    if (j % coins[0] == 0) dp[0][j] = 1;
}
```

最左列，`dp[i][0]`容量为0的背包装满有一种方法：什么都不装。不用考虑重量为0的物品，题目有约束。

### 4、确定遍历顺序

从递推公式上看 i j依赖于上方和正左方，因此先遍历背包，还是先遍历物品都是可以的。只是都必须正序

### 5、举例推导

amount为5，coins为：[2,3,5] 为例

```bash
coin1: 1 1 1 1 1 1 
coin2: 1 1 2 2 3 3 
coin5: 1 1 2 2 3 4
```

## 代码实现

```cpp
int change_2dp(int amount, vector<int> &coins) {
    vector<vector<uint64_t>> dp(coins.size(), vector<uint64_t>(amount + 1, 0));
    for (int i = 0; i < coins.size(); i++) {
        dp[i][0] = 1;
    }
    for (int j = 0; j <= amount; j++) {
        if (j % coins[0] == 0)
            dp[0][j] = 1;
    }
    for (int i = 1; i < coins.size(); i++) {
        for (int j = 0; j <= amount; j++) {
            if (j < coins[i])
                dp[i][j] = dp[i - 1][j];
            else
                dp[i][j] = dp[i - 1][j] + dp[i][j - coins[i]];
        }
    }
    return dp[coins.size() - 1][amount];
}

int change_1dp(int amount, vector<int> &coins) {
    vector<uint64_t> dp(amount + 1, 0);
    dp[0] = 1;
    for(int i = 0;i < coins.size();i++){
        for(int j = coins[i];j <= amount;j++){
            dp[j] += dp[j - coins[i]];
        }
        std::cout << "coin" << coins[i] << ": ";
        for(int zuhe:dp){
            std::cout << zuhe << " ";
        }
        std::cout << std::endl;
    }
    return dp[amount];
}
```