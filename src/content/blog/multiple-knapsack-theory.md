---
title: '多重背包理论基础'
description: '有N种物品和一个容量为V的背包。第i种物品最多有Mi件可用，每件耗费的空间是Ci，价值是Wi。求解将哪些物品装入背包可使这些物品的耗费的空间总和不超过背包容量，且价值总和最大。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 背包问题
  - 多重背包
  - 理论基础
---

## 题目描述

有N种物品和一个容量为V 的背包。第i种物品最多有Mi件可用，每件耗费的空间是Ci ，价值是Wi 。求解将哪些物品装入背包可使这些物品的耗费的空间 总和不超过背包容量，且价值总和最大。

每种物品依然是选或不选，但并非无限选，也不是只能选用一次，而是规定了物品的数量，限制了选用次数。

因此可以将物品的数量作为物品的属性。也可以将物品展开。相同物品有多个。

如下图：

背包最大重量为10。

物品为：

```cpp
重量	价值	数量
物品0	1	15	2
物品1	3	20	3
物品2	4	30	2
```

问背包能背的物品最大价值是多少？

将物品展开，和如下情况有区别么？

```cpp
重量	价值	数量
物品0	1	15	1
物品0	1	15	1
物品1	3	20	1
物品1	3	20	1
物品1	3	20	1
物品2	4	30	1
物品2	4	30	1
```

毫无区别，这就转成了一个01背包问题了，且每个物品只用一次。

## 代码实现

```text
// 超时了
#include<iostream>
#include<vector>
using namespace std;
int main() {
    int bagWeight,n;
    cin >> bagWeight >> n;
    vector<int> weight(n, 0); 
    vector<int> value(n, 0);
    vector<int> nums(n, 0);
    for (int i = 0; i < n; i++) cin >> weight[i];
    for (int i = 0; i < n; i++) cin >> value[i];
    for (int i = 0; i < n; i++) cin >> nums[i];    
    
    for (int i = 0; i < n; i++) {
        while (nums[i] > 1) { // 物品数量不是一的，都展开
            weight.push_back(weight[i]);
            value.push_back(value[i]);
            nums[i]--;
        }
    }
 
    vector<int> dp(bagWeight + 1, 0);
    for(int i = 0; i < weight.size(); i++) { // 遍历物品，注意此时的物品数量不是n
        for(int j = bagWeight; j >= weight[i]; j--) { // 遍历背包容量
            dp[j] = max(dp[j], dp[j - weight[i]] + value[i]);
        }
    }
    cout << dp[bagWeight] << endl;
}
```

push_back会导致不断扩容，可以 先把 所有物品数量都计算好，一起申请vector的空间。

也可以把数量作为物品属性，遍历的时候加一层 数量的 for循环即可。

```cpp
for(int i = 0; i < n; i++) { // 遍历物品
        for(int j = bagWeight; j >= weight[i]; j--) { // 遍历背包容量
            // 以上为01背包，然后加一个遍历个数
            for (int k = 1; k <= nums[i] && (j - k * weight[i]) >= 0; k++) { // 遍历个数
                dp[j] = max(dp[j], dp[j - k * weight[i]] + k * value[i]);
            }
        }
    }
```