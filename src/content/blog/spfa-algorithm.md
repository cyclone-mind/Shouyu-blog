---
title: 'SPFA算法'
description: 'SPFA算法：队列优化的Bellman-Ford算法，用于最短路问题'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 最短路算法
  - SPFA算法
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

[文章讲解](https://programmercarl.com/kamacoder/0094.%E5%9F%8E%E5%B8%82%E9%97%B4%E8%B4%A7%E7%89%A9%E8%BF%90%E8%BE%93I-SPFA.html)

## 思考

这道题是**经典的带负权值的单源最短路问题，Bellman_ford可以解决**

Bellman_ford 队列优化算法 ，也叫SPFA算法（Shortest Path Faster Algorithm）。

在之前的 Bellman_ford 中,

```cpp
// 松弛操作
if (minDist[start] != INT32_MAX &&
    minDist[end] > minDist[start] + val) {
    minDist[end] = minDist[start] + val;
    updated = true; // 标记发生了更新
}
```

这个判断条件意味着无论 start 节点是否被更新过，都尝试松弛。

即：

* 每轮都要检查所有边，包括那些起点距离没有变化的边

* 例如：如果节点3的距离在这轮没变，那么检查3→5这条边就是无效工作

那么我们需要做的是什么呢？我们实际上需要松弛的是那些距离有变化的出发节点的边。

也就是说

Bellman_ford 算法每次松弛 都是对所有边进行松弛。但真正有效的松弛，是基于已经计算过的节点在做的松弛。

所以**只需要对 上一次松弛的时候更新过的节点作为出发节点所连接的边 进行松弛就够了**。

如何记录上一次松弛的时候更新过的节点呢？

使用队列或栈都是可以的，并没有要求顺序。

如何记录出发节点所连接的边呢？

使用邻接表记录节点的“邻居” 是非常方便的。

## 注意点

需要注意的是，需要更新的邻居加入队列的时候可能队列里面已经存在这个邻居了，会导致重复添加的问题。因此我们使用一个数组记录已经在队列中的元素即可`vector<bool> inQue(n + 1, false);`

#### 举例

说明一下Bellman-Ford和SPFA的区别

假设图中有节点1→2→3→4，权重都是1：

##### Bellman-Ford的执行过程：

```text
第1轮：检查所有边
- 1→2: 松弛成功，minDist[2] = 1
- 2→3: 松弛成功，minDist[3] = 2  
- 3→4: 松弛成功，minDist[4] = 3

第2轮：再次检查所有边
- 1→2: 检查但不更新（浪费时间）
- 2→3: 检查但不更新（浪费时间）
- 3→4: 检查但不更新（浪费时间）
```

##### SPFA的执行过程：

```text
初始：queue = [1]

处理节点1：
- 松弛1→2，minDist[2] = 1
- 节点2入队：queue = [2]

处理节点2：
- 松弛2→3，minDist[3] = 2
- 节点3入队：queue = [3]

处理节点3：
- 松弛3→4，minDist[4] = 3
- 节点4入队：queue = [4]

处理节点4：
- 没有出边，queue = []
- 算法结束
```

## 代码实现

```cpp
/*
Bellman_ford 队列优化算法 ，也叫SPFA算法（Shortest Path Faster Algorithm）
*/

#include <cstdint>
#include <iostream>
#include <list>
#include <queue>
#include <stdint.h>
#include <vector>

using namespace std;

struct Edge {
    int p2;
    int val;
};

int main() {
    int n, m, s, t, v;
    cin >> n >> m;

    vector<list<Edge>> grah(n + 1);
    for (int i = 0; i < m; i++) {
        cin >> s >> t >> v;
        grah[s].push_back({t, v});
    }

    queue<int> que;
    int start = 1;
    int end = n;
    que.push(start);
    vector<int> minDist(n + 1, INT32_MAX);
    vector<bool> inQue(n + 1, false);
    minDist[start] = 0;
    inQue[start] = true;

    while (!que.empty()) {
        int cur = que.front();
        que.pop();
        inQue[cur] = false;
        for (auto edge : grah[cur]) {
            int to = edge.p2;
            int price = edge.val;
            if (minDist[to] > minDist[cur] + price) {
                minDist[to] = minDist[cur] + price;
                if(inQue[to] == false){
                    que.push(to);
                    inQue[to] = true;
                }
            }
        }
    }

    if (minDist[end] == INT32_MAX)
        cout << "unconnected" << endl;
    else
        cout << minDist[end] << endl;
}
```

### 效率分析

从代码上看什么时候节点会加入队列？当它是其他节点的邻居时。所以说对于非常稠密的双向图，如：

一个双向图，且每一个节点和所有其他节点都相连的话，那么该算法的时间复杂度就接近于 Bellman_ford 的 O(N * E) N 为节点数量，E为边的数量。

在这种图中，每一个节点都会重复加入队列 n - 1次。因为它是 n-1个其余节点的邻居。

总结：如果图越稠密，则 SPFA的效率越接近与 Bellman_ford。

反之，图越稀疏，SPFA的效率就越高。

SPFA时间复杂度 $O(K*N)$---$K$为不定值。

例如图是一条线形图且单向的话，每个节点的入度为1，那么只需要加入一次队列，这样时间复杂度就是 $O(N)$。

所以 SPFA 在最坏的情况下是$O(N * E)$，但 一般情况下 时间复杂度为 $O(K * N)$。

以上只是理论上的时间复杂度。

虽然入队列出队列的时间复杂度都是 $O(1)$ 但是实际执行时间可能因为语言的不同而耗时不一致 。出队列和入队列 其实也是十分耗时的

所以 SPFA（队列优化版Bellman_ford） 在理论上更胜一筹，但如果 图很大且非常稠密的情况下，虽然 SPFA的理论上时间复杂度接近Bellman_ford，但实际时间消耗 可能是 SPFA耗时更多。