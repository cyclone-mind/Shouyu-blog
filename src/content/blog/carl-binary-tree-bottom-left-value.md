---
title: '左下角的值'
description: '给定一个二叉树的根节点 root，请找出该二叉树的最底层最左边节点的值。'
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

给定一个二叉树的**根节点**`root`，请找出该二叉树的**最底层 最左边**节点的值。

假设二叉树中至少有一个节点。

[题目链接](https://leetcode.cn/problems/sum-of-left-leaves/)

[文章讲解](https://programmercarl.com/0404.%E5%B7%A6%E5%8F%B6%E5%AD%90%E4%B9%8B%E5%92%8C.html)

## 思考

层序遍历十分简单，不断把 result 设置为每层的最左边(队列中第一个)的值。不断更新这个result。那么最后的result自然是最底层的最左边值。

递归法就稍微有点复杂。

最底层要求我们知道节点的深度，在最大深度时更新节点值。

最左边要求我们第一次遇到最大深度时更新节点值。

## 递归三部曲

1、递归函数

设置两个全局变量，一个记录遍历到此时的最大深度maxDepth ，一个记录此时最大深度的那个节点的值result。每次首先达到最大深度的节点就是最左边的节点。

需要两个参数，当前节点、当前节点的深度。

2、终止条件

遇到叶子节点时终止，统计此时最大深度，记录节点值。第一个达到最大深度的就是最左边的节点。

3、单层递归逻辑

前中后序遍历都可以，因为我们的中没有处理逻辑。只要保证左在右的前面就行了，优先向左递归。

如果优先向右探索，那就是找树右下角的值了。

另外需要及时回溯，因为节点深度随着节点在不断变化。递归需要深度加一，回溯需要深度减一。

## 代码实现

层序遍历

```cpp
class Solution {
public:
    int findBottomLeftValue(TreeNode* root) {
        int result = 0;
        queue<TreeNode*> que;
        que.push(root);
        while(!que.empty()){
            int size = que.size();
            for(int i = 0;i < size;i++){
                TreeNode* node = que.front();que.pop();
                if(i == 0) result=node->val;
                if(node->left) que.push(node->left);
                if(node->right) que.push(node->right);
            }
        }
        return result;
    }
};
```

递归前序遍历

```cpp
class Solution {
public:
    int result;
    int maxDepth = INT_MIN;
    void traversal(TreeNode* node, int depth){
        if(node->left == nullptr && node->right == nullptr){
            if(depth > maxDepth){
                maxDepth = depth;
                result = node->val;
            }
            return;
        }
        if(node->left){
            depth++;
            traversal(node->left,depth);
            depth--;
        }
        if(node->right){
            depth++;
            traversal(node->right,depth);
            depth--;
        }
    }
    int findBottomLeftValue(TreeNode* root) {
        traversal(root,1);
        return result;
    }
};
```