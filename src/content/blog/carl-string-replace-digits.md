---
title: '代码随想录 字符串：替换数字'
description: '给定一个字符串s，它包含小写字母和数字字符，将字符串中的字母字符保持不变，而将每个数字字符替换为number。'
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

# 代码随想录 字符串 卡码 替换数字

**发布日期:** 2025/12/21
**阅读时间:** 1 分钟
**浏览次数:** 1
**标签:** 算法笔记, 字符串, 代码随想录, 数据结构与算法, Leetcode

## 摘要
给定一个字符串 s，它包含小写字母和数字字符，请编写一个函数，将字符串中的字母字符保持不变，而将每个数字字符替换为 number。

## 正文
[题目链接](https://kamacoder.com/problempage.php?pid=1064)

[文章讲解](https://programmercarl.com/kamacoder/0054.%E6%9B%BF%E6%8D%A2%E6%95%B0%E5%AD%97.html)

## 题目描述

给定一个字符串 s，它包含小写字母和数字字符，请编写一个函数，将字符串中的字母字符保持不变，而将每个数字字符替换为 number。

例如，对于输入字符串 "a1b2c3"，函数应该将其转换为 "anumberbnumbercnumber"。

对于输入字符串 "a5b"，函数应该将其转换为 "anumberb"

输入：一个字符串 s,s 仅包含小写字母和数字字符。

输出：打印一个新的字符串，其中每个数字字符都被替换为了 number

样例输入：a1b2c3

样例输出：anumberbnumbercnumber

数据范围：1 <= s.length < 10000。

## 思路

首先应该遍历找到所有数字的个数，然后进行数组（字符数组）扩容，扩容多少倍？因为要去掉数字加上'number'，所以是加上 5*数字的个数。

扩容完成后，遍历到第一个数字后将'number'替换上然后后面所有的字符向后移动 5 位吗？这样就成了 On2 的时间复杂度了，有没有更好的办法？

其实，对于字符串中的移位操作，使用双指针法是常用的做法。

头指针开始指向字符串中的最后移位，依次向前遍历，查找需要替换的数字元素，尾指针负责填充元素（包括需要替换的数字字符和原字母字符。这样保证了替换后的字符串的正确顺序。

### 参考代码

```cpp
#include <string>
#include <iostream>
using namespace std;
int main()
{
    string s;
    while (cin >> s)
    {
        int sleft = s.size() - 1;
        int count = 0;
        for (int i = 0; i < s.size(); i++)
        {
            if (s[i] >= '0' && s[i] <= '9')
            {
                count++;
            }
        }
        s.resize(s.size() + count * 5);
        int sright = s.size() - 1;
        while (sleft >= 0)
        {
            if (s[sleft] >= '0' && s[sleft] <= '9')
            {
                s[sright--] = 'r';
                s[sright--] = 'e';
                s[sright--] = 'b';
                s[sright--] = 'm';
                s[sright--] = 'u';
                s[sright--] = 'n';
            } else {
                s[sright--] = s[sleft];
            }
            sleft--;

        }
        cout << s << endl;
    }
}
```

### Tips

1. 判断数字字符时，需要使用s[sleft] >= '0' && s[sleft] <= '9'，而不是普通数字，即使是关系运算符，也能比较非数字---字符，因为字符的本质是 ASCII 对应的整数，其实比较的是整数。