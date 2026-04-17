---
title: '平衡二叉树'
description: '给定一个二叉树，判断它是否是平衡二叉树。平衡二叉树是树中任意节点左右子树的高度相差不超过1。'
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

给定一个二叉树，判断它是否是 平衡二叉树

[题目链接](https://leetcode.cn/problems/balanced-binary-tree)

[文章讲解](https://programmercarl.com/0110.%E5%B9%B3%E8%A1%A1%E4%BA%8C%E5%8F%89%E6%A0%91.html)

平衡二叉树是树中任意节点左右子树的高度相差不超过1。

书的高度是根节点的高度，而节点的高度指该节点到叶子节点的**最长简单路径边**的条数，但很显然 leetcode 是按照节点计算。

那么这就简单咯，每个节点都应该满足其左右子树的高度相差不超过1。

因为节点的高度取决于左右两子节点的高度，所以应该采用后序遍历。

递归三部曲

1、递归函数

就是获取节点高度，所以要传入节点。但是我们需要注意的是，如果左右子树已经不是平衡二叉树了，那么自然当前节点的树也不是平衡二叉树了，还返回高度就已经没意义了，因此可以返回-1来标记一下

-1 表示已经不是平衡二叉树了，否则返回值是以该节点为根节点树的高度

2、终止条件

说是终止条件，其实就是考虑所有不同种类的节点可能的返回值，我们这里设置为空节点的高度为0，并直接返回0。

3、单层递归逻辑

验证当前传入节点为根节点的二叉树是否是平衡二叉树，必须根据其左子树高度和其右子树高度的差值。

如果差值大于1，说明不是平衡二叉树，返回-1。如果差值小于等于1，则返回两子树较大的那个并加1

最后将根节点传入该递归函数，就可以获取整棵树的高度或者-1。

## 代码实现

```cpp
class Solution {
public:
    int getheight(TreeNode* node) {
        if(node == nullptr) return 0;
        int leftheight = getheight(node->left);
        if(leftheight == -1) return -1;
        int rightheight = getheight(node->right);
        if(rightheight == -1) return -1;
        int diff = abs(leftheight-rightheight);
        return diff > 1 ? -1 : 1+max(leftheight,rightheight);
    }

    bool isBalanced(TreeNode* root) {
        return getheight(root) == -1 ? false : true;
    }
};
```
