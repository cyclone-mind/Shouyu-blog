---
title: '491. 递增子序列'
description: '给你一个整数数组 nums，找出并返回所有该数组中不同的递增子序列，递增子序列中至少有两个元素。'
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

给你一个整数数组`nums`，找出并返回所有该数组中不同的递增子序列，递增子序列中**至少有两个元素**。你可以按**任意顺序**返回答案。

数组中可能含有重复元素，如出现两个整数相等，也可以视作递增序列的一种特殊情况。

**示例 1：**

```text
输入：nums = [4,6,7,7]
输出：[[4,6],[4,6,7],[4,6,7,7],[4,7],[4,7,7],[6,7],[6,7,7],[7,7]]
```

**示例 2：**

```text
输入：nums = [4,4,3,2,1]
输出：[[4,4]]
```

**提示：**

* 1 <= nums.length <= 15

* -100 <= nums[i] <= 100

## 思考

子序列本质是子集，那么本题其实和**子集**问题差不多不过有以下区别：

1. 子序列要求元素的顺序和原来要相同。子集是从中任意挑选，顺序可以打乱（在子集II中我们进行了排序，就是打乱了）

1. 另外非递减，意味着子序列元素是非递减的。元素加入子序列的时候不能比最后一个元素小

1. 数组中有重复元素，类似于子集II，不过我们不能打乱顺序实现去重了，因为第一个区别已经说明了这一点。

1. 子序列至少有两个元素，而子集 没有要求元素个数

明白了以上区别，再分析就好分析了。

## 回溯三部曲

**1、回溯函数参数及返回值**

同一个集合求子序列，所以 需要startIndex。

**2、终止条件**

类似于求**子集**，要收集每个节点上的结果。所以可以不加终止条件。startIndex 超过了范围，就不再会进入递归了

但是收集结果有所不同，要求元素至少两个。所以要判断path已收集元素是否超过1个，超过了我才收集。

**3、单层回溯搜索逻辑**

for循环从 startIndex 开始，进入循环后就要往子集添加元素了，

区别2要求我们判断nums[i]比path的最后一个元素小的跳过本次循环。

区别3要求我们进行树层去重，本层/同一个for循环里面已经添加到path中的元素，下次又遍历到相同数值元素，则跳过。

随后将取得的元素使用set标记，并添加到子序列中。

递归

回溯，从子序列中去除当前元素。

#### 优化

set本质是甄别本层元素，放的是同一层的元素。那么题目给的条件元素范围是比较小的：`-100 <= nums[i] <= 100`

所以我们可以使用一个200大小的数组，对应位置为1说明该元素已使用过。

## 代码实现

使用set

```cpp
class Solution {
public:
    vector<vector<int>> result;
    vector<int> path;

    void backtracking(vector<int>& nums,int startIndex){
        if(path.size() > 1) { result.push_back(path);}
        unordered_set<int> uset;
        for(int i = startIndex;i < nums.size();i++){
            if((!path.empty() && nums[i] < path.back()) || uset.find(nums[i]) != uset.end()){
                continue;
            }
            uset.insert(nums[i]);
            path.push_back(nums[i]);
            backtracking(nums,i + 1);
            path.pop_back();
        }
    }
    vector<vector<int>> findSubsequences(vector<int>& nums) {
        result.clear();
        backtracking(nums,0);
        return result;
    }
};
```

数组优化版

```cpp
class Solution {
public:
    vector<vector<int>> result;
    vector<int> path;

    void backtracking(vector<int>& nums,int startIndex){
        if(path.size() > 1) { result.push_back(path);}
        int used[201] = {0};
        for(int i = startIndex;i < nums.size();i++){
            if((!path.empty() && nums[i] < path.back()) || used[nums[i] + 100] == 1){
                continue;
            }
            used[nums[i] + 100] = 1;
            path.push_back(nums[i]);
            backtracking(nums,i + 1);
            path.pop_back();
        }
    }
    vector<vector<int>> findSubsequences(vector<int>& nums) {
        result.clear();
        backtracking(nums,0);
        return result;
    }
};
```