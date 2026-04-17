---
title: '代码随想录 哈希表：383. 赎金信'
description: '给你两个字符串ransomNote和magazine，判断ransomNote能不能由magazine里面的字符构成。如果可以，返回true；否则返回false。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 哈希表
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

[题目链接](https://leetcode.cn/problems/ransom-note/description/)

[文章讲解](https://programmercarl.com/0383.%E8%B5%8E%E9%87%91%E4%BF%A1.html)

## 题目描述

给你两个字符串：`ransomNote`和`magazine`，判断`ransomNote`能不能由`magazine`里面的字符构成。

如果可以，返回`true`；否则返回`false`。

`magazine`中的每个字符只能在`ransomNote`中使用一次。

**示例 1：**

```text
输入：ransomNote = "a", magazine = "b"
输出：false
```

**示例 2：**

```text
输入：ransomNote = "aa", magazine = "ab"
输出：false
```

**示例 3：**

```text
输入：ransomNote = "aa", magazine = "aab"
输出：true
```

**提示：**

* 1 <= ransomNote.length, magazine.length <= 105

* ransomNote 和 magazine 由小写英文字母组成

## 思路

这道题比较简单，将 magazine 转为哈希表，然后遍历 ransomNote，在哈希表对应位置上减 1，如果哈希表有数小于 0，就说明 ransomNote 中的字符在 magazine 已经用光了，出现了存在于 ransomNote 未存在于 magazine 上的情况。

1. 统计 magazine 每个字母出现的次数

​ 用一个长度为 26 的整型数组（nums），下标 025 分别对应 'a''z'。

1. 遍历 ransomNote，消耗 magazine 的字母

​ 每遇到一个字母，就让对应的计数减 1。如果减到小于 0，说明 magazine 里的字母不够用，直接返回 false。

1. 全部遍历完没问题就返回 true。

​ 全小写字母，我们就用 26 长度的数组作为哈希表。

```cpp
class Solution {
public:
    bool canConstruct(string ransomNote, string magazine) {
        if (ransomNote.size() > magazine.size()) // ransomNote长度大于magazine，那么肯定有用超了的情况
            return false;

        int nums[26] = {0};
        for (int i = 0; i < magazine.size(); i++) {
            nums[magazine[i] - 'a']++;
        }
        for (int i = 0; i < ransomNote.size(); i++) {
            nums[ransomNote[i] - 'a']--;
            if (nums[ransomNote[i] - 'a'] < 0) {
                return false;
            }
        }
        return true;
    }
};
```

tip

1. 字符映射到数组下标的理解

很多初学者不熟悉 ch - 'a' 这种技巧，其实就是把 'a''z' 映射到 025。

1. 只用一次的限制

因为要记录字母出现的次数，即 key 为字符，value 为次数，所以要用计数数组而不是 set 或 bool。