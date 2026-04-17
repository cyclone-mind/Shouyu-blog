---
title: '46. 全排列'
description: '给定一个不含重复数字的数组 nums，返回其所有可能的全排列。你可以按任意顺序返回答案。'
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

给定一个不含重复数字的数组`nums`，返回其*所有可能的全排列*。你可以**按任意顺序**返回答案。

**示例 1：**

```text
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**示例 2：**

```text
输入：nums = [0,1]
输出：[[0,1],[1,0]]
```

**示例 3：**

```text
输入：nums = [1]
输出：[[1]]
```

**提示：**

* 1 <= nums.length <= 6

* -10 <= nums[i] <= 10

* nums 中的所有整数 互不相同

## 思考

组合、子集、分割回文串都已经学完了，接下来看排列

这道题要求全排列，元素个数是集合个数。

另外排列意味着[1,2]、[2,1]是两个集合。所以不再需要startIndex了。startIndex是为了确保同一层使用过的元素再次选择（递归）时不再使用。我们可以重复使用，因此不再需要。

但是排列问题需要一个used数组标记同一树枝上已经选择的元素。

## 回溯三部曲

**1、回溯函数参数及返回值**

与子集不同，排列是有序的，所以我们不用startIndex。但是需要一个used数组标记已经选择的元素。

本题因为数组中元素不重复，因此遍历path查找元素是否出现过也可以，这道题数组大小只有6，所以也很快。

但是使用used是空间换时间，符合常规思维。

另外如果数组元素可重复，就不能遍历path了，这正是下一题**全排列II**涉及到的问题，那是就必须使用used了

**2、终止条件**

因为要求全排列，所以当path长度等于数组长度时，即到叶子节点，我们就收集结果。

**3、单层回溯搜索逻辑**

for循环里不用startIndex，每次都从0开始。

加入path时需要判断此时path里面是否已经有该元素了。

我们借助used实现这一点，而不是遍历path

**而used数组，其实就是记录此时path里都有哪些元素使用了，一个排列里一个元素只能使用一次**。

## 代码实现

```cpp
class Solution {
public:
    vector<vector<int>> result;
    vector<int> path;

    void backtracking(vector<int>& nums,vector<bool>& used){
        if(path.size() == nums.size()){
            result.push_back(path);
            return;
        }
        for(int i = 0;i < nums.size();i++){
            if(used[i] == true) continue;
            used[i] = true;
            path.push_back(nums[i]);
            backtracking(nums,used);
            path.pop_back();
            used[i] = false; 
        }
    }
    vector<vector<int>> permute(vector<int>& nums) {
        result.clear();path.clear();
        vector<bool> used(nums.size(),false);
        backtracking(nums,used);
        return result;
    }
};
```