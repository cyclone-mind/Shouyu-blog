---
title: '区间和'
description: '使用前缀和技巧快速计算数组指定区间内元素的总和。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 数组
  - 前缀和
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

[题目链接](https://kamacoder.com/problempage.php?pid=1070)

[文章链接](https://programmercarl.com/kamacoder/0058.%E5%8C%BA%E9%97%B4%E5%92%8C.html)

题目描述

​ 给定一个整数数组 Array，请计算该数组在每个指定区间内元素的总和。

输入描述

​ 第一行输入为整数数组 Array 的长度 n，接下来 n 行，每行一个整数，表示数组的元素。随后的输入为需要计算总和的区间，直至文件结束。

输出描述

​ 输出每个指定区间内元素的总和。

输入示例

```text
5
1
2
3
4
5
0 1
1 3
```

输出示例

```text
3
9
```

数据范围：

0 < n <= 100000

## 思路

**在一个数组内随意划定一个区间，求和**。这看起来很简单一个 for 循环就行，但是如果要求 n 次呢？岂不是又要一个 for 循环？就 o(n^2)了啊。

其实，对于数组区间和的问题，可以提前计算累计和或叫前缀和。

前缀和的思想是重复利用计算过的子数组之和，从而降低区间查询需要累加计算的次数。

有一个 `vec` 数组，先求出来前缀和数组 p。

例如我们想统计，在 `vec` 数组上 下标 2 到下标 5 之间的累加和，那是不是就用 `p[5] - p[1]` 就可以了。

为什么呢？

```text
p[1] = vec[0] + vec[1];
p[5] = vec[0] + vec[1] + vec[2] + vec[3] + vec[4] + vec[5];
p[5] - p[1] = vec[2] + vec[3] + vec[4] + vec[5];
```

求 a 到 b 的区间和，就`p[b]-p[a-1]`就行。

```cpp
#include <iostream>
#include <vector>
using namespace std;
int main()
{
    int n, a, b;
    cin >> n;
    vector<int> vec(n);
    vector<int> p(n);
    int persum = 0;
    for (int i = 0; i < n; i++)
    {
        // cin >> vec[i];
        scanf("%d",&vec[i]);
        persum += vec[i]; // 在输入的时候就进行计算其前缀和，前缀和是累加的，每得到一个值就把他填充到前缀和数组中
        p[i] = persum;
    }
    while (cin >> a >> b)
    {
        int sum;
        if (a == 0)
            sum = p[b]; // 特殊情况，这是因为如果不设置这个判断，按照下面计算就会出现p[0-1]，超出索引范围了
        else
            sum = p[b] - p[a - 1];
        // cout << sum << endl;
        printf("%d\n",sum);
    }
}
```
