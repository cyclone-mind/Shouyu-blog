---
title: '分发饼干'
description: '贪心算法典型例题：大饼干优先给大胃口的小朋友。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 贪心算法
  - 双指针
  - Leetcode
---

## 题目描述

假设你是一位很棒的家长，想要给你的孩子们一些小饼干。但是，每个孩子最多只能给一块饼干。
对每个孩子`i`，都有一个胃口值`g[i]`，这是能让孩子们满足胃口的饼干的最小尺寸；并且每块饼干`j`，都有一个尺寸`s[j]`。如果`s[j]&nbsp;>= g[i]`，我们可以将这个饼干`j`分配给孩子`i`，这个孩子会得到满足。你的目标是满足尽可能多的孩子，并输出这个最大数值。


## 思考

想要满足更多的小孩一定是**大饼干优先给大胃口小朋友**。小饼干优先给小胃口小朋友这个想是一个伪命题，因为小饼干就不能给大胃口的小朋友吃。

从后向前遍历小孩数组，用大饼干优先满足胃口大的，并统计满足小孩数量。

需要注意的是饼干数量可能比较少，因此对于每个朋友，先确定饼干还有没有了再比较能不能吃得下 ：`if(index >= 0 && (g[i] <= s[index]))`

## 代码实现

```cpp
int findContentChildren(vector<int>& g, vector<int>& s) {
    sort(g.begin(), g.end());
    sort(s.begin(), s.end());
    int index = s.size() - 1;
    int result = 0;
    for(int i = g.size() - 1;i>=0;i--){ 
        if(index >= 0 && (g[i] <= s[index])){ 
            result++; 
            index--; 
        }
    }
    return result;
}
```