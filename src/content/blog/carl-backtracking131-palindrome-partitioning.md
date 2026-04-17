---
title: '131. 分割回文串'
description: '给你一个字符串 s，请你将 s 分割成一些子串，使每个子串都是回文串。返回 s 所有可能的分割方案。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 回溯
  - 代码随想录
  - 数据结构与算法
  - Leetcode
  - 回溯算法
---

## 题目描述

给你一个字符串`s`，请你将`s`分割成一些 子串，使每个子串都是**回文串**。返回`s`所有可能的分割方案。


## 思考

这道题目可以抽象成组合问题：**有重复数组**中选择组合，约束条件是组合中的元素每个都是**回文串**。组合元素**无数量要求**。组合中元素**不可重复选取**。

## 回溯三部曲

1、回溯函数参数及返回值

全局变量path存放切割后回文子串，二维数组result存放结果。

因为是同一集合，所以需要 startIndex ，不可重复选取后续会要求我们 进入递归时 startIndex 从 i + 1 开始；

参数还有字符串`s`。

2、终止条件

切割完毕，得到一套切割方案/组合时，我们认为到达叶子节点，应该终止。startIndex 起始位置大于等于 s 的大小，我们认为得到一套切割方案了。

3、单层回溯搜索逻辑

单层搜索的for循环i从startIndex开始，[startIndex,i]就是要截取的子串。

如果子串是回文，就加入到path中否则，随后继续递归，回溯。如果不是回文，则跳过此次遍历。

##### 判断回文子串

判断回文子串很简单，双指针向内就可以了。

## 代码实现

```cpp
class Solution {
public:
    bool isPalindrome(string& s) {
        int left = 0;
        int right = s.size() - 1;
        while (left <= right) {
            if (s[left++] != s[right--])
                return false;
        }
        return true;
    }
    vector<vector<string>> result;
    vector<string> path;
    void backtracking(string& s, int startIndex) {
        if (startIndex >= s.size()) {
            result.push_back(path);
            return;
        }
        for (int i = startIndex; i < s.size(); i++) {
            string str = s.substr(startIndex, i - startIndex + 1);
            if (isPalindrome(str)) {
                path.push_back(str);
            } else {
                continue;
            }
            backtracking(s, i + 1);
            path.pop_back();
        }
    }

    vector<vector<string>> partition(string s) {
        result.clear();
        path.clear();
        backtracking(s, 0);
        return result;
    }
};
```

#### 优化

可以发现每次判断回文子串的时候都需要重新从两边计算。但是有重复存在。

例如给定字符串`"abcde"`, 在已知`"bcd"`不是回文字串时, 不再需要去双指针操作`"abcde"`而可以直接判定它一定不是回文字串。

具体来说, 给定一个字符串`s`, 长度为`n`, 它成为回文字串的充分必要条件是`s[0] == s[n-1]`且`s[1:n-1]`是回文字串。

这里就用了动态规划的思想，前一步是回文子串的话，只需要计算外一层就知道是否是回文子串了

我们想要判断任意的s[startIndex,i]是否是回文子串。可以事先计算出，针对一个字符串`s`, 它的任何子串是否是回文字串, 然后在我们的回溯函数中直接查询即可, 省去了双指针移动判定这一步骤。

**递推公式：**

单个字符组成的串 i== j`isPalindrome[i][j] = true;`

两个相邻字符组成的串j - i == 1`isPalindrome[i][j] = (s[i] == s[j]);`

三个以上字符组成的串`isPalindrome[i][j] = (s[i] == s[j] && isPalindrome[i+1][j-1]);`

```cpp
vector<vector<bool>> isPalindrome;

...
    
 void computePalindrome(const string& s) {
        // isPalindrome[i][j] 代表 s[i:j](双边包括)是否是回文字串 
        isPalindrome.resize(s.size(), vector<bool>(s.size(), false)); // 根据字符串s, 刷新布尔矩阵的大小
        for (int i = s.size() - 1; i >= 0; i--) { 
            // 需要倒序计算, 保证在i行时, i+1行已经计算好了
            for (int j = i; j < s.size(); j++) {
                if (j == i) {isPalindrome[i][j] = true;}
                else if (j - i == 1) {isPalindrome[i][j] = (s[i] == s[j]);}
                else {isPalindrome[i][j] = (s[i] == s[j] && isPalindrome[i+1][j-1]);}
            }
        }
    }
```