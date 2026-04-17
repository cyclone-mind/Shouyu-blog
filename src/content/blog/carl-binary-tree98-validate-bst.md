---
title: '代码随想录 二叉树：98. 验证二叉搜索树'
description: '给你一个二叉树的根节点root，判断其是否是一个有效的二叉搜索树。有效二叉搜索树定义：节点的左子树只包含小于当前节点的数，节点的右子树只包含大于当前节点的数。'
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

给你一个二叉树的根节点`root`，判断其是否是一个有效的二叉搜索树。

**有效**二叉搜索树定义如下：

* 节点的左子树只包含 小于 当前节点的数。

* 节点的右子树只包含 大于 当前节点的数。

* 所有左子树和右子树自身必须也是二叉搜索树。

[题目链接](https://leetcode.cn/problems/validate-binary-search-tree/)

[文章讲解](https://programmercarl.com/0098.%E9%AA%8C%E8%AF%81%E4%BA%8C%E5%8F%89%E6%90%9C%E7%B4%A2%E6%A0%91.html)

## 思考

### 后序遍历

如果使用后序遍历，我刚开始这样思考 “如果使用后序遍历呢？左子树是二叉搜索树，右子树也是二叉搜索树，并且左子树根节点小于中间节点小于右子树根节点，这样判断中间节点构成的树就是二叉搜索树”

但这样思考是绝对不对的！！这是一个陷阱！！我搞混了一个条件。并非 左子树根节点小于中间节点小于右子树根节点就行，而是：

* 左子树是BST

* 右子树是BST

* 当前节点值大于左子树最大值，小于右子树最小值

我的想法遇到上面这个图就不正确，10大于了右子树的最小值，不是二叉搜索树。

所以如果要后序遍历，关键要找到左子树最大值和右子树最小值

1. 如何获取左子树最大值和右子树最小值？


在递归返回时，除了返回“是否是BST”，还要返回“当前子树的最大值和最小值”。


这样父节点才能判断自己的值是否在正确区间内

1. 如何组织递归返回值？

可以自定义一个结构体，包含：是否是BST、最大值、最小值。

## 易错点

后序遍历注意细节，本题有INT_MAX INT_MIN 测试用例，因此可以改为long long类型，使用LONG_MIN作为最小值。还需要注意，默认传进来的root-val，使用min和max函数得到当前子树的最小值和最大值是需要吧root-val强转为long long类型，才能使用min和max函数。

### 中序遍历

要知道中序遍历下，输出的二叉搜索树节点的数值是有序序列。

所以只需要判断遍历的元素是不是从小到大即可。不断比较相邻元素大小。设置一个maxVal = LONG_MIN，符合条件就不断更新，不符合就返回 false，

## 递归三部曲

1、确定递归函数的参数和返回值

* 参数：当前遍历到的节点 TreeNode* root

* 返回值：bool，表示以当前节点为根的子树是否为有效的二叉搜索树

此外，为了实现中序遍历时判断“前一个节点的值”，我们需要一个全局变量或外部变量来记录上一个访问的节点值。

2、终止条件

* 当 root == nullptr 时，说明遍历到空节点，空树也是二叉搜索树，直接返回 true。

3、单层递归逻辑

* 递归判断左子树是否为二叉搜索树

* 判断当前节点值是否大于“上一个访问的节点值”（即中序遍历的前驱节点）

* 更新“上一个访问的节点值”为当前节点值

* 递归判断右子树是否为二叉搜索树

## 代码实现

中序遍历

```cpp
long long maxval = LONG_MIN;
bool isValidBST(TreeNode* root) {
	if(root == nullptr) return true;
    bool leftValid = isValidBST(root->left);
    if(root->val > maxval) maxval = root->val;
    else return false;
    bool rightValid = isValidBST(root->right);
    return leftValid && rightValid;
}
```

后序遍历

```cpp
/*
后序遍历法判断二叉搜索树
每个节点递归返回：是否是BST、子树最大值、子树最小值
时间复杂度：O(n)
空间复杂度：O(h)
*/

    struct Info {
        bool isBST;
        long long minVal;
        long long maxVal;
        Info(bool isBST, long long minVal, long long maxVal)
            : isBST(isBST), minVal(minVal), maxVal(maxVal) {}
    };

    Info dfs(TreeNode* root) {
        if (root == nullptr) {
            // 空树是BST，最小值设为LONG_MAX，最大值设为LONG_MIN
            return Info(true, LONG_MAX, LONG_MIN);
        }
        // 递归处理左子树和右子树
        Info left = dfs(root->left);
        Info right = dfs(root->right);

        // 当前节点是否满足BST条件
        bool isBST = left.isBST && right.isBST && (root->val > left.maxVal) &&
                     (root->val < right.minVal);

        // 当前子树的最小值和最大值
        long long minVal = std::min((long long)root->val, left.minVal);
        long long maxVal = std::max((long long)root->val, right.maxVal);

        return Info(isBST, minVal, maxVal);
    }

    bool isValidBST(TreeNode* root) { return dfs(root).isBST; }
```