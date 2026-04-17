---
title: '最长公共子序列'
description: '最长公共子序列算法题解，使用动态规划解决'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 字符串
  - 子序列
  - Leetcode
---

## 题目描述

给定两个字符串`text1`和`text2`，返回这两个字符串的最长**公共子序列**的长度。如果不存在**公共子序列**，返回`0`。

一个字符串的**子序列**是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符（也可以不删除任何字符）后组成的新字符串。

* 例如，"ace" 是 "abcde" 的子序列，但 "aec" 不是 "abcde" 的子序列。

两个字符串的**公共子序列**是这两个字符串所共同拥有的子序列。

**示例 1：**

```text
输入：text1 = "abcde", text2 = "ace" 
输出：3  
解释：最长公共子序列是 "ace" ，它的长度为 3 。
```

[题目链接](https://leetcode.cn/problems/longest-common-subsequence/)

[文章讲解](https://programmercarl.com/1143.%E6%9C%80%E9%95%BF%E5%85%AC%E5%85%B1%E5%AD%90%E5%BA%8F%E5%88%97.html)

## 思路

子序列和子数组的区别在于中间元素可以删减。那么仍然是五部曲分析，不过在递推的时候有所不同

## 递归五部曲

### 1、dp 数组及下标含义

`dp[i][j]`：长度为[0, i - 1]的字符串text1与长度为[0, j - 1]的字符串text2的最长公共子序列为`dp[i][j]`

### 2、递推公式

两种情况：

* 情况1：text1[i - 1] 与 text2[j - 1]相同

那么找到了一个公共元素，长度+1  dp[i][j] = dp[i - 1][j - 1] + 1;

* 那么找到了一个公共元素，长度+1  dp[i][j] = dp[i - 1][j - 1] + 1;

* 情况2：text1[i - 1] 与 text2[j - 1]不同

这里和子数组问题不同了，子数组问题是保持为初始值 0 不变。而这道题因为不要求连续，所以可以跳过 i - 1 元素，那么就继续向前看 text1[0, i - 2]与text2[0, j - 1]的最长公共子序列 和 text1[0, i - 1]与text2[0, j - 2]的最长公共子序列，取最大的。

* 这里和子数组问题不同了，子数组问题是保持为初始值 0 不变。而这道题因为不要求连续，所以可以跳过 i - 1 元素，那么就继续向前看 text1[0, i - 2]与text2[0, j - 1]的最长公共子序列 和 text1[0, i - 1]与text2[0, j - 2]的最长公共子序列，取最大的。

```cpp
if (text1[i - 1] == text2[j - 1]) {
    dp[i][j] = dp[i - 1][j - 1] + 1;
} else {
    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
}
```

### 3、初始化

从递推公式上看，需要初始化 i 和 j 为 0 的情况。和上一题一样，初始化为0即可。其余会被覆盖，也一起初始化为0。

### 4、确定遍历顺序

从左边上边和左上方推出`dp[i][j]`因此从左至右从上至下遍历即可。两个个字符串无论谁在外层均可。

### 5、举例推导

输入：text1 = "abcde", text2 = "ace" 为例，dp状态如图：

dp 定义时不要求要以 i j 结尾，因此最后红框`dp[text1.size()][text2.size()]`为最终结果

## 代码实现

```cpp
int longestCommonSubsequence(string text1, string text2) {
    int m = text1.size(), n = text2.size();
    vector<vector<int>> dp(m+1,vector<int>(n+1,0));
    for(int i = 1;i < m+1;i++){
        for(int j = 1;j < n+1;j++){
            if(text1[i - 1] == text2[j - 1]){
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = max(dp[i][j - 1],dp[i - 1][j]);
            }
        }
    }
    return dp[m][n];
}
```