---
title: '电话号码字母组合'
description: '回溯算法解决电话号码字母组合问题，给定数字字符串返回所有可能的字母组合。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 回溯算法
  - 代码随想录
  - 数据结构与算法
---

## 题目描述

给定一个仅包含数字`2-9`的字符串，返回所有它能表示的字母组合。答案可以按**任意顺序**返回。

给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。

## 思考

直接思考，过程就是先从'2'到'9'选一个数字，然后从这个数字对应的字符串中选一个字母。然后就是接着选第二个数字，选再选第二个数字对应的字符串中选一个数字。以此类推。终止条件是path的长度达到digits的长度。注意题目是给定了digits，不用我们自行生成所有可能的digits

## 回溯法三部曲

* 回溯函数参数及返回值
使用全局变量path收集叶子节点结果，结果数组result保存起来。参数是指定的digits，和index。这个index并非startIndex，而是记录遍历第几个数字。同时index也表示深度。

* 终止条件
到达叶子节点，index深度等于数字个数的时候（如果使用这个条件，则index必须从0开始），收集结果，结束本层递归。

* 回溯搜索的遍历过程
首先取到index指向的digits中的其中一个数字，然后遍历这个数字对应的字符集，for循环里面添加字符到path，递归，回溯

## 代码实现

index从1开始的写法

```cpp
class Solution {
public:
    vector<string> result;
    string path;
    vector<string> lettermap = {"",    "",    "abc",  "def", "ghi",
                                "jkl", "mno", "pqrs", "tuv", "wxyz"};
    void backtracking(string& digits, int index) {
        if (index - 1 == digits.size()) {
            result.push_back(path);
            return;
        }
        int digit = digits[index - 1] - '0';
        string letters = lettermap[digit];
        for (int i = 0; i < letters.size(); i++) {
            path.push_back(letters[i]);
            backtracking(digits, index + 1);
            path.pop_back();
        }
    }
    vector<string> letterCombinations(string digits) {
        result.clear();
        path.clear();
        if (digits.size() == 0)
            return result;
        backtracking(digits, 1);
        return result;
    }
};
```

index从0开始

```cpp
class Solution {
private:
    const string letterMap[10] = {
        "", // 0
        "", // 1
        "abc", // 2
        "def", // 3
        "ghi", // 4
        "jkl", // 5
        "mno", // 6
        "pqrs", // 7
        "tuv", // 8
        "wxyz", // 9
    };
public:
    vector<string> result;
    string s;
    void backtracking(const string& digits, int index) {
        if (index == digits.size()) {
            result.push_back(s);
            return;
        }
        int digit = digits[index] - '0';        // 将index指向的数字转为int
        string letters = letterMap[digit];      // 取数字对应的字符集
        for (int i = 0; i < letters.size(); i++) {
            s.push_back(letters[i]);            // 处理
            backtracking(digits, index + 1);    // 递归，注意index+1，一下层要处理下一个数字了
            s.pop_back();                       // 回溯
        }
    }
    vector<string> letterCombinations(string digits) {
        s.clear();
        result.clear();
        if (digits.size() == 0) {
            return result;
        }
        backtracking(digits, 0);
        return result;
    }
};
```