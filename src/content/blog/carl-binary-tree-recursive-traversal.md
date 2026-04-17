---
title: '递归遍历'
description: '使用递归法实现二叉树的前序、中序、后序遍历。'
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

[题目链接]

* 144.二叉树的前序遍历

* 145.二叉树的后序遍历

* 94.二叉树的中序遍历

[文章讲解](https://programmercarl.com/%E4%BA%8C%E5%8F%89%E6%A0%91%E7%9A%84%E9%80%92%E5%BD%92%E9%81%8D%E5%8E%86.html)

## 题目描述

给你二叉树的根节点`root`，返回它节点值的**前序**、中序、后序 遍历。

## 思路

得益于二叉树的链表实现，对于这三种遍历，天然适合递归。

前、中、后指的是“中”的位置。

## 递归三要素

1. **确定递归函数的参数和返回值

1. **确定终止条件

1. **确定单层递归的逻辑

题目要求返回的是一个数组，那么一般情况下我们借助辅助函数的形式来对结果数组进行操作。逻辑更清晰。

### 前序遍历 中左右

```cpp
void preorder(TreeNode *node, vector<int> &result) {
  if (node == nullptr) return; // 终止条件
  result.push_back(node->val); // 中
  preorder(node->left, result); // 左
  preorder(node->right, result); // 右
}
vector<int> preorderTraversal(TreeNode *root) {
    vector<int> result;
    preorder(root, result);
    return result; // 迭代法
}
```

### 中序遍历 左中右

```cpp
void inorder(TreeNode *root, std::vector<int> &result){
    if(root == nullptr) return ;
    inorder(root->left,result);
    result.push_back(root->val);
    inorder(root->right, result);
}
std::vector<int> inorderTraversal(TreeNode *root) {
    std::vector<int> result;
    inorder(root, result);
    return  result;
}
```

### 后序遍历 左右中

```cpp
void postorder(TreeNode *root, std::vector<int> &result){
    if(root == nullptr) return ;
    postorder(root->left,result);
    postorder(root->right, result);
    result.push_back(root->val);
}
std::vector<int> postorderTraversal(TreeNode *root) {
    std::vector<int> result;
    postorder(root, result);
    return  result;
}
```

对于迭代法的前中后序遍历，只需要调换访问代码位置即可。