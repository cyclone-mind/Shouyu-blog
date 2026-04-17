---
title: '两个字符串的删除操作'
description: '给定两个单词，计算使它们相同所需的最少删除操作次数'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 字符串
  - 编辑距离
---

# 两个字符串的删除操作

**发布日期:** 2025/12/21
**阅读时间:** 1 分钟
**标签:** 算法笔记, 动态规划, 算法, 字符串, 编辑距离, Leetcode

## 正文
# 两个字符串的删除操作

## 题目描述

给定两个单词 word1 和 word2，找到使得 word1 和 word2 相同所需的最小步数，每步可以删除任意一个字符串中的一个字符。

示例：

* 输入: "sea", "eat"

* 输出: 2

* 解释: 第一步将 "sea" 变为 "ea" ，第二步将 "eat" 变为 "ea"

[题目链接](https://leetcode.cn/problems/delete-operation-for-two-strings/)

[文章讲解](https://programmercarl.com/0583.%E4%B8%A4%E4%B8%AA%E5%AD%97%E7%AC%A6%E4%B8%B2%E7%9A%84%E5%88%A0%E9%99%A4%E6%93%8D%E4%BD%9C.html)

## 思路

与**不同的子序列**相比，这次两个字符串都可以删除了。那道题求得是出现次数，实际上总长度减去出现次数也就是本题中的操作数了。所以两者实际考的东西是一样的。

## 递归五部曲

### 1、dp 数组及下标含义

`dp[i][j]`：以i-1为结尾的字符串word1，和以j-1位结尾的字符串word2，想要达到相等，所需要删除元素的最少次数。

### 2、递推公式

情况1：当word1[i - 1] 与 word2[j - 1]相同的时候，`dp[i][j] = dp[i - 1][j - 1];`

情况2：当word1[i - 1] 与 word2[j - 1]不同的时候。有三种情况：

* 只要删除word1[i - 1]就能相等，次数就是dp[i - 1][j] + 1

* 只要删除word2[j - 1]就能相等，次数就是dp[i][j - 1] + 1

* 两者都需要删除才能相等，次数就是dp[i - 1][j - 1] +2

* 以上三种情况需要取最小值，因为要求最小操作数嘛

### 3、初始化

需要初始化`dp[i][0] dp[0][j]`.

`dp[i][0]`word1要删到空字符串大小，最少需要操作 i 次。

同理`dp[0][j]`最少是 j 次

### 4、确定遍历顺序

左上方、正上方、正左方推。因此从上到下从左到右

### 5、举例推导

word1:"sea"，word2:"eat"为例，推导dp数组状态图如下：

## 代码实现

```cpp
int minDistance(string word1, string word2) {
    int m = word1.size(), n = word2.size();
    vector<vector<int>> dp(m+1,vector<int>(n+1,0));
    for(int i = 1;i < m+1;i++){
        for(int j = 1;j < n+1;j++){
            if(word1[i - 1] == word2[j - 1]){
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = max(dp[i][j - 1],dp[i - 1][j]);
            }
        }
    }
    return m + n - dp[m][n]*2;
}
```