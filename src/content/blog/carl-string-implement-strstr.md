---
title: '代码随想录 字符串：28. 实现 strStr() 函数'
description: '给你两个字符串haystack和needle，在haystack字符串中找出needle字符串的第一个匹配项的下标。如果needle不是haystack的一部分，则返回-1。'
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

给你两个字符串 haystack 和 needle ，请你在 haystack 字符串中找出 needle 字符串的第一个匹配项的下标（下标从 0 开始）。如果 needle 不是 haystack 的一部分，则返回  -1 。

示例 1：

输入：haystack = "sadbutsad", needle = "sad"
输出：0
解释："sad" 在下标 0 和 6 处匹配。
第一个匹配项的下标是 0 ，所以返回 0 。
示例 2：

输入：haystack = "leetcode", needle = "leeto"
输出：-1
解释："leeto" 没有在 "leetcode" 中出现，所以返回 -1 。

[题目链接](https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string)

## 思考

该题目定义与C语言中strStr()函数定义一致，不过C语言找不到不会返回任何值，找到了也是返回char*。

C和C++使用如下

```cpp
#include <iostream>
#include <string>
#include <cstring>
using namespace std;

int main(){
    char s1[] = "hello,world";
    char s2[] = "world";
    cout << strstr(s1,s2) << endl;

    string s3 = "hello,world";
    string s4 = "world";
    cout << s3.find(s4) << endl;
    return 0;
}
```

理解KMP首先需要了解next数组，或者叫前缀数组。推荐这篇文章：KMP算法的前缀next数组最通俗的解释，如果看不懂我也没辙了

总之，看了这篇文章就会理解，原来next数组表示了模式串的中心字符块对称程度。

```cpp
void getPerfix(vector<int>& perfix,string& needle){
        perfix[0] = 0;
        for(int i = 1;i < perfix.size();i++){
            int k = perfix[i-1];
            while(needle[i] != needle[k] && k != 0){
                k = perfix[k-1];
            }
            if(needle[i] == needle[k]){
                perfix[i] = k + 1;
            } else {
                perfix[i] = 0;
            }
        }
    }
```

也许你明白了继承的实现，但是中间的递归---while循环，是怎么回事？在`(a g c t a g c )( a g c t a g c) t`这个例子中，t原本是想匹配索引8的元素的，但是发现匹配不上，无法继承，那么它就特别想往前找到另一个t匹配上。怎么做？

此时我们知道t要重新计算对称性，但此刻他前面的c是一定有对称性的，那么这个t必定要跟着c形成对称性才行，它得先找到前一个c，然后这个c后面跟一个t，这样才算是匹配上，可以继承c的对称性了(此时不是继承索引13这个c的对称，而是往前的某一个c的对称性)

第一次`k = perfix[k-1];`是想要继承索引13这个c的对称性，需要匹配的位置是索引7，匹配不上，但它还是要跟着c走，怎么办？那么继续往前找c，第二次`k = perfix[k-1];`是想要继承索引6这个c的对称性，需要匹配的位置是索引3，匹配上了！

ok，假设你已经明白了next数组原理。接下来以暴力的思想逐步理解KMP。

从朴素匹配的思路进行优化思考。示例，原本匹配失败的话，主串匹配指针要回退到索引1，模式串要回退到索引0的。但是因为我们从模式串中找到了最长相等的前缀和后缀，那么可以适当的主串匹配指针往后移动一段距离，移动到哪里呢？原不匹配指针再往前一个模式串的最长相等前缀的长度即可。然后在这个前提下两指针再往后移动一个模式串的最长相等前缀的长度。这样恰好重新开始尝试匹配。

![](https://pic.leetcode-cn.com/1637734775-ZKogAh-file_1637734775322]

下面按步骤说明KMP算法的实现：

#### 1. 构建前缀数组（getPerfix函数）

**目的**：为模式串构建部分匹配表（next数组）

**步骤**：

* perfix[0] = 0：第一个字符的最长相等前后缀长度为0

* 对于每个位置i（从1开始）：

取前一个位置的前缀值 k = perfix[i-1]
如果当前字符与需要匹配的前缀字符不匹配且k不为0，就回退到更短的前缀 k = perfix[k-1]
如果字符匹配，则前缀长度加1：perfix[i] = k + 1
否则设为0

* 取前一个位置的前缀值 k = perfix[i-1]

* 如果当前字符与需要匹配的前缀字符不匹配且k不为0，就回退到更短的前缀 k = perfix[k-1]

* 如果字符匹配，则前缀长度加1：perfix[i] = k + 1

* 否则设为0

**示例**：对于模式串"ABABC"

* A: 0

* AB: 0 (A≠B)

* ABA: 1 (A=A)

* ABAB: 2 (AB=AB)

* ABABC: 0 (C≠A)

#### 2. 字符串匹配（strStr函数）

**步骤**：

1. 初始化：创建前缀数组，设置主串指针i和模式串指针j

1. 匹配过程：

如果字符不匹配且j>0，根据前缀数组跳转j的位置
如果字符匹配，两个指针都前进
当j到达模式串末尾时，找到匹配位置

1. 返回结果：找到则返回起始位置，未找到返回-1

**核心优势**：利用已匹配的信息，避免主串指针回溯，时间复杂度O(m+n)

#### 参考代码

```cpp
class Solution {
public:
    void getNext(vector<int> &next,string pattern){
        next[0] = 0;
        for(int i = 1;i < next.size();i++){
            int k = next[i-1];
            while(k > 0 && pattern[i] !=pattern[k]){
                k = next[k-1];
            }
            if(pattern[i] == pattern[k]){
                next[i] = k+1;
            } else {
                next[i] = 0;
            }
        }
    }
    int strStr(string haystack, string needle) {
        vector<int> next(needle.length(),0);
        getNext(next,needle);
        for(int i = 0,j=0;i < haystack.length();i++){
            while(j>0 && needle[j] != haystack[i]){
                j = next[j-1];
            }
            if(needle[j] == haystack[i]){
                j++;
            }
            if(j == needle.length()){
                return (i-needle.length()+1);
            }
        }
        return -1;
    }
};
```