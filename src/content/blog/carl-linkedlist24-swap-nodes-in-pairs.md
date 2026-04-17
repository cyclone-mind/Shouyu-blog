---
title: '代码随想录 链表：24. 两两交换链表中的节点'
description: '给你一个链表，两两交换其中相邻的节点，并返回交换后链表的头节点。必须在不修改节点内部的值的情况下完成本题。'
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

代码随想录链接：https://programmercarl.com/0024.%E4%B8%A4%E4%B8%A4%E4%BA%A4%E6%8D%A2%E9%93%BE%E8%A1%A8%E4%B8%AD%E7%9A%84%E8%8A%82%E7%82%B9.html

题目：给你一个链表，两两交换其中相邻的节点，并返回交换后链表的头节点。你必须在不修改节点内部的值的情况下完成本题（即，只能进行节点交换）。

**示例 1：**

```text
输入：head = [1,2,3,4]
输出：[2,1,4,3]
```

**示例 2：**

```text
输入：head = []
输出：[]
```

**示例 3：**

```text
输入：head = [1]
输出：[1]
```

## 思路

1. 涉及到修改节点的，使用虚拟头节点比较好。

1. 两两交换即改变指向即可，dum->1->2->3 变为 dum->2->1 这样。因为同时需要修改两个节点的指向，所以或许需要定义两个临时指针来记录需要修改的两个节点。

总结一下就是：

1. 引入虚拟头结点（dummyhead）

* 这样可以统一处理头结点和后续节点的交换逻辑，避免头结点特殊处理。

1. 用 cur 指针遍历链表

* cur 指向每一对要交换的前一个节点（初始为 dummyhead）。

1. 每次交换 cur->next 和 cur->next->next

* 用 tmp0、tmp1 分别保存这两个节点，按顺序调整它们的 next 指针。

1. cur 向后移动两位

* 这样可以继续处理下一对节点。

参考代码

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

ListNode* swapPairs(ListNode* head) {
   ListNode *dummyhead = new ListNode();
    dummyhead->next = head;
    ListNode *cur = dummyhead;
    while (cur->next != nullptr && cur->next->next != nullptr) // 为什么是这个条件，因为下面代码有cur->next和cur->next->next的使用，不能出现空指针，从题意上来讲也是cur后面必须是两个实际存在的节点，不能只有一个或一个都没有。如果有一个或没有，就不进行交换
    {
        ListNode *tmp0 = cur->next;          // cur后的第一个节点
        ListNode *tmp1 = cur->next->next;    // cur后的第二个节点

        // 交换 tmp0 和 tmp1
        tmp0->next = tmp1->next;  // 1 -> 3
        tmp1->next = tmp0;        // 2 -> 1
        cur->next = tmp1;         // dummy -> 2

        cur = tmp0;  // 移动到交换后的第二个节点，也就是需要交换的两个节点的前一个节点
    }
    ListNode *result = dummyhead->next; // 为什么是dummyhead->next？因为在第一次交换时cur->next = tmp1;         // dummy -> 2，这导致了dummyhead也跟着指向了2，所以新链表的头指针自然就由dummyhead->next取出了
    delete dummyhead; // 删除虚拟头节
    return result;
}

int main(){

}
```

#### 启发

1. 涉及到修改节点的，统一使用虚拟头节点。

1. 在使用 cur->next 出现在等号右边的时候，也就是要解引用的时候，不能为空指针，题中是在 while 循环中进行了判断。

1. 操作 cur 的后两个节点的指向时，一般先存临时指针，再进行指针的改变是良好的选择；

1. 返回真实头节点时，一定要注意头节点在哪里，一般都是 dummydead->next