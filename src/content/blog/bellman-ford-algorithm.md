---
title: 'Bellman-Ford算法'
description: '深入理解Bellman-Ford最短路算法，处理负权边问题。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 数据结构
  - 最短路算法
  - Bellman-Ford算法
  - 负权边
  - Leetcode
---

## 题目描述

某国为促进城市间经济交流，决定对货物运输提供补贴。共有 n 个编号为 1 到 n 的城市，通过道路网络连接，网络中的道路仅允许从某个城市单向通行到另一个城市，不能反向通行。

网络中的道路都有各自的运输成本和政府补贴，**道路的权值计算方式为：运输成本 - 政府补贴**。权值为正表示扣除了政府补贴后运输货物仍需支付的费用；权值为负则表示政府的补贴超过了支出的运输成本，实际表现为运输过程中还能赚取一定的收益。

请找出从城市 1 到城市 n 的所有可能路径中，综合政府补贴后的最低运输成本。如果最低运输成本是一个负数，它表示在遵循最优路径的情况下，运输过程中反而能够实现盈利。

**城市 1 到城市 n 之间可能会出现没有路径的情况，同时保证道路网络中不存在任何负权回路。**

### 输入描述

第一行包含两个正整数，第一个正整数 n 表示该国一共有 n 个城市，第二个整数 m 表示这些城市中共有 m 条道路。

接下来为 m 行，每行包括三个整数，s、t 和 v，表示 s 号城市运输货物到达 t 号城市，道路权值为 v （单向图）。

### 输出描述

如果能够从城市 1 到连通到城市 n， 请输出一个整数，表示运输成本。如果该整数是负数，则表示实现了盈利。如果从城市 1 没有路径可达城市 n，请输出 "unconnected"。

[题目链接](https://kamacoder.com/problempage.php?pid=1152)

[文章讲解](https://programmercarl.com/kamacoder/0094.%E5%9F%8E%E5%B8%82%E9%97%B4%E8%B4%A7%E7%89%A9%E8%BF%90%E8%BE%93I.html)

## 思考

这道题是**经典的带负权值的单源最短路问题，Bellman_ford可以解决**

核心思想：**对所有边松弛n-1次**

## 松弛

如果 通过 A 到 B 这条边可以获得更短的从起始节点到达B节点的路径，即如果`minDist[B] > minDist[A] + value`，那么我们就更新`minDist[B] = minDist[A] + value`，**这个过程就叫做 “松弛**” 。

为什么是 n-1 次呢？经过模拟

可以得出规律：对所有边松弛一次，就是计算了从起点出发 到达一条边范围以内的节点的最短距离。

所有边松弛两次，就是计算了从起点出发 到达两条边范围以内的节点的最短距离。

所有边松弛n-1次，就是计算了从起点出发 到达n-1条边范围以内的节点的最短距离。

而从节点1到达节点n最多需要n-1条边，因为是单向的不能返回。

## 代码实现

```cpp
#include <cstdint>
#include <iostream>
#include <vector>

using namespace std;

struct Edge {
    int p1;
    int p2;
    int val;

    Edge(int p1, int p2, int val) : p1(p1), p2(p2), val(val) {}
};

int main() {
    int n, m, s, t, v;
    cin >> n >> m;


    vector<Edge> edges;
    for (int i = 0; i < m; i++) {
        cin >> s >> t >> v;
        edges.push_back(Edge(s, t, v));
    }

    vector<int> minDist(n + 1, INT32_MAX);
    minDist[1] = 0;

    // Bellman-Ford算法：进行n-1轮松弛
    for (int i = 1; i < n; i++) {
        for (auto edge : edges) {
            int start = edge.p1;
            int end = edge.p2;
            int val = edge.val;
            if (minDist[start] != INT32_MAX &&
                minDist[end] > minDist[start] + val) {
                minDist[end] = minDist[start] + val;
            }
        }
    }

    if (minDist[n] == INT32_MAX)
        cout << "unconnected" << endl;
    else
        cout << minDist[n] << endl;
}
```

## 易错点

初始化边时不要给定边的数量，不要这样写：

```cpp
vector<Edge> edges(m);  // 先创建了m个默认边
while (m--) {
    cin >> s >> t >> v;
    edges.push_back(Edge(s,t,v));  // 又push_back了m个边
}
```

这样做的话 vector 会调用 Edge 的默认构造函数来初始化 m 个元素，而我们没有指定默认构造函数！或者说构建了 m 个空的 Edge，随后又在标准输入中构造了 m 个正确的Edge，这会是2m个元素！

另外之前这种指定容量是因为基本类型。`vector<int> vec(5);`// 创建5个元素，每个都是0。总共，push_back 的时候前面不要指定容量。

所以不指定数量就ok

```cpp
vector<Edge> edges;
```

还可以更简便一点，不用构造函数，直接使用这个简单的结构体就行了。

```cpp
struct Edge {
    int p1;
    int p2;
    int val;
};
while (m--) {
    cin >> s >> t >> v;
    edges.push_back({s,t,v});  // 又push_back了m个边
}
```