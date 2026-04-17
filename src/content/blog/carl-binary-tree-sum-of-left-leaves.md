---
title: '左叶子之和'
description: '给定二叉树的根节点 root，返回所有左叶子之和。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 二叉树
  - 代码随想录
  - 数据结构与算法
---

## 题目描述

给定二叉树的根节点`root`，返回所有左叶子之和。

[题目链接](https://leetcode.cn/problems/sum-of-left-leaves/)

[文章讲解](https://programmercarl.com/0404.%E5%B7%A6%E5%8F%B6%E5%AD%90%E4%B9%8B%E5%92%8C.html)

## 思考

一棵树的左叶子之和等于左子树左叶子之和加右子树左叶子之和。因此使用后序遍历。那叶子节点没有子树，它的左叶子之和就为0。所以遍历到叶子节点就终止，返回0。

左叶子的特点是什么。左叶子没有子节点，且它是父节点的左子节点。

因此如果我们遍历到一个节点，该节点左子节点不为空，且左子节点没有子节点，则它的左子节点就是左叶子。

递归三部曲

1、递归函数

获取任意树的左叶子之和

2、终止条件

遇到叶子节点时终止，其左叶子之和为0。

3、单层递归逻辑

后序遍历，先拿到左子树的左叶子之和，在拿到右子树的左叶子之和。相加便是该树的左叶子之和。

但是需要考虑特殊情况。如

以 20 节点为根节点的树，左右子树都是叶子节点，那么这棵树左叶子之和为0吗？显然不是，应该为15。

所以我们需要拿到左子树左叶子之和后，需要判断一下这种情况，即该节点左子节点不为空，且左子节点没有子节点，则它的左子节点就是左叶子。

## 代码实现

```cpp
class Solution {
public:
    int sumOfLeftLeaves(TreeNode* root) {
        if(root->left == nullptr && root->right == nullptr) return 0;
        int leftvalue = sumOfLeftLeaves(root->left);
        if(root->left!= nullptr && root->left->left == nullptr && root->left->right == nullptr) leftvalue = root->left->val;
        return leftvalue + sumOfLeftLeaves(root->right);
    }
};
```