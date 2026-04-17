---
title: '右旋'
description: '字符串的右旋转操作'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 字符串
---

## 题目描述

字符串的右旋转操作是把字符串尾部的若干个字符转移到字符串的前面。给定一个字符串 s 和一个正整数 k，请编写一个函数，将字符串中的后面 k 个字符移到字符串的前面，实现字符串的右旋转操作。
例如，对于输入字符串 "abcdefg" 和整数 2，函数应该将其转换为 "fgabcde"。

输入：输入共包含两行，第一行为一个正整数 k，代表右旋转的位数。第二行为字符串 s，代表需要旋转的字符串。
输出：输出共一行，为进行了右旋转操作后的字符串。

[题目链接](https://kamacoder.com/problempage.php?pid=1065)

[文章链接](https://programmercarl.com/kamacoder/0055.%E5%8F%B3%E6%97%8B%E5%AD%97%E7%AC%A6%E4%B8%B2.html)

## 思路

先反转整个字符串，再分别反转前k个字符和后边的部分，实现右移。
反转不是本题的考点，因此直接使用 reverse 库函数。

## 代码实现

```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main(){
    int K;
    string s;
    cin >> K;
    cin >> s;
    reverse(s.begin(),s.end());
    reverse(s.begin(),s.begin() + K);
    reverse(s.begin() + K,s.end());
    cout << s << endl;
}
```