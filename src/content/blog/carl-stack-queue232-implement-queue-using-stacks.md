---
title: '代码随想录 栈与队列：232. 用栈实现队列'
description: '请你仅使用两个栈实现先入先出队列。队列应当支持一般队列支持的所有操作（push、pop、peek、empty）。'
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

# 代码随想录 栈与队列：232. 栈实现队列

**发布日期:** 2025/12/21
**阅读时间:** 1 分钟
**标签:** 算法笔记, 栈和队列, 代码随想录, 数据结构与算法, Leetcode, 栈, 队列

## 摘要
使用两个栈实现先入先出队列

## 正文
## 题目描述

请你仅使用两个栈实现先入先出队列。队列应当支持一般队列支持的所有操作（`push`、`pop`、`peek`、`empty`）：
实现`MyQueue`类：

* void push(int x) 将元素 x 推到队列的末尾

* int pop() 从队列的开头移除并返回元素

* int peek() 返回队列开头的元素

* boolean empty() 如果队列为空，返回 true ；否则，返回 false

[题目链接](https://leetcode.cn/problems/implement-queue-using-stacks/)

[文章讲解](https://programmercarl.com/0232.%E7%94%A8%E6%A0%88%E5%AE%9E%E7%8E%B0%E9%98%9F%E5%88%97.html)

## 思路

这道题配置两个栈，一个输入栈，一个输出栈。整体并不难，主要是把控一些细节点和代码的复用，简化代码。这点十分重要。

类初始化不需要传参数，编译器会自动实现成员变量的初始化。

push 直接向输入栈添加即可。

pop 需要先判断输出栈是否为空，如果为空，需要把输入栈的元素转移到输出栈上来。然后再取出(top)再弹出(pop)，注意 pop 没有返回值。

peek 可以借助 实现好的 pop 方法，**实现代码复用**。先弹出并返回队列的队头元素，再放进去即可。

empty 直接 返回`stIn.empty() && stOut.empty();`即可，不必再搞`if else`。

## 代码实现

```cpp
class MyQueue {
private:
    stack<int> inStack;
    stack<int> outStack;

public:
    MyQueue() {}

    void push(int x) { inStack.push(x); }

    int pop() {
        if (outStack.empty()) {
            while (!inStack.empty()) {
                int num = inStack.top();
                inStack.pop();
                outStack.push(num);
            }
        }
        // 因为题目说明都是有效操作，因此这里不必考虑取不到元素的情况
        int num = outStack.top();
        outStack.pop();
        return num;
    }

    int peek() {
        int num = this->pop();
        outStack.push(num);
        return num;
    }

    bool empty() {
        if (outStack.empty() && inStack.empty()) {
            return true;
        } else {
            return false;
        }
    }
};

/**
 * Your MyQueue object will be instantiated and called as such:
 * MyQueue* obj = new MyQueue();
 * obj->push(x);
 * int param_2 = obj->pop();
 * int param_3 = obj->peek();
 * bool param_4 = obj->empty();
 */
```