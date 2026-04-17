---
title: '统一迭代'
description: '统一迭代法实现二叉树的前、中、后序遍历。'
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

## 思路

统一迭代法实现前中后序遍历。回想之前的中序遍历、前序遍历和后序遍历。

前序遍历：访问节点就是处理节点，都在栈中

```cpp
while (!st.empty()) {
    TreeNode *node = st.top();
    st.pop();
    result.push_back(node->val); // 立即处理节点
    if (node->right) st.push(node->right);
    if (node->left) st.push(node->left);
}
```

中序遍历：访问和处理分离，先到最左边，回溯时才能处理

```cpp
while (cur != NULL || !st.empty()) {
    if (cur != NULL) {
        st.push(cur);
        cur = cur->left; // 先走到最左边
    } else {
        TreeNode *node = st.top();
        st.pop();
        result.push_back(node->val); // 回溯时才处理
        cur = node->right;
    }
}
```

后序遍历：与前序遍历类似

##### 统一迭代法

统一把访问和处理分离，把需要处理的节点打上`nullptr`标记；

```cpp
while (!st.empty()) {
    TreeNode *node = st.top();
    if (node != nullptr) {
        // 访问阶段：按遍历顺序压入栈
    } else {
        // 处理阶段：真正处理节点
        st.pop(); // 弹出NULL
        node = st.top();
        st.pop();
        result.push_back(node->val);
    }
}
```

中序遍历：统一迭代

```cpp
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        stack<TreeNode*> st;
        vector<int> result;
        if(root!=nullptr) st.push(root); 
        while(!st.empty()){
            TreeNode* node = st.top();
            if(node != nullptr){
                st.pop();
                if(node->right) st.push(node->right);
                st.push(node);
                st.push(nullptr);
                if(node->left) st.push(node->left);
            } else {
                st.pop();
                TreeNode* node = st.top(); // 先弹出一个再取栈顶可能出现非法，弹出的是最后一个元素，也就是最后一个元素为 nullptr
                st.pop();
                result.push_back(node->val);
            }
        }
        return result;
    }
};
```