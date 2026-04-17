---
title: '分发糖果'
description: '贪心算法解决分发糖果问题，相邻评分高的孩子获得更多糖果。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 贪心算法
  - 数组
  - Leetcode
---

## 题目描述

老师想给孩子们分发糖果，有 N 个孩子站成了一条直线，老师会根据每个孩子的表现，预先给他们评分。

你需要按照以下要求，帮助老师给这些孩子分发糖果：

* 每个孩子至少分配到 1 个糖果。

* 相邻的孩子中，评分高的孩子必须获得更多的糖果。

那么这样下来，老师至少需要准备多少颗糖果呢？

[题目链接](https://leetcode.cn/problems/candy/)

[文章讲解](https://programmercarl.com/0135.%E5%88%86%E5%8F%91%E7%B3%96%E6%9E%9C.html)

## 思考

每个孩子的糖果数取决于左右两个孩子，如果我们遍历每个孩子，然后比较左右评分分配糖果，那么我们会顾此失彼，为什么？

在从左到右的一次遍历中，当我们处理位置i时，`candyVec[i+1]`的值可能还没有被正确计算。

考虑ratings = [1, 2, 3, 2, 1]：

```txt
索引:    0  1  2  3  4
评分:    1  2  3  2  1
初始:    1  1  1  1  1
```

如果试图同时考虑左右两边：

1. 处理索引1（评分2）：

比左边高：`candyVec[1] = candyVec[0] + 1 = 2`
比右边低：无需处理
结果：`candyVec[1] = 2`

1. 处理索引2（评分3）：

比左边高：`candyVec[2] = candyVec[1] + 1 = 3`
比右边高：`candyVec[2] = candyVec[3] + 1 = ? `（candyVec[3]还没正确计算）
这里出现问题：我们不知道`candyVec[3]`应该是多少

1. 处理索引3（评分2）：

比左边高：`candyVec[3] = candyVec[2] + 1 = ? `（`candyVec[2]`在上面被设为3）
比右边高：`candyVec[3] = candyVec[4] + 1 = 2`
应该取哪个值？这里就顾此失彼了

我们应该进行两次遍历

先确定右边评分大于左边的情况（也就是从前向后遍历）

此时局部最优：只要右边评分比左边大，右边的孩子就多一个糖果，全局最优：相邻的孩子中，评分高的右孩子获得比左边孩子更多的糖果。

再确定左孩子大于右孩子的情况（从后向前遍历）

为什么不能从前向后遍历？

因为 `rating[5]`与`rating[4]`的比较 要利用上 `rating[5]`与`rating[6]`的比较结果，所以 要从后向前遍历。

如果从前向后遍历，`rating[5]`与`rating[4]`的比较 就不能用上 `rating[5]`与`rating[6]`的比较结果了 。

整体而言就是

采用了两次贪心的策略：

* 一次是从左到右遍历，只比较右边孩子评分比左边大的情况。

* 一次是从右到左遍历，只比较左边孩子评分比右边大的情况。

## 代码实现

```cpp
class Solution {
public:
    int candy(vector<int>& ratings) {
        vector<int> candyVec(ratings.size(), 1);
        // 从前向后
        for (int i = 1; i < ratings.size(); i++) {
            if (ratings[i] > ratings[i - 1]) candyVec[i] = candyVec[i - 1] + 1;
        }
        // 从后向前
        for (int i = ratings.size() - 2; i >= 0; i--) {
            if (ratings[i] > ratings[i + 1] ) {
                candyVec[i] = max(candyVec[i], candyVec[i + 1] + 1);
            }
        }
        // 统计结果
        int result = 0;
        for (int i = 0; i < candyVec.size(); i++) result += candyVec[i];
        return result;
    }
};
```
