---
title: 'Dijkstra堆优化版'
description: '使用小顶堆和邻接表优化Dijkstra算法，降低时间复杂度'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 最短路算法
  - Dijkstra算法
  - 优先队列
---

# Dijkstra堆优化版

**发布日期:** 2025/12/21
**阅读时间:** 2 分钟
**标签:** 算法笔记, 图论, 数据结构, 算法, 最短路算法, Dijkstra算法, 优先队列, Leetcode

## 正文
# Dijkstra堆优化版

## 题目描述

小明是一位科学家，他需要参加一场重要的国际科学大会，以展示自己的最新研究成果。

小明的起点是第一个车站，终点是最后一个车站。然而，途中的各个车站之间的道路状况、交通拥堵程度以及可能的自然因素（如天气变化）等不同，这些因素都会影响每条路径的通行时间。

小明希望能选择一条花费时间最少的路线，以确保他能够尽快到达目的地。

[题目链接](https://kamacoder.com/problempage.php?pid=1047)

[文章讲解](https://programmercarl.com/kamacoder/0047.%E5%8F%82%E4%BC%9Adijkstra%E6%9C%B4%E7%B4%A0.html)

## 思考

堆优化 dijkstra。

**朴素 Dijkstra 的时间复杂度分析**

-**总体复杂度**：$O(n^2)$

-**外层循环**：遍历所有节点，确保每个节点都被访问 - $O(n)$

-**内层循环**：在未访问节点中寻找距离源点最近的节点 - $O(n)$

**关键问题：什么情况下朴素版本效率低下？**

稀疏图（边数相对于节点数较少）

**为什么稀疏图效率低？**

在稀疏图中，内层 for 循环会遍历大量节点，但实际上很多节点之间没有直接连接，导致大量无效的遍历操作。

##### Dijkstra 三部曲的耗时操作

Dijkstra 算法的三个核心步骤：

**第一步：选择距离源点最近且未访问的节点**

**当前做法**：遍历 minDist 数组，查找最小值 - $O(n)$

**问题**：为什么每次都要重新遍历整个数组？

**第二步：标记该节点为已访问**

**耗时**：$O(1)$ - 无优化空间

**第三步：更新相邻节点的距离**

**当前做法**：遍历所有节点，更新 minDist 数组 - $O(n)$

**问题**：为什么要遍历所有节点，而不是只遍历实际相邻的节点？

#### 优化

我们需要的是快速获取当前距离源点最近的未访问节点，而**小顶堆**可以快速获取最小值。

##### 针对第一步的优化

**原来**：线性搜索 minDist 数组找最小值

**现在**：使用小顶堆，堆顶就是最小值。

**时间复杂度**：从 $O(n)$ 降到 $O(\log m)$，其中 m 是堆中元素个数

##### 针对第三步的优化

**原来**：遍历所有节点更新距离

**现在**：只遍历当前节点的实际邻居节点

**问题**：如何高效存储和访问邻居节点？使用邻接表而不是邻接矩阵

##### 数据结构

使用**小顶堆**：存储 (节点编号，源点到该节点的权值) 对。C++使用优先级队列实现小顶堆。

使用**邻接表**：存储图的结构，便于快速访问邻居。除了邻居编号，还要存储权值，使用 pair 不太方便区分，可以使用自定义的结构体。

**注意！**构建邻接表是需要预先分配大小，否则后面添加会导致越界。执行`grah[p1].push_back(Edge(p2,val))`时，由于`grah`是空的`vector`，访问`grah[p1]`会导致越界访问

##### 算法流程

1. 初始化：将源点加入堆

1. 主循环：

从堆顶取出距离最小的节点
如果该节点已访问，跳过（处理重复入堆问题）
标记为已访问
遍历其邻居，更新距离并加入堆

#### 复杂度分析

时间复杂度：$O((E) \log V)$

* V：节点数

* E：边数

* 堆操作：每条边最多导致一次入堆操作，每次操作 $O(\log V)$

* 总操作数：最多 E 次入堆 + V 次出堆

空间复杂度：$O(V + E)$

* 邻接表：$O(V + E)$

* 堆：最多 $O(E)$ 个元素

## 代码实现

```cpp
#include <iostream>
#include <vector>
#include <list>
#include <queue>
#include <climits>
using namespace std; 
// 小顶堆
class mycomparison {
public:
    bool operator()(const pair<int, int>& lhs, const pair<int, int>& rhs) {
        return lhs.second > rhs.second;
    }
};
// 定义一个结构体来表示带权重的边
struct Edge {
    int to;  // 邻接顶点
    int val; // 边的权重

    Edge(int t, int w): to(t), val(w) {}  // 构造函数
};

int main() {
    int n, m, p1, p2, val;
    cin >> n >> m;

    vector<list<Edge>> grid(n + 1);

    for(int i = 0; i < m; i++){
        cin >> p1 >> p2 >> val; 
        // p1 指向 p2，权值为 val
        grid[p1].push_back(Edge(p2, val));

    }

    int start = 1;  // 起点
    int end = n;    // 终点

    // 存储从源点到每个节点的最短距离
    std::vector<int> minDist(n + 1, INT_MAX);

    // 记录顶点是否被访问过
    std::vector<bool> visited(n + 1, false); 
    
    // 优先队列中存放 pair<节点，源点到该节点的权值>
    priority_queue<pair<int, int>, vector<pair<int, int>>, mycomparison> pq;


    // 初始化队列，源点到源点的距离为0，所以初始为0
    pq.push(pair<int, int>(start, 0)); 
    
    minDist[start] = 0;  // 起始点到自身的距离为0

    while (!pq.empty()) {
        // 1. 第一步，选源点到哪个节点近且该节点未被访问过 （通过优先级队列来实现）
        // <节点， 源点到该节点的距离>
        pair<int, int> cur = pq.top(); pq.pop();

        if (visited[cur.first]) continue;

        // 2. 第二步，该最近节点被标记访问过
        visited[cur.first] = true;

        // 3. 第三步，更新非访问节点到源点的距离（即更新minDist数组）
        for (Edge edge : grid[cur.first]) { // 遍历 cur指向的节点，cur指向的节点为 edge
            // cur指向的节点edge.to，这条边的权值为 edge.val
            if (!visited[edge.to] && minDist[cur.first] + edge.val < minDist[edge.to]) { // 更新minDist
                minDist[edge.to] = minDist[cur.first] + edge.val;
                pq.push(pair<int, int>(edge.to, minDist[edge.to]));
            }
        }

    }

    if (minDist[end] == INT_MAX) cout << -1 << endl; // 不能到达终点
    else cout << minDist[end] << endl; // 到达终点最短路径
}
```