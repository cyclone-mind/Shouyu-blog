---
title: '代码随想录 栈与队列：理论基础'
description: '栈与队列的理论基础，包含栈与队列的特性、STL实现、面试题等内容。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 栈和队列
  - 代码随想录
  - 数据结构与算法
---

## 栈理论基础

4个问题：

* C++中 stack 是容器吗

* 我们使用的 stack 属于哪个版本的 STL

* 我们使用的 STL 中 stack 是如何实现的

* stack 提供迭代器来遍历 stack 空间吗

栈 和 队列 是STL 里面的两种数据结构，是容器。STL 由多个版本，自然栈就有多个版本。
最普遍的STL版本：

1. HP STL 其他版本的C++ STL，一般是以HP STL为蓝本实现出来的，HP STL是C++ STL的第一个实现版本，而且开放源代码。

1. P.J.Plauger STL 由P.J.Plauger参照HP STL实现出来的，被Visual C++编译器所采用，不是开源的。

1. SGI STL 由Silicon Graphics Computer Systems公司参照HP STL实现，被Linux的C++编译器GCC所采用，SGI STL是开源软件，源码可读性甚高。

栈提供 push 和 pop 等接口，符合先进后出原则。不提供走访功能，无法遍历，**没有迭代器**。
只要实现了栈以上的功能，无论底层使用哪种数据结构，都可以被称为栈。
因此 在STL 中，**栈往往不被归类为容器**，而被归类为容器适配器。**我们常用的SGI STL，如果没有指定底层实现的话，默认是以deque为缺省情况下栈的底层结构**