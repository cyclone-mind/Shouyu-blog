---
title: '寻找存在的路径'
description: '判断无向图中从source到destination是否存在路径，使用并查集解决'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 并查集
---

## 题目描述

给定一个包含 n 个节点的无向图中，节点编号从 1 到 n （含 1 和 n ）

你的任务是判断是否有一条从节点 source 出发到节点 destination 的路径存在。

[题目链接](https://kamacoder.com/problempage.php?pid=1179)

[文章讲解](https://programmercarl.com/kamacoder/0107.%E5%AF%BB%E6%89%BE%E5%AD%98%E5%9C%A8%E7%9A%84%E8%B7%AF%E5%BE%84.html)

## 思考

本题题意有几个关键点：

1. 无向图：节点之间是双向的。因此交换 join 的两个节点效果是相同的。符合并查集操作的对称性。

1. 判断连通性：只需要判断两个节点能否到达，不需要具体路径。

1. 静态查询：所有边都给定后再查询连通性。对边进行合并。

实际上，这道题适合并查集的核心原因是：

1. 无向图 + 连通性判断 + 静态查询

1. 不需要路径信息，只需要连通性

1. 所有边都是等权的（或者说权重不重要）

如果改成有向图、需要路径信息、或者涉及边权，就需要考虑其他算法了

时间复杂度： $O(m×α(n) + α(n)) ≈ O(m)$

空间复杂度： $O(n)$

其中α(n)是阿克曼函数的反函数，在实际应用中可以认为是常数

个人理解：

节点之间用边链接，在并查集中就意味着两个节点属于同一个集合。对于非常多的链接起来的边，就意味着需要将边合并，即将多个集合合并。

不再需要构建图了，而是把所有边合并即可，形成多个节点组成的集合。

## 代码实现

```cpp
// 给定一个包含 n 个节点的无向图中，节点编号从 1 到 n （含 1 和 n ）。
// 你的任务是判断是否有一条从节点 source 出发到节点 destination 的路径存在。
#include <vector>
#include <iostream>
using namespace std;

vector<int> father(101,0);

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
    int n,m,s,t,source,destination;
    cin >> n >> m;
    init();
    while(m--){
        cin >> s >> t;
        join(s,t);
    }
    cin >> source >> destination;
    if (isSame(source, destination)) cout << 1 << endl;
    else cout << 0 << endl;

}
```