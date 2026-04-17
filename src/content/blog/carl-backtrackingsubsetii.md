---
title: '子集II'
description: '给你一个整数数组 nums，其中可能包含重复元素，请你返回该数组所有可能的子集（幂集）。解集不能包含重复的子集。'
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

给你一个整数数组`nums`，其中可能包含重复元素，请你返回该数组所有可能的 子集（幂集）。

解集**不能**包含重复的子集。返回的解集中，子集可以按**任意顺序**排列。


## 思考

本题于**子集**唯一的不同就在于可重复元素的数组/集合。

因此借鉴**组合总和II**，需要进行树层去重。

## 回溯三部曲

**1、回溯函数参数及返回值**

同**子集**

**2、终止条件**

同**子集**

**3、单层回溯搜索逻辑**

同**子集**

## 易错点

去重一定记着排序！

## 代码实现

使用used数组

```cpp
class Solution {
public:
    vector<vector<int>> result;
    vector<int> path;
    vector<bool> used;
    void backtracking(vector<int>& nums, int startIndex) {
        result.push_back(path);
        if (startIndex >= nums.size()) {
            return;
        }
        for (int i = startIndex; i < nums.size(); i++) {
            if (i > 0 && nums[i] == nums[i - 1] && used[i - 1] == false)
                continue;
            used[i] = true;
            path.push_back(nums[i]);
            backtracking(nums, i + 1);
            path.pop_back();
            used[i] = false;
        }
    }
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        result.clear();path.clear();used.clear();
        used.resize(nums.size(),false);
        sort(nums.begin(), nums.end());
        backtracking(nums, 0);
        return result;
    }
};
```

使用set代替一维数组used。

```cpp
class Solution {
public:
    vector<vector<int>> result;
    vector<int> path;
    vector<bool> used;
    void backtracking(vector<int>& nums, int startIndex) {
        result.push_back(path);
        unordered_set<int> uset;
        for (int i = startIndex; i < nums.size(); i++) {
            if (i > 0 && nums[i] == nums[i - 1] && uset.find(nums[i]) != uset.end())
                continue;
            uset.insert(nums[i]);
            path.push_back(nums[i]);
            backtracking(nums, i + 1);
            path.pop_back();
        }
    }
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        result.clear();path.clear();used.clear();
        used.resize(nums.size(),false);
        sort(nums.begin(), nums.end());
        backtracking(nums, 0);
        return result;
    }
};
```

这道题不使用used或者set也是可以的，原因是

```cpp
class Solution {
public:
    vector<vector<int>> result;
    vector<int> path;

    void backtracking(vector<int>& nums, int startIndex) {
        result.push_back(path);
        for (int i = startIndex; i < nums.size(); i++) {
            if (i > startIndex && nums[i] == nums[i - 1])
                continue;
            path.push_back(nums[i]);
            backtracking(nums, i + 1);
            path.pop_back();
        }
    }
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        result.clear();path.clear();
        sort(nums.begin(), nums.end());
        backtracking(nums, 0);
        return result;
    }
};
```