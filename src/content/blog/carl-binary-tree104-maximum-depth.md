---
title: '代码随想录 二叉树：104. 最大深度'
description: '给定一个二叉树root，返回其最大深度。二叉树的最大深度是指从根节点到最远叶子节点的最长路径上的节点数。'
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

给定一个二叉树`root`，返回其最大深度。

二叉树的**最大深度**是指从根节点到最远叶子节点的最长路径上的节点数。

[题目链接](https://leetcode.cn/problems/maximum-depth-of-binary-tree)

[文章讲解](https://programmercarl.com/0104.%E4%BA%8C%E5%8F%89%E6%A0%91%E7%9A%84%E6%9C%80%E5%A4%A7%E6%B7%B1%E5%BA%A6.html)

## 思路

二叉树的最大深度实际上是整个树的高度，而要整个树的高度是左子树高度和右子树高度中的最大值 + 1。

实际上任意一棵树，其树高度求取决于左右两个子树。因此是父节点取决于子节点，后序遍历即可求高度。

## 代码实现

```cpp
class Solution {
public:
    int maxDepth(TreeNode* root) {
        if(root == nullptr) return 0;
        int leftDepth = maxDepth(root->left);
        int rightDepth = maxDepth(root->right);
        return max(leftDepth,rightDepth) + 1;
    }
};
```

对于使用前序遍历求深度的思考。

深度是节点的概念，不是树的概念，我们可以说某个节点深度是多少，而树的最大深度就可以理解为最底层的叶子节点的深度，也可以理解为遍历了所有节点后，这其中所有节点中深度的最大值。

那么某个节点的深度取决于谁呢？这就是我们要实现的递归函数要做的事的一部分。

某个节点的深度等于父节点的深度+1

也就是说**该节点信息取决于其父节点**，所以是**中左右**的顺序，前序遍历了！

* 递归函数的参数就是1.某个节点 2.某个节点的深度

* 终止条件为:空节点没有深度的概念，因此我们不要遍历到空节点，不能以看节点作为终止条件。叶子节点不能再向下遍历，因此设置为终止条件。

* 单层递归的逻辑：
​	有了当前节点的深度，先更新最大深度。再左递归，左递归的参数是左节点的当前节点深度+1，递归完之后有回到本层节点，因此回溯到当前节点的深度，以便处理右孩子。

* if (node->left) { depth++; getDepth(node->left, depth); depth--; }: 如果当前节点有左孩子，我们就将深度 depth 加 1，然后递归调用 getDepth 去处理左孩子。当左孩子及其子树处理完毕返回后，我们需要将 depth 减 1，回溯到当前节点的深度，以便处理右孩子。这就像是走迷宫，走进去一步，出来的时候要退回来一步 👣。

* if (node->right) { depth++; getDepth(node->right, depth); depth--; }: 同理，处理右孩子。

## 代码实现 求深度

```cpp
class Solution {
public:
    int result;
    void getdepth(TreeNode* node, int depth) {
        result = depth > result ? depth : result; // 中

        if (node->left == NULL && node->right == NULL) return ;

        if (node->left) { // 左
            depth++;    // 深度+1
            getdepth(node->left, depth);
            depth--;    // 回溯，深度-1
        }
        if (node->right) { // 右
            depth++;    // 深度+1
            getdepth(node->right, depth);
            depth--;    // 回溯，深度-1
        }
        return ;
    }
    int maxDepth(TreeNode* root) {
        result = 0;
        if (root == NULL) return result;
        getdepth(root, 1);
        return result;
    }
};
```