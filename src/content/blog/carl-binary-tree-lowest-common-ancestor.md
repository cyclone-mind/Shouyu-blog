---
title: '二叉树的最近公共祖先'
description: '给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。'
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

给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。

百度百科中最近公共祖先的定义为：“对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（**一个节点也可以是它自己的祖先**）。”

## 思考

遍历每个节点，看看是不是给定的p和q的公共祖先。这个节点应该满足几种情况：

* 如果 p 和 q 分别在某节点的左右子树中，那么这个节点就是最近公共祖先

* 如果 p 和 q 都在左子树，那么左子树会返回它们的最近公共祖先

* 如果 p 和 q 都在右子树，那么右子树会返回它们的最近公共祖先

* 如果 p 是 q 的祖先（或反之），那么在遇到 p 时就会直接返回 p

针对于以上情况

## 递归三部曲

1、递归参数及返回值

递归函数接受一个树，p节点和q节点，返回该树中p节点和q节点的最近公共祖先。如果找到 p 或 q，返回对应节点，如果找到 p 和 q 的最近公共祖先，返回该祖先节点，如果都没找到，返回 nullptr。

2、终止条件

遍历到空节点时，说明该路径上没有目标节点，返回 nullptr

当遍历到p或q中的任意一个，返回该节点（这里包含了 p 是 q 的祖先或 q 是 p 的祖先的情况）

3、单层递归逻辑

递归地在左右子树中找p和q；

这里的判断逻辑是：

* 如果左右子树分别找到了 p 和 q，那么当前节点就是它们的最近公共祖先

* 如果只有一个子树找到了 p 或 q（或它们的公共祖先），则返回该子树的结果

* 如果两个子树都没找到，返回 nullptr

## 代码实现

```cpp
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if(root == nullptr) return nullptr;
        if(root == p || root == q) return root;
        TreeNode* left = lowestCommonAncestor(root->left, p, q);
        TreeNode* right = lowestCommonAncestor(root->right,p, q);
        if(left != nullptr && right == nullptr) {
            return left;
        } else if(right != nullptr && left == nullptr){
            return right;
        } else if (left != nullptr && right != nullptr) {
            return root;
        } else {
            return nullptr;
        }
    }
};
```