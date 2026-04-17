---
title: '二叉搜索树中的插入'
description: '给定一个二叉搜索树和要插入的值，将值插入二叉搜索树。返回插入后的二叉搜索树的根节点。'
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

给定一个二叉搜索树, 找到该树中两个指定节点的最近公共祖先。

百度百科中最近公共祖先的定义为：“对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（**一个节点也可以是它自己的祖先**）。”

例如，给定如下二叉搜索树: root = [6,2,8,0,4,7,9,null,null,3,5]

## 思考

示例中给了两种插入方式，我们选择第一种。

按照预定的方向遍历，遍历到空节点插入元素即可

## 递归三部曲

1、确定递归函数返回值和参数

返回值是插入值之后的二叉搜索树根节点，参数是二叉搜索树根节点

2、终止条件

遇到空节点时，构造value节点然后返回该节点。即这颗空节点的二叉搜索树就就变成了插入该value值节点的二叉搜索树了

3、递归条件

按照预定方向递归，返回插入值之后的二叉搜索树。

如，遍历节点小于value，那么应该在其右子树上进行插值，将插入该值后的右子树设置为遍历节点的右子树。

最终返回当前遍历节点。

## 代码实现

```cpp
class Solution {
public:
    TreeNode* insertIntoBST(TreeNode* root, int val) {
        if(root == nullptr) {
            TreeNode* node = new TreeNode(val);
            return node;
        } else if(root->val < val){
            root->right = insertIntoBST(root->right,val);
        } else if(root->val > val){
            root->left = insertIntoBST(root->left,val);
        }
        return root;
    }
};
```