---
title: '代码随想录 栈与队列：150. 逆波兰表达式'
description: '给你一个字符串数组tokens，表示一个根据逆波兰表示法表示的算术表达式。计算该表达式并返回表示表达式值的整数。'
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

## 摘要
给你一个字符串数组tokens，表示一个根据逆波兰表示法表示的算术表达式。

## 正文
## 题目描述

给你一个字符串数组`tokens`，表示一个根据逆波兰表示法表示的算术表达式。 请你计算该表达式。返回一个表示表达式值的整数。
[题目链接](https://leetcode.cn/problems/evaluate-reverse-polish-notation[文章讲解]https://programmercarl.com/0150.%E9%80%86%E6%B3%A2%E5%85%B0%E8%A1%A8%E8%BE%BE%E5%BC%8F%E6%B1%82%E5%80%BC.html)

## 思路

实际上逆波兰表达式对于计算机十分友好，对于表达式人类能够清晰地理解哪部分先计算，哪部分后计算。对于逆波兰表达式，只需要放到栈中一个个取就行了。

遍历数组，遇到操作对象就放入栈中，遇到运算符就取出栈中的前两个元素进行计算，再把结果放回栈中。最后栈只剩下最后一个数，就是所需要的结果。

将`string`转为`int`或`long long`类型，可使用`stoi`和`stoll`。

## 代码实现

```cpp
class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        stack<long long> st;
        for(auto s:tokens){
            if(s == "+" || s == "-" || s== "*" || s== "/"){
                long long num1 = st.top();
                st.pop();
                long long num2 = st.top();
                st.pop();
                long long num;
                if(s == "+") num = num2+num1;
                if(s == "-") num = num2-num1;
                if(s == "*") num = num2*num1;
                if(s == "/") num = num2/num1;
                st.push(num);
            } else {
                st.push(stoll(s));
            }
        }
        return st.top();
    }
};
```