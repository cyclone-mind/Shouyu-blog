---
title: '最小生成树之Kruskal'
description: '最小生成树Kruskal算法详解，使用并查集实现'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 数据结构
  - 最小生成树
  - Kruskal算法
  - 并查集
  - Leetcode
---

## 题目描述

在世界的某个区域，有一些分散的神秘岛屿，每个岛屿上都有一种珍稀的资源或者宝藏。国王打算在这些岛屿上建公路，方便运输。

不同岛屿之间，路途距离不同，国王希望你可以规划建公路的方案，如何可以以最短的总公路距离将 所有岛屿联通起来（注意这是一个无向图）。

给定一张地图，其中包括了所有的岛屿，以及它们之间的距离。以最小化公路建设长度，确保可以链接到所有岛屿。

[题目链接](https://kamacoder.com/problempage.php?pid=1053)

[文章链接](https://programmercarl.com/kamacoder/0053.%E5%AF%BB%E5%AE%9D-prim.html)

## 思考

kruskal 算法同样能用来解决最小生成树的问题。不同的是前者从边的角度出发，后者从节点的角度出发。

思路：

* 对边的权值从小到大排序，因为需要优先选最小的边组成树。

* 遍历排序后的边

如果边在树中，即边的首尾节点在同一个集合，说明再连上这条边会出现环，因此跳过。
如果边不在树中，即边的首尾节点不在同一个集合，则可以把这条边加入到树，也就是把两个节点加入同一个集合

* 如果边在树中，即边的首尾节点在同一个集合，说明再连上这条边会出现环，因此跳过。

* 如果边不在树中，即边的首尾节点不在同一个集合，则可以把这条边加入到树，也就是把两个节点加入同一个集合

很明显判断节点是否在同一个集合，添加两个节点到一个集合，应该使用并查集。

因为对于边，不仅要存首尾节点，还需要存权值，因此使用结构体比较方便。

```cpp
struct Edge {
    int u,v,val;
};
```

对于排序，compare 函数可以采用匿名函数，就地构造。

### prim 和 kruskal 比较

在 稀疏图中，用 Kruskal 更优。 在稠密图中，用 prim 算法更优。

Prim 算法 时间复杂度为 $O(n^2)$，其中 n 为节点数量，它的运行效率和图中边树无关，适用稠密图。

Kruskal算法 时间复杂度 为 $nlogn$，其中 n 为边的数量，适用稀疏图

## 代码实现

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Edge {
    int u,v,val;
};

vector<int> father(1001,-1);

void init(){
    for(int i = 0;i < 1001;i++){
        father[i] = i;
    }
}

int find(int u){
    return u == father[u] ? u : father[u] = find(father[u]);
}

bool isSame(int u,int v){
    u = find(u);
    v = find(v);
    return u == v;
}

void join(int u,int v){
    u = find(u);
    v = find(v);
    if(u == v) return;
    father[v] = u;
}

int main() {
    int v, e, v1, v2, val;
    cin >> v >> e;
    vector<Edge> edges;
    while(e--){
        cin >> v1 >> v2 >> val;
        edges.push_back({v1,v2,val});
    }
    init();
    int result = 0;
    sort(edges.begin(), edges.end(),[](const Edge& a, const Edge& b){return a.val < b.val;});
    for(auto edge:edges){
        if(isSame(edge.u,edge.v) == false) {
            result += edge.val;
            join(edge.u,edge.v);
        }
    }
    cout << result << endl;
}
```