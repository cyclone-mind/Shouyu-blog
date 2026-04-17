---
title: '字符串接龙'
description: '字符串接龙问题：广度优先搜索'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - BFS
  - 字符串
  - Leetcode
---

## 题目描述

字典 strList 中从字符串 beginStr 和 endStr 的转换序列是一个按下述规格形成的序列：

1. 序列中第一个字符串是 beginStr。

1. 序列中最后一个字符串是 endStr。

1. 每次转换只能改变一个字符。

1. 转换过程中的中间字符串必须是字典 strList 中的字符串，且strList里的每个字符串只用使用一次。

给你两个字符串 beginStr 和 endStr 和一个字典 strList，找到从 beginStr 到 endStr 的最短转换序列中的字符串数目。如果不存在这样的转换序列，返回 0。

[题目链接](https://kamacoder.com/problempage.php?pid=1183)

[文章讲解](https://programmercarl.com/kamacoder/0110.%E5%AD%97%E7%AC%A6%E4%B8%B2%E6%8E%A5%E9%BE%99.html)

## 思路

借助卡哥画的图理解。

给定一个起始单词和目标单词，以及一个单词列表，每次只能改变一个字母，问最少需要多少步从起始单词变换到目标单词。

需要找最短转换序列中的字符串数目，就是要求最短转换路径长度，求最短路径一般用广搜。

本质上是在一个图中求两给定节点最短路径。

* 每个单词是一个节点

* 如果两个单词对应位置只相差一个字母，他们之间就有一条边

* 需要找起始节点到目标节点最短路径

两个关键点

1. 两个字符串能否转换，能否相连？需要遍历字符串中每一个字符，再遍历26个字母挨个换，如果替换后字符串与需要转换的字符串相等，则两者能转换，是一条路径。

1. 起点和终点的最短路径长度。从起始节点，开始广搜，搜的方向就是对节点每个字符用26个字母替换。搜的方向是否合法看两点：方向要在单词列表中，方向要没有搜索过。若合法，则找到了下个节点，我们就把这个节点和步数+1添加到 visitMap 中，防止重复访问并且记录当前节点步数，随后把该节点放入队列中进行下一次搜索。

为了防止广搜重复搜索（陷入死循环），需要使用容器标记当前节点，另外最终需要求最短路径长度，因此还需要记录以下从起始节点到当前节点所走过的步数，因此使用`unordered_map<string, int> visitMap`

## 代码实现

```cpp
#include <iostream>
#include <queue>
#include <string>
#include <unordered_map>
#include <unordered_set>

using namespace std;

int main() {
    int N;
    cin >> N;
    string beginStr;
    string endStr;
    cin >> beginStr >> endStr;
    unordered_set<string> strList;
    string s;
    for (int i = 0; i < N; i++) { 
        cin >> s;
        strList.insert(s);
    }

    unordered_map<string, int> visitMap;
    visitMap.insert({beginStr, 1});
    queue<string> que;
    que.push(beginStr);
    while (!que.empty()) {
        string word = que.front();
        que.pop();
        for (int i = 0; i < word.size(); i++) {
            string newword = word;
            for (int j = 0; j < 26; j++) {
                newword[i] = j + 'a';
                if (newword == endStr) {
                    cout << visitMap[word] + 1 << endl;
                    return 0;
                }
                if (strList.find(newword) != strList.end() &&
                    visitMap.find(newword) == visitMap.end()) {
                    visitMap.insert({newword, visitMap[word] + 1});
                    que.push(newword);
                }
            }
        }
    }
    cout << 0 << endl;
}
```