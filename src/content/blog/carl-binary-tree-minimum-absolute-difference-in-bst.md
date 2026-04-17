---
title: '二叉搜索树的最小绝对差'
description: '给你一棵所有节点为非负值的二叉搜索树，请你计算树中任意两节点的差的绝对值的最小值。'
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

给你一棵所有节点为非负值的二叉搜索树，请你计算树中任意两节点的差的绝对值的最小值。
示例：提示：树中至少有 2 个节点。

[题目链接]530

[文章讲解]530

## 思考

在二叉搜索树上求什么最值啊，差值之类的，就把它想成在一个有序数组上求最值，求差值，这样就简单多了。要使用中序遍历记的。

**在一个有序数组上求两个数最小差值，一直计算相邻两元素差值，不断更新，保持最小**

那么可以使用pre指针指向相邻两元素的前一个元素，cur指针指向后一个元素。在树上就是pre为左子节点，cur为中节点。

cur是我们的遍历节点，我们不用手动移动。但是pre作为自指定的节点，必须要手动移动，pre节点记录cur节点的前一个节点。

将pre指定为一个全局变量，每次更新完将pre移动到cur上即可

## 代码实现

```cpp
class Solution {
public:
    int result = INT_MAX;
    TreeNode* pre;
    void traversal(TreeNode* root) {
        if (root == nullptr)
            return;
        traversal(root->left);
        if (pre != nullptr) {
            result =
                result < root->val - pre->val ? result : root->val - pre->val;
        }
        pre = root;
        traversal(root->right);
    }
    int getMinimumDifference(TreeNode* root) {
        traversal(root);
        return result;
    }
};
```
