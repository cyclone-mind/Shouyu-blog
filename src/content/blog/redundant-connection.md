---
title: '冗余连接'
description: '无向图的冗余连接问题'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 并查集
  - 环检测
  - Leetcode
---

## 题目描述

有一个图，它是一棵树，他是拥有 n 个节点（节点编号1到n）和 n - 1 条边的连通无环无向图。

现在在这棵上的基础上，添加一条边（依然是n个节点，但有n条边），使这个图变成了有环图，如图：

先请你找出冗余边，删除后，使该图可以重新变成一棵树。

[题目链接](https://kamacoder.com/problempage.php?pid=1181)

[文章讲解](https://programmercarl.com/kamacoder/0108.%E5%86%97%E4%BD%99%E8%BF%9E%E6%8E%A5.html)

## 思考

给我们的图的特点是n个节点 n-1条边的树，意味着它只可能是一种形状，即

在此基础上增加一条边，变成有环图可以有如下加法等等。

由于树有 n 个节点只需要 n-1 条边，所以我们需要找到那条"多余"的边。

### 并查集思路

把没有冗余边的情况（n-1条边）看作一个连通空间，所有节点之间都有连通性，即所有节点都在同一集合。冗余的边意味着即使不加这条边，这条边的两个节点也在同一集合，即冗余的边加入这个集合之前，两个节点就已经在同一集合了。

所以我们可以遍历所有边，将没在同一集合的边合并到同一集合，将已在同一集合的边输出，并退出程序。

**输出描述：输出一条可以删除的边。如果有多个答案，请删除标准输入中最后出现的那条边。**

注意，这个输出描述是什么意思呢？

我们的图原本是一棵树，在树中，任何新增的边都会形成环。所以我们按照输入顺序处理时，第一次检测到环的那条边，就是"最后添加导致环形成"的边，也就是题目要求的答案。

1. 第一条导致环的边 = 最后一条冗余边

1. 因为在树中，任何新增的边都会形成环

1. 按输入顺序处理时，第一次检测到环的那条边，就是"最后添加导致环形成"的边

### 深搜或广搜

非常麻烦。

* 逆向思维：从最后一条边开始，尝试移除每条边

* 移除边后，用邻接表构建图（跳过指定移除的边），随后用DFS检查图的连通性（借助visited)

* 第一个移除后仍保持连通的边就是答案

## 代码实现（并查集）

```cpp
#include <vector>
#include <iostream>
using namespace std;

vector<int> father(1002,0);

void init(){
    for(int i = 0;i < father.size();i++){
        father[i] = i;
    }
}

int find(int u){
    return u == father[u] ? u : father[u] = find(father[u]);
}

bool isSame(int u,int v){
    u  = find(u);
    v = find(v);
    return u == v;
}

void join(int u,int v){
    u  = find(u);
    v = find(v);
    if(u == v) return;
    father[v] = u;
}

int main(){
    int n,s,t;
    cin >> n;
    init();
    while(n--){
        cin >> s >> t;
        if(isSame(s,t)){
            cout << s << ' ' << t << endl;
            return 0;
        } else {
            join(s,t);
        }
    }
}
```