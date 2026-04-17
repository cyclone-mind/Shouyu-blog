---
title: '代码随想录 栈与队列：前K个高频元素'
description: '给定一个非空的整数数组，返回其中出现频率前 k 高的元素。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 栈和队列
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

## 摘要
给定一个非空的整数数组，返回其中出现频率前 k 高的元素。

## 正文
## 题目描述

给定一个非空的整数数组，返回其中出现频率前 k 高的元素。

示例 1:

* 输入: nums = [1,1,1,2,2,3], k = 2

* 输出: [1,2]

示例 2:

* 输入: nums = [1], k = 1

* 输出: [1]

提示：

* 你可以假设给定的 k 总是合理的，且 1 ≤ k ≤ 数组中不相同的元素的个数。

* 你的算法的时间复杂度必须优于 $O(n \log n)$ , n 是数组的大小。

* 题目数据保证答案唯一，换句话说，数组中前 k 个高频元素的集合是唯一的。

* 你可以按任意顺序返回答案。

[题目链接](https://leetcode.cn/problems/top-k-frequent-elements/)

[文章链接]https://programmercarl.com/0347.%E5%89%8DK%E4%B8%AA%E9%AB%98%E9%A2%91%E5%85%83%E7%B4%A0.html

## 思路

三块内容：

1. 要统计元素出现频率

1. 对频率排序

1. 找出前K个高频元素

传统的思路是对出现的所有元素线性遍历( $O(n)$ )计算数字出现的次数/频率。随后对这些元素采用排序(最优的是$O(nlogn)$)，从高到低，选择前k个就行。

这种思路实现如下：

```cpp
#include <vector>
#include <map>
#include <algorithm> // for std::sort

// ... existing code ...

vector<int> topKFrequent(vector<int>& nums, int k) {
    // 1. 统计每个数字的频率
    std::map<int, int> freqMap;
    for (int num : nums) {
        freqMap[num]++;
    }

    // 2. 将频率和数字存储到 pair 向量中，方便排序
    // pair.first 存储频率，pair.second 存储数字
    std::vector<std::pair<int, int>> freqVector;
    for (auto const& [num, freq] : freqMap) {
        freqVector.push_back({freq, num});
    }

    // 3. 按照频率降序排序
    // 使用 lambda 表达式作为比较函数，按频率（first 元素）从大到小排序
    std::sort(freqVector.begin(), freqVector.end(), [](const std::pair<int, int>& a, const std::pair<int, int>& b) {
        return a.first > b.first;
    });

    // 4. 提取前 k 个元素
    std::vector<int> result;
    for (int i = 0; i < k; ++i) {
        result.push_back(freqVector[i].second);
    }

    return result;
}
```

这道题 Leetcode 要求时间复杂度必须优于 $O(nlogn)$。总之计算所有元素这一步肯定是没办法再优化了，能优化的只有排序。能够注意到题目只要求我们返回出出现频率前`k`高的元素，其实对剩余`n-k`个元素排序我们是没必要维护的。

对于堆来说，时间复杂度随着堆的大小而变化。

只需要记住堆维护的是一个排好序的`k`大小的容器，往里添加或删除元素，我们使得保持`k`大小不变，并且从小到大或者从大到小的顺序不变。时间复杂度取决于堆大小。

小顶堆的方法在处理数据流时也很有用，因为它不需要一次性加载所有数据并进行全局排序，而是可以增量地维护前 k 个元素。

我们依次的把所有元素入堆，堆大小不变，就意味着我们要弹出元素，弹出的元素应该是堆里面所有元素中最小的，因为题目要求我们只保留前`k`个最大的。使用小顶堆，弹出元素是就是堆中元素最小的。

另外，元素之间的顺序是频率，元素本身是数字，题目要求我们返回数字，那么需要一个容器保留这个元素，元组组成是频率和数字，元素之间的排序依据是频率。

使用小顶堆，若元素是纯数字，则直接排序，若元素是频率和数字，我们需要使用`std::pair<int, int>`来保存元素，并且排序顺序是按照`pair`中的第一个元素来。

## 代码实现

```cpp
class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int,int> freMap;
        for(auto num : nums){
            freMap[num]++;
        }
        priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> minHeap;
        for(auto const &[num,freq]:freMap){
            minHeap.push({freq,num});
            if(minHeap.size() > k){
                minHeap.pop();
            }
        }
        vector<int> result;
        while(!minHeap.empty()){
            result.push_back(minHeap.top().second);
            minHeap.pop();
        }
        reverse(result.begin(),result.end());
        return result;
    }
};
```