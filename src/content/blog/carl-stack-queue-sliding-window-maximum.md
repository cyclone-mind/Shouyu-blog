---
title: '代码随想录 栈与队列：239. 滑动窗口最大值'
description: '给你一个整数数组nums，有一个大小为k的滑动窗口从数组的最左侧移动到数组的最右侧。返回滑动窗口中的最大值。'
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

# 代码随想录 栈与队列：滑动窗口最大值

**发布日期:** 2025/12/21
**阅读时间:** 1 分钟
**标签:** 算法笔记, 栈和队列, 代码随想录, 数据结构与算法, 栈与队列

## 正文
## 题目描述

给你一个整数数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 k 个数字。滑动窗口每次只向右移动一位。

返回 滑动窗口中的最大值 。

[题目链接](https://leetcode.cn/problems/sliding-window-maximum[文章讲解]https://programmercarl.com/0239.%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3%E6%9C%80%E5%A4%A7%E5%80%BC.html)

## 思路

正常思路，维护一个k大小的容器，如数组，移动的时候需要，添加右侧新元素，删除最靠左的旧元素，线性查找找到窗口内最大值。这样时间复杂度是 O(n*k)。

这里可以优化的是线性查找最大值这个操作，如果时间复杂度不是遍历而是O(1)的就好了。

一个显而易见的想法是这个容器从大到小排列，如一个单调队列，这样添加元素在队尾是O(1)，取最大值是 front，但是又出现了问题是弹出元素时这个需要弹出的元素可能是中间的元素。

比如 nums = [1,3,-1,-3,5,3,6,7], k = 3。这样首先维护的一个 [3,1,-1] 这样的队列，右移一位需要添加 -3， 去除 1。这里 1 是在中间，那么问题来了，已经排序之后的队列 怎么能把窗口要移除的元素（这个元素可不一定是最大值）弹出呢。

实际上队列没有必要维护窗口里的所有元素，**只需要维护有可能成为窗口里最大值的元素**就可以了，同时保证队列里的元素数值是由大到小的。怎么理解 ？对于前三个元素1，3，-1。已经排好序了，3在最前面。窗口右移一位，**需要弹出的这个 1 不可能成为窗口最大值**，因为它没有3大，并且也在3的左边。那么我们为什么还要把 1 放到我们的队列里呢？我们永远也用不到它！

那么怎么实现呢？

设计单调队列的时候，pop，和push操作要保持如下规则：

1. pop(value)：如果窗口移除的元素value等于单调队列的出口元素，那么队列弹出元素，否则不用任何操作

1. push(value)：如果push的元素value大于入口元素的数值，那么就将队列入口的元素弹出，直到push元素的数值小于等于队列入口元素的数值为止

通过如上规则，每次窗口移动就可以通过  front() 就拿到最大值。

## 代码实现

```cpp
class Solution {
public:
    class MyQue {
        public:
        deque<int> que;
        MyQue(){}
        int front(){
            return que.front();
        }
        void push(int num){
            while(!que.empty() && que.back() < num){
                que.pop_back();
            }
            que.push_back(num);
        }
        void pop(int num){
            if(!que.empty() && que.front() == num){
                que.pop_front();
            }
        }
    };
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        MyQue que;
        for(int i = 0;i < k;i++){
            que.push(nums[i]);
        }
        vector<int> result;
        result.push_back(que.front());
        for(int i = k;i < nums.size();i++){
            que.push(nums[i]);
            que.pop(nums[i-k]);
            result.push_back(que.front());
        }
        return result;
    }
};
```