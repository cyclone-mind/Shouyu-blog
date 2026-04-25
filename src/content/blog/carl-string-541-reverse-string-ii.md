---
title: '代码随想录 字符串：541. 反转字符串 II'
description: '给定一个字符串s和一个整数k，从字符串开头算起，每计数至2k个字符，就反转这2k个字符中的前k个字符。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 字符串
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

[题目链接](https://leetcode.cn/problems/reverse-string-ii/description/)

[文章讲解](https://programmercarl.com/0541.%E5%8F%8D%E8%BD%AC%E5%AD%97%E7%AC%A6%E4%B8%B2II.html)

## 题目描述

给定一个字符串 s 和一个整数 k，从字符串开头算起, 每计数至 2k 个字符，就反转这 2k 个字符中的前 k 个字符。

如果剩余字符少于 k 个，则将剩余字符全部反转。

如果剩余字符小于 2k 但大于或等于 k 个，则反转前 k 个字符，其余字符保持原样。

示例:

输入: s = "abcdefg", k = 2
输出: "bacdfeg"

## 思路

该题目依然是反转字符串，但是不同的是，按照一定规律进行翻转，每 2k 个翻转前 k 个。

依然要用到双指针，头指针指向前 k 个中的第一个，尾指针指向前 k 个中的最后一个。当然也可以只用库函数，因为 reverse 只是该解决步骤中的一小步。循环 2k 个即可。需要注意的是 reverse 函数接受的是迭代器，注意用法即可。

```cpp
#include <string>
#include <algorithm>
using namespace std;

string reverseStr(string s, int k)
{
    for (int i = 0; i < s.size(); i += (2 * k)) // 步长位2k
    {
        if (i + k <= s.size()) // 剩余字符小于 2k 但大于或等于 k 个
        {
            reverse(s.begin() + i, s.begin() + i + k);
        }
        else // 剩余字符少于 k 个
        {
            reverse(s.begin() + i, s.end());
        }
    }
    return s;
}
int main(){}
```