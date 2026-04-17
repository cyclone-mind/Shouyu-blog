---
title: '代码随想录 栈与队列：用队列实现栈'
description: '请你仅使用两个队列实现一个后入先出（LIFO）的栈，并支持普通栈的全部四种操作（push、top、pop和empty）。'
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

# 代码随想录 栈与队列：队列实现栈

**发布日期:** 2025/12/21
**阅读时间:** 1 分钟
**标签:** 算法笔记, 栈和队列, 代码随想录, 数据结构与算法, 栈与队列

## 摘要
请你仅使用两个队列实现一个后入先出（LIFO）的栈

## 正文
## 题目描述

请你仅使用两个队列实现一个后入先出（LIFO）的栈，并支持普通栈的全部四种操作（`push`、`top`、`pop`和`empty`）。
实现`MyStack`类：

* void push(int x) 将元素 x 压入栈顶。

* int pop() 移除并返回栈顶元素。

* int top() 返回栈顶元素。

* boolean empty() 如果栈是空的，返回 true ；否则，返回 false 。

[题目链接](https://leetcode.cn/problems/implement-stack-using-queues)

[文章链接]https://programmercarl.com/0225.%E7%94%A8%E9%98%9F%E5%88%97%E5%AE%9E%E7%8E%B0%E6%A0%88.html

## 思路

两个栈可以将 先进后出 改为 先进先出，而两个队列仍然是 先进先出 的顺序，并不能改为 先进后出的顺序。因此本题目可以有华为一个队列实现。

push 直接向队列加。

pop 需要依次将队列中前面的元素 弹出再追加到末尾，然后再把此时的头元素（也就是原来的末尾元素）弹出。  从**队列中取出头元素使用的是**`**front**`**方法**，而非`top`方法，区别于栈。

top 可以借助 已实现的 pop 先弹出并拿到元素，再追加。

empty 判断队列是否为空即可。

## 代码实现

```cpp
class MyStack {
private:
queue<int> que;
public:
    MyStack() {
        
    }
    
    void push(int x) {
        que.push(x);
    }
    
    int pop() {
        int size = que.size();
        size--;
        while(size--){
            que.push(que.front());
            que.pop();
        }
        int num = que.front();
        que.pop();
        return num;
    }
    
    int top() {
        int num = this->pop();
        que.push(num);
        return num;
    }
    
    bool empty() {
        return que.empty();
    }
};

/**
 * Your MyStack object will be instantiated and called as such:
 * MyStack* obj = new MyStack();
 * obj->push(x);
 * int param_2 = obj->pop();
 * int param_3 = obj->top();
 * bool param_4 = obj->empty();
 */
```