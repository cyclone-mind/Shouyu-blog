---
title: '所有路径'
description: '给定一个二叉树，返回所有从根节点到叶子节点的路径。说明: 叶子节点是指没有子节点的节点。'
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

给定一个二叉树，返回所有从根节点到叶子节点的路径。

说明: 叶子节点是指没有子节点的节点。

[题目链接](https://leetcode.cn/problems/binary-tree-paths/)

[文章讲解](https://programmercarl.com/0257.%E4%BA%8C%E5%8F%89%E6%A0%91%E7%9A%84%E6%89%80%E6%9C%89%E8%B7%AF%E5%BE%84.html)

## 思考

根节点到叶子节点的路径，先处理根节点，在处理叶子节点，所以前序遍历。

我们会有一个path跟着节点走，每到一个新的节点就把节点值加入到path里面，如果返回就把path的最后一个值删除（这是回溯），如果到了叶子节点，就构造一个字符串，按照要求把path所包含的所有节点串联起来添加到结果列表中。

递归三部曲

1、递归函数

不用返回值，传入根节点和path和result的引用

2、终止条件

叶子节点时终止，并构造字符串并加入到结果中

3、单层递归逻辑

先处理中间节点，即当前遍历到的节点，加入到path中。随后是递归和回溯。当前节点有左子节点，就递归且回溯。右子节点同理

## 代码实现

```cpp
class Solution {
public:
    void traversal(TreeNode* node, vector<string>& result,vector<int>& path){
        path.push_back(node->val);
        if(node->left == nullptr && node->right == nullptr){
            string spath;
            for(auto pa:path){
                spath+= to_string(pa);
                spath+="->";
            }
            spath.pop_back();
            spath.pop_back();
            result.push_back(spath);
            return;
        }
        if(node->left != nullptr){
            traversal(node->left,result,path);
            path.pop_back();
        }
        if(node->right != nullptr){
            traversal(node->right,result,path);
            path.pop_back();
        }

    }
    vector<string> binaryTreePaths(TreeNode* root) {
        vector<string> result;
        vector<int> path;
        traversal(root,result,path);
        return result;
    }
};
```

注意path里面是int，而构造的spath是字符串，int到string要转换一下。