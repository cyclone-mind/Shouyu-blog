---
title: '78. 子集'
description: '给你一个整数数组 nums，数组中的元素互不相同。返回该数组所有可能的子集（幂集）。解集不能包含重复的子集。'
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

给你一个整数数组`nums`，数组中的元素**互不相同**。返回该数组所有可能的子集（幂集）。

解集**不能**包含重复的子集。你可以按**任意顺序**返回解集。


## 思考

子集问题不同于组合和分割问题，**子集收集树左右节点，而组合和分割收集树的叶子节点。**

因为在**同一集合**中选取元素组成子集，那么还是需要 startIndex 。不过仍因为是组合，startIndex 仍然要从 i 开始 。如果是排列，则要从0 开始。另外，不可重复选取，所以进入递归要从i+1开始。

## 回溯三部曲

**1、回溯函数参数及返回值**

全局变量path收集节点元素/子集，result存放path/子集组合。也可以放在递归函数中，是一样的。

**2、终止条件**

剩余集合为空时，到达叶子节点，即为终止条件。startIndex代表着剩余集合的起始位置，所以，如果startIndex大于数组长度，那就是没有元素可取，终止。

起始不加也行，因为for循环的条件也是要从待选集合中选取元素。待选集合没有元素自然这个for循环就不会执行。

**3、单层回溯搜索逻辑**

for循环里递归，遍历整棵树。将每个节点加入到path中。

## 代码实现

```cpp
class Solution {
public:
    vector<vector<int>> result;
    vector<int> path;

    void backtracking(vector<int>& nums, int startIndex) {
        result.push_back(path);
        for (int i = startIndex; i < nums.size(); i++) {
            path.push_back(nums[i]);
            backtracking(nums, i + 1);
            path.pop_back();
        }
    }
    vector<vector<int>> subsets(vector<int>& nums) {
        result.clear();
        path.clear();
        backtracking(nums, 0);
        return result;
    }
};
```