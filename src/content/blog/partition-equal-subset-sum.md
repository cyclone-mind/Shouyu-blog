---
title: '分割等和子集'
description: '分割等和子集算法题解，使用01背包的动态规划解决'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 背包问题
  - 01背包
  - Leetcode
---

## 题目描述

给你一个**只包含正整数**的**非空**数组`nums`。请你判断是否可以将这个数组分割成两个子集，使得两个子集的元素和相等。

**示例 1：**

```text
输入：nums = [1,5,11,5]
输出：true
解释：数组可以分割成 [1, 5, 5] 和 [11] 。
```

**示例 2：**

```text
输入：nums = [1,2,3,5]
输出：false
解释：数组不能分割成两个元素和相等的子集。
```

[题目链接](https://leetcode.cn/problems/partition-equal-subset-sum)

[文章讲解](https://programmercarl.com/0416.%E5%88%86%E5%89%B2%E7%AD%89%E5%92%8C%E5%AD%90%E9%9B%86.html)

## 思路

这道题换一个思路理解，就是我们要在数组中找到一些数，使得这些数的和为数组总和的1/2。

可以假设我们有容量为数组总和的 1/2 这么大小的一个背包。我们要求的就是把这些数组里面的一些数，能不能刚好放满这个背包。

这么理解的一个原因是，因为对于这个背包来说，数组里面的每一个数无非就是在这个背包里和不在这个背包里两种状态，并且每个树的两个状态互相不影响。那就符合我们的决策树模型。

本题的本质是，**能否把容量为 sum / 2的背包装满**。

不过有一点区别，就是一般物品是有重量和价值两个维度，而这道题这个数组这个数的大小既是重量也是价值，也就是一个维度。

我们仍然求容量为 j 的背包能装的最大价值/重量是多少，如果 dp[j] == j 说明刚好能装满，只可能小于 j ，就是装不满，不会大于 j

## 递归五部曲

##### 1、确定dp数组含义

01背包中，dp[j] 表示： 容量（所能装的重量）为j的背包，所背的物品价值最大可以为dp[j]。

### 2、递推公式

```cpp
dp[j] = max(dp[j], dp[j - weight[i]] + value[i]);
转化为
dp[j] = max(dp[j], dp[j - nums[i]] + nums[i]);
```

### 3、初始化

定义上，dp[0] = 0，其余元素因为本身非空且有max函数，所以初始化为0即可，

背包每个元素重量不超过100，个数不超过200个，因此初始化背包重量为20001即可。足够放得下

### 4、遍历顺序

一维滚动数组，先物品后容量，容量需要从大到小

```cpp
for(int i = 0;i < nums.size();i++){
    for(int j = target;j >= nums[i];j--){
        dp[j] = max(dp[j],dp[j-nums[i]] + nums[i]);
    }
}
```

##### 5、举例打印dp数组

如果 dp[j] == j 说明背包刚好放满。如果此时 j = target，元素和刚好为 target 数组总和的1/2

## 代码实现

```cpp
class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int sum = 0;
        for (int i = 0; i < nums.size(); i++)
            sum += nums[i];
        if (sum % 2)
            return false;
        int target = sum / 2;
        vector<int> dp(target + 1, 0);
        for (int i = 0; i < nums.size(); i++) {
            for (int j = target; j >= nums[i]; j--) {
                dp[j] = max(dp[j], dp[j - nums[i]] + nums[i]);
            }
        }
        return dp[target] == target;
    }
};
```