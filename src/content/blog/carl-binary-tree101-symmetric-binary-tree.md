---
title: '101. 对称二叉树'
description: '给你一个二叉树的根节点 root，检查它是否轴对称。'
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

给你一个二叉树的根节点 root ， 检查它是否轴对称。

[题目链接](https://leetcode.cn/problems/symmetric-tree)

[文章讲解](https://programmercarl.com/0101.%E5%AF%B9%E7%A7%B0%E4%BA%8C%E5%8F%89%E6%A0%91.html)

## 思路

轴对称意味着根节点的左右两个子树是镜像的，是可以翻转的。两颗子树的外侧和内侧节点值全部相等。

遍历时要同时遍历两颗树。题目数据中为什么轴对称，因为2-2、3-3、4-4。三个条件都满足了才轴对称。我们可以发现，对于2 这两棵树为什么对称，因为 2 下面对应位置的子树是对称的。

来自题解的解释：

对称二叉树定义： 对于树中 任意两个对称节点`L`和`R`，一定有：

* 值对称：L.val = R.val ：即此两对称节点值相等。

* 子树对称：L.left.val = R.right.val ：即 L 的 左子节点 和 R 的 右子节点 对称。

* 子树对称：L.right.val = R.left.val ：即 L 的 右子节点 和 R 的 左子节点 对称。

可以这么理解，`L`和`R`对称取决于以上三个条件成立。否则都不成立。

对称二叉树的子树对称条件是递归的！要判断当前两个节点是否对称，我们必须先知道它们的子树是否对称。

这种父节点的信息取决于子节点信息的情况就必须使用**后序遍历**！即先处理孩子，再处理自己。

## 代码实现

```cpp
class Solution {
public:
    bool compare(TreeNode* left, TreeNode* right){
        if(left == nullptr && right == nullptr) return true;
        if(left == nullptr || right == nullptr || left->val != right->val) return false;
        return compare(left->left,right->right) && compare(left->right,right->left);
    }
    bool isSymmetric(TreeNode* root) {
        if(root == nullptr) return true;
        return compare(root->left,root->right);
    }
};
```