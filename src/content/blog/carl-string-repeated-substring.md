---
title: '代码随想录 字符串：459. 重复的子字符串'
description: '给定一个非空的字符串s，检查是否可以通过由它的一个子串重复多次构成。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 字符串
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

## 题目描述

给定一个非空的字符串 s ，检查是否可以通过由它的一个子串重复多次构成。

示例 1:

输入: s = "abab"
输出: true
解释: 可由子串 "ab" 重复两次构成。
示例 2:

输入: s = "aba"
输出: false
示例 3:

输入: s = "abcabcabcabc"
输出: true
解释: 可由子串 "abc" 重复四次构成。 (或子串 "abcabc" 重复两次构成。)

[题目链接](https://leetcode.cn/problems/repeated-substring-pattern/)

## 思考

(移动匹配+库函数)/KMP两种方法。

移动匹配很简单。如果一个字符串由多个子串重复构成，例如`[]...[]...[]`这样，我们假设`[]`是至少存在两个重复的子串。假如有两个吧`s = [][]`那么把两个s拼接起来是这样`t = [][][][]`。

我们会发现 第2个`[]`和第3个`[]`会重新组成s。也就是说拼接起来的t中间存在一个s，这个s由第一个s前半部分组成，第二个s后半部分组成。这就很妙了。

所以我们可以在拼接起来的t串中寻找s，找到了就说明是拼接起来的。注意要刨除 s + s 的首字符和尾字符，这样避免在s+s中搜索出原来的s，我们要搜索的是中间拼接出来的s。

以上是一个感性的认识，至于这里面的数学原理，充分性必要性证明啥的，应该也搞不明白。那就不管了

所以目标变为了在t中寻找s。这里可以使用find库函数就可以了。

KMP

重复子串很容易想到next数组这个表达字符串中心字符块对称程度的定义。next数组的最后一个表达了整个字符串的最长相等前后缀的长度，或者说表达了最长的重复的块的长度。

•	如果 next[len - 1] > 0，说明字符串有整体对称性的可能。
•	如果字符串的长度 len 可以被 len - next[len - 1] 整除，说明字符串可以分解为若干个相同的子串。

假设字符串长度为 len，next[len - 1] 是整个字符串的最长相等前后缀的长度：
• 如果字符串是由重复子串构成的，那么重复子串的长度为 len - next[len - 1]。
• 如果 len % (len - next[len - 1]) == 0，说明字符串可以被该子串整除，符合条件。

注意细节，如果next[len - 1]为0，则直接false，只有next[len - 1]>0时才去比较是否能整除。

以字符串 s = "abcabcabc" 为例：

1. 构造 next 数组：
•	next 数组为 [0, 0, 0, 1, 2, 3, 4, 5, 6]。
•	解释：例如，next[8] = 6 表示以第 8 个字符结尾的子串 abcabcab 的最长相等前后缀长度为 6。

1. 判断重复子串：
•	len = 9，lastNext = 6。
•	重复子串长度为 len - lastNext = 3。
•	检查 len % 3 == 0，条件成立，因此字符串可以由子串 "abc" 重复构成。

#### 参考代码

**移动匹配**

```cpp
class Solution {
public:
    bool repeatedSubstringPattern(string s) {
        string t = s+s;
        t.erase(t.begin());
        t.erase(t.end()-1);
        if(t.find(s) != string::npos) return true;
        return false;
    }
};
```

**KMP**

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

void getNext(vector<int>& next, string pattern) {
    if (next.size() != 0) next[0] = 0;
    for (int i = 1; i < next.size(); i++) {
        int k = next[i - 1];
        while (k > 0 && pattern[i] != pattern[k]) {
            k = next[k - 1];
        }
        if (pattern[i] == pattern[k]) {
            next[i] = k + 1;
        } else {
            next[i] = 0;
        }
    }
}

bool repeatedSubstringPattern(string s) {
    vector<int> next(s.length(), 0);
    getNext(next, s);

    int len = s.length();
    int lastNext = next[len - 1];
    if (lastNext > 0 && len % (len - lastNext) == 0) {
        return true;
    } else {
        return false;
    }
}

int main() {
    string s = "abcabcabc";
    cout << repeatedSubstringPattern(s) << endl;
}
```