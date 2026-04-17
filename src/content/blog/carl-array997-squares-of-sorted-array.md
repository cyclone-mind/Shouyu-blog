---
title: '有序数组的平方'
description: '双指针法解决有序数组的平方问题，非递减顺序排序的整数数组平方后仍按非递减顺序排列。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 数组
  - 双指针
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

[题目链接](https://leetcode.cn/problems/squares-of-a-sorted-array/)

[文章讲解](https://programmercarl.com/0977.%E6%9C%89%E5%BA%8F%E6%95%B0%E7%BB%84%E7%9A%84%E5%B9%B3%E6%96%B9.html)

题目：给你一个按 非递减顺序 排序的整数数组 nums，返回 每个数字的平方 组成的新数组，要求也按 非递减顺序 排序。

示例 1：

* 输入：nums = [-4,-1,0,3,10]

* 输出：[0,1,9,16,100]

* 解释：平方后，数组变为 [16,1,0,9,100]，排序后，数组变为 [0,1,9,16,100]

示例 2：

* 输入：nums = [-7,-3,2,3,11]

* 输出：[4,9,9,49,121]

## 思路

有了前面双指针的思路，我们看到这道题是非递减排序，那么如果把每个数字都平方之后，它们的值应该是从大到小再到最大，那么我们可以有两个指针分在两侧，然后依次比较左右两侧指针指向的值的绝对值的大小，大的值放到新数组，然后移动大值对应的指针，这样循环下来即可。

```cpp
#include <vector>
#include <iostream>
using namespace std;
class Solution
{
public:
    vector<int> sortedSquares(vector<int> &nums)
    {
        int n = nums.size();
        int left = 0;
        int right = n - 1;
        vector<int> result(n, 0);
        int k = n - 1; // 指针k，用于从后往前填充result数组

        while (left <= right)
        {
            // 使用long long避免平方后整数溢出，尽管对于此题int可能足够
            long long square_left = static_cast<long long>(nums[left]) * nums[left];
            long long square_right = static_cast<long long>(nums[right]) * nums[right];

            if (square_right >= square_left)
            {
                result[k] = square_right;
                right--; // 移动原始数组的右指针
            }
            else
            {
                result[k] = square_left;
                left++; // 移动原始数组的左指针
            }
            k--; // 结果数组的填充指针向前移动
        }
        return result;
    }
};

//时间复杂度：O(n)，其中 n 是数组 nums 的长度。
//空间复杂度：O(1)。除了存储答案的数组以外，我们只需要维护常量空间。
```

如果出于简洁考虑，使用 python 的 sorted 结合推导式 更加简洁

```python
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        return sorted(num * num for num in nums)

#时间复杂度：O(nlogn)，其中 n 是数组 nums 的长度。
#空间复杂度：O(logn)。除了存储答案的数组以外，我们需要 O(logn) 的栈空间进行排序
```

## 启发

1. 还是有序数组，也许可以考虑双指针