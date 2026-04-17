---
title: '路径总和'
description: '给你二叉树的根节点 root 和一个表示目标和的整数 targetSum，判断该树中是否存在根节点到叶子节点的路径，这条路径上所有节点值相加等于目标和。'
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

设置一个count跟随节点，记录遍历到该节点时的路径和。使用前序遍历。到达叶子节点时判断此时路径和是否等于目标和。等于则true，不等于则返回false，意味着此时路径不满足要求。

## 递归三部曲

1、递归函数

判断当前节点为根节点的树是否存在**根节点到叶子节点**的路径，这条路径上所有节点值相加等于目标和`targetSum`。返回值为bool。

参数需要传入节点、当前路径和、目标和

2、终止条件

count 去累加然后判断是否等于目标和

如果最后count == 0，同时到了叶子节点的话，说明找到了目标和。

如果遍历到了叶子节点，count不为0，就是没找到。

3、单层递归逻辑

因为终止条件是判断叶子节点，所以递归的过程中就不要让空节点进入递归了。

递归函数是有返回值的，如果递归函数返回true，说明找到了合适的路径，应该立刻返回。

## 代码实现

递归

```cpp
class Solution {
public:
    bool traversal(TreeNode* node, int count,int targetSum) {
        if (node->left == nullptr && node->right == nullptr && count == targetSum) {
            return true;
        }
        if(node->left){
            count+=node->left->val;
            if(traversal(node->left,count,targetSum) == true) return true;
            count-=node->left->val;
        }
        if(node->right){
            count+=node->right->val;
            if(traversal(node->right,count,targetSum) == true) return true;
            count-=node->right->val;
        }
        return false;
    }
    bool hasPathSum(TreeNode* root, int targetSum) {
        if (root == nullptr)
            return false;
        int sum = root->val;
        return traversal(root, sum,targetSum);
    }
};
```

## 拓展

要求输出所有满足条件的路径。比如：

给你二叉树的根节点`root`和一个整数目标和`targetSum`，找出所有**从根节点到叶子节点**路径总和等于给定目标和的路径。

核心思路如下：

1. 初始化与终止条件

当遇到叶子节点（node->left == nullptr && node->right == nullptr）时：

若剩余目标值 count == 0，将当前路径 path 加入结果集 result
否则直接返回（剪枝）

1. 递归遍历子树

对非空子节点：

选择：将子节点值加入 path，更新剩余目标值 count -= child->val
递归：进入子节点继续搜索
回溯：从 path 弹出子节点值，恢复 count（撤销选择）

1. 选择：将子节点值加入 path，更新剩余目标值 count -= child->val

1. 递归：进入子节点继续搜索

1. 回溯：从 path 弹出子节点值，恢复 count（撤销选择）

1. 入口处理

从根节点开始，初始化 path 为根节点值，count = targetSum - root->val

```cpp
class Solution {
public:
    std::vector<std::vector<int>> result;
    std::vector<int> path;
    void traversal(TreeNode* node, int count) {
        if (node->left == nullptr && node->right == nullptr && count == 0) {
            result.push_back(path);
            return;
        }
        if (node->left == nullptr && node->right == nullptr)
            return;
        if (node->left) {
            path.push_back(node->left->val);
            count -= node->left->val;
            traversal(node->left, count);
            count += node->left->val;
            path.pop_back();
        }
        if (node->right) {
            path.push_back(node->right->val);
            count -= node->right->val;
            traversal(node->right, count);
            count += node->right->val;
            path.pop_back();
        }
        return;
    }

    std::vector<std::vector<int>> pathSum(TreeNode* root, int targetSum) {
        result.clear();
        path.clear();
        if (root == nullptr)
            return result;
        int count = targetSum - root->val;
        path.push_back(root->val);
        traversal(root, count);
        return result;
    }
};
```