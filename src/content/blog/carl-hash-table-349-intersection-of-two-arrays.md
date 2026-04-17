---
title: '代码随想录 哈希表：349. 两个数组的交集'
description: '给定两个数组nums1和nums2，返回它们的交集。输出结果中的每个元素一定是唯一的。'
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

[题目链接](https://leetcode.cn/problems/intersection-of-two-arrays/)

[文章链接]https://programmercarl.com/0349.%E4%B8%A4%E4%B8%AA%E6%95%B0%E7%BB%84%E7%9A%84%E4%BA%A4%E9%9B%86.html

## 题目描述

给定两个数组`nums1`和`nums2`，返回*它们的 交集*。输出结果中的每个元素一定是**唯一**的。我们可以**不考虑输出结果的顺序**。

**示例 1：**

```text
输入：nums1 = [1,2,2,1], nums2 = [2,2]
输出：[2]
```

**示例 2：**

```text
输入：nums1 = [4,9,5], nums2 = [9,4,9,8,4]
输出：[9,4]
解释：[4,9] 也是可通过的
```

**提示：**

* 1 <= nums1.length, nums2.length <= 1000

* 0 <= nums1[i], nums2[i] <= 1000

## 思路

交集就是在元素在数组 1 中出现过，也在数组 2 中出现过。思考上一道题：字符在两个字符串中出现次数的比较。换到这里，数字在两个数组中是否同时出现-》数字在两个数组中出现次数都大于 1-》数字在两个数组中出现次数的比较。

咦？是不是属于一类的问题？没错。

那上题是把字符串转变为了数组计数器（数组），那么这次也要把数组转变为数组？（数字做索引，出现次数做值？）不不不，上次字符个数是有限的，共 26 个，很少，数组合适，这道题数组中的元素种类（也就是数字范围）会很大，**而且如果哈希值比较少、特别分散、跨度非常大，使用数组就造成空间的极大浪费。**比如数组中有个 0 和 1 和 1000000，我们要建立一个长度为 1000002 的数组？这是极大的浪费！

另外题目中比较的次数只可能为 0 或 1，也就是有没有出现，这时使用 set 有天然的优势。

此时就要使用另一种结构体了，set ，关于 set，C++ 给提供了如下三种可用的数据结构：

* std::set

* std::multiset

* std::unordered_set

std::set 和 std::multiset 底层实现都是红黑树，std::unordered_set 的底层实现是哈希表， 使用 unordered_set 读写效率是最高的，并不需要对数据进行排序，而且还不要让数据重复，所以选择 unordered_set。

所以整体思路就是

先建立一个空的结果 unordered_set ，然后数组 1 转变为 unordered_set，然后遍历数组 2，看看是否在 unordered_set 出现过，如果出现，则加入到结果中，如果没出现，则跳过。

```cpp
class Solution {
public:
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        unordered_set<int> result_set; // 存放结果，之所以用set是为了给结果集去重
        unordered_set<int> nums_set(nums1.begin(), nums1.end());
        for (int num : nums2) {
            // 发现nums2的元素 在nums_set里又出现过
            if (nums_set.find(num) != nums_set.end()) {
                result_set.insert(num);
            }
        }
        return vector<int>(result_set.begin(), result_set.end());
    }
};
```