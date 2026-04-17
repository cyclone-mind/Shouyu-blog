---
title: '代码随想录 链表：19. 删除链表的倒数第N个节点'
description: '给你一个链表，删除链表的倒数第n个结点，并且返回链表的头结点。'
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

[题目链接](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/description/)

[文章讲解](https://programmercarl.com/0019.%E5%88%A0%E9%99%A4%E9%93%BE%E8%A1%A8%E7%9A%84%E5%80%92%E6%95%B0%E7%AC%ACN%E4%B8%AA%E8%8A%82%E7%82%B9.html)

题目描述：给你一个链表，删除链表的倒数第`n`个结点，并且返回链表的头结点。

**示例 1：**

```text
输入：head = [1,2,3,4,5], n = 2
输出：[1,2,3,5]
```

**示例 2：**

```text
输入：head = [1], n = 1
输出：[]
```

**示例 3：**

```text
输入：head = [1,2], n = 1
输出：[1]
```

## 思路

1. 对于删除操作统一使用虚拟头节点

1. 删除链表的倒数第 n 个结点，我们首先要找到他的前一个节点。

1. 注意，题目并没有给出链表类，而是给出的原始的由节点连起来的链表，所以是没有长度属性的。那我们最想想到的肯定是先遍历拿到长度 size，然后 cur 右移 size-n 次，遍历到删除节点的前一个结点不就行了？显然暴力解法需要循环两次

1. 一次循环能找到吗？可以使用双指针。快指针先右移动 n+1 次，然后快慢指针同时右移，直到快指针移动到 nullptr，这时慢指针会移动到第 n 个节点的前一个节点，然后删除即可

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

ListNode *removeNthFromEnd(ListNode *head, int n)
{
    ListNode *dummyhead = new ListNode();
    dummyhead->next = head;
    ListNode *fast = dummyhead;
    ListNode *slow = dummyhead;
    n++;        // 让fast先走n+1步
    while (n--) // 通常leetcode上的n设置都是合法的。
    {
        fast = fast->next;
        //   if (fast == nullptr) {
        //     // 通常leetcode上的n设置都是合法的。但是如果n+1大于链表长度，直接返回原链表，防止出现空指针->next的错误
        //     ListNode* res = dummyhead->next;
        //     delete dummyhead;
        //     return res;
        // }
        // fast = fast->next;
    }
    while (fast != nullptr)
    {
        fast = fast->next;
        slow = slow->next;
    }
    ListNode *tmp = slow->next;
    slow->next = tmp->next;
    delete tmp;
    return dummyhead->next; // 注意需要返回虚拟节点的next才是头节点，如果换成head，删除第一个节点是，head就出现了空指针访问的问题了。
}
```

## 易错点

1. fast 要提前走 n+1 步，slow 才能停在待删节点前一个

1. 代码随想录使用的是第二种方法，fast 先走到最后一个真实节点，然后再右移。为什么不能直接移动到尾空指针呢？因为循环的逻辑中使用了 fast = fast->next;，对 fast 进行了解引用，而空指针是不能解引用的，所以在 while 中加入了条件判断 fast != NULL。而方法一也同样存在这个问题，只不过 leetcode 上一般是比较严谨的，可以通过过提交。

1. 删除节点后要记得 delete 掉，防止内存泄漏。dummyhead 也要记得 delete（方法二有做，方法一没做）。

```cpp
/*
 * 方法二：fast先走n步，然后再多走一步
 * 这样slow和fast之间同样保持n+1的距离
 * 这种写法常见于LeetCode讨论区
 */
// ListNode* removeNthFromEnd(ListNode* head, int n) {
//     ListNode* dummyHead = new ListNode(0);
//     dummyHead->next = head;
//     ListNode* slow = dummyHead;
//     ListNode* fast = dummyHead;
//     while(n-- && fast != NULL) { // 这里的判断是先让fast走到最后一个节点，绝对不能走到null，因为下面要fast->next
//         fast = fast->next;
//     }
//     fast = fast->next; // fast再提前走一步
//     while (fast != NULL) {
//         fast = fast->next;
//         slow = slow->next;
//     }
//     ListNode* tmp = slow->next;
//     slow->next = tmp->next;
//     delete tmp;
//     ListNode* newHead = dummyHead->next;
//     delete dummyHead;
//     return newHead;
// }
```