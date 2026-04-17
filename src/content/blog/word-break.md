---
title: '单词拆分'
description: '单词拆分：完全背包问题'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 动态规划
  - 完全背包
  - 字符串
  - Leetcode
---

## 题目描述

给你一个字符串`s`和一个字符串列表`wordDict`作为字典。如果可以利用字典中出现的一个或多个单词拼接出`s`则返回`true`。

**注意**不要求字典中出现的单词全部都使用，并且字典中的单词可以重复使用。

**示例 1：**

```cpp
输入: s = "leetcode", wordDict = ["leet", "code"]
输出: true
解释: 返回 true 因为 "leetcode" 可以由 "leet" 和 "code" 拼接成。
```

[题目链接](https://leetcode.cn/problems/word-break/)

[文章讲解](https://programmercarl.com/0139.%E5%8D%95%E8%AF%8D%E6%8B%86%E5%88%86.html)

## 思路

本题有两个角度，一个是分割字符串，判断是否在字典中出现过。；

另一个角度是组合字符串，用字典中的单子组合字符串。

前者本质上是回溯，不断地分割字符串，判断所有可能的分割方案分割出来的字符串是否在字典中出现过。

分割方案类似于 这道题回溯算法：分割回文串 了。那道题判断每次分割出来的字符串是否回文，这道题判断分割出来的是否在字典中出现过。

后者是背包问题，动态规划。

单词就是物品，字符串s就是背包，单词能否组成字符串s，就是问物品能不能把背包装满。

拆分时可以重复使用字典中的单词，说明就是一个完全背包！

## 递归五部曲

### 1、dp数组及下标含义

**dp[i] : 字符串长度为i的话，dp[i]为true，表示可以拆分为一个或多个在字典中出现的单词**。

### 2、递推公式

我们假设这个长度为 i 的字符串，最后一个单词为word，区间是 [j,i]，那么：

* 条件1：这个word会出现在字典里，假定 j < i

* 条件2：长度为j的字符串可以拆分为一个或多个在字典中出现的单词，即 dp[j] == true

* 满足以上两个条件认为dp[i] == true

那么如果[j,i]这个单词没有出现在字典里，那么`dp[j] == false`

```cpp
if([j, i] 这个区间的子串出现在字典里 && dp[j]是true) 那么 dp[i] = true
```

### 3、dp数组初始化

`dp[i]`的状态依靠`dp[j]`是true，才能得到true，那么dp[0]就是递推的根基，如果第一个是false，那么递推下去后面都都是false了。

### 4、确定遍历顺序

"可以重复使用字典中的单词。" 意味着是完全背包。

物品拼背包的时候，字符串是有顺序的。拿`s = "applepenapple", wordDict = ["apple", "pen"]`举例。

"apple", "pen" 是物品，那么我们要求 物品的组合一定是 "apple" + "pen" + "apple" 才能组成 "applepenapple"。

"apple" + "apple" + "pen" 或者 "pen" + "apple" + "apple" 是不可以的，那么我们就是强调物品之间顺序。

求排列就一定是先遍历背包背包再遍历物品

### 5、举例推导

输入: s = "leetcode", wordDict = ["leet", "code"]为例，dp状态如图：

## 代码实现

```cpp
bool wordBreak(string s, vector<string> &wordDict) {
    unordered_set<string> wordSet(wordDict.begin(), wordDict.end());
    vector<bool> dp(s.size() + 1, false);
    dp[0] = true;
    for (int j = 1; j <= s.size(); j++) { // 背包
        for (int i = 0; i < j; i++) {   // 物品
            string word = s.substr(i, j - i);
            if (wordSet.count(word) && dp[i]) {
                dp[j] = true;
            }
        }
    }
    return dp[s.size()];
}
```

#### 详细示例

```bash
字符串: "applepenapple"
字典: ["apple", "pen"]

初始dp数组: [true, false, false, false, false, false, false, false, false, false, false, false, false, false]

=== 计算dp[1] (子串:"a") ===
  检查分割点i=0: s[0:1]="a" 不在字典中, dp[0]=true
当前dp数组: [true, false, false, false, false, false, false, false, false, false, false, false, false, false]

=== 计算dp[2] (子串:"ap") ===
  检查分割点i=0: s[0:2]="ap" 不在字典中, dp[0]=true
  检查分割点i=1: s[1:2]="p" 不在字典中, dp[1]=false
当前dp数组: [true, false, false, false, false, false, false, false, false, false, false, false, false, false]

=== 计算dp[3] (子串:"app") ===
  检查分割点i=0: s[0:3]="app" 不在字典中, dp[0]=true
  检查分割点i=1: s[1:3]="pp" 不在字典中, dp[1]=false
  检查分割点i=2: s[2:3]="p" 不在字典中, dp[2]=false
当前dp数组: [true, false, false, false, false, false, false, false, false, false, false, false, false, false]

=== 计算dp[4] (子串:"appl") ===
  检查分割点i=0: s[0:4]="appl" 不在字典中, dp[0]=true
  检查分割点i=1: s[1:4]="ppl" 不在字典中, dp[1]=false
  检查分割点i=2: s[2:4]="pl" 不在字典中, dp[2]=false
  检查分割点i=3: s[3:4]="l" 不在字典中, dp[3]=false
当前dp数组: [true, false, false, false, false, false, false, false, false, false, false, false, false, false]

=== 计算dp[5] (子串:"apple") ===
  检查分割点i=0: s[0:5]="apple" 在字典中, dp[0]=true → 设置dp[5]=true
当前dp数组: [true, false, false, false, false, true, false, false, false, false, false, false, false, false]

=== 计算dp[6] (子串:"applep") ===
  检查分割点i=0: s[0:6]="applep" 不在字典中, dp[0]=true
  检查分割点i=1: s[1:6]="pplep" 不在字典中, dp[1]=false
  检查分割点i=2: s[2:6]="plep" 不在字典中, dp[2]=false
  检查分割点i=3: s[3:6]="lep" 不在字典中, dp[3]=false
  检查分割点i=4: s[4:6]="ep" 不在字典中, dp[4]=false
  检查分割点i=5: s[5:6]="p" 不在字典中, dp[5]=true
当前dp数组: [true, false, false, false, false, true, false, false, false, false, false, false, false, false]

=== 计算dp[7] (子串:"applepe") ===
  检查分割点i=0: s[0:7]="applepe" 不在字典中, dp[0]=true
  检查分割点i=1: s[1:7]="pplepe" 不在字典中, dp[1]=false
  检查分割点i=2: s[2:7]="plepe" 不在字典中, dp[2]=false
  检查分割点i=3: s[3:7]="lepe" 不在字典中, dp[3]=false
  检查分割点i=4: s[4:7]="epe" 不在字典中, dp[4]=false
  检查分割点i=5: s[5:7]="pe" 不在字典中, dp[5]=true
  检查分割点i=6: s[6:7]="e" 不在字典中, dp[6]=false
当前dp数组: [true, false, false, false, false, true, false, false, false, false, false, false, false, false]

=== 计算dp[8] (子串:"applepen") ===
  检查分割点i=0: s[0:8]="applepen" 不在字典中, dp[0]=true
  检查分割点i=1: s[1:8]="pplepen" 不在字典中, dp[1]=false
  检查分割点i=2: s[2:8]="plepen" 不在字典中, dp[2]=false
  检查分割点i=3: s[3:8]="lepen" 不在字典中, dp[3]=false
  检查分割点i=4: s[4:8]="epen" 不在字典中, dp[4]=false
  检查分割点i=5: s[5:8]="pen" 在字典中, dp[5]=true → 设置dp[8]=true
当前dp数组: [true, false, false, false, false, true, false, false, true, false, false, false, false, false]

=== 计算dp[9] (子串:"applepena") ===
  检查分割点i=0: s[0:9]="applepena" 不在字典中, dp[0]=true
  检查分割点i=1: s[1:9]="pplepena" 不在字典中, dp[1]=false
  检查分割点i=2: s[2:9]="plepena" 不在字典中, dp[2]=false
  检查分割点i=3: s[3:9]="lepena" 不在字典中, dp[3]=false
  检查分割点i=4: s[4:9]="epena" 不在字典中, dp[4]=false
  检查分割点i=5: s[5:9]="pena" 不在字典中, dp[5]=true
  检查分割点i=6: s[6:9]="ena" 不在字典中, dp[6]=false
  检查分割点i=7: s[7:9]="na" 不在字典中, dp[7]=false
  检查分割点i=8: s[8:9]="a" 不在字典中, dp[8]=true
当前dp数组: [true, false, false, false, false, true, false, false, true, false, false, false, false, false]

=== 计算dp[10] (子串:"applepenap") ===
  检查分割点i=0: s[0:10]="applepenap" 不在字典中, dp[0]=true
  检查分割点i=1: s[1:10]="pplepenap" 不在字典中, dp[1]=false
  检查分割点i=2: s[2:10]="plepenap" 不在字典中, dp[2]=false
  检查分割点i=3: s[3:10]="lepenap" 不在字典中, dp[3]=false
  检查分割点i=4: s[4:10]="epenap" 不在字典中, dp[4]=false
  检查分割点i=5: s[5:10]="penap" 不在字典中, dp[5]=true
  检查分割点i=6: s[6:10]="enap" 不在字典中, dp[6]=false
  检查分割点i=7: s[7:10]="nap" 不在字典中, dp[7]=false
  检查分割点i=8: s[8:10]="ap" 不在字典中, dp[8]=true
  检查分割点i=9: s[9:10]="p" 不在字典中, dp[9]=false
当前dp数组: [true, false, false, false, false, true, false, false, true, false, false, false, false, false]

=== 计算dp[11] (子串:"applepenapp") ===
  检查分割点i=0: s[0:11]="applepenapp" 不在字典中, dp[0]=true
  检查分割点i=1: s[1:11]="pplepenapp" 不在字典中, dp[1]=false
  检查分割点i=2: s[2:11]="plepenapp" 不在字典中, dp[2]=false
  检查分割点i=3: s[3:11]="lepenapp" 不在字典中, dp[3]=false
  检查分割点i=4: s[4:11]="epenapp" 不在字典中, dp[4]=false
  检查分割点i=5: s[5:11]="penapp" 不在字典中, dp[5]=true
  检查分割点i=6: s[6:11]="enapp" 不在字典中, dp[6]=false
  检查分割点i=7: s[7:11]="napp" 不在字典中, dp[7]=false
  检查分割点i=8: s[8:11]="app" 不在字典中, dp[8]=true
  检查分割点i=9: s[9:11]="pp" 不在字典中, dp[9]=false
  检查分割点i=10: s[10:11]="p" 不在字典中, dp[10]=false
当前dp数组: [true, false, false, false, false, true, false, false, true, false, false, false, false, false]

=== 计算dp[12] (子串:"applepenappl") ===
  检查分割点i=0: s[0:12]="applepenappl" 不在字典中, dp[0]=true
  检查分割点i=1: s[1:12]="pplepenappl" 不在字典中, dp[1]=false
  检查分割点i=2: s[2:12]="plepenappl" 不在字典中, dp[2]=false
  检查分割点i=3: s[3:12]="lepenappl" 不在字典中, dp[3]=false
  检查分割点i=4: s[4:12]="epenappl" 不在字典中, dp[4]=false
  检查分割点i=5: s[5:12]="penappl" 不在字典中, dp[5]=true
  检查分割点i=6: s[6:12]="enappl" 不在字典中, dp[6]=false
  检查分割点i=7: s[7:12]="nappl" 不在字典中, dp[7]=false
  检查分割点i=8: s[8:12]="appl" 不在字典中, dp[8]=true
  检查分割点i=9: s[9:12]="ppl" 不在字典中, dp[9]=false
  检查分割点i=10: s[10:12]="pl" 不在字典中, dp[10]=false
  检查分割点i=11: s[11:12]="l" 不在字典中, dp[11]=false
当前dp数组: [true, false, false, false, false, true, false, false, true, false, false, false, false, false]

=== 计算dp[13] (子串:"applepenapple") ===
  检查分割点i=0: s[0:13]="applepenapple" 不在字典中, dp[0]=true
  检查分割点i=1: s[1:13]="pplepenapple" 不在字典中, dp[1]=false
  检查分割点i=2: s[2:13]="plepenapple" 不在字典中, dp[2]=false
  检查分割点i=3: s[3:13]="lepenapple" 不在字典中, dp[3]=false
  检查分割点i=4: s[4:13]="epenapple" 不在字典中, dp[4]=false
  检查分割点i=5: s[5:13]="penapple" 不在字典中, dp[5]=true
  检查分割点i=6: s[6:13]="enapple" 不在字典中, dp[6]=false
  检查分割点i=7: s[7:13]="napple" 不在字典中, dp[7]=false
  检查分割点i=8: s[8:13]="apple" 在字典中, dp[8]=true → 设置dp[13]=true
当前dp数组: [true, false, false, false, false, true, false, false, true, false, false, false, false, true]

最终结果: 可以拆分
1
```