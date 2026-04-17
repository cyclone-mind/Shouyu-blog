---
title: '最大二叉树'
description: '给定一个不重复的整数数组 nums，最大二叉树可以用下面的算法从 nums 递归地构建。'
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

给定一个不重复的整数数组`nums`。**最大二叉树**可以用下面的算法从`nums`递归地构建:

1. 创建一个根节点，其值为 nums 中的最大值。

1. 递归地在最大值 左边 的 子数组前缀上 构建左子树。

1. 递归地在最大值 右边 的 子数组后缀上 构建右子树。

返回`*nums*`*构建的****最大二叉树***。

[题目链接](https://leetcode.cn/problems/maximum-binary-tree)

[文章讲解](https://programmercarl.com/0654.%E6%9C%80%E5%A4%A7%E4%BA%8C%E5%8F%89%E6%A0%91.html)

## 思考

这道题依然是构造树，最大二叉树意味着它要求优先选择最大的元素作为根节点。然后递归地创建左右节点

构造步骤

### 单层递归

在数组中找到最大值，构造这个数组能够构造地树的根节点

根据这个最大值切割数组，得到左右两个数组，分别用来构造左子树和右子树

使用上一步得到的两个数字，递归地构造左右两个子树。

根节点以及左右两个子树都有了之后，就可以返回根节点。

### 终止条件

考虑数组为空时，应该直接返回 空指针，也不用构造节点和左右子树了。

### 函数参数和返回

从以上分析来看，需要数组，返回根节点。

## 优化

和**从中序遍历和后序遍历构造二叉树**一样，没必要在单层递归中切割数组地时候创建一个全新的数组，只需要记录切割后的数组范围，首尾元素在原数组的索引即可

## 代码实现

```cpp
class Solution {
public:
    TreeNode* traversal(vector<int>& nums,int leftIndex,int rightIndex){
        if(rightIndex == leftIndex) return nullptr;
        int maxValue = INT_MIN;
        int maxIndex = leftIndex;
        for(int i = leftIndex;i < rightIndex;i++){
            if(nums[i] > maxValue){
                maxValue = nums[i];
                maxIndex = i;
            }
        }
        TreeNode* root = new TreeNode(maxValue);
        int leftNumsEnd = maxIndex;
        int rightNumsStart = maxIndex+1;
        root->left = traversal(nums,leftIndex,leftNumsEnd);
        root->right = traversal(nums,rightNumsStart,rightIndex);
        return root;
    }
    TreeNode* constructMaximumBinaryTree(vector<int>& nums) {
        if(nums.size() == 0) return nullptr;
        return traversal(nums,0,nums.size());
    }
};
```