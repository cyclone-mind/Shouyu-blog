---
title: 'Dijkstra朴素版'
description: 'Dijkstra朴素版算法讲解，在有权图中求从起点到其他节点的最短路径'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 最短路算法
  - Dijkstra算法
---

## 题目描述

小明是一位科学家，他需要参加一场重要的国际科学大会，以展示自己的最新研究成果。

小明的起点是第一个车站，终点是最后一个车站。然而，途中的各个车站之间的道路状况、交通拥堵程度以及可能的自然因素（如天气变化）等不同，这些因素都会影响每条路径的通行时间。

小明希望能选择一条花费时间最少的路线，以确保他能够尽快到达目的地。

[题目链接](https://kamacoder.com/problempage.php?pid=1047)

[文章讲解](https://programmercarl.com/kamacoder/0047.%E5%8F%82%E4%BC%9Adijkstra%E6%9C%B4%E7%B4%A0.html)

## 思考

这道题就是在一个有权的有向图中，给定起点和终点，找最短路径。

`dijkstra`算法：在有权图（权值非负数）中求从起点到其他节点的最短路径算法。

需要注意的是两点

1. 权值不能为负；

1. 2.这个算法除了能求到终点的最短路径，还能求到其他所有节点的最短路径。

Dijkstra 算法 和 prim 算法十分接近。

dijkstra 三部曲：

1. 选择距离源点最近的且未被访问过的节点；

1. 将该最近节点标记访问过；

1. 更新所有非访问节点到源点的距离（即更新 minDist 数组）

minDist 数组的含义是记录了所有节点到源点的最短路径。

和 prim 三部曲很像：

1. 选择生成树最近的非生成树节点。

1. 将该节点加入到树中

1. 更新非生成树节点到生成树的距离（即更新 minDist 数组）

实现步骤：

0、初始化：

图用邻接矩阵保存

minDist 数组数值初始化为int最大值，其中将源点到自己的距离设置为0。

节点是否被访问过使用一个布尔类型的数组做标记。

因为车站编号都是从1开始，因此minDist 数组和访问数组大小都设置为n+1，将下标0做无效位，同一从1开始处理。

```cpp
#include <iostream>
#include <vector>
#include <climits>
using namespace std;
int main() {
    int n, m, p1, p2, val;
    cin >> n >> m;

    vector<vector<int>> grid(n + 1, vector<int>(n + 1, INT_MAX));
    for(int i = 0; i < m; i++){
        cin >> p1 >> p2 >> val;
        grid[p1][p2] = val;
    }

    int start = 1;
    int end = n;

    // 存储从源点到每个节点的最短距离
    std::vector<int> minDist(n + 1, INT_MAX);

    // 记录顶点是否被访问过
    std::vector<bool> visited(n + 1, false);

    minDist[start] = 0;  // 起始点到自身的距离为0
```

初始化完成之后遍历所有节点，每个节点都要进行三部曲

三部曲

1. 选择距离源点最近的且未被访问过的节点；

1. 将该最近节点标记访问过；

1. 更新所有非访问节点到源点的距离（即更新 minDist 数组）

```cpp
for (int i = 1; i <= n; i++) { // 遍历所有节点

        int minVal = INT_MAX;
        int cur = 1;

        // 1、选距离源点最近且未访问过的节点
        for (int v = 1; v <= n; ++v) {
            if (!visited[v] && minDist[v] < minVal) {
                minVal = minDist[v];
                cur = v;
            }
        }

        visited[cur] = true;  // 2、标记该节点已被访问

        // 3、第三步，更新非访问节点到源点的距离（即更新minDist数组）
        for (int v = 1; v <= n; v++) {
            if (!visited[v] && grid[cur][v] != INT_MAX && minDist[cur] + grid[cur][v] < minDist[v]) {
                minDist[v] = minDist[cur] + grid[cur][v];
            }
        }

    }

    if (minDist[end] == INT_MAX) cout << -1 << endl; // 不能到达终点
    else cout << minDist[end] << endl; // 到达终点最短路径
```

#### 求路径

如果要求打印出来最短路径，可以存一个数组，下标是边尾节点，值为起始节点。

然后第三步时记录一下即可。

```cpp
...
vector<int> parent(n+1,-1)
...
    parent[v] = cur;
...
for(int i = 1;i <= n;i++){
    cout << parent[i] << "->" << i << endl;
}
```

#### 有负数

权值有负数时怎么处理？

dijkstra 没办法处理负数权值，归根结底是因为在第一步，选择距离源点最近的非访问节点时会因为**短视**或者说**贪心**的策略导致优先选择了看起来最近的那个节点，因为它假定后面的路径是累加的，都是整数。

就比如这种情况，把1标记访问，然后更新了节点2和节点3到源点的距离，这时它会选择节点3作为新的起始节点，从节点1到节点3的最短路径就是1。

为什么它这么选？因为它认为从其他路绕再到节点3的话，只能从100往上加一个整数，这一定是比1要大的，所以它选择了路长为1的这条路。

对于求解带有负权值的最短路问题，可以使用 Bellman-Ford 算法 ，我在后序会详细讲解。

#### dijkstra 与prim算法的区别

唯一区别在 三部曲中的 第三步： 更新minDist数组

因为**prim是求 非访问节点到最小生成树的最小距离，而 dijkstra是求 非访问节点到源点的最小距离**。

一个是到树这个整体，一个是到源点，这个单点。

**prim**

```cpp
for (int j = 1; j <= v; j++) {
    if (!isInTree[j] && grid[cur][j] < minDist[j]) {
        minDist[j] = grid[cur][j];
    }
}
```

**dijkstra**

```cpp
for (int v = 1; v <= n; v++) {
    if (!visited[v] && grid[cur][v] != INT_MAX && minDist[cur] + grid[cur][v] < minDist[v]) {
        minDist[v] = minDist[cur] + grid[cur][v];
    }
}
```