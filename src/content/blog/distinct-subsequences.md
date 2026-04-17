---
title: '不同的子序列'
description: '统计在字符串s的子序列中t出现的个数'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 字符串
  - 子序列
---

# 不同的子序列

**发布日期:** 2025/12/21
**阅读时间:** 2 分钟
**标签:** 算法笔记, 动态规划, 算法, 字符串, 子序列, Leetcode

## 正文
# 不同的子序列

## 题目描述

给你两个字符串`s`和`t`，统计并返回在`s`的**子序列**中`t`出现的个数。

测试用例保证结果在 32 位有符号整数范围内。

**示例 1：**

```cpp
输入：s = "rabbbit", t = "rabbit"
输出：3
解释：
如下所示, 有 3 种可以从 s 中得到 "rabbit" 的方案。
rabbbit
rabbbit
rabbbit
```

[题目链接](https://leetcode.cn/problems/distinct-subsequences)

[文章讲解](https://programmercarl.com/0115.%E4%B8%8D%E5%90%8C%E7%9A%84%E5%AD%90%E5%BA%8F%E5%88%97.html)

## 思路

并非是 一个字符串的子序列**是否**在另一个字符串中出现过，而是出现的**次数**。

是否出现  可以转化为次数等于字符串长度，而这道题就再用转化了。

## 递归五部曲

### 1、dp 数组及下标含义

`dp[i][j]`：以 i-1为结尾的字符串的子序列 中 出现以j-1为结尾的字符串 t 的个数为`dp[i][j]`。

### 2、递推公式

两种情况：

* s[i - 1] == t[j - 1]

这种情况下 dp[i][j]可以有两种情况：

a) 使用当前字符匹配：dp[i-1][j-1]（表示前i-1和j-1的匹配数）
b) 不使用当前字符匹配：dp[i-1][j]（表示跳过s的当前字符）。这里跳过的意思是

* 这种情况下 dp[i][j]可以有两种情况：

a) 使用当前字符匹配：dp[i-1][j-1]（表示前i-1和j-1的匹配数）
b) 不使用当前字符匹配：dp[i-1][j]（表示跳过s的当前字符）。这里跳过的意思是

* a) 使用当前字符匹配：dp[i-1][j-1]（表示前i-1和j-1的匹配数）

* b) 不使用当前字符匹配：dp[i-1][j]（表示跳过s的当前字符）。这里跳过的意思是

* s[i - 1] != t[i - 1]

只能选择不匹配当前字符：继承dp[i-1][j]

* 只能选择不匹配当前字符：继承dp[i-1][j]

### 3、初始化

递推公式有边界条件，j = 0 和 i = 0 的情况。

那么`dp[0][j] = 0  (j > 0)`，空字符串s不可能含有非空t

`dp[i][0] = 1`，空字符串是任何字符串的子序列。

### 4、确定遍历顺序

从上到下，从左到右

### 5、举例推导

以s："baegg"，t："bag"为例，推导dp数组状态如下：

## 代码实现

```cpp
int numDistinct(string s, string t) {
    vector<vector<unsigned int>> dp(s.size() + 1, vector<unsigned int>(t.size() + 1,0));
    for(int j = 0;j < t.size() + 1;j++) dp[0][j] = 0;
    for(int i = 0;i < s.size() + 1;i++) dp[i][0] = 1;
    for(int i = 1;i < s.size() + 1;i++){
        for(int j = 1;j < t.size() + 1;j++){
            if(s[i - 1] == t[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]; 
            } else {
                dp[i][j] = dp[i - 1][j];
            }
        }
    }
    return dp[s.size()][t.size()]; 
}
```