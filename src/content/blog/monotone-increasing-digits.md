---
title: '单调递增的数字'
description: '单调递增的数字算法题解，使用贪心算法解决'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 贪心
  - 贪心算法
  - 数学
  - Leetcode
---


## 题目描述

当且仅当每个相邻位数上的数字`x`和`y`满足`x <= y`时，我们称这个整数是**单调递增**的。

给定一个整数`n`，返回*小于或等于*`*n*`*的最大数字，且数字呈****单调递增***。

[题目链接](https://leetcode.cn/problems/monotone-increasing-digits/)

[文章讲解](https://programmercarl.com/0738.%E5%8D%95%E8%B0%83%E9%80%92%E5%A2%9E%E7%9A%84%E6%95%B0%E5%AD%97.html)

## 思考

题目要求最大数字，因此我们先试着-1，对于332这个例子，-1后是331，数字不是单调递增的，因此-1没有意义，可以让10位-1，得到322，后两位满足单调递增，继续让百位-1，得到222，百位减1之后10位和个位可以变为99

总体思路就是从后向前遍历，如果不满足单调递增就调至单调递增，如果满足就找到最后一个变化的位置，往后位数字全部变为9

例如342，遍历`i==2`，此时`str[i-1] < str[i]`那么标志位就是`i==1`，标志位-1后，从标志位往后全变成9

## 代码实现

```cpp
class Solution {
public:
    int monotoneIncreasingDigits(int n) {
        string str = to_string(n);
        int flag = str.size();
        for (int i = str.size() - 1; i > 0; i--) {
            if (str[i - 1] > str[i]) {
                str[i - 1]--;
                flag = i;
            }
        }
        for (int i = flag; i < str.size(); i++) {
            str[i] = '9';
        }
        return std::stoi(str);
    }
};
```