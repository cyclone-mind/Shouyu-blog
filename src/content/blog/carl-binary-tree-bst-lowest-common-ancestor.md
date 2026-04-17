---
title: '二叉搜索树的最近公共祖先'
description: '给定一个二叉搜索树, 找到该树中两个指定节点的最近公共祖先。'
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

因为是有序树，所以 如果 中间节点是 q 和 p 的公共祖先，那么 中节点的数组 一定是在 [p, q]区间的。即 中节点 > p && 中节点 < q 或者 中节点 > q && 中节点 < p。

那么只要从上到下去遍历，**第一次**遇到 cur节点是数值在[p, q]区间中则一定可以说明该节点cur就是p 和 q的最近公共祖先。

## 递归三部曲

1、递归参数及返回值

在二叉树中会递归到不相关的节点，因此要返回nullptr以及单节点的情况。而二叉搜索树是有序的，只会沿着预定的方向进行，因此只会返回最近公共祖先，不存在其他情况。

2、终止条件

因为题目中说了p、q 为不同节点且均存在于给定的二叉搜索树中。也就是说一定会找到公共祖先的，所以并不存在遇到空的情况。所以不用写。

3、单层递归逻辑

在遍历二叉搜索树的时候就是寻找区间[p->val, q->val]（注意这里是左闭右闭）

那么如果 cur->val 大于 p->val，同时 cur->val 大于q->val，那么就应该向左遍历（说明目标区间在左子树上）。

**需要注意的是此时不知道p和q谁大，所以两个都要判断**。

这道题是搜索某条边，到达条件后立刻返回的写法

```cpp
if (递归函数(root->left)) return ;
if (递归函数(root->right)) return ;
```

搜索整个树写法：

```cpp
left = 递归函数(root->left);
right = 递归函数(root->right);
left与right的逻辑处理;
```

如果 cur->val 小于 p->val，同时 cur->val 小于 q->val，那么就应该向右遍历（目标区间在右子树）。

剩下的情况，就是cur节点在区间（p->val <= cur->val && cur->val <= q->val）或者 （q->val <= cur->val && cur->val <= p->val）中，那么cur就是最近公共祖先了，直接返回cur。

## 代码实现

```cpp
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if(root->val > p->val && root->val > q->val){
            return lowestCommonAncestor(root->left,p,q);
        } else if(root->val < p->val && root->val < q->val){
            return lowestCommonAncestor(root->right,p,q);
        } else {
            return root;
        }
    }
};
```