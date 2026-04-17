---
title: '代码随想录 二叉树：700. 二叉搜索树中的搜索'
description: '给定二叉搜索树（BST）的根节点root和一个整数值val，你需要在BST中找到节点值等于val的节点，返回以该节点为根的子树。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 二叉树
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

## 题目描述

给定二叉搜索树（BST）的根节点`root`和一个整数值`val`。

你需要在 BST 中找到节点值等于`val`的节点。 返回以该节点为根的子树。 如果节点不存在，则返回`null`。

**注意**合并过程必须从两个树的根节点开始

[题目链接](https://leetcode.cn/problems/search-in-a-binary-search-tree)

[文章讲解](https://programmercarl.com/0700.%E4%BA%8C%E5%8F%89%E6%90%9C%E7%B4%A2%E6%A0%91%E4%B8%AD%E7%9A%84%E6%90%9C%E7%B4%A2.html)

## 思考

首先想法是遍历每个节点，看看哪个节点的值是val，然后返回这个节点。本题是二叉搜索树，节点是有顺序的，所以我们可以有方向的搜索。

另外考虑终止条件，或者说遍历到的节点可能会出现哪种情况：空节点、目标节点、比目标节点大、比目标节点小。

对于前两种情况，应该直接返回遍历节点。对以后两种，应该进入递归。

另外本题要求返回目标节点子树，有返回值的。进入左右递归的返回值是什么？应该返回的是当前左子树往下搜索的目标节点、或者返回当前右子树往下搜索的目标节点。

## 递归三部曲

1、确定递归函数的参数和返回值

递归函数的参数传入的就是根节点和要搜索的数值，返回的就是以这个搜索数值所在的节点

2、终止条件

如果root为空，或者找到这个数值了，就返回root节点。

3、单层递归逻辑

有方向的去搜索。

如果root->val > val，搜索左子树，如果root->val < val，就搜索右子树，最后如果都没有搜索到，就返回NULL。

## 代码实现

```cpp
class Solution {
public:
    TreeNode* searchBST(TreeNode* root, int val) {
        if (root == nullptr || root->val == val)
            return root;
        TreeNode* result;
        if (val < root->val)
            result = searchBST(root->left, val);
        if (val > root->val)
            result = searchBST(root->right, val);
        return result;
    }
};
```