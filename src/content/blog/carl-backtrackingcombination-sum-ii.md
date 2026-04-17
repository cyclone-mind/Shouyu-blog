---
title: '组合总和II'
description: '给定一个候选人编号的集合 candidates 和一个目标数 target，找出 candidates 中所有可以使数字和为 target 的组合。每个数字在每个组合中只能使用一次。'
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

给定一个候选人编号的集合`candidates`和一个目标数`target`，找出`candidates`中所有可以使数字和为`target`的组合。

`candidates`中的每个数字在每个组合中只能使用**一次**。

**注意**解集不能包含重复的组合。

## 思考

这道组合题有几个关键信息点：1、目标和；2、不限制个数；3、集合中有重复元素4、每个元素在每个组合中只能出现一次；

其中第1、2、4我们都是见过的，不过这个集合中有重复元素倒是第一次见。

一图胜千言。

上面看有可能取到`{1，2}`和`{1，2}`两个重复的组合。第一个组合中的1是第一个1，第二个组合中的1是第二个1。这种情况就是出现了重复的组合，不符合题意。为避免这种情况，需要去重。

for循环遍历时如果当前遍历的元素和上一个遍历的元素相等，那么就需要去重。

我们会使用`candidates[i] == candidates[i - 1]`这个条件，但是这里这个条件中`candidates[i - 1]`并不一定是同一个for循环，同一层的上一个遍历元素，还有可能是同一树枝，递归得来的上一个遍历元素。

因此我们要对同一树层去重，对同一树枝不去重。为了区分，我们使用used数组标记同一路径/组合上的遍历情况。

## 回溯法三部曲

* 回溯函数参数及返回值
增加了used数组

```cpp
void backtracking(
    std::vector<int> &candidates, // 候选数组
    int target,                   // 目标和
    int sum,                      // 当前已经收集的元素之和
    int startIndex,               // 下一轮搜索的起始位置
    std::vector<bool> &used       // 记录元素是否被使用过的数组
);
```

* 终止条件
终止条件为 `sum > target 和 sum == target`

* 回溯搜索的遍历过程
for循环从startIndex开始，先判断是否树层重复，如果是则跳过本次循环，如果不是，则做出选择：选择的元素加入当前组合、计算累加和、标记访问数组，往下递归，回溯，撤回选择。
单层逻辑的重点是去重
排序：在调用回溯函数之前，我们必须对 candidates 数组进行排序。这样才能让所有相同的数字都相邻，为去重做准备。

## 剪枝优化

在**组合总和**讲过目标和的`sum + candidates[i] <= target`的剪枝操作。

## 代码实现

剪枝优化版

```cpp
class Solution {
public:
    std::vector<std::vector<int>> result;
    std::vector<int> path;
    std::vector<bool> used;

    void backtracking(std::vector<int>& candidates, int target, int sum,
                      int startIndex) {
        if (sum == target) {
            result.push_back(path);
            return;
        }

        for (int i = startIndex; i < candidates.size() && sum + candidates[i] <= target; i++) {
            if (i > 0 && candidates[i] == candidates[i - 1] &&
                used[i - 1] == false) {
                continue;
            }
            path.push_back(candidates[i]);
            sum += candidates[i];
            used[i] = true;
            backtracking(candidates, target, sum, i + 1);
            sum -= candidates[i];
            used[i] = false;
            path.pop_back();
        }
    }

    std::vector<std::vector<int>> combinationSum2(std::vector<int>& candidates,
                                                  int target) {
        result.clear();
        path.clear();
        used = std::vector<bool>(candidates.size(), false);
        sort(candidates.begin(), candidates.end());
        backtracking(candidates, target, 0, 0);
        return result;
    }
};
```