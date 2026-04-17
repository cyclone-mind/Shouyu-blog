---
title: '组合总和'
description: '给你一个无重复元素的整数数组 candidates 和一个目标整数 target，找出 candidates 中可以使数字和为目标数 target 的所有不同组合。'
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

给你一个**无重复元素**的整数数组`candidates`和一个目标整数`target`，找出`candidates`中可以使数字和为目标数`target`的 所有**不同组合**，并以列表形式返回。你可以按**任意顺序**返回这些组合。

`candidates`中的**同一个**数字可以**无限制重复被选取**。如果至少一个数字的被选数量不同，则两种组合是不同的。

对于给定的输入，保证和为`target`的不同组合数少于`150`个。

## 思考

同一个数字无限制，不过还好数字范围在2到40，不包括0。这道题相对于之前的**组合总和III**问题，增加了数字无限重复被选取的规则，约束条件仍然是目标和。一个集合来求组合的话，就需要startIndex，本题同一个数组无限制重复被选取，意味着 进入递归时 startIndex 要从当前选择的元素遍历起。

## 回溯法三部曲

* 回溯函数参数及返回值
既然要求目标和就要有sum，不过这个sum随着节点变，因此设置为全局遍历。result全局存放结果。其实sum也能作为局部变量。然后是题目中给出的参数，集合candidates, 和目标值target。

* 终止条件
从图中可以看出来，终止只有两种情况，sum大于target和sum等于target。等于的时候需要收集结果。

* 回溯搜索的遍历过程
单层for循环依然从startIndex开始，搜索candidates集合。因为元素可以重复选取，所以进入递归时 startIndex 应为当前的i。这样使得重复选取。

### 剪枝优化

从图中可以看出取{2,5} {2,3}都是没必要的，因为取了{2,2}已经到达终止条件了，后面3和5都比它大，所以其实没必要进入递归。我们想要是这个for循环遍历的顺序是2、3、5就好了。因此我们可以先对集合进行排序，这样for循环遍历时如果sum+当前遍历元素大于目标和，就不再进行这次遍历。

## 代码实现

剪枝优化版

```cpp
class Solution {
public:
    std::vector<std::vector<int>> result;
    std::vector<int> path;

    void backtracking(std::vector<int>& candidates, int target, int sum,
                      int startIndex) {
        if(sum == target) {
            result.push_back(path);
            return;
        }
        for (int i = startIndex;
             i < candidates.size() && sum + candidates[i] <= target; i++) {
            path.push_back(candidates[i]);
            sum += candidates[i];
            backtracking(candidates, target, sum, i);
            sum -= candidates[i];
            path.pop_back();
        }
    }

    std::vector<std::vector<int>> combinationSum(std::vector<int>& candidates,
                                                 int target) {
        result.clear();
        path.clear();
        std::sort(candidates.begin(), candidates.end());
        backtracking(candidates, target, 0, 0);
        return result;
    }
};
```