---
title: '代码随想录 字符串：344. 反转字符串'
description: '编写一个函数，将输入的字符串反转过来。输入字符串以字符数组char[]的形式给出。不要给另外的数组分配额外的空间，必须原地修改输入数组。'
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

[题目链接](https://leetcode.cn/problems/reverse-string/description/)

[文章讲解](https://programmercarl.com/0344.%E5%8F%8D%E8%BD%AC%E5%AD%97%E7%AC%A6%E4%B8%B2.html)

## 题目描述

编写一个函数，其作用是将输入的字符串反转过来。输入字符串以字符数组 char[] 的形式给出。

不要给另外的数组分配额外的空间，你必须原地修改输入数组、使用 O(1) 的额外空间解决这一问题。

你可以假设数组中的所有字符都是 ASCII 码表中的可打印字符。

示例 1：
输入：["h","e","l","l","o"]
输出：["o","l","l","e","h"]

示例 2：
输入：["H","a","n","n","a","h"]
输出：["h","a","n","n","a","H"]

## 思路

该题目使用双指针法，头尾指针交换元素，然后向中间移动即可。

关于是否要使用库函数，要看具体情境，如果你的代码里面只是一小步使用到了库函数，并且你也知道库函数背后的原理是什么， 则可以使用库函数。如果这个库函数能够直接解决你的问题，则不要使用库函数。

对于交换两个元素，可以使用位运算，也可以开辟一个临时内存进行交换，一般是这两种。这里使用位运算。运用了以下性质：

1. a^a = 0;

1. a^0 = a;

1. 异或运算满足结合律

1. 异或运算满足交换律。

这道题比较简单，直接贴代码。

```cpp
#include <iostream>
#include <vector>
using namespace std;

void reverseString(vector<char> &s)
{
    for (int i = 0, j = s.size() - 1; i < j; i++, j--)
    {
        s[i] ^= s[j];
        s[j] ^= s[i];
        s[i] ^= s[j];
    }
}

int main()
{
    vector<char> xx = {'a', 'l', 'e', 'x'};
    reverseString(xx);
    for (char i : xx)
    {
        std::cout << i << " ";
    }
}
```