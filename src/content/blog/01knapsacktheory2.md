---
title: '01背包理论基础二'
description: '01背包问题的一维dp数组实现，空间优化版本详解。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 背包问题
  - 01背包
  - 空间优化
  - Leetcode
---

## 一维dp数组

因为`dp[i][j]`只依赖于 i -1 层的结果，因此完全没必要用那么多层。使用一层滚动记录即可。

这就是滚动数组的由来，需要满足的条件是上一层可以重复利用，直接拷贝到当前层。

## 思路

### 1、确定dp数组含义

`dp[i][j]`**表示从下标为[0-i]的物品里任意取，放进容量为j的背包，价值总和最大是多少**。

### 2、递推公式

```cpp
dp[j] = max(dp[j],dp[j-weight[i]] + value[i])
```

### 3、初始化

dp数组在推导的时候一定是取价值最大的数，如果题目给的价值都是正整数那么非0下标都初始化为0就可以了。

**这样才能让dp数组在递归公式的过程中取的最大的价值，而不是被初始值覆盖了**。

### 4、遍历顺序

先物品再容量。物品从前到后，容量从大到小

```cpp
for(int i = 0; i < weight.size(); i++) { // 遍历物品
    for(int j = bagWeight; j >= weight[i]; j--) { // 遍历背包容量
        dp[j] = max(dp[j], dp[j - weight[i]] + value[i]);
    }
}
```

为什么？如果容量从小到大：

### 5、举例打印dp数组

### 代码实现

```cpp
#include <iostream>
#include <vector>
int main() {
  int n, bagweight;
  std::cin >> n >> bagweight;
  std::vector<int> weight(n, 0);
  std::vector<int> value(n, 0);
  for (int i = 0; i < n; i++) {
    std::cin >> weight[i];
  }
  for (int j = 0; j < n; j++) {
    std::cin >> value[j];
  }
  std::vector<int> dp(bagweight + 1, 0);

  for (int i = 0; i < n; i++) {
    for (int j = bagweight; j >= weight[i]; j--) {
    dp[j] = std::max(dp[j], dp[j - weight[i]] + value[i]);
    }
  }
  // 输出小明能够携带的研究材料的最大价值
  std::cout << dp[bagweight] << std::endl;
  return 0;
}
```