---
title: '全排列II'
description: '给定一个可包含重复数字的序列 nums，按任意顺序返回所有不重复的全排列。'
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

给定一个可包含重复数字的序列`nums`，***按任意顺序***返回所有不重复的全排列。

**示例 1：**

```text
输入：nums = [1,1,2]
输出：
[[1,1,2],
 [1,2,1],
 [2,1,1]]
```

**示例 2：**

```text
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

## 思考

这道题目和46.全排列 的区别在与**给定一个可包含重复数字的序列**，要返回**所有不重复的全排列**.

类比于40.组合总和II 、90.子集II 的组合问题和子集问题去重。

不同于子序列，我们需要排序后去重。仍然是对树层去重。

## 回溯三部曲

步骤和 全排列 一样。只是借助了used。进行树层去重。

## 代码实现

```cpp
class Solution {
public:
    vector<vector<int>> result;
    vector<int> path;

    void backtracking(vector<int>& nums, vector<bool> used) {
        if (path.size() == nums.size()) {
            result.push_back(path);
            return;
        }
        for (int i = 0; i < nums.size(); i++) {
            if (i > 0 && nums[i] == nums[i - 1] && used[i - 1] == false) {
                continue;
            }
            if (used[i] == false) {
                used[i] = true;
                path.push_back(nums[i]);
                backtracking(nums, used);
                path.pop_back();
                used[i] = false;
            }
        }
    }

    vector<vector<int>> permuteUnique(vector<int>& nums) {
        result.clear();
        path.clear();
        sort(nums.begin(), nums.end());
        vector<bool> used(nums.size(), false);
        backtracking(nums, used);
        return result;
    }
};
```