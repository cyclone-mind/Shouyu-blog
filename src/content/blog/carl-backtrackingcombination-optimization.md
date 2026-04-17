---
title: '组合优化'
description: '给定两个整数 n 和 k，返回范围 [1, n] 中所有可能的 k 个数的组合。优化回溯搜索的剪枝策略。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 回溯
  - 代码随想录
  - 数据结构与算法
  - 回溯算法
---

## 题目描述

给定两个整数`n`和`k`，返回范围`[1, n]`中所有可能的`k`个数的组合。

你可以按**任何顺序**返回答案。

## 思考

优化，回想1234这个集合，如果从中选4个数，那么那么第一层for循环的时候选1往下递归有意义的，选了2往下递归没有意义，因为选了2，剩余元素只有3和4，凑不齐4个了。因此我们可以总结规律：

**如果for循环选择的起始位置之后的元素个数 已经不足 我们需要的元素个数了，那么就没有必要搜索了**。

例如for循环选择起始为2，那么剩余2个元素不足以我们需要的元素个数，因此这个for循环没必要进行。没必要进入递归。

## 回溯法三部曲

* 回溯函数参数即返回值

* 终止条件
`for (int i = startIndex; i <= n - (k - path.size()) + 1; i++) // i为本次搜索的起始位置`

* 回溯搜索的遍历过程

## 代码实现

```cpp
class Solution {
public:
    vector<int> path;
    vector<vector<int>> result;
    void backtracking(int n,int k,int startIndex){
        if(path.size() == k) {
            result.push_back(path);
            return;
        }
        for(int i = startIndex;i <= n-(k-path.size())+1;i++){
            path.push_back(i);
            backtracking(n,k,i+1);
            path.pop_back();
        }
    }
    vector<vector<int>> combine(int n, int k) {
        result.clear();
        path.clear();
        backtracking(n,k,1);
        return result;
    }
};
```