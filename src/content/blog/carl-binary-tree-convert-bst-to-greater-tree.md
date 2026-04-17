---
title: '二叉搜索树转换为累加树'
description: '给出二叉搜索树的根节点，该树的节点值各不相同，请你将其转换为累加树，使每个节点的新值等于原树中大于或等于该节点的值之和。'
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

给出二叉**搜索**树的根节点，该树的节点值各不相同，请你将其转换为累加树（Greater Sum Tree），使每个节点`node`的新值等于原树中大于或等于`node.val`的值之和。

提醒一下，二叉搜索树满足下列约束条件：

* 节点的左子树仅包含键 小于 节点键的节点。

* 节点的右子树仅包含键 大于 节点键的节点。

* 左右子树也必须是二叉搜索树。

[题目链接]538

[文章讲解]538

## 思考

仔细阅读题目要求，其实就是将二叉搜索树以倒序从最后一个数开始累加，类似于后缀和，求这么一个新数组

所以以右中左这个遍历顺序遍历二叉树，右的值加到中节点上，在累加到左节点上。

因此需要使用一个pre指针指向右节点，随着遍历节点向左移而向左移。

## 递归三部曲

1、确定递归函数返回值和参数

给定二叉搜索树根节点，无返回值

2、终止条件

遇到空则返回

3、单层递归逻辑

右中左遍历二叉树，当前节点cur的数值就是cur->val + 前一个节点的数值，我们以pre来替代。累加完当前节点后还需要将pre往左移，使pre = cur

## 代码实现

```cpp
class Solution {
public:
    int pre = 0;
    void traversal(TreeNode* node) {
        if (node == nullptr)
            return;
        traversal(node->right);
        node->val += pre;
        pre = node->val;
        traversal(node->left);
    }

    TreeNode* convertBST(TreeNode* root) {
        traversal(root);
        return root;
    }
};
```