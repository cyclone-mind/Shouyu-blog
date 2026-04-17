---
title: '代码随想录 哈希表：15. 三数之和'
description: '给定一个整数数组nums，判断是否存在三元组满足i != j、i != k且j != k，同时满足nums[i] + nums[j] + nums[k] == 0。返回所有和为0且不重复的三元组。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 哈希表
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

[题目链接](https://leetcode.cn/problems/3sum/description/)

[文章讲解](https://programmercarl.com/0015.%E4%B8%89%E6%95%B0%E4%B9%8B%E5%92%8C.html)

## 题目描述

* 给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，同时还满足 nums[i] + nums[j] + nums[k] == 0 。请你返回所有和为 0 且不重复的三元组。
**注意**答案中不可以包含重复的三元组。
示例 1：
输入：nums = [-1,0,1,2,-1,-4]
输出：[[-1,-1,2],[-1,0,1]]
解释：
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0 。
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0 。
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0 。
不同的三元组是 [-1,0,1] 和 [-1,-1,2] 。
注意，输出的顺序和三元组的顺序并不重要。

示例 2：
输入：nums = [0,1,1]
输出：[]
解释：唯一可能的三元组和不为 0 。

示例 3：
输入：nums = [0,0,0]
输出：[[0,0,0]]
解释：唯一可能的三元组和为 0 。

提示：

3 <= nums.length <= 3000
-105 <= nums[i] <= 105

* 3 <= nums.length <= 3000

* -105 <= nums[i] <= 105

## 思路

属于经典的双指针+排序+去重问题。

固定第一个数 nums[i]，问题就变成了"在剩下的区间里找两个数，使它们的和等于 -nums[i]"。这时使用双指针很合适，前提是排序好的数组。

这其实就是"两数之和"的变种，而有序数组里找两数之和最优解法就是双指针。

题目要求不能有重复三元组。

排序后，相同的数会连在一起，跳过重复的数就能避免重复三元组。

只要遇到"找 k 个数的和为定值且不能重复"，都可以考虑"排序+双指针+去重"这个套路。

先暴力，发现超时，再思考能不能降维、利用有序性、用哈希表或双指针优化。

1. 排序
首先对数组进行排序，方便后续去重和使用双指针。

1. 枚举第一个数
用 for 循环枚举第一个数 nums[i]，对于每个 nums[i]，用双指针在剩下的区间查找另外两个数。

1. 双指针查找

left 指向 i+1，right 指向数组末尾。
计算三数之和 sum = nums[i] + nums[left] + nums[right]。
如果 sum == 0，找到一个三元组，左右指针分别跳过重复元素后收缩。
如果 sum < 0，说明需要更大的数，left++。
如果 sum > 0，说明需要更小的数，right--。

1. 去重

i > 0 时，若 nums[i] == nums[i-1]，跳过，避免三元组重复。
找到三元组后，left/right 也要跳过重复值。

```cpp
vector<vector<int>> threeSum(vector<int> &nums)
{
    vector<vector<int>> result;
    // 先对数组进行排序，方便后续去重和双指针查找
    sort(nums.begin(), nums.end());
    for (int i = 0; i < nums.size(); i++)
    {
        // 如果当前数字大于0，后面不可能有三数之和为0，直接结束
        if (nums[i] > 0)
            break;
        // 跳过重复的第一个数，避免三元组重复
        if (i > 0 && nums[i] == nums[i - 1])
            continue;
        int left = i + 1, right = nums.size() - 1;
        while (left < right)
        {
            int sum = nums[i] + nums[left] + nums[right];
            if (sum == 0)
            {
                result.push_back({nums[i], nums[left], nums[right]});
                // 跳过重复的 left
                while (left < right && nums[left] == nums[left + 1])
                    left++;
                // 跳过重复的 right
                while (left < right && nums[right] == nums[right - 1])
                    right--;
                left++;
                right--;
            }
            else if (sum < 0)
            {
                left++;
            }
            else
            {
                right--;
            }
        }
    }
    return result;
}
```

* 时间复杂度：O(n^2)，排序 O(nlogn)，主循环 O(n^2)

* 空间复杂度：O(1)（不算输出结果）

### 难点

1. 去重技巧

i、left、right 三个指针都要注意去重，防止结果重复。
特别是 while 循环跳过重复元素的写法，容易漏掉。

1. 双指针的边界处理

left < right 的条件，left/right 的移动和跳过重复的顺序。

1. 提前终止

如果 nums[i] > 0，可以直接 break，提升效率。

## 易错点

1. 去重不彻底

只对 i 去重，忘了对 left/right 去重，导致结果重复。

1. 指针越界

left/right 的边界条件没处理好，可能越界或死循环。

1. 排序遗漏

忘记排序，导致去重和双指针失效。

1. 三元组顺序

题目要求三元组按升序排列，排序后直接按顺序 push 即可。