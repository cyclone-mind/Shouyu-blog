---
title: '二分查找'
description: '二分查找算法模板，在有序数组中搜索目标值。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 数组
  - 二分查找
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

[题目链接](https://leetcode.cn/problems/binary-search/)

[文章讲解](https://programmercarl.com/0704.%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE.html)

题目：给定一个`n`个元素有序的（升序）整型数组`nums`和一个目标值`target`，写一个函数搜索`nums`中的`target`，如果目标值存在返回下标，否则返回`-1`。

**示例 1:**

```text
输入: nums = [-1,0,3,5,9,12], target = 9
输出: 4
解释: 9 出现在 nums 中并且下标为 4
```

**示例 2:**

```text
输入: nums = [-1,0,3,5,9,12], target = 2
输出: -1
解释: 2 不存在 nums 中因此返回 -1
```

## 思路

通常来说查找数组中的某个元素那就是循环一个一个找呗。但这最坏循环 N 次。

那么题目中有一个条件是有序数组，怎么利用？

也许我们可以先假设在数组中找到一个数然后我们知道它的位置，然后我们将这个数和目标值做比较，如果这个数小于这个目标值，那么是不是这个目标值一定在这个数的右边，所在的范围就不再是整个数组而是从这个数到最后的位置呢？缩小了范围之后就要再次确定一个数和目标值比较。

那这个数怎么找？每次缩小的范围是多少？

二分法查找区间每次缩小一半，查找次数：最多 log₂n 次

三分法查找区间每次缩小到原来的 2/3，查找次数：最多 log₍₃⁄₂₎n ≈ 1.71×log₂n 次（比二分法多）

四分法查找区间每次缩小到原来的 3/4，查找次数：最多 log₍₄⁄₃₎n ≈ 2.41×log₂n 次（比二分法更多）

所以选用二分查找。

二分查找的关键在于你要确定一个什么样的区间？我们常用的是左闭右开和左闭右闭。

```cpp
// 左闭右闭
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int left = 0;
        int right = nums.size()-1;   //  [,] 确保取到所有值
        while(left <= right){ // 确保left 与 right相等时合法例如[1,1]
            int middle = left + (right - left) / 2;
            if (nums[middle] < target){
                left = middle + 1; // 因为nums[middle]已不在查找范围内
            }else if(nums[middle] > target){
                right = middle - 1;
            }else{
                return middle;
            }
        }
        return -1;
    }
};
```

```python
# 左闭右开
class Solution(object):
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        left = 0
        right = len(nums) #  [,) 确保取到所有值
        while left < right:
            middle = (left + right) // 2
            if nums[middle] < target:
                left = middle + 1
            elif nums[middle] > target:
                right = middle
            else:
                return middle
        return -1
```

时间复杂度是 O(log n)。

空间复杂度 O(1)，只用常数个变量，无递归/新数组。

## 启发

所以当我们在有序数组中，想要快速查找某个元素时，二分查找能大大提高效率。

1. 边界条件的处理

1. 两个 int 相加时的防溢出

## 困难

边界条件的处理