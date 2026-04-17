---
title: '最后一块石头的重量'
description: '最后一块石头的重量算法题解，使用动态规划解决'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 01背包
  - Leetcode
---

## 题目描述

有一堆石头，用整数数组`stones`表示。其中`stones[i]`表示第`i`块石头的重量。

每一回合，从中选出**任意两块石头**，然后将它们一起粉碎。假设石头的重量分别为`x`和`y`，且`x <= y`。那么粉碎的可能结果如下：

* 如果 x == y，那么两块石头都会被完全粉碎；

* 如果 x != y，那么重量为 x 的石头将会完全粉碎，而重量为 y 的石头新重量为 y-x。

最后，**最多只会剩下一块**石头。返回此石头**最小的可能重量**。如果没有石头剩下，就返回`0`。

**示例 1：**

```text
输入：stones = [2,7,4,1,8,1]
输出：1
解释：
组合 2 和 4，得到 2，所以数组转化为 [2,7,1,8,1]，
组合 7 和 8，得到 1，所以数组转化为 [2,1,1,1]，
组合 2 和 1，得到 1，所以数组转化为 [1,1,1]，
组合 1 和 1，得到 0，所以数组转化为 [1]，这就是最优值。
```

[题目链接](https://leetcode.cn/problems/last-stone-weight-ii/)

[文章讲解](https://programmercarl.com/1049.%E6%9C%80%E5%90%8E%E4%B8%80%E5%9D%97%E7%9F%B3%E5%A4%B4%E7%9A%84%E9%87%8D%E9%87%8FII.html)

## 思路

来回选石头，然后消灭。

其实好像就是从这堆石头里面选出总和尽可能相近的两个石头堆。然后看这两个石头堆之间的重量差是多少。

这样看的话，假如我们有第一个石头堆和第二个石头堆，那么每一个石头要么在第一个石头堆，要么在第二个石头堆。

那么其实也是一个决策的过程，来决策每一个石头究竟是在哪一块石头堆。符合决策树模型。

又因为题目只要求返回最小石头重量，是一个最优化的描述。因此，可以用动态规划来解决。

把石头堆总和的二分之一设置为 target，然后问这个 target 大小的背包能够装的石头最大重量是多少？

和上一道题目相同：重量既是重量还是价值。

## 递归五部曲

### 1、dp数组及下标含义

**dp[j]表示容量（这里说容量更形象，其实就是重量）为j的背包，最多可以背最大重量为dp[j]**。

“最多可以装的价值为 dp[j]” 等同于 “最多可以背的重量为dp[j]”

### 2.、递推公式

和上一道题相同

```cpp
dp[j] = max(dp[j],dp[j - stones[i] + stones[i]])
```

### 3、dp数组初始化

背包的容量一般设置为所有的石头可能的最大重量和是多少。

提示中给出1 <= stones.length <= 30，1 <= stones[i] <= 1000，所以最大重量就是30 * 1000 。

因为 target 是最大重量和的一半，所以 dp数组大小设置为 15000 就行了。

因为石头重量不会是负数，而又有max函数，所以 dp[j] 初始化为0就行了。

```cpp
vector(15001,0)
```

### 4、确定遍历顺序

这里一维dp数组，先遍历物品，再遍历背包，并且背包容量是倒序遍历。

```cpp
for(int i = 0;i < stones.size();i++){
    for(int j = target;j >= stones[i];j--){
        dp[j] = max(dp[j],dp[j-stones[i]] + stones[i]);
    }
}
```

### 5、举例推导

输入：[2,4,1,1]，此时target = (2 + 4 + 1 + 1)/2 = 4 ，dp数组状态图如下：

我们得到Target容量的背包最多能装重量 dp[Target]。回到我们的问题，我们的问题可以转化为两个背包容量之间的差别。一个背包容量是 Target，石头重量是 dp[target] 另一堆就是sum-dp[target]。**计算target的时候，target = sum / 2 因为是向下取整，所以sum - dp[target] 一定是大于等于dp[target]的**。

相撞之后剩下的最小石头重量就是 (sum - dp[target]) - dp[target]。

## 代码实现

```cpp
class Solution {
public:
    int lastStoneWeightII(vector<int>& stones) {
        vector<int> dp(15001, 0);
        int sum = 0;
        for (int i = 0; i < stones.size(); i++)
            sum += stones[i];
        int target = sum / 2;
        for (int i = 0; i < stones.size(); i++) {
            for (int j = target; j >= stones[i]; j--) {
                dp[j] = max(dp[j], dp[j - stones[i]] + stones[i]);
            }
        }
        return sum - dp[target] - dp[target];
    }
};
```