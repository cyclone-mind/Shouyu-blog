---
title: '回文子串'
description: '字符串中回文子串的数目算法题解，使用动态规划或双指针法解决'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 字符串
  - 回文
  - Leetcode
---

## 题目描述

给你一个字符串`s`，请你统计并返回这个字符串中**回文子串**的数目。

**回文字符串**是正着读和倒过来读一样的字符串。

**子字符串**是字符串中的由连续字符组成的一个序列。

**示例 1：**

```text
输入：s = "abc"
输出：3
解释：三个回文子串: "a", "b", "c"
```

[题目链接](https://leetcode.cn/problems/palindromic-substrings/)

[文章讲解](https://programmercarl.com/0647.%E5%9B%9E%E6%96%87%E5%AD%90%E4%B8%B2.html)

## 思路

如果做了很多这类的动态规划问题，可能很轻易地就想起来dp定义，`dp[i]`为 [0,i] 字符串中回文子串的数目。

但是可能就想不起来公式如何定义了，好像和`dp[i - 1]`没有递推关系 。

所以我们应该从回文子串数目增长这个角度思考，那么对于一个已经是回文串的字符串，它的数目还能怎么增长呢？

例如对于长度为 5 的字符串 S ，那么如果我们知道 s[1]，s[2]，s[3] 这个子串是回文的，那么只需要比较 s[0]和s[4]这两个元素是否相同，如果相同的话，这个字符串 S 就是回文串。并且字符串 S 中回文字符串的数目也确定了+1。

递推关系：一个字符串（字符串下标范围[i,j]）是否回文，依赖于，子字符串（下标范围[i + 1, j - 1]）） 是否是回文。

这样对于所有的i和j 都有配对关系，都能知道 [i,j] 是否是回文子串，随后统计即可哪些状态 i j 是回文子串即可。

## 递归五部曲

### 1、dp 数组及下标含义

定义：`dp[i][j]`表示**区间范围 [i,j] （注意是左闭右闭）的子串是否是回文子串**，如果是`dp[i][j]`为true，否则为false。

### 2、递推公式

两种情况：

* s[i] != s[j] 那么 直接为false

* s[i] == s[j] 那么有三种情况：

i == j ，这是表示单个字符，所以也是回文子串
i < j 但相差1，就是两个字符，例如 aa 所以也是回文子串
i < j 相差超过1，那么就比较 i+1 与 j-1区间 dp[i - 1][j - 1]是否为true即可

* i == j ，这是表示单个字符，所以也是回文子串

* i < j 但相差1，就是两个字符，例如 aa 所以也是回文子串

* i < j 相差超过1，那么就比较 i+1 与 j-1区间 dp[i - 1][j - 1]是否为true即可

### 3、初始化

我们知道i > j 时 不是回文子串，应为false。

那么 i <= j 时 若s[i] == s[j]，也应为false。

若 s[i] != s[j] ，自然由递推公式决定是否为true，因此也初始化为false，否则递推没有意义。

所以就全部设置为false

### 4、确定遍历顺序

根据递推公式，计算`dp[i][j]`由左下角得来。因此遍历顺序应该从下到上，从左到右

### 5、举例推导

## 代码实现

```cpp
int countSubstrings(string s) {
    vector<vector<bool>> dp(s.size(), vector<bool>(s.size(), false));
    int result = 0;
    for (int i = s.size() - 1; i >= 0; i--) {
        for (int j = i; j < s.size(); j++) {
            if (s[i] == s[j]) {
                if (j - i <= 1) {
                    result++;
                    dp[i][j] = true;
                } else if (dp[i + 1][j - 1]) {
                    result++;
                    dp[i][j] = true;
                }
            }
        }
    }
    return result;
}
```

#### 双指针法

上面思路提到 回文字符串的数目的增加 依赖于 在原回文子串基础上增加字符后的子串满足首尾元素相同。

增加字符在两侧增加可以一次增加一个。

那么我们找到中心，然后向两边扩散看是不是对称的就可以了。

中心点可能是一个也可能是两个。对所有可能的中心都实行一次两侧扩散。

```cpp
int extend(const string& s,int l,int r){
    int count = 0;
    while(l >=0 && r < s.size() && s[l] == s[r]){
        count++;
        l--;
        r++;
    }
    return count;
}
int countSubstrings(string s) {
    int result = 0;
    for(int i = 0;i < s.size();i++){
        result += extend(s,i,i);
        result += extend(s,i,i+1);
    }
    return result;
}
```