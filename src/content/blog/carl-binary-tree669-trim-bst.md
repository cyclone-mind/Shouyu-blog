---
title: '代码随想录 二叉树：669. 二叉搜索树的修剪'
description: '给你二叉搜索树的根节点root，同时给定最小边界low和最大边界high。通过修剪二叉搜索树，使得所有节点的值在[low, high]中。'
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

给你二叉搜索树的根节点`root`，同时给定最小边界`low`和最大边界`high`。通过修剪二叉搜索树，使得所有节点的值在`[low, high]`中。修剪树**不应该**改变保留在树中的元素的相对结构 (即，如果没有被移除，原有的父代子代关系都应当保留)。 可以证明，存在**唯一的答案**。

所以结果应当返回修剪好的二叉搜索树的新的根节点。注意，根节点可能会根据给定的边界发生改变。

[题目链接]450

[文章讲解]450

## 思考

题目要求给定根节点和边界，返回修剪后的根节点。

那么对于任意一棵树，若根节点小于左边界，则应该剪去左子树，继续修剪该节点的右子树。若根节点大于左边界，应该剪去右子树，继续修剪左子树。若根节点在边界之中，应该修剪左右两颗子树。

经历三种情况之后，修剪后的树就是满足要求的树

## 递归三部曲

1、确定递归函数返回值和参数

给定根节点和边界，返回修剪后的树的根节点

2、终止条件

空树修剪后还是空树

3、单层递归逻辑

* 若根节点小于左边界，则应该剪去左子树，继续修剪该节点的右子树。返回修剪后的右子树

* 若根节点大于左边界，应该剪去右子树，继续修剪左子树，返回修剪后的左子树。

* 若根节点在边界之中，应该修剪左右两颗子树，返回修剪后的根节点的树。

## 代码实现

```cpp
class Solution {
public:
    TreeNode* trimBST(TreeNode* root, int low, int high) {
        if(root == nullptr)  return nullptr;
        if(root->val < low) return trimBST(root->right,low,high);
        if(root->val > high) return trimBST(root->left,low,high);
        root->left = trimBST(root->left,low,high);
        root->right = trimBST(root->right,low,high);
        return root;
    }
};
```