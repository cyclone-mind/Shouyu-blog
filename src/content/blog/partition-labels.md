---
title: '划分字母区间'
description: '划分字母区间算法题解，使用贪心算法解决'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 贪心
  - 贪心算法
  - 字符串
  - 哈希表
  - Leetcode
---

## 题目描述

给你一个字符串`s`。我们要把这个字符串划分为尽可能多的片段，同一字母最多出现在一个片段中。例如，字符串`"ababcc"`能够被分为`["abab", "cc"]`，但类似`["aba", "bcc"]`或`["ab", "ab", "cc"]`的划分是非法的。

注意，划分结果需要满足：将所有划分结果按顺序连接，得到的字符串仍然是`s`。

返回一个表示每个字符串片段的长度的列表。

[题目链接](https://leetcode.cn/problems/partition-labels/)

https://programmercarl.com/0763.%E5%88%92%E5%88%86%E5%AD%97%E6%AF%8D%E5%8C%BA%E9%97%B4.html

## 思考

这道题直观想法，对于这个例子：

**示例 1：**

```cpp
输入：s = "ababcbacadefegdehijhklij"
输出：[9,7,8]
解释：
划分结果为 "ababcbaca"、"defegde"、"hijhklij" 。
每个字母最多出现在一个片段中。
像 "ababcbacadefegde", "hijhklij" 这样的划分是错误的，因为划分的片段数较少。
```

对于字母a因为a的右边界出现在索引8的位置，因此对于字母a来说就必须分割在索引8的右边，对于b来说右边界是5，就必须分割再索引5的右边。

这个**必须**是满足了“每个字母最多出现在一个片段中。”的条件

而正好分割在索引8而不是索引9等靠后的位置，则是贪心的体现：**字符串划分为尽可能多的片段**--为了划分地多，应该使每个片段长一点。

因此必须统计每一个字符最后出现的位置。因为题目只有常见字母，所以使用数组是比较方便的选择，下标为字符，值为最后出现的位置。

这之后，需要从头遍历字符，如果发现字符的下标和字符最后出现的位置相等了，则找到了分割点。

如图：

## 代码实现

```cpp
class Solution {
public:
    vector<int> partitionLabels(string s) {
		int hash[27] = {0};
        for(int i = 0;i < s.size();i++){
            hash[s[i] - 'a'] = i;
        }
        vector<int> result;
        int left = 0;
        int right = 0;
        for(int i = 0;i < s.size();i++){
            right = max(right, hash[s[i] - 'a']);
            if(i == right){
                result.push_back(right - left +1);
                left = right + 1;
            }
        }
        return result;
    }
};
```