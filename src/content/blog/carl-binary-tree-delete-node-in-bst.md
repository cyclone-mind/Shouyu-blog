---
title: '二叉搜索树的删除'
description: '给定一个二叉搜索树的根节点 root 和一个值 key，删除二叉搜索树中的 key 对应的节点，并保证二叉搜索树的性质不变。'
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

给定一个二叉搜索树的根节点**root**和一个值**key**，删除二叉搜索树中的**key**对应的节点，并保证二叉搜索树的性质不变。返回二叉搜索树（有可能被更新）的根节点的引用。

一般来说，删除节点可分为两个步骤：

1. 首先找到需要删除的节点；

1. 如果找到了，删除它。

[题目链接]450

[文章讲解]450

## 思考

题目要求给定根节点和key，返回删除key之后的二叉搜索树的根节点。

遍历节点，节点可能有几种情况：

* 节点为 nullptr 对于空的二叉搜索树，删除key之后的二叉搜索树仍然是nullptr

* 节点值等于key，即找到目标节点。往下分有几种情况

节点是叶子节点，直接返回nullptr，即对于这颗只有一个节点的二叉搜索树，删除key之后的二叉搜索树是nullptr
节点不是叶子节点，左子树为空，右子树不为空，那么应该删除该节点，返回该节点的右子树
节点不是叶子节点，左子树不为空，右子树为空，那么应该删除该节点，返回该节点的左子树
节点不是叶子节点，左右子树都不为空，需要把左子树接到（转移到）右子树的左下角节点上。做法是设置一个cur节点为该节点的右子树上，然后cur向下移动到左下角，之后移动左子树到cur的左节点，随后删除遍历节点，返回遍历节点的右子树

* 节点是叶子节点，直接返回nullptr，即对于这颗只有一个节点的二叉搜索树，删除key之后的二叉搜索树是nullptr

* 节点不是叶子节点，左子树为空，右子树不为空，那么应该删除该节点，返回该节点的右子树

* 节点不是叶子节点，左子树不为空，右子树为空，那么应该删除该节点，返回该节点的左子树

* 节点不是叶子节点，左右子树都不为空，需要把左子树接到（转移到）右子树的左下角节点上。做法是设置一个cur节点为该节点的右子树上，然后cur向下移动到左下角，之后移动左子树到cur的左节点，随后删除遍历节点，返回遍历节点的右子树

* 节点值大于key，向左递归，节点的左子树设置为左子树删除节点之后的左子树

* 节点值小于key，向右递归，节点的右子树设置为右子树删除节点之后的右子树

返回遍历节点。

## 递归三部曲

1、确定递归函数返回值和参数

给定根节点和key，返回删除key之后的二叉搜索树的根节点

2、终止条件

遇到空返回，即没找到和删除的节点

3、单层递归逻辑

详写遍历节点遇到空节点之外的情况。

返回删除了key之后的根节点。

## 代码实现

```cpp
class Solution {
public:
    TreeNode* deleteNode(TreeNode* root, int key) {
        if (root == nullptr)
            return nullptr;
        if (root->val == key) {
            if (root->left == nullptr && root->right == nullptr) {
                delete root;
                return nullptr;
            } else if (root->left == nullptr && root->right != nullptr) {
                auto node = root->right;
                delete root;
                return node;
            } else if (root->right == nullptr && root->left != nullptr) {
                auto node = root->left;
                delete root;
                return node;
            } else if (root->left != nullptr && root->right != nullptr) {
                TreeNode* cur = root->right;
                while (cur->left != nullptr) {
                    cur = cur->left;
                }
                cur->left = root->left;
                TreeNode* tmp = root;
                root = root->right;
                delete tmp;
                return root;
            }
        }
        if (root->val > key) {
            root->left =  deleteNode(root->left, key);
        } else if (root->val < key) {
            root->right =  deleteNode(root->right, key);
        } 
        return root;
    }
};
```