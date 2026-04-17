---
title: '代码随想录 链表：140. 环形链表 II'
description: '给定一个链表，返回链表开始入环的第一个节点。如果链表无环，则返回null。'
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


给定一个链表，返回链表开始入环的第一个节点。 如果链表无环，则返回 null。

## 正文
力扣题目链接

[文章讲解](https://programmercarl.com/0142.%E7%8E%AF%E5%BD%A2%E9%93%BE%E8%A1%A8II.html)

## 题目描述

题意： 给定一个链表，返回链表开始入环的第一个节点。 如果链表无环，则返回 null。

为了表示给定链表中的环，使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。

**说明**：不允许修改给定的链表。

**示例 1：**

```text
输入：head = [3,2,0,-4], pos = 1
输出：返回索引为 1 的链表节点
解释：链表中有一个环，其尾部连接到第二个节点。
```

**示例 2：**

```text
输入：head = [1,2], pos = 0
输出：返回索引为 0 的链表节点
解释：链表中有一个环，其尾部连接到第一个节点。
```

**示例 3：**

```text
输入：head = [1], pos = -1
输出：返回 null
解释：链表中没有环。
```

**提示：**

* 链表中节点的数目范围在范围 [0, 104] 内

* -105 <= Node.val <= 105

* pos 的值为 -1 或者链表中的一个有效索引

**进阶：**你是否可以使用`O(1)`空间解决此题？

## 思路

这道题很有意思，如何证明一个环状结构存在？如果链表有环，普通遍历会无限循环，无法判断环的起点。而让两个速度不等的指针遍历，只要他们相遇，就一定存在环状结构。

1. 快慢指针相遇：

* 定义两个指针，fast 每次走两步，slow 每次走一步。

* 如果有环，fast 迟早会追上 slow，在环内相遇。

1. 找到环的入口：

* 相遇后，让一个指针回到链表头，另一个留在相遇点。

* 两个指针都每次走一步，再次相遇的地方就是环的入口。

#### 数学原理（简化版）：

* 设链表头到环入口长度为 a，环入口到相遇点长度为 b，环长度为 c。

* 快指针走的路程是慢指针的两倍，所以有：

a + b + n*c = 2*(a + b)

n 设置 1，推导得：a = c - b

也就是说，从头和从相遇点出发，每次走一步，最终会在环入口相遇。

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

ListNode *detectCycle(ListNode *head) {
    ListNode *fast = head;
    ListNode *slow = head;
    while (fast != nullptr && fast->next != nullptr) // 如果有环一定走里面，拿到返回值，如果无环，就一定有遍历到null，循环就不执行
    {
        fast = fast->next->next;
        slow = slow->next;
        if (fast == slow){
            ListNode *index1 = fast;
            ListNode * index2 = head;
            while (index1!= index2)
            {
                index1 = index1->next;
                index2 = index2->next;
            }
            return index2;
        }
    }
    return NULL;

}

int main(){

}
```