---
title: 'K次取反后最大化数组和'
description: 'K次取反后最大化数组和算法题解，使用贪心算法解决'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 贪心
  - 贪心算法
  - 数组
  - Leetcode
---

## 题目描述

给定一个整数数组 A，我们只能用以下方法修改该数组：我们选择某个索引 i 并将 A[i] 替换为 -A[i]，然后总共重复这个过程 K 次。（我们可以多次选择同一个索引 i。）

以这种方式修改数组后，返回数组可能的最大和。

[题目链接](https://leetcode.cn/problems/maximize-sum-of-array-after-k-negations/)

[文章讲解](https://leetcode.cn/problems/maximize-sum-of-array-after-k-negations)

## 思考

### 贪心解法

本题思路应该比较简单，尽可能让小的负数取反，尽可能让小的非负数取反。整体和最大。

首先应该把尽可能小的负数取反，如果所有负数都取反了，还不够k次，那么此时就应该找数值最小的非负整数取反。

又因为可以多次反转同一个索引，所以我们只需要逮着同一个非负整数反转就行。

还有一点需要注意的是，选择非负整数反转的时候不一定选择原生数反转，还有可能选择原来是负数的（但经过反转）的数。

这样达到全局最优。

解题步骤：

* 第一步：将数组按照绝对值大小从大到小排序，注意要按照绝对值的大小

* 第二步：从前向后遍历，遇到负数将其变为正数，同时K--

* 第三步：如果K还大于0，那么反复转变数值最小的元素，将K用完

* 第四步：求和

## 代码实现

```cpp
int largestSumAfterKNegations(vector<int>& A, int K){
    std::sort(A.begin(),A.end(),[](int a,int b){return abs(a) > abs(b);});
    for(int i = 0;i<A.size();i++){
        if(A[i] < 0 && K > 0){
            A[i] *= -1;
            K--;
        }
    }
    if(K % 2 == 1) A[A.size()-1]*=-1;
    int result = 0;
    for(auto a:A){result+=a;}
    return result;
}
```