---
title: '代码随想录 链表：707. 设计链表'
description: '设计一个链表类，包含初始化对象、获取链表中下标为index的节点的值、在链表第一个元素之前插入一个值为val的节点、追加一个值为val的节点到链表末尾、插入一个值为val的节点到链表下标为index的节点之前、删除下标为index的节点等操作。'
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

题目链接https://leetcode.cn/problems/design-linked-list/description/

文章链接https://programmercarl.com/0707.%E8%AE%BE%E8%AE%A1%E9%93%BE%E8%A1%A8.html#

题目描述 实现`MyLinkedList`类：

* MyLinkedList() 初始化 MyLinkedList 对象。

* int get(int index) 获取链表中下标为 index 的节点的值。如果下标无效，则返回 -1 。

* void addAtHead(int val) 将一个值为 val 的节点插入到链表中第一个元素之前。在插入完成后，新节点会成为链表的第一个节点。

* void addAtTail(int val) 将一个值为 val 的节点追加到链表中作为链表的最后一个元素。

* void addAtIndex(int index, int val) 将一个值为 val 的节点插入到链表中下标为 index 的节点之前。如果 index 等于链表的长度，那么该节点会被追加到链表的末尾。如果 index 比长度更大，该节点将 不会插入 到链表中。

* void deleteAtIndex(int index) 如果下标有效，则删除链表中下标为 index 的节点。

tips

文章中的描述个人有点问题

* get(index)：获取链表中第 index 个节点的值。如果索引无效，则返回-1。

* 原题目描述的是 下标为 index 的节点的值

## 思路

Leercode 中的 C++模式 默认实现了节点结构体，ListNode，你只需要直接使用即可，但是 python 没有。

1. 一个链表类的成员变量应该有一个 size 和 head ，我们初始化一下。

1. int get(int index) 首先判断索引范围，然后将 cur 遍历到 index 这个节点

1. void addAtHead(int val) addAtIndex(0, val)

1. void addAtTail(int val) addAtIndex(size, val);

1. void addAtIndex(int index, int val) 判断索引范围，插入到某个节点之前必须找到它的前一个节点，cur 遍历到前一个节点。

```cpp
class LinkedList
{
private:
    int size;
    ListNode *head;
public:
    MyLinkedList() {
        this->size = 0;
        this->head = new ListNode(0);
    }
    int get(int index) {
        if (index < 0 || index >= size) {
            return -1;
        }
        ListNode *cur = head;
        for (int i = 0; i <= index; i++) {
            cur = cur->next;
        }
        return cur->val;
    }
    void addAtHead(int val) {
        addAtIndex(0, val);
    }
    void addAtTail(int val) {
        addAtIndex(size, val);
    }

    void addAtIndex(int index, int val)
    {
        if (index < 0)
        {
            addAtHead(val);
        }
        if (index > _size)
        {
            return;
        }
        ListNode *newnode = new ListNode(val);
        ListNode *cur = _dummyhead;
        while (index--)
        {
            cur = cur->next;
        }
        newnode->next = cur->next;
        cur->next = newnode;
        _size++;
    }
     void deleteAtIndex(int index)
    {
        if (index > _size || index < 0)
        {
            return;
        }
        ListNode *cur = _dummyhead;
        while (index--)
        {
            cur = cur->next;
        }
        ListNode *tmp = cur->next;
        cur->next = cur->next->next;
        delete tmp;
        tmp = nullptr;
        _size--;
    }

    void printLinkedList()
    {
        ListNode *cur = _dummyhead;
        while (cur->next != nullptr)
        {
            std::cout << cur->next->val << " ";
            cur = cur->next;
        }
        std::cout << std::endl;
    }

};
```

#### 启发

1. 任何时候输入索引，都需要判断索引范围有效性

1. 任何一个链表都只定义 size 和头指针这两个成员属性，这个类实例 实际上不包含后面的节点

1. 插入和删除元素时需要找到需要操作的前一个节点，前一个结点为 遍历节点 cur

1. 查询时 cur 遍历到操作节点即可