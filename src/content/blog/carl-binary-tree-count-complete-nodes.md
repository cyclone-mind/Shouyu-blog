---
title: '完全二叉树节点个数'
description: '给你一棵完全二叉树的根节点 root，求出该树的节点个数。完全二叉树除了最底层节点可能没填满外，其余每层节点数都达到最大值。'
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

给你一棵**完全二叉树**的根节点`root`，求出该树的节点个数。

完全二叉树的定义如下：在完全二叉树中，除了最底层节点可能没填满外，其余每层节点数都达到最大值，并且最下面一层的节点都集中在该层最左边的若干位置。若最底层为第`h`层（从第 0 层开始），则该层包含`1~ 2h`个节点。

[题目链接](https://leetcode.cn/problems/count-complete-tree-nodes/)

[文章讲解](https://programmercarl.com/0222.%E5%AE%8C%E5%85%A8%E4%BA%8C%E5%8F%89%E6%A0%91%E7%9A%84%E8%8A%82%E7%82%B9%E4%B8%AA%E6%95%B0.html)

## 思路

按照普通二叉树的思路来求解的话，就是遍历每一个节点，数字+1就行了。应该采用什么遍历顺序？

对一棵树进行拆解，其节点数量=左子树节点数量+右子树节点数量+1；

可以看到父节点信息取决于子节点，因此先处理孩子再处理父亲，因此使用后序遍历。

```cpp
class Solution {
public:
    int countNodes(TreeNode* root) {
        if(root == nullptr) return 0;
        return 1 + countNodes(root->left) + countNodes(root->right);
    }
};
```

但是时间复杂度 $O(n)$ 空间复杂度 $O(logn)$ 。

层序遍历版本

```cpp
class Solution {
public:
    int countNodes(TreeNode* root) {
        queue<TreeNode*> que;
        if(root != nullptr) que.push(root);
        int result = 0;
        while(!que.empty()){
            int size = que.size();
            while(size--){
                TreeNode* node = que.front();
                que.pop();
                result++;
                if(node->left) que.push(node->left);
                if(node->right) que.push(node->right);
            }
        }
        return result;
    }
};
```

### 利用完全二叉树的性质

完全二叉树可以拆分，直到拆出满二叉树，就能用公式计算 $2^k -1$ ，`k`是深度，从 1 开始。

可以这样理解

完全二叉树只有两种情况，情况一：就是满二叉树，情况二：最后一层叶子节点没有满。

对于情况一，可以直接用 2^树深度 - 1 来计算，注意这里根节点深度为1。

对于情况二，分别递归左孩子，和右孩子，递归到某一深度一定会有左孩子或者右孩子为满二叉树，然后依然可以按照情况1来计算。

所以我们先判断树是否为满二叉树，如果不是，就递归其左右孩子，直到遇到满二叉树为止。用公式计算这个子树（满二叉树）的节点数量。

关键在于如何去判断一个左子树或者右子树是不是满二叉树呢？

在完全二叉树中，如果递归向左遍历的深度等于递归向右遍历的深度，那说明就是满二叉树。

在完全二叉树中，如果递归向左遍历的深度不等于递归向右遍历的深度，则说明不是满二叉树。

所以我们写这个代码逻辑

递归函数，返回当前树的节点数量：

1. 如果是空节点，节点数量为0

1. 如果是满二叉树，使用公式计算当前节点数量

1. 如果不是满二叉树，则当前节点数量=左子树节点数量+右子树节点数量 +1；

### 左移运算符 <<

`A << B`的含义是：将数字`A`的二进制位向左移动`B`位。

当我们将一个数字的二进制位向左移动一位时，实际上就相当于将这个数字乘以 2。
例如：

* 1 的二进制是 0001

* 1 << 1 (1 左移 1 位) 变成 0010，这表示十进制的 2。 (1 * 2^1 = 2)

* 1 << 2 (1 左移 2 位) 变成 0100，这表示十进制的 4。 (1 * 2^2 = 4)

* 1 << 3 (1 左移 3 位) 变成 1000，这表示十进制的 8。 (1 * 2^3 = 8)

所以，通用公式是：`A << B`等价于`A * (2^B)`。

`(2 << leftdepth) - 1`：

* leftdepth 代表的是满二叉树的 高度 (从 0 开始计数)。

* 满二叉树的节点总数公式是 2^(高度+1) - 1。

让我们把`A`设为`2`，`B`设为`leftdepth`。
那么`2 << leftdepth`就等价于`2 * (2^leftdepth)`。
根据指数运算的规则，`2 * (2^leftdepth)`等于`2^(1 + leftdepth)`，也就是`2^(leftdepth + 1)`。

所以，`2 << leftdepth`实际上就是在计算`2^(高度+1)`。

### 为什么使用位运算而不是 pow 函数？

使用位运算`<<`来计算`2`的幂次方通常比使用`pow(2, some_exponent)`函数更高效 ，因为它直接在二进制层面进行操作，不需要浮点数运算，而且编译器通常会将其优化为非常快的机器指令。在算法题或性能敏感的代码中，这是一种常见的优化技巧。

## 代码实现

```cpp
class Solution {
public:
    int countNodes(TreeNode* root) {
        if(root == nullptr) return 0;
        // 判断是否为满二叉树
        TreeNode* left = root->left;
        TreeNode* right = root->right;
        int leftDepth = 0;
        int rightDepth = 0;
        while(left != nullptr){
            left = left->left;
            leftDepth++;
        }
        while(right != nullptr){
            right = right->right;
            rightDepth++;
        }
        if(leftDepth == rightDepth) return (2 << leftDepth) -1;
        return 1 + countNodes(root->left) + countNodes(root->right);
    }
};
```