---
title: '移除元素'
description: '原地移除数组中所有等于val的元素，返回不同元素的数量。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 数组
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

[题目链接](https://leetcode.cn/problems/remove-element/)

[文章讲解](https://programmercarl.com/0027.%E7%A7%BB%E9%99%A4%E5%85%83%E7%B4%A0.html)

## 题目描述

给你一个数组`nums`和一个值`val`，你需要**原地**移除所有数值等于`val`的元素。元素的顺序可能发生改变。然后返回`nums`中与`val`不同的元素的数量。

假设`nums`中不等于`val`的元素数量为`k`，要通过此题，您需要执行以下操作：

* 更改 nums 数组，使 nums 的前 k 个元素包含不等于 val 的元素。nums 的其余元素和 nums 的大小并不重要。

* 返回 k。

**示例 1：**

```text
输入：nums = [3,2,2,3], val = 3
输出：2, nums = [2,2,_,_]
解释：你的函数函数应该返回 k = 2, 并且 nums 中的前两个元素均为 2。
你在返回的 k 个元素之外留下了什么并不重要（因此它们并不计入评测）。
```

**示例 2：**

```text
输入：nums = [0,1,2,2,3,0,4,2], val = 2
输出：5, nums = [0,1,4,0,3,_,_,_]
解释：你的函数应该返回 k = 5，并且 nums 中的前五个元素为 0,0,1,3,4。
注意这五个元素可以任意顺序返回。
你在返回的 k 个元素之外留下了什么并不重要（因此它们并不计入评测）。
```

## 思路

### 暴力解法

第一层循环找到需要移除的值，第二层循环依次将需要移除的值的后面所有的值向前移一位

```cpp
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
		int i = 0;
    	int current_size = array_size;
        while (i < current_size)
        {
            if (nums[i] == val)
            {
                for (int j = i + 1; j < current_size; j++)
                {
                    nums[j - 1] = nums[j];
                }
                current_size--;
            }
            else
            {
                i++;
            }
        }
    }
};
//时间复杂度：O(n^2)
//空间复杂度：O(1)
```

### 双指针法

暴力解法需要循环两次，每次找到一个值。那反过来，我们每次循环找到两个值不就行了？不也是一样的效果？

我们使用快慢指针，一个快指针用于**找移除目标值**，一个慢指针用于**更新元素**。

```cpp
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        {
            int slow = 0;
            for (int fast = 0; fast < nums.size(); fast++)
            {
                if (nums[fast] != val)
                {
                    nums[slow++] = nums[fast]; // 这里每一个非移除元素都需要赋值。后面的左右指针则只需要对移除元素赋值即可，它没了原来的顺序。
                }
            }
            return slow;
        }
  }
};
//时间复杂度：O(n^2)
//空间复杂度：O(1)
```

也可以使用左右指针，没错，左指针用来找 需要移除的元素，右指针的值用来更新左指针找到的元素。

```cpp
int removeElement3(std::vector<int> &nums, int val)
{
    // 当左指针 left 指向的元素是我们想要移除的 val 时，我们尝试用右指针 right 指向的元素去覆盖它。
    // 这样做的目的是尽量把"有效"的元素往前挪，把"无效"的元素（或者暂时不关心的元素）往后挪。
    int left = 0, right = nums.size();
    while (left < right)
    {
        if (nums[left] == val)
        {
            nums[left] = nums[right - 1]; // 为什么要-1？因为你使用了nums.size()
            right--; // 右指针的值已经给左边了，因此左移找到新的待更新元素
            // 因为此时左指针已经指向新值了，因此左指针不需要右移，不需要left++;它需要重新判断该值是否是需要删除的值
        }
        else
        {
            left++; // 已确定不是想要移除的值，左指针右移
        }
    }
    return left;
}
//时间复杂度：O(n^2)
//空间复杂度：O(1)
```

## 启发

1. 原地修改数组的做法，这是题目要求

1. 只要遇到"需要筛选/移动/覆盖数组元素"的问题，都可以优先考虑双指针法。

## 困难

1. 边界条件的处理

2. 指针的移动逻辑，什么时候++ 什么时候--
