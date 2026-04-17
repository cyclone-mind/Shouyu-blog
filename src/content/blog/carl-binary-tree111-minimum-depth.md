---
title: '代码随想录 二叉树：111. 最小深度'
description: '给定一个二叉树，找出其最小深度。最小深度是从根节点到最近叶子节点的最短路径上的节点数量。'
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

给定一个二叉树，找出其最小深度。

最小深度是从根节点到最近叶子节点的最短路径上的节点数量。

**说明：叶子节点是指没有子节点的节点**。

[题目链接](https://leetcode.cn/problems/minimum-depth-of-binary-tree)

[文章讲解](https://programmercarl.com/0111.%E4%BA%8C%E5%8F%89%E6%A0%91%E7%9A%84%E6%9C%80%E5%B0%8F%E6%B7%B1%E5%BA%A6.html)

## 思路

深度和高度对应，那么自然，有最小深度就一定有最小高度。

* 二叉树节点的深度：指从根节点到该节点的最长简单路径边的条数或者节点数（取决于深度从0开始还是从1开始）

* 二叉树节点的高度：指从该节点到叶子节点的最长简单路径边的条数或者节点数（取决于高度从0开始还是从1开始）

* 二叉树的最小深度：根节点到任意叶子节点的最短路径上的节点数量。

根节点到**任意叶子节点**的最短路径上的**节点数量**又取决于什么？

取决于：根节点左子节点到其子树中最近叶子节点的路径上的节点数量left 和 根节点右子节点到其子树中最近叶子节点的路径上的节点数量right。这两者之间的最小值+1。

扩展一下，当前节点到**任意叶子节点**的最短路径上的**节点数量**又取决于什么？这是我们的递归函数需要解决的问题

分情况：

1. 当前节点是空节点，结果就是 0；

1. 当前节点的树是单边树时，如左子节点为空，右子节点不为空时，结果就是右子节点到任意叶子节点的最短路径上的节点数量+1 ；

1. 当前节点的左右子节点都不为空，则结果就是 左右子节点到任意叶子节点的最短路径上的节点数量的最小值+1；

一些同学可能会写如下代码：

```cpp
int leftDepth = getDepth(node->left);
int rightDepth = getDepth(node->right);
int result = 1 + min(leftDepth, rightDepth);
return result;
```

这就是没有考虑单边子树的情况。单边子树的话，最小深度应该继承单边子树那边的最小深度

## 代码实现

### 详细注释

```cpp
int getMinDepthFromNode(
    TreeNode
        *node) { // 获取从当前节点开始的最小深度（到最近叶子节点的节点数量）
    if (node == nullptr)
        return 0; // 空节点，路径长度为 0

    // 单层递归逻辑
    int leftPathLength =
        getMinDepthFromNode(node->left); // 左子树的最小路径长度（节点数量）
    int rightPathLength =
        getMinDepthFromNode(node->right); // 右子树的最小路径长度（节点数量）

    // 处理特殊情况：当前节点只有一个子树（即单边子树）
    // 题目定义叶子节点是左右子节点都为空的节点。
    // 如果一个节点只有一个子节点，那么它到最近叶子节点的路径必须经过那个唯一的子节点。
    if (leftPathLength == 0 && rightPathLength != 0) {
        // 左子树为空，右子树不为空，最小深度来自右子树
        return rightPathLength + 1; // 加上当前节点
    }
    if (leftPathLength != 0 && rightPathLength == 0) {
        // 右子树为空，左子树不为空，最小深度来自左子树
        return leftPathLength + 1; // 加上当前节点
    }

    // 处理常规情况：左右子树都存在，或当前节点是叶子节点（左右子树都为空）
    // 此时，选择左右子树中较短的路径，并加上当前节点自身
    int result = 1 + std::min(leftPathLength, rightPathLength);
    return result;
}

int minDepth(TreeNode *root) {
    return getMinDepthFromNode(root); // 调用辅助函数计算根节点的最小深度
}
```

### 代码简化

```cpp
class Solution {
public:
    int minDepth(TreeNode* root) {
        if(root == nullptr) return 0;
        int leftminHeight = minDepth(root->left);
        int rightminHeight = minDepth(root->right);
        if(leftminHeight == 0 && rightminHeight !=0) return rightminHeight+1;
        if(leftminHeight != 0 && rightminHeight == 0) return leftminHeight+1;
        return 1+ min(leftminHeight,rightminHeight);
    }
};
```

#### 二叉树深度与高度概念一览表（包含转化关系）