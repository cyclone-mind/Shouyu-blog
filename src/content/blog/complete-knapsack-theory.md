---
title: '完全背包理论基础'
description: '完全背包问题理论讲解，与01背包的区别在于每种物品有无限个'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 完全背包
  - 理论基础
---

# 完全背包理论基础

**发布日期:** 2025/12/21
**阅读时间:** 2 分钟
**标签:** 算法笔记, 动态规划, 算法, 背包问题, 完全背包, 理论基础

## 正文
# 完全背包理论基础

## 题目描述

有N件物品和一个最多能背重量为W的背包。第i件物品的重量是weight[i]，得到的价值是value[i] 。**每件物品都有无限个（也就是可以放入背包多次）**，求解将哪些物品装入背包里物品价值总和最大。

**完全背包和01背包问题唯一不同的地方就是，每种物品有无限件**。

[题目链接](https://kamacoder.com/problempage.php?pid=1052)

[文章讲解](https://programmercarl.com/%E8%83%8C%E5%8C%85%E9%97%AE%E9%A2%98%E7%90%86%E8%AE%BA%E5%9F%BA%E7%A1%80%E5%AE%8C%E5%85%A8%E8%83%8C%E5%8C%85.html)

## 思路

思路和 01 背包分析思路基本一致，唯一的区别在于状态转移。

## 递归五部曲

### 1、dp数组及下标含义

`**dp[i][j]**`**表示从下标为[0-i]的物品，每个物品可以取无限次，放进容量为j的背包，价值总和最大是多少**。

### 2.、递推公式

考虑 [0,i] 物品

* 不放物品i：背包容量为j，里面不放物品i的最大价值是dp[i - 1][j]。

* 放物品i：背包空出物品i的容量后，背包容量为j - weight[i]，dp[i][j - weight[i]] 为背包容量为 j - weight[i]且不放物品i的最大价值，那么dp[i][j - weight[i]] + value[i] （物品i的价值），就是背包放物品i得到的最大价值。 关键点在于，如果去掉物品 i，背包里也还可能有其他物品i，

```cpp
dp[i][j] = max(dp[i - 1][j],dp[i][j-weight[i]] + value[i])
```

可以与01背包对比`dp[i][j] = max(dp[i-1][j], dp[i - 1][j - weight[i]] + value[i])`

### 3、dp数组初始化

第一列，如果背包容量j为0的话，即`dp[i][0]`，无论是选取哪些物品，背包价值总和一定为0。

第一行，`dp[0][j]`存放编号为0的物品，各个容量的背包所能存放的最大价值。

那么很明显当`j < weight[0]`的时候，`dp[0][j]`应该是 0，因为背包容量比编号0的物品重量还小。

当`j >= weight[0]`时，`**dp[0][j]**`**如果能放下weight[0]的话，就一直装，每一种物品有无限个**。

```cpp
for(int j = weight[0];j <= bagWeight;j++){
    dp[0][j] = dp[0][j-weight[0]] + value[0]; // 这里是用了动态规划的思想初始化
}
```

其他位置会被逐层覆盖因此初始化什么都行，我们初始化为0。

```cpp
// 初始化 dp
vector<vector<int>> dp(weight.size(), vector<int>(bagweight + 1, 0));
for (int j = weight[0]; j <= bagWeight; j++) {
    dp[0][j] = dp[0][j - weight[0]] + value[0]; 
}
```

### 4、确定遍历顺序

两种遍历顺序，对于二维dp数组来说，递推公式所需要的值，二维dp数组里对应的位置都有。

可以先物品再背包

```cpp
for (int i = 1; i < n; i++) { // 遍历物品
    for(int j = 0; j <= bagWeight; j++) { // 遍历背包容量
        if (j < weight[i]) dp[i][j] = dp[i - 1][j];
        else dp[i][j] = max(dp[i - 1][j], dp[i][j - weight[i]] + value[i]);
    }
}
```

### 5、举例推导

以本篇举例数据为例，填满了dp二维数组如图：

## 代码实现

```cpp
int main() {
    int n, bagWeight;
    std::cin >> n >> bagWeight;
    std::vector<int> weight(n, 0);
    std::vector<int> value(n, 0);
    for (int i = 0; i < n; i++) {
        std::cin >> weight[i] >> value[i];
    }
    std::vector<std::vector<int>> dp(n, std::vector<int>(bagWeight + 1, 0));
    for (int j = weight[0]; j <= bagWeight; j++) {
        dp[0][j] = dp[0][j - weight[0]] + value[0];
    }
    for (int i = 1; i < n; i++) {
        for (int j = 0; j <= bagWeight; j++) {
            if(j < weight[i]) dp[i][j] = dp[i - 1][j];
            else 
            dp[i][j] = std::max(dp[i - 1][j], dp[i][j - weight[i]] + value[i]);
        }
    }
    std::cout << dp[n - 1][bagWeight] << std::endl;
}
```

#### 一维dp

从递推关系上，`dp[i][j]`只依赖上一层，所以可以使用滚动数组。

递推关系：`dp[j] = max(dp[j], dp[j - weight[i]] + value[i])`

我们知道01背包中二维dp数组的两个for遍历的先后循序是可以颠倒；

一维dp数组的两个for循环先后循序一定是先遍历物品，再遍历背包容量。

完全背包中，对于一维dp数组，两个for循环嵌套顺序无所谓。

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
int main(){
    int n,bagWeight;
    std::cin >> n >> bagWeight;
    std::vector<int> weight(n,0);
    std::vector<int> value(n,0);
    for(int i = 0;i < n;i++){
        std::cin >> weight[i] >> value[i];
    }
    std::vector<int> dp(bagWeight + 1,0);
    for(int i = 0;i < n;i++){
        for(int j = weight[i];j <= bagWeight;j++){
            dp[j] = std::max(dp[j],dp[j - weight[i]] + value[i]);
        }
    }
    std::cout << dp.back() << std::endl;
    return 0;
}
```