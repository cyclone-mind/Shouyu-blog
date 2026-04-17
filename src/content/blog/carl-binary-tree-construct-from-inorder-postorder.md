---
title: '从中序遍历和后序遍历构造二叉树'
description: '给定两个整数数组 inorder 和 postorder ，其中 inorder 是二叉树的中序遍历，postorder 是后序遍历，请你构造二叉树。'
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

给你二叉树的根节点 root 和一个表示目标和的整数 targetSum 。判断该树中是否存在 根节点到叶子节点 的路径，这条路径上所有节点值相加等于目标和 targetSum 。如果存在，返回 true ；否则，返回 false 。

叶子节点 是指没有子节点的节点

[题目链接](https://leetcode.cn/problems/path-sum/)

[文章讲解](https://programmercarl.com/0112.%E8%B7%AF%E5%BE%84%E6%80%BB%E5%92%8C.html)

## 思考

1. 后序遍历的特点：左子树 → 右子树 → 根节点

后序遍历的最后一个元素就是根节点

1. 中序遍历的特点：左子树 → 根节点 → 右子树

找到根节点在中序遍历中的位置，可以将序列分为左右子树

解题思路：

1. 如果数组大小为零的话，说明是空节点了。

2. 如果不为空，那么取后序数组最后一个元素作为节点元素。

3. 找到后序数组最后一个元素在中序数组的位置，作为切割点。

4. 切割中序数组，切成中序左数组和中序右数组。

5. 切割后序数组，切成后序左数组和后序右数组。

6. 递归处理左区间和右区间。

时间复杂度：O(n)，其中 n 是树中节点的个数

利用两种遍历方式的互补特性，通过后序确定根节点，通过中序划分子树，递归地重建整个二叉树结构。

## 易错点

切割数组时尽量使用左闭右开区间，这是STL推荐标准。

如果使用左闭右闭：

当 index 为 0 时（即根节点是中序遍历的第一个元素）：

* inorder.begin()+index-1 = inorder.begin()-1，这会导致迭代器越界

* leftinorder.size()-1 当 leftinorder 为空时，size() 返回 0，0-1 会导致无符号整数下溢，变成一个非常大的数字

* 这个巨大的数字超过了 vector 的最大容量限制，从而抛出 std::length_error

就需要处理这种特殊情况，确实没必要

## 代码实现

```cpp
class Solution {
public:
    TreeNode* traversal(vector<int>& inorder, vector<int>& postorder){
        if(postorder.size() == 0) return nullptr;
        int rootvalue = postorder[postorder.size()-1];
        TreeNode* root = new TreeNode(rootvalue);
        int index;
        for(index = 0;index < inorder.size();index++){
            if(inorder[index] == rootvalue) break;
        }
        vector<int> leftinorder(inorder.begin(),inorder.begin()+index);
        vector<int> rightinorder(inorder.begin()+index+1,inorder.end());
        postorder.resize(postorder.size()-1);
        vector<int> leftpostorder(postorder.begin(),postorder.begin()+leftinorder.size());
        vector<int> rightpostorder(postorder.begin()+leftinorder.size(),postorder.end());

        root->left = traversal(leftinorder,leftpostorder);
        root->right = traversal(rightinorder,rightpostorder);
        return root;
    }

    TreeNode* buildTree(vector<int>& inorder, vector<int>& postorder) {
        return traversal(inorder,postorder);
    }
};
```

## 优化

从上述代码看，每遍历一个节点或者说每构造一个节点就要创建两个数组。非常耗时，其实没必要。我们只需要知道在原数组中对应的范围即可

```cpp
class Solution {
private:
    // 中序区间：[inorderBegin, inorderEnd)，后序区间[postorderBegin, postorderEnd)
    TreeNode* traversal (vector<int>& inorder, int inorderBegin, int inorderEnd, vector<int>& postorder, int postorderBegin, int postorderEnd) {
        if (postorderBegin == postorderEnd) return NULL;

        int rootValue = postorder[postorderEnd - 1];
        TreeNode* root = new TreeNode(rootValue);

        if (postorderEnd - postorderBegin == 1) return root;

        int delimiterIndex;
        for (delimiterIndex = inorderBegin; delimiterIndex < inorderEnd; delimiterIndex++) {
            if (inorder[delimiterIndex] == rootValue) break;
        }
        // 切割中序数组
        // 左中序区间，左闭右开[leftInorderBegin, leftInorderEnd)
        int leftInorderBegin = inorderBegin;
        int leftInorderEnd = delimiterIndex;
        // 右中序区间，左闭右开[rightInorderBegin, rightInorderEnd)
        int rightInorderBegin = delimiterIndex + 1;
        int rightInorderEnd = inorderEnd;

        // 切割后序数组
        // 左后序区间，左闭右开[leftPostorderBegin, leftPostorderEnd)
        int leftPostorderBegin =  postorderBegin;
        int leftPostorderEnd = postorderBegin + delimiterIndex - inorderBegin; // 终止位置是 需要加上 中序区间的大小size
        // 右后序区间，左闭右开[rightPostorderBegin, rightPostorderEnd)
        int rightPostorderBegin = postorderBegin + (delimiterIndex - inorderBegin);
        int rightPostorderEnd = postorderEnd - 1; // 排除最后一个元素，已经作为节点了

        root->left = traversal(inorder, leftInorderBegin, leftInorderEnd,  postorder, leftPostorderBegin, leftPostorderEnd);
        root->right = traversal(inorder, rightInorderBegin, rightInorderEnd, postorder, rightPostorderBegin, rightPostorderEnd);

        return root;
    }
public:
    TreeNode* buildTree(vector<int>& inorder, vector<int>& postorder) {
        if (inorder.size() == 0 || postorder.size() == 0) return NULL;
        // 左闭右开的原则
        return traversal(inorder, 0, inorder.size(), postorder, 0, postorder.size());
    }
};
```