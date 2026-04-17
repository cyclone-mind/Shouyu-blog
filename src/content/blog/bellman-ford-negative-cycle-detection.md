---
title: 'Bellman-Ford之判断负权回路'
description: '使用Bellman-Ford算法检测图中是否存在负权回路。'
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
  - 负权回路
  - Leetcode
---

## 题目描述

某国为促进城市间经济交流，决定对货物运输提供补贴。共有 n 个编号为 1 到 n 的城市，通过道路网络连接，网络中的道路仅允许从某个城市单向通行到另一个城市，不能反向通行。

网络中的道路都有各自的运输成本和政府补贴，**道路的权值计算方式为：运输成本 - 政府补贴**。权值为正表示扣除了政府补贴后运输货物仍需支付的费用；权值为负则表示政府的补贴超过了支出的运输成本，实际表现为运输过程中还能赚取一定的收益。

然而，在评估从城市 1 到城市 n 的所有可能路径中综合政府补贴后的最低运输成本时，存在一种情况：**图中可能出现负权回路。**负权回路是指一系列道路的总权值为负，这样的回路使得通过反复经过回路中的道路，理论上可以无限地减少总成本或无限地增加总收益。为了避免货物运输商采用负权回路这种情况无限的赚取政府补贴，算法还需检测这种特殊情况。

请找出从城市 1 到城市 n 的所有可能路径中，综合政府补贴后的最低运输成本。同时能够检测并适当处理负权回路的存在。

**城市 1 到城市 n 之间可能会出现没有路径的情况**

[题目链接](<https://kamacoder.com/problempage.php?pid=1153>)

[文章链接](<https://programmercarl.com/kamacoder/0095.%E5%9F%8E%E5%B8%82%E9%97%B4%E8%B4%A7%E7%89%A9%E8%BF%90%E8%BE%93II.html>)

## 思考

本题是bellman-Ford 的存在负权回路的场景。

以示例说明

问图中 节点1 到 节点4 的最短路径是多少（题目中的最低运输成本） （注意边可以为负数的）

我们正常情况可以是节点1 -> 节点2 -> 节点3 -> 节点4，这样的路径总成本为 -1 + 1 + 1 = 1。

如果出现了负权回路：

这就意味着我在到达终点前可以一致绕圈减少成本。出现了无穷小的成本，本体就无解了。

在正常结构中，我们知道至多松弛 n-1 条边就可以得到起点到任何节点的最短路径。松弛 n 以上 minDist 数组不会有变化。

然而负权回路中，无限次松弛，会得到无限小成本。即使按照正常算法我们进行n-1轮并停止，得到的也不是真正的最短距离！因为实际上可以通过负权回路让距离变得更小，所以只需要做第n轮检测，还在更新，就说明存在负权回路。

所以说最短路径问题的**前提**：图中不存在从源点可达的负权回路

## 实现步骤

所以怎么做？在未优化的算法中，进行第n次尝试松弛判断负权回路，若发现仍和可更新：`(minDist[from] != INT_MAX && minDist[to] > minDist[from] + price`那么就是有负权回路。

在SPFA算法中，极端情况下，即：所有节点都与其他节点相连，每个节点的入度为 n-1 （n为节点数量），所以每个节点最多加入 n-1 次队列。

那么如果节点加入队列的次数 超过了 n-1次 ，那么该图就一定有负权回路。

所以只需要一个数组记录节点添加到队列中多少次即可：`vector<int> count(n+1, 0);`，在成功松弛后添加到队列中后计数器+1，随后判断计数器是否达到了第n次即可。

## 代码实现

### Bellman-ford

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
    bool flag = false;
    // Bellman-Ford算法：进行n-1轮松弛，添加提前终止条件
    for (int i = 1; i <= n; i++) {
        bool updated = false; // 标记本轮是否有更新

        for (auto edge : edges) {
            int start = edge.p1;
            int end = edge.p2;
            int val = edge.val;
            if (i < n) {
                // 松弛操作
                if (minDist[start] != INT32_MAX &&
                    minDist[end] > minDist[start] + val) {
                    minDist[end] = minDist[start] + val;
                    updated = true; // 标记发生了更新
                }
            } else {
                if (minDist[start] != INT32_MAX &&
                    minDist[end] > minDist[start] + val) {
                    flag = true;
                }
            }
        }
        // 提前终止条件：如果本轮没有任何更新，说明已经收敛
        if (!updated) {
            // cout << "算法在第 " << i << " 轮提前收敛" << endl;
            break;
        }
    }
    if (flag) {
        cout << "circle" << endl;
        return 0;
    }
    if (minDist[n] == INT32_MAX)
        cout << "unconnected" << endl;
    else
        cout << minDist[n] << endl;
}
```

### SPFA

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
    vector<int> count(n+1,0);
    count[start]++;
    bool flag = false;
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
                    count[to]++;
                    if(count[to] >= n){
                        flag = true;
                        while (!que.empty()) {
                            que.pop();
                        }
                        break;
                    }
                }
            }
        }
    }
    if (flag) {
        cout << "circle" << endl;
        return 0;
    }
    if (minDist[end] == INT32_MAX)
        cout << "unconnected" << endl;
    else
        cout << minDist[end] << endl;
}
```
