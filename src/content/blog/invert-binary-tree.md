---
title: '翻转字符串中的单词'
description: '反转字符串中单词的顺序'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 字符串
---

## 题目描述

给你一个字符串`s`，请你反转字符串中**单词**的顺序。**单词**是由非空格字符组成的字符串。`s`中使用至少一个空格将字符串中的**单词**分隔开。
返回**单词**顺序颠倒且**单词**之间用单个空格连接的结果字符串。
**注意**输入字符串`s`中可能会存在前导空格、尾随空格或者单词间的多个空格。返回的结果字符串中，单词间应当仅用单个空格分隔，且不包含任何额外的空格。

[题目链接](https://leetcode.cn/problems/reverse-words-in-a-string/description/)

[文章链接]https://programmercarl.com/0151.%E7%BF%BB%E8%BD%AC%E5%AD%97%E7%AC%A6%E4%B8%B2%E9%87%8C%E7%9A%84%E5%8D%95%E8%AF%8D.html

## 思路

思路是颠倒两次，首先把整个字符串颠倒，再挨个把单个单词颠倒。

题目要求去除前导空格、尾随空格，保留单词之间只有一个空格，所以我们要先对字符串去除额外空格的操作。如果是移除所有空格就简单了，我们在**移除元素**那一节学习了原地去除数组中的元素。但是这道题目还要求我们保留单词之间的空格，因此我们可以采用两种方法：

法一：双指针法，快指针找到一个单词（遍历到第一个不是空格的字符，我们就认为找到了一个单词的开头），然后在它前面（如果不是第一个单词）添加一个空格（填充慢指针实现），然后复制整个单词（快指针填充慢指针实现）。所有多余的空格都被 fast 指针在寻找下一个单词时自然跳过。

```cpp
void removeExtraSpaces(string &s)
{
    int slow = 0; 
    for (int fast = 0; fast < s.size(); fast++) 
    {
        // 核心逻辑：如果快指针遇到了一个非空格字符 (即一个单词的开始)
        if (s[fast] != ' ')
        {
            // 步骤1：在单词前添加一个空格 (如果它不是第一个单词的话)
            // 只有当 slow > 0 时 (说明前面已经有单词被复制了)，才会在当前单词前面添加一个空格。
            // 这确保了单词之间只有一个空格，并且不会在字符串开头添加多余的空格。
            if (slow != 0)
                s[slow++] = ' '; // 写入一个空格，并移动慢指针

            // 步骤2：复制当前单词
            // fast 指针继续前进，逐个字符地将当前单词复制到 slow 指针指向的位置
            while (fast < s.size() && s[fast] != ' ')
            {
                s[slow++] = s[fast++]; // 复制字符，同时移动快慢指针
            }
            // 注意当内层 while 循环结束时，fast 会停在当前单词后面的第一个空格 (或字符串末尾)
            // 外层 for 循环的 fast++ 会进一步将 fast 移动到下一个位置
        }
        // 如果 s[fast] 是空格，那么外层 for 循环会直接跳过这个 if 块，
        // 从而有效地跳过所有连续的空格，直到 fast 再次遇到一个非空格字符 (新单词的开始)。
    }
    // 步骤3：调整字符串大小
    // 循环结束后，slow 指针会指向处理后字符串的有效长度。
    // 使用 resize 截断字符串，移除所有多余的字符 (包括原字符串末尾可能有的多余空格)。
    s.resize(slow);
}
```

法二：双指针法，快指针遇到非空字符，则替换慢指针，如果遇到空字符但是此时慢指针的前一位不是空字符，则填充慢指针（添加空格），但是需要注意如果字符串最后还有一个空格，slow指针会指向空格的下一位，此时resize之前需要使slow-1。

```cpp
void removeExtraSpaces(string& s) {
    int slow = 0; // 慢指针，用于构建新字符串
    for (int fast = 0; fast < s.size(); fast++) {
        // 如果当前字符不是空格，或者当前是空格但前一个字符不是空格（避免连续空格）
        if (s[fast] != ' ') {
            // 处理非空格字符
            s[slow++] = s[fast];
        } else if (slow > 0 && s[slow - 1] != ' ') {
            // 处理第一个空格（避免连续空格）
            s[slow++] = s[fast];
        }
    }
    // 移除末尾可能的多余空格
    if (slow > 0 && s[slow - 1] == ' ') {
        slow--;
    }
    s.resize(slow);
}
```

无论是反转整个字符串还是反转单个单词，我们只需要string，起始位置，结束位置者三个变量即可，因此我们使用自定义的reverse函数。这个和**反转字符串**一样的。

最后就是反转单个单词了，我们需要找到每个单词的起始位置，然后遍历到找到结束位置，反转单词即可，需要注意的是找最后一个单词的结束位置实际是s.size() ，因此定义结束位置的循环条件要为`right <= s.size()`

## 代码实现

```cpp
#include <string>
#include <algorithm>
#include <iostream>
using namespace std;

void removeExtraSpaces(string &s)
{
    int slow = 0; 
    for (int fast = 0; fast < s.size(); fast++) 
    {
        if (s[fast] != ' ')
        {
            if (slow != 0)
                s[slow++] = ' '; 
            while (fast < s.size() && s[fast] != ' ')
            {
                s[slow++] = s[fast++]; // 复制字符，同时移动快慢指针
            }

        }
    }
    s.resize(slow);
}

void reverse(string &s, int start, int end)
{ // 翻转，区间写法：左闭右闭 []
    for (int i = start, j = end; i < j; i++, j--)
    {
        swap(s[i], s[j]);
    }
}

string reverseWords(string s)
{
    removeExtraSpaces(s);
    reverse(s, 0, s.size() - 1);
    int left = 0;
    for (int right = 0; right <= s.size(); right++)
    {
        if (s[right] == ' ' || right == s.size())
        {
            reverse(s, left, right - 1);
            left = right + 1;
        }
    }
    return s;
}

int main()
{
    string s = "  hello   wordddld  ";
    string news = reverseWords(s);
    std::cout << news << std::endl;
}
```