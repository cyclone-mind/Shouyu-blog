---
title: '将有序数组转换为二叉搜索树'
description: '给你一个整数数组 nums，其中元素已经按升序排列，请你将其转换为一棵平衡二叉搜索树。'
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

给你一个整数数组`nums`，其中元素已经按**升序**排列，请你将其转换为一棵 平衡 二叉搜索树。

## 思考

之前有学**从中序和后序遍历序列构造二叉树**和**构造最大二叉树**。本质上就是寻找分割点，以分割点作为当前节点，然后递归左区间和右区间。

这道题相对简单一些，想法就是找到这个有序数组的中间节点作为根节点，然后递归

## 递归三部曲

1、确定递归函数返回值和参数

和之前题目类似，优化空间复杂度，递归时可以传递nums范围，而不用每次构造新的nums。传入nums，左边界、右边界。左闭右开。返回构造好的平衡二叉搜索树的根节点

2、终止条件

用来构造的数组越界时，构造不出节点，返回nullptr

3、单层递归逻辑

找到数组的中间值，设为根节点，然后切割数组，随后将根节点的左子树设置为使用切割后的左数组转换而来的平衡二叉搜索树，将根节点的右子树设置为使用切割后的右数组转换而来的平衡二叉搜索树。

返回根节点

## 注意点

本题若使用左闭右闭区间，则终止条件应为`if(left > right) return nullptr;`

若使用左闭右开区间，则应为`if(left >= right) return nullptr;`左闭右开[a,b)，a不能等于b，否则越界。

左闭右闭[a,b] a可以等于b。

因为如果使用左闭右开，但是你写了`if(left > right) return nullptr;`。区间只有一个元素时，mid = 1，left = 0，进入递归后mid会为0，left也是0，再次进入递归后mid和left永远都是0，并且不满足终止条件，会导致无限递归！

## 代码实现

左闭右开

```cpp
class Solution {
public:
    TreeNode* traversal(vector<int>& nums,int left,int right){
        if(left >= right) return nullptr;
        int mid = (left + right) / 2;
        TreeNode* root = new TreeNode(nums[mid]);
        root->left = traversal(nums,left,mid);
        root->right = traversal(nums,mid+1,right);
        return root;
    }

    TreeNode* sortedArrayToBST(vector<int>& nums) {
        return traversal(nums,0,nums.size());
    }
};
```

左闭右闭

```cpp
class Solution {
public:
    TreeNode* traversal(vector<int>& nums,int left,int right){
        if(left > right) return nullptr;
        int mid = (left + right) / 2;
        TreeNode* root = new TreeNode(nums[mid]);
        root->left = traversal(nums,left,mid-1);
        root->right = traversal(nums,mid+1,right);
        return root;
    }

    TreeNode* sortedArrayToBST(vector<int>& nums) {
        return traversal(nums,0,nums.size());
    }
};
```