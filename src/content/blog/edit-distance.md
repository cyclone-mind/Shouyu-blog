---
title: '编辑距离'
description: '计算将word1转换成word2所需的最少操作数，包括插入、删除和替换操作'
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

## 题目描述

给你两个单词 word1 和 word2，请你计算出将 word1 转换成 word2 所使用的最少操作数 。

你可以对一个单词进行如下三种操作：

* 插入一个字符

* 删除一个字符

* 替换一个字符

示例 1：

* 输入：word1 = "horse", word2 = "ros"

* 输出：3

* 解释： horse -> rorse (将 'h' 替换为 'r') rorse -> rose (删除 'r') rose -> ros (删除 'e')

[题目链接](https://leetcode.cn/problems/edit-distance/)

[文章讲解](https://programmercarl.com/0072.%E7%BC%96%E8%BE%91%E8%B7%9D%E7%A6%BB.html)

## 思路

有了之前的经验，判断一个字符串 能否 从另一个字符串转换而来，或者转换而来的所需要的步数，都可以用动态规划。这里的转换不限于子序列、增加和删除等形式。

## 递归五部曲

### 1、dp 数组及下标含义

`dp[i][j]`表示 word1 中由前 i 个字符组成的子串 (word1[0...i-1])转换成 word2 中由前 j 个字符组成的子串 (word2[0...j-1])所用的最少操作数。 数组大小 +1 是因为我们需要包含一个空字符串的状态(即长度为0的子串)。

### 2、递推公式

字符匹配时，继承左上方状态`dp[i - 1][j - 1]`因为匹配不需要操作。

字符不匹配时对应三种情况：

* 替换，word1替换word1[i - 1]，使其与word2[j - 1]相同，此时不用增删加元素。dp[i - 1][j - 1] + 1;

* 删除，word1删除一个元素，那么就是以下标i - 2为结尾的word1 与 j-1为结尾的word2的最近编辑距离 再加上一个操作。dp[i][j] = dp[i - 1][j] + 1; 或者 word2删除一个元素，那么就是以下标i - 1为结尾的word1 与 j-2为结尾的word2的最近编辑距离 再加上一个操作。即 dp[i][j] = dp[i][j-1] = 1

* 添加，word1增加一个元素，使与word2相同，那么这就意味着word2删除一个元素，也可以与word1相同，此时dp[i][j] = dp[i][j-1] = 1 。同理 word2增加，就等同于word1删除dp[i][j] = dp[i - 1][j] + 1;

不匹配时，我们取三种情况中的最小值。

### 3、初始化

任意一个字符串为空时，另一个字符串都需要经过它的长度的删除次数才能变成空。

`dp[i][0] = i dp[0][j] = j`

### 4、确定遍历顺序

左上方，正左方正上方，因此从前往后从上往下遍历

### 5、举例推导

输入：`word1 = "horse", word2 = "ros"`为例，dp矩阵状态图如下：

## 代码实现

```cpp
int minDistance(std::string word1, std::string word2) {
    int m = word1.length();
    int n = word2.length();
    std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1, 0));

    for (int i = 0; i <= m; ++i) {
        dp[i][0] = i;
    }

    for (int j = 0; j <= n; ++j) {
        dp[0][j] = j;
    }

    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (word1[i - 1] == word2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] =
                    std::min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]}) +
                    1;
            }
        }
    }

    // dp[m][n] 存储了 word1 转换为 word2 的最终结果
    return dp[m][n];
}
```