---
title: '组合总和III'
description: '找出所有相加之和为 n 的 k 个数的组合，且满足只使用数字 1 到 9，每个数字最多使用一次。'
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

找出所有相加之和为`n`的`k`个数的组合，且满足下列条件：

* 只使用数字1到9

* 每个数字 最多使用一次

返回*所有可能的有效组合的列表*。该列表不能包含相同的组合两次，组合可以以任何顺序返回。

## 思考

等同于找出1-9的k个数的组合总和为n的组合。在**组合**的问题上加上了和为n的约束条件。所以终止条件不止判断path长度，还要判断path中元素和

## 回溯法三部曲

* 回溯函数参数及返回值
n k startIndex sum``

* 终止条件
path长度达到k，终止，如果同时sum = tarSum，则path加入result，否则不加入

* 回溯搜索的遍历过程
for循环遍历从startIndex到n - (k - path.size()) +1，每次循环都计算累计和并将节点i加入path，递归进入，回溯撤回选择。这一步是做了剪枝，组合问题的通用剪枝操作

## 代码实现

```cpp
class Solution {
public:
    std::vector<std::vector<int>> result;
    std::vector<int> path;
    void backtracking(int targetSum, int k, int sum, int startIndex) {
        if (path.size() == k) {
            if (sum == targetSum) {
                result.push_back(path);
            }
            return;
        }
        for (int i = startIndex; i <= n - (k - path.size())+1; i++) {
            sum += i;
            path.push_back(i);
            backtracking(targetSum, k, sum, i + 1);
            sum -= i;
            path.pop_back();
        }
    }

    std::vector<std::vector<int>> combinationSum3(int k, int n) {
        backtracking(n, k, 0, 1);
        return result;
    }
};
```