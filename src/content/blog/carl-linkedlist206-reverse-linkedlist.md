---
title: '代码随想录 链表：206. 翻转链表'
description: '反转一个单链表。示例：输入1->2->3->4->5->NULL，输出5->4->3->2->1->NULL。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 链表
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

力扣题目链接

题意：反转一个单链表。

示例: 输入: 1->2->3->4->5->NULL 输出: 5->4->3->2->1->NULL

## 思路

改变链表中节点的走向，使链表指向上个节点，怎么做？

我们知道链表的末尾节点的 next 是空指针，那我们先搞一个空指针。然后第一个节点指向它，但是因为是单向列表，第一个节点指向空了之后他就会丢失掉原来指向的第二个节点。所以我们要先记录下来当前节点的下一个节点存起来。这样就出现了两个链表：，这两个链表都在变化。

[1] → nullptr
[2] → [3] → nullptr

注意上面的 tmp 应在循环外就消失。

```cpp
#include <iostream>
struct ListNode
{
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {};
    ListNode(int x) : val(x), next(nullptr) {};
    ListNode(int x, ListNode *p) : val(x), next(p) {};
};

ListNode *reverseList(ListNode *head)
{
    ListNode *pre = nullptr;
    ListNode *cur = head;
    while (cur)
    {
        ListNode *tmp = cur->next; // 存储下个节点
        cur->next = pre; // 改变方向
        pre = cur; // 左指针右移
        cur = tmp; // 右指针右移
    }
    return pre; // 当cur指向null的时候，pre在他前面，自然就是头节点了
}

int main()
{
}
```

### AI 绘图

假设原始链表为`1 -> 2 -> 3 -> nullptr`，目标是将其反转为`3 -> 2 -> 1 -> nullptr`。

### 初始状态

```text
head → [1] → [2] → [3] → nullptr
pre = nullptr
cur = head (指向 1)
```

### 步骤 1：第一次循环

1. 保存 cur->next：tmp = 2（保存 1 的下一个节点）。

1. 反转指针：cur->next = pre（1 的 next 指向 nullptr）。

1. 移动 pre 和 cur：

pre 移动到 1。
cur 移动到 tmp（即 2）。

**图形化结果**：

```text
pre → [1] → nullptr
cur → [2] → [3] → nullptr
```

### 步骤 2：第二次循环

1. 保存 cur->next：tmp = 3（保存 2 的下一个节点）。

1. 反转指针：cur->next = pre（2 的 next 指向 1）。

1. 移动 pre 和 cur：

pre 移动到 2。
cur 移动到 tmp（即 3）。

**图形化结果**：

```text
pre → [2] → [1] → nullptr
cur → [3] → nullptr
```

### 步骤 3：第三次循环

1. 保存 cur->next：tmp = nullptr（保存 3 的下一个节点）。

1. 反转指针：cur->next = pre（3 的 next 指向 2）。

1. 移动 pre 和 cur：

pre 移动到 3。
cur 移动到 tmp（即 nullptr）。

**图形化结果**：

```text
pre → [3] → [2] → [1] → nullptr
cur → nullptr
```

### 循环结束

* cur 为 nullptr，循环终止。

* 返回 pre，即反转后的链表头节点 3。

**最终链表**：

```text
[3] → [2] → [1] → nullptr
```

### 动态演示

```text
初始: 1 → 2 → 3 → nullptr
Step1: 1 → nullptr | pre=1, cur=2
Step2: 2 → 1 → nullptr | pre=2, cur=3
Step3: 3 → 2 → 1 → nullptr | pre=3, cur=nullptr
```

### 关键点总结

1. 指针操作：每次循环只修改当前节点 cur 的 next 指针。

1. 顺序移动：pre 和 cur 像"双指针"一样逐步向后滑动。

1. 终止条件：cur 为 nullptr 时结束。