---
title: '代码随想录 哈希表：454. 四数相加 II'
description: '给定四个整数数组nums1、nums2、nums3和nums4，计算有多少个元组(i, j, k, l)能满足0 <= i, j, k, l < n且nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0。'
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

[题目链接](https://leetcode.cn/problems/4sum-ii/description/)

[文章讲解](https://programmercarl.com/0454.%E5%9B%9B%E6%95%B0%E7%9B%B8%E5%8A%A0II.html)

## 题目描述

给你四个整数数组`nums1`、`nums2`、`nums3`和`nums4`，数组长度都是`n`，请你计算有多少个元组`(i, j, k, l)`能满足：

* 0 <= i, j, k, l < n

* nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0

## 思路

四个数组中各找一个数，相加等于 0。直观的想法是 4 个嵌套的 for 循环，然后判断出来和是否等于 n。

思考，假设四个数分别是 a,b,c,d，如果我们先确定 a 和 b，然后再找有没有 0-(c+d)。好像还是 4 个循环？不是的，先双层 for 循环把所有的 a+b 记录起来放进一个哈希表 1，然后同样双层 for 循环把所有的 c+d 记录起来放进一个哈希表吗？不是的，直接另起双层 for 循环找就行。找谁？找 0-(c+d) 在不在哈希表 1 里面。

或者说

如果用四重循环暴力枚举所有组合，时间复杂度是 O(n^4)，数据量大时会超时。我们可以用哈希表优化到 O(n^2)：

1. 分组思想：把四个数组分成两组，先枚举前两个数组的所有和，存到哈希表里，key 是和，value 是出现次数。

1. 查找互补：再枚举后两个数组的所有和，查找哈希表中是否存在"相反数"，即 0 - (c + d)。如果存在，说明这四个数的和为 0，把出现次数加到答案里。

因为题目给定`-228 <= nums1[i], nums2[i], nums3[i], nums4[i] <= 228`所以使用 map 作为哈希表比较合适。

```cpp
#include <unordered_map>
#include <vector>
#include <iostream>
using namespace std;

int fourSumCount(vector<int> &nums1, vector<int> &nums2, vector<int> &nums3, vector<int> &nums4)
{
    unordered_map<int, int> record;

    for (int a : nums1)
    {
        for (int b : nums2)
        {
            record[a + b]++;
        }
    }
    int count = 0;
    for (int c : nums3)
    {
        for (int d : nums4)
        {
            if (record.find(0 - (c + d)) != record.end())
            {
                count += record[0 - (c + d)];
            }
        }
    }
    return count;
}
```

### 启发

1. 理解用什么数据结构做哈希表，根据数据范围和所要求存放的数据种类。

1. int 可能超范围，需要检查是否需要使用 long 强转