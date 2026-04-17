---
title: '代码随想录 二叉树：102. 层序遍历'
description: '给你二叉树的根节点 root ，返回其节点值的层序遍历（即逐层地，从左到右访问所有节点）。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 二叉树
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

## 题目描述

给你二叉树的根节点 root ，返回其节点值的 层序遍历 。 （即逐层地，从左到右访问所有节点）。

[题目链接](https://leetcode.cn/problems/binary-tree-level-order-traversal)

[文章讲解](https://programmercarl.com/0102.%E4%BA%8C%E5%8F%89%E6%A0%91%E7%9A%84%E5%B1%82%E5%BA%8F%E9%81%8D%E5%8E%86.html)

## 思路

层序遍历要求一层一层，从左至右遍历。先上层再下层，先进先出。

使用队列实现广度优先遍历。

遍历顺序

* 初始化：首先，如果根节点不为空，将根节点 root 放入队列。if(root != NULL) que.push(root);

* 循环遍历：当队列不为空时，循环进行以下操作：while (!que.empty())

* 获取当前层的节点数量：在每次外层循环开始时，记录当前队列中的元素数量 int size = que.size();。这个 size 就是当前层级的节点数量。这是非常关键的一步，它确保我们一次只处理一整层的节点。

* 遍历当前层：创建一个 std::vector<int> vec; 用于存放当前层的所有节点值。然后，进行 for (int i = 0; i < size; i++) 循环，将当前层的所有节点从队列中取出并处理：


取出队列头部的节点：TreeNode *node = que.front();


将节点从队列中移除：que.pop();


将节点的值加入当前层的结果向量 vec 中：vec.push_back(node->val);


添加子节点：如果当前节点的左子节点不为空，将其入队：if(node->left) que.push(node->left);


如果当前节点的右子节点不为空，将其入队：if(node->right) que.push(node->right);

* 取出队列头部的节点：TreeNode *node = que.front();

* 将节点从队列中移除：que.pop();

* 将节点的值加入当前层的结果向量 vec 中：vec.push_back(node->val);

* 添加子节点：如果当前节点的左子节点不为空，将其入队：if(node->left) que.push(node->left);

* 如果当前节点的右子节点不为空，将其入队：if(node->right) que.push(node->right);

* 保存当前层结果：将  vec （当前层的所有节点值）添加到最终的结果 result 中：result.push_back(vec);

## 代码实现

```cpp
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> result;
        queue<TreeNode*> que;
        if(root != nullptr) que.push(root);
        while (!que.empty()) {
            vector<int> vec;
            int size = que.size();
            while (size--) {
                TreeNode* node = que.front();
                vec.push_back(node->val);
                que.pop();
                if (node->left)
                    que.push(node->left);
                if (node->right)
                    que.push(node->right);
            }
            result.push_back(vec);
        }
        return result;
    }
};
```