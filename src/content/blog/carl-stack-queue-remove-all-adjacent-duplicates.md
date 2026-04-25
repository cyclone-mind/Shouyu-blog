---
title: '代码随想录 栈与队列：1047. 删除字符串中所有相邻重复项'
description: '给出由小写字母组成的字符串s，重复项删除操作会选择两个相邻且相同的字母，并删除它们。在反复执行重复项删除操作后返回最终的字符串。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 栈和队列
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

[题目链接](https://leetcode.cn/problems/remove-all-adjacent-duplicates-in-string/description/)

[文章讲解](https://programmercarl.com/1047.%E5%88%A0%E9%99%A4%E5%AD%97%E7%AC%A6%E4%B8%B2%E4%B8%AD%E7%9A%84%E6%89%80%E6%9C%89%E7%9B%B8%E9%82%BB%E9%87%8D%E5%A4%8D%E9%A1%B9.html)

## 题目描述

给出由小写字母组成的字符串`s`，**重复项删除操作**会选择两个相邻且相同的字母，并删除它们。

在`s`上反复执行重复项删除操作，直到无法继续删除。

在完成所有重复项删除操作后返回最终的字符串。答案保证唯一。

**示例：**

```text
输入："abbaca"
输出："ca"
解释：
例如，在 "abbaca" 中，我们可以删除 "bb" 由于两字母相邻且相同，这是此时唯一可以执行删除操作的重复项。之后我们得到字符串 "aaca"，其中又只有 "aa" 可以执行重复项删除操作，所以最后的字符串为 "ca"。
```

**提示**

1. 1 <= s.length <= 105

1. s 仅由小写英文字母组成。

## 思考

重复项是一个匹配项，对匹配项操作是栈的强项。

初始化一个栈，for循环遍历字符串，如果栈为空或栈顶元素与遍历字符不一致，则将其入栈，否则将栈顶元素出栈。最后遍历完成时栈内剩余的元素就是重复项删除后剩余的字符了。

但此时栈内元素还是倒序的，取出组成字符串，然后翻转一下就ok。

本质上，删除相邻重复项的时候，其实就是要知道当前遍历的这个元素，与前一位是不是一样的元素，那么如何记录前面遍历过的元素呢？

栈的目的，就是存放遍历过的元素，当遍历当前的这个元素的时候，去栈里看一下我们是不是遍历过相同数值的相邻元素。然后再去做对应的消除操作。

#### 字符串作为栈

因为栈的本质是一种对一个入口进行增删查操作的数据结构，我们只需要把字符串的末尾定义为栈顶就行，再字符串的末尾实现添加删除查询字符。少了栈的转换，空间复杂度变为O(1）

```cpp
class Solution {
public:
    string removeDuplicates(string S) {
        string result;
        for(char s : S) {
            if(result.empty() || result.back() != s) {
                result.push_back(s);
            }
            else {
                result.pop_back();
            }
        }
        return result;
    }
};
```

#### 二刷

二刷时只是掌握了可以使用栈，写出了如下代码，还是有很多优化的地方。

遍历时有三种情况

1. 当前字符与栈顶字符不相等。push

1. 栈顶没有字符，栈是空的。push

1. 当前字符与栈顶字符相等。pop

```cpp
class Solution {
public:
    string removeDuplicates(string s) {
        stack<char> st;
        for (char c : s) {
            if (st.empty()) {
                st.push(c);
            } else if (c == st.top()) {
                st.pop();
            } else {
                st.push(c); // 可以与前一个 st.push(c) 进行合并，
            }
        }
        string result;
        while (!st.empty()) {
            char c = st.top();
            st.pop();
            result.push_back(c);
        }
        reverse(result.begin(), result.end());
        return result;
    }
};
```