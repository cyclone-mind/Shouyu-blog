---
title: '四数之和'
description: '在数组中找出满足条件的不重复四元组'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 哈希
---


给你一个由`n`个整数组成的数组`nums`，和一个目标值`target`。请你找出并返回满足下述全部条件且**不重复**的四元组`[nums[a], nums[b], nums[c], nums[d]]`（若两个四元组元素一一对应，则认为两个四元组重复）：

* 0 <= a, b, c, d&nbsp;< n

* a、b、c 和 d 互不相同

* nums[a] + nums[b] + nums[c] + nums[d] == target

你可以按**任意顺序**返回答案 。

[题目链接](https://leetcode.cn/problems/4sum/)

[文章讲解](https://programmercarl.com/0018.%E5%9B%9B%E6%95%B0%E4%B9%8B%E5%92%8C.html)

## 思路

相比于三数之和，这道题将三元组升为四元组，`target`由 0 变为自定义。整体思路不变，不过有些细节需要注意。

可以两层 for 循环`k`,`i`，然后找剩余元素中和为`target - nums[k] - nums[i]`的两个元素。使用双指针。

由于`target`自定义，因此剪枝`k`时就不能只写`nums[k] > target`，因为比如：数组是`[-4, -3, -2, -1]`，`target`是`-10`，不能因为`-4 > -10`而跳过。但是我们依旧可以去做剪枝，逻辑变成`nums[k] > target && (nums[k] >=0 || target >= 0)`就可以了。

同理 剪枝`i`时需要变为`nums[k] + nums[i] > target && nums[k] + nums[i] >= 0`。其余内部不变

## 代码实现

```cpp
class Solution {
public:
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        vector<vector<int>> result;
        sort(nums.begin(), nums.end());
        for (int k = 0; k < nums.size(); k++) {
            if (nums[k] > target && nums[k] > 0)
                break;
            if (k > 0 && nums[k] == nums[k - 1])
                continue;
            for (int i = k + 1; i < nums.size(); i++) {
                if (nums[k] + nums[i] > target && nums[k] + nums[i] >= 0)
                    break;
                if (i > k + 1 && nums[i] == nums[i - 1])
                    continue;
                int left = i + 1;
                int right = nums.size() - 1;
                while (left < right) {
                    long sum =
                        (long)nums[k] + nums[i] + nums[left] + nums[right];
                    if (sum == target) {
                        result.push_back(
                            {nums[k], nums[i], nums[left], nums[right]});
                        // 跳过重复的 left
                        while (left < right && nums[left] == nums[left + 1])
                            left++;
                        // 跳过重复的 right
                        while (left < right && nums[right] == nums[right - 1])
                            right--;
                        left++;
                        right--;
                    } else if (sum < target) {
                        left++;
                    } else {
                        right--;
                    }
                }
            }
        }
        return result;
    }
};
```