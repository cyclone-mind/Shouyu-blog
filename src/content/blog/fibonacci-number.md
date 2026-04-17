---
title: '斐波那契数'
description: '经典斐波那契数列问题，计算F(n)的值'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 基础DP
  - 递归
---


## 题目描述

斐波那契数，通常用 F(n) 表示，形成的序列称为 斐波那契数列 。该数列由 0 和 1 开始，后面的每一项数字都是前面两项数字的和。也就是： F(0) = 0，F(1) = 1 F(n) = F(n - 1) + F(n - 2)，其中 n > 1 给你n ，请计算 F(n) 。

示例 1：

* 输入：2

* 输出：1

* 解释：F(2) = F(1) + F(0) = 1 + 0 = 1

[题目链接](https://leetcode.cn/problems/fibonacci-number/)

[文章讲解](https://programmercarl.com/0509.%E6%96%90%E6%B3%A2%E9%82%A3%E5%A5%91%E6%95%B0.html)

## 思路

很典型的

```cpp
F(0) = 0，F(1) = 1
F(n) = F(n - 1) + F(n - 2)，其中 n > 1
```

就是递归公式，后一个数由前面的数决定，因此尝试动态规划

#### 五部曲

### 1、确定dp数组以及下标的含义

dp[i] 为第i个斐波那契数

### 2、确定递推公式

题目已给，`F(n) = F(n - 1) + F(n - 2)，其中 n > 1`转化为`dp[i] = dp[i - 1] + dp[i - 2]`

##### 3、p数组如何初始化

观察递归公式，确保数组不越界，那么 i 就要保证大于等于2，所以需要确定i=0和i=1，题目已经给了。`F(0) = 0，F(1) = 1`即`dp[0] = 0,dp[1] = 1`。

### 4、确定遍历顺序

从递推公式可知后一个数由前面两个数决定，所以从前向后遍历。

### 5、举例推导dp数组

打印数组，循环的时候打印就行了

## 代码实现

```cpp
class Solution{
    public:
    inf fib(int N){
        if(N <= 1) return 1;
        vector<int> dp(N+1);
        dp[0] = 0;dp[1] = 1;
        for(int i = 2;i < dp.siz();i++){
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        return dp[N]
    }
}
```

* 时间复杂度：O(n)

* 空间复杂度：O(n)

从递推公式可知只需要维护两个数值就可以了，不用记录整个数列，因此可以使用长度为2的数组或者两个单独int

```cpp
class Solution{
    public:
    inf fib(int N){
        if(N <= 1) return 1;
        vector<int> dp(2);
        dp[0] = 0;dp[1] = 1;
        for(int i = 2;i < N+1;i++){
            int cur_num = dp[0] + dp[1];
            dp[0] = dp[1];
            dp[1] = cur_sum;
        }
        return dp[1];
    }
}
```

#### 递归解法

```cpp
class Solution {
public:
    int fib(int N) {
        if (N < 2) return N;
        return fib(N - 1) + fib(N - 2);
    }
};
```

递归算法的时间复杂度本质上是要看:**递归的次数 * 每次递归中的操作次数**。

每层递归两次，每次递归中进行一次加法操作

* 时间复杂度：O(2^n)

* 空间复杂度：O(n)，递归的深度是n，有n层