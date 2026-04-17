---
title: '目标和'
description: '目标和问题：01背包与回溯算法'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 01背包
  - 回溯
  - Leetcode
---

## 题目描述

给你一个非负整数数组`nums`和一个整数`target`。

向数组中的每个整数前添加`'+'`或`'-'`，然后串联起所有整数，可以构造一个**表达式**：

* 例如，nums = [2, 1] ，可以在 2 之前添加 '+' ，在 1 之前添加 '-' ，然后串联起来得到表达式 "+2-1" 。

返回可以通过上述方法构造的、运算结果等于`target`的不同**表达式**的数目。

**示例 1：**

```text
输入：nums = [1,1,1,1,1], target = 3
输出：5
解释：一共有 5 种方法让最终目标和为 3 。
-1 + 1 + 1 + 1 + 1 = 3
+1 - 1 + 1 + 1 + 1 = 3
+1 + 1 - 1 + 1 + 1 = 3
+1 + 1 + 1 - 1 + 1 = 3
+1 + 1 + 1 + 1 - 1 = 3
```

[题目链接](https://leetcode.cn/problems/target-sum)

[文章讲解](https://programmercarl.com/0494.%E7%9B%AE%E6%A0%87%E5%92%8C.html)

## 思路

每个整数要不就是正的，要不就是负的。这也是一个决策的过程。符合**决策树模型**

仔细看问题，本题需要选出一些数作为正数，我们可以设置其和为 left；另外再选择一些数作为负数，我们设置和为 right。那么 left + right = sum，这个 sum 是固定的。

另外，题目还告诉我们，有一个 target，这个 target = left - right 。

所以 left - (sum - left) = target 推导出 left = (target + sum)/2 。

target是固定的，sum是固定的，left就可以求出来。

此时问题就是**在集合nums中找出和为left的组合**。

所以其实可以用回溯法来得到所有的不同表达式，当然其数量也就有了。

不过这道题没有要求我们给出不同的表达式，而只是要求我们给出不同表达式的数目。因此，使用动态规划是可行的。

所以此时可以转化为**用 nums中的元素 来装满容量为 left 的背包有几种方法**。

我们由target = left - right和left + right = sum推出2*left = (target + sum)。

这意味着target + sum只能是偶数。如果不是偶数，那么就没有方案。

即，left有可能是小数，target + sum不能够被2整除。那么，这个时候拥有小数容量的背包是怎么装都装不满的。所以说，此时没有方案。

```cpp
if ((target + sum) % 2 == 1) return 0; // 此时没有方案
```

另外target的绝对值大于sum的话，意味着即使我们将`nums`数组中的所有数字都加上正号（得到最大的可能和`sum`），或者都加上负号（得到最小的可能和`-sum`），我们都无法达到`target`这个值。因为任何组合的和的绝对值都不可能超过`sum`。在这种情况下，函数直接返回`0`，

```cpp
if(abs(target) > sum) return 0;
```

所以说这道题，虽然是用物品来装背包，但是求的并非最多能装多少，而是恰好装满有多少种方法。而这其实就是一个组合问题了。

## 递归五部曲

### 1、dp数组及下标含义

`dp[i][j]`：使用 下标为 [0, i] 的 nums[i] 能够凑满 j（包括 j ）这么大容量的包，有`dp[i][j]`种方法。

### 2.、递推公式

考虑递推推公式的时候，先可以固定一个状态维度（容量）来考虑另一个维度的前一个状态（是否放物品 i ）会是什么样。

这道题假设 举例 nums = [1,1,1,1,1], target = 3

此时状态： i = 2, j  = 2。

**容量为2 的背包，如果放 物品2 有几种方法呢**？

首先 要在背包里 先把物品2的容量空出来， 装满 刨除物品2容量 的背包 有几种方法呢？

刨除物品2容量后的背包容量为 1。

此时装满背包容量为1 有`dp[1][1]`种方法，即： 不放物品2，背包容量为1，只考虑物品 0 和 物品 1，有`dp[1][1]`种方法。

**容量为2 的背包，如果不放 物品2 有几种方法呢**？

有`dp[1][2]`种方法，即 背包容量为2，只考虑物品0 和 物品1 ，有`dp[1][2]`种方法

所以`dp[2][2] = dp[1][2] + dp[1][1]`

以上过程，抽象化如下：

* 不放物品i：即背包容量为j，里面不放物品i，装满有dp[i - 1][j]中方法。

* 放物品i： 即：先空出物品i的容量，背包容量为（j - 物品i容量），放满背包有 dp[i - 1][j - 物品i容量] 种方法。

本题中，物品 i 的容量是nums[i]，价值也是nums[i]。

递推公式：`dp[i][j] = dp[i - 1][j] + dp[i - 1][j - nums[i]];`

不过写完这个之后，需要注意这个 j - nums[i] 不能小于0就行了。如果 nums[i] > j 那么就是背包里一定不妨物品 i ，那就是对应第一种情况。

### 3、dp数组初始化

从递推公式上看，I，J 由上方和左上方推出。所以要初始化第一层和第一列。

第一列：装满背包容量为0的方法数量是1，即什么都不放。

第一层的话，对于第一个物品，把容量为 j 的背包填满就是当背包容量和物品 0 的容量一致时，方法为 1，正好填满，其余都是为 0。所以说，要么是装不下和装不满（其余位置），要么是不装（左上角）。要么是正好装下（物品0重量等于背包容量）

还需要考虑一种特殊情况，就是装满背包容量为0的方法。什么都不放就等于放一个重量为0的物品。

> 呃，这道题leetcode上说了是非负整数。也就是说，不存在重量为零的物品。所以说，这个情况其实不考虑也能得到正确答案。

举个例子：

有两个物品，物品0为0， 物品1为0，装满背包容量为0的方法有几种。

* 放0件物品

* 放物品0

* 放物品1

* 放物品0 和 物品1

此时是有4种方法。

其实就是算数组里有t个0，然后按照组合数量求，即 2^t 。

```cpp
int zero_count = 0;
for(int i = 0;i < nums.size();i++){
    if(nums[i] == 0) zero_count = 0;
    dp[i][0] = (int) pow(2.0, zero_count);
}
```

### 4、确定遍历顺序

从递推公式上看，遍历顺序应该是从上到下，从左到右。对于二维数组，先 从上到下 ，再从左到右遍历   还是先 从左到右，再从上到下 这两种顺序其实都可以。

因为这两种顺序确保了之前的 i,j 之前的状态是存在的，`dp[i - 1][j]`+`dp[i - 1][j - nums[i]]`已有值，已经计算过。

```cpp
for (int i = 1; i < nums.size(); i++) { // 行，遍历物品
    for (int j = 0; j <= bagSize; j++) { // 列，遍历背包
    }
}
```

### 5、举例推导

输入：nums: [1, 1, 1, 1, 1], target: 3

bagSize = (target + sum) / 2 = (3 + 5) / 2 = 4

dp数组状态变化如下：

## 代码实现

二维数组：

```cpp
class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        int sum = 0;
        for (int i = 0; i < nums.size(); i++) sum += nums[i];
        if (abs(target) > sum) return 0; // 此时没有方案
        if ((target + sum) % 2 == 1) return 0; // 此时没有方案
        int bagSize = (target + sum) / 2;
        
        vector<vector<int>> dp(nums.size(), vector<int>(bagSize + 1, 0));
        
        // 初始化最上行
        if (nums[0] <= bagSize) dp[0][nums[0]] = 1; 

        // 初始化最左列，最左列其他数值在递推公式中就完成了赋值
        dp[0][0] = 1; 

        int numZero = 0;
        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] == 0) numZero++;
            dp[i][0] = (int) pow(2.0, numZero);
        }

        // 以下遍历顺序行列可以颠倒
        for (int i = 1; i < nums.size(); i++) { // 行，遍历物品
            for (int j = 0; j <= bagSize; j++) { // 列，遍历背包
                if (nums[i] > j) dp[i][j] = dp[i - 1][j]; 
                else dp[i][j] = dp[i - 1][j] + dp[i - 1][j - nums[i]];
            }
        }
        return dp[nums.size() - 1][bagSize];
    }
};
```

从递推公式上来看，i j 只依赖于上一层：i-1层。

所以可以将二维dp数组压缩成一维dp数组

`dp[i][j]`去掉 行的维度，即 dp[j]，表示：填满j（包括j）这么大容积的包，有dp[j]种方法

递推公式:`dp[j] = dp[j] + dp[j - nums[i]]`

初始化：就像初始化二维数组的第一层那样就行

遍历顺序，先物品，正序，再背包，倒序

```cpp
class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        int sum = 0;
        for (int i = 0; i < nums.size(); i++) sum += nums[i];
        if (abs(target) > sum) return 0; // 此时没有方案
        if ((target + sum) % 2 == 1) return 0; // 此时没有方案
        int bagSize = (target + sum) / 2;
        vector<int> dp(bagSize + 1, 0);
        dp[0] = 1;// 背包容量为0，什么也不装也是一种方法。
        for (int i = 0; i < nums.size(); i++) {
            for (int j = bagSize; j >= nums[i]; j--) {
                dp[j] += dp[j - nums[i]];
            }
        }
        return dp[bagSize];
    }
};
```

#### 物品重量为0

考虑了物品重量为0的情况，有些多此一举：

1. 处理非零元素: 首先，它使用动态规划（类似于 0/1 背包问题）来计算仅使用数组中的非零元素可以得到的所有可能子集和。dp[j] 表示使用非零元素能够组成和为 j 的方式的数量。

1. 处理零元素: 在计算出非零元素的所有组合后，它会考虑数组中的零。对于数组中的每一个零，我们都可以选择给它加上 +0 或 -0，这两种选择都不会改变总和，但会增加组合的可能性。如果有 zero_count 个零，那么每一种由非零元素组成的有效组合，都可以与这 zero_count 个零的 2^zero_count 种符号分配方式相结合。 因此，在初始化 dp 数组时，dp[0] 被设置为 pow(2, zero_count)。这意味着，在开始计算非零元素对 DP 表的影响之前，就已经为零元素的所有可能组合方式预留了基础。在后续的 DP 迭代中，会跳过零元素（if (nums[i] == 0) continue;），因为零对子集和本身没有贡献，其影响已在 dp[0] 的初始化中体现。

```cpp
int findTargetSumWays(vector<int> &nums, int target) {
    int sum = 0;
    int zero_count = 0;
    for (int i = 0; i < nums.size(); i++) {
        sum += nums[i];
        if (nums[i] == 0)
            zero_count++;
    };
    if (abs(target) > sum)
        return 0;
    if ((sum + target) % 2 != 0)
        return 0; // 检查 (sum + target) 是否能被 2 整除
    
    int target_sum = (sum + target) / 2;
    vector<int> dp(target_sum + 1, 0);
    dp[0] = pow(2, zero_count);

    std::cout << "初始dp数组: ";
    for (int k = 0; k <= target_sum; k++) {
        std::cout << dp[k] << " ";
    }
    std::cout << std::endl;

    for (int i = 0; i < nums.size(); i++) {
        if (nums[i] == 0)
            continue;
        for (int j = target_sum; j >= nums[i]; j--) {
            dp[j] += dp[j - nums[i]];
        }
        std::cout << "处理完 nums[" << i << "] = " << nums[i]
                  << " 后的dp数组: ";
        for (int k = 0; k <= target_sum; k++) {
            std::cout << dp[k] << " ";
        }
        std::cout << std::endl;
    }
    return dp[target_sum];
}
```