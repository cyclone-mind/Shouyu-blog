---
title: '二叉搜索树中的众数'
description: '给你一个含重复值的二叉搜索树（BST）的根节点 root，找出并返回 BST 中的所有众数（即，出现频率最高的元素）。'
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

* 给你一个含重复值的二叉搜索树（BST）的根节点 root ，找出并返回 BST 中的所有 众数（即，出现频率最高的元素）。
如果树中有不止一个众数，可以按 任意顺序 返回。
假定 BST 满足如下定义：

结点左子树中所含节点的值 小于等于 当前节点的值
结点右子树中所含节点的值 大于等于 当前节点的值
左子树和右子树都是二叉搜索树

* 结点左子树中所含节点的值 小于等于 当前节点的值

* 结点右子树中所含节点的值 大于等于 当前节点的值

* 左子树和右子树都是二叉搜索树

## 思考

本身二叉搜索树中的值是不重复的，本题重新定义了可以有重复值。

将二叉搜索树按照中序输出，是一个有序数组。我们需要遍历每个节点。还是设置一个pre和cur节点。

不断向左递归。

随后处理中的逻辑：

刚开始，pre指向nullptr，cur指向第一个节点，此时没有差值。count置1。随后移动后pre不为nullptr，就可以判断cur和pre元素相同时count+1，不同时，count置1。

然后pre移动到cur上。这样count完成了更新。

然后继续比较count和当前出现次数最多的元素的出现次数maxCount，如果相等，那么把当前节点返给结果result中，如果count > maxCount，那么就是找到了出现次数更多的元素，这时就要把result清空，将新元素加入到result中，更新最大出现次数 maxCount。

不断向右递归

左中右都遍历完，return；返回

## 代码实现

```cpp
class Solution {
public:
    vector<int> result;
    int maxCount = 0;
    int count = 0;
    TreeNode* pre = nullptr;
    void traversal(TreeNode* cur){
        if(cur == nullptr) return;
        traversal(cur->left);
        if(pre == nullptr) {
            count = 1;
        } else if(cur->val == pre->val){
            count++;
        } else {
            count = 1;
        }
        pre = cur;
        if(count == maxCount) {
            result.push_back(cur->val);
        }
        if(count > maxCount) {
            result.clear();
            maxCount = count;
            result.push_back(cur->val);
        }
        traversal(cur->right);
        return;
    }
    vector<int> findMode(TreeNode* root) {
        traversal(root);
        return resultQ;
    }
};
```