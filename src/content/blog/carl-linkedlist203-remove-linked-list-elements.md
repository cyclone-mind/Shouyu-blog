---
title: '代码随想录 链表：203. 移除链表元素'
description: '删除链表中等于给定值val的所有节点。'
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

题意：删除链表中等于给定值 val 的所有节点。

示例 1： 输入：head = [1,2,6,3,4,5,6], val = 6 输出：[1,2,3,4,5]

示例 2： 输入：head = [], val = 1 输出：[]

示例 3： 输入：head = [7,7,7,7], val = 7 输出：[]

## 思路

1. 链表中删除某个节点的前提是要找到他之前的那个节点，这很重要。把它之前的那个节点连接到它之后的那个节点，然后删除这个节点即可。

1. 理解了上述思路后会产生一个问题，就是如果你要删除第一个节点怎么办？因为第一个节点没有前一个节点。这时候你可能需要分情况讨论。删除第一个节点就把头节点移到第二个节点，然后删除这个节点即可。我们不分情况，而是采用虚拟头节点的方式。

1. 如果有一个虚拟头节点连接到到已有的头节点，我们就能以统一的方式删除节点了。因为每个节点都有前一个节点了。

1. 还需要知道的是，为了不使头指针丢失，我们创建一个虚拟头节点的副本--》cur 当前节点指针，循环遍历所有节点。值得注意的是不是所有时候 cur 都指向虚拟头节点，因为这道题的 cur->next 可能是头节点，我们才这样使用。

```cpp
// 先定义节点，值得注意的是，leetcode 上C++模式下默认已经实现了，貌似其他链表的题目也是。我们在本地运行需要提前定义好节点。
#include <iostream>

struct ListNode{
	int val;
	ListNode* next;
	ListNode():val(0),next(nullptr){};
	ListNode(int x):val(x),next(nullptr){};
	ListNode(int x, ListNode *next): val(x), next(next){};
};

void removeElements(ListNode *head, int target){
	ListNode *dummhead = new ListNode(); // 虚拟头节点
	ListNode *cur = dummhead; // 当前节点，这是头结点的一个副本，我们使用这个指针遍历
	while(cur->next!=nullptr){ // 我们只能删除cur的下一个节点，因此cur不应该是尾节点
		if(cur->next->val == target){
			ListNode *tmp = cur->next; // 要删除的节点备份一下
			cur->next = cur->next->next; // 删除操作，cur不指向要删除的节点，而是指向要删除的节点的下个节点
			delete tmp; // 释放要删除节点的内存
		}else{
			cur = cur->next; // 遍历操作，当前指针指向下个节点即可，这是遍历链表的基础操作
		}
	}
}

void deleteList(ListNode *head){ // 释放链表，传入一个头节点。操作任何链表都需要从头节点开始操作。
	ListNode *cur = head;
	while (cur != nullptr) // 我们只能删除cur的下一个节点，因此cur不应该是尾节点
	{
		ListNode *tmp = cur;
		cur = cur->next;
		delete tmp;
	}

}



int main(){
	ListNode *head = new ListNode(0);
	ListNode *node1 = new ListNode(1);
	ListNode *node2 = new ListNode(2);
	ListNode *node3 = new ListNode(3);
	head->next = node1;
	node1->next = node2;
	node2->next = node3;
	delete head;
}
```

#### 启发

1. 遍历链表 cur = cur->next;

1. 统一使用虚拟头节点 ListNode *cur = dummhead;