---
title: '代码随想录 二叉树：226. 翻转二叉树'
description: '给你一棵二叉树的根节点root，翻转这棵二叉树，并返回其根节点。'
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

给你一棵二叉树的根节点`root`，翻转这棵二叉树，并返回其根节点。。

[题目链接](https://leetcode.cn/problems/invert-binary-tree)

[文章讲解](https://programmercarl.com/0226.%E7%BF%BB%E8%BD%AC%E4%BA%8C%E5%8F%89%E6%A0%91.html)

## 思路

翻转整个二叉树就是对每个子树进行翻转，就是对每个节点做左右子节点的交换。

我们需要遍历整个二叉树，遍历到每个节点时交换他们的子节点。

什么遍历顺序？

前序、后序、层序都可以。

## 代码实现

```cpp
class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if(root == nullptr) return nullptr;
        swap(root->left, root->right);
        invertTree(root->left);
        invertTree(root->right);
    }
};
```