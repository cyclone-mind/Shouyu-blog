---
title: '77. 组合'
description: '给定两个整数 n 和 k，返回范围 [1, n] 中所有可能的 k 个数的组合。你可以按任何顺序返回答案。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 回溯
  - 代码随想录
  - 数据结构与算法
  - Leetcode
  - 回溯算法
---

## 题目描述

给定两个整数`n`和`k`，返回范围`[1, n]`中所有可能的`k`个数的组合。

你可以按**任何顺序**返回答案。

## 思考

直接的解法是嵌套for循环，外层选第一个数，内层再选第二个数。如果k=2，那么两层就可以解决。但是这里k不确定，我们怎么知道要写多少层？

回溯搜索可以解决这个问题，虽然也是暴力，但能写出来。

之前理解回溯法一棵树，横向是for循环，纵向是递归。这道题可以理解为k层for循环

## 回溯法三部曲

* 回溯函数参数即返回值
n K startIndex，这个 startIndex 控制是本层递归中，集合元素的可选范围，为什么需要？因为这道题是组合问题，如果每次递归都是从相同的集合选，会导致出现重复的组合。例如第一次选了1，第二次选了2，和第一次选2，第二次选1是一样的。而 startIndex 则会在第二套的第二次选择时为2，代表第二次选择只能从集合里面第二个元素以后选，这样第二次就不会再选{2,1}的情况

* 终止条件
path大小为k的时候，认为达到了叶子节点，将path加入到结果中，终止。

* 回溯搜索的遍历过程
for循环每次从startIndex 开始遍历，然后用path保存取出的节点i。
这里使用了回溯的标准写法：
先处理节点/做出选择，再进入递归函数，函数结束再撤销选择。

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
        for(int i = startIndex;i <=n;i++){
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