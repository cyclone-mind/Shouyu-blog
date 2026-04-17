---
title: '最小生成树之Prim'
description: '最小生成树Prim算法详解'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 数据结构
  - 最小生成树
  - Prim算法
  - Leetcode
---


## 题目描述

在世界的某个区域，有一些分散的神秘岛屿，每个岛屿上都有一种珍稀的资源或者宝藏。国王打算在这些岛屿上建公路，方便运输。

不同岛屿之间，路途距离不同，国王希望你可以规划建公路的方案，如何可以以最短的总公路距离将 所有岛屿联通起来（注意这是一个无向图）。

给定一张地图，其中包括了所有的岛屿，以及它们之间的距离。以最小化公路建设长度，确保可以链接到所有岛屿。

[题目链接](https://kamacoder.com/problempage.php?pid=1053)

[文章链接](https://programmercarl.com/kamacoder/0053.%E5%AF%BB%E5%AE%9D-prim.html)

## 思考

本题是 prim 算法的应用。是最小生成树的模板题。

为什么这道题本质是要找一个树？

因为如果存在环状结构，那么一定是有边是多余的，多余就不是最短距离，因此一定是求一棵树。

既然是树，可能存在 n 条边的权值小于 n-1 条的情况吗？

不可能，数学证明了对于连通无环图（即树）：

* n 个节点的树恰好有 n-1 条边

* 多于 n-1 条边必然产生环路

* 少于 n-1 条边必然不连通。

题目要求

> 以最短的总公路距离将所有岛屿联通起来"

关键词：**最短距离**+**连通所有节点**

数学证明：连通 + 最短 = 树

反证法：

假设我们找到了一个连通所有节点且总权重最小的子图G：

1. G必须连通

1. G的边数最少

1. 如果G中有环：


环中必定有一条边可以删除


删除后仍然连通


但是权重更少


这与“G权重最小”矛盾

1. 所以G无环！

直观理解就是，把所有岛屿都修上公路连接上，花费最少，但是有环，那么一定有多余的路。

### 最小生成树

最小生成树是所有节点的最小连通子图，即：以**最小的成本**（边的权值）将图中**所有节点链接**到一起。

n 个节点最少需要n-1条边连接在一起

### Prim

Prim 的基本思想是：

从节点的角度，采用贪心的策略**每次寻找距离最小生成树最近**的节点并加入到最小生成树中。

三部曲：

1. 第一步，选距离生成树最近的非生成树节点

1. 第二步，最近节点加入生成树

1. 第三步，更新非生成树节点到生成树的距离（即更新 minDist 数组）

对于第一步中需要判断节点是否为生成树的一部分，可以使用一个数组来判断`vector<bool> isTree(v + 1, false);`下标是节点编号。

对于第三步中非生成树节点到生成树的距离可以使用一个数组来表示，`vector<int> minDist(v + 1, 10001);`

`**minDist**`**数组用来记录每一个节点距离最小生成树的最近距离**。

## 易错点

* 在prim循环里，需要每次都初始化 cur 。

* 每次prim循环里，最小距离可以是10001，也可以是INT_MAX。但是这两者影响到了初始化策略。

如果选择`int minDistance = 10001;`那么第一次找未加入MST且距离最小的节点时就不会将 cur 设置为 1，后续就会出错。所以必须在进入prim循环之前手动初始化将节点1加入到树里。这时，即使不在prim循环，也依然要进行第三步：更新非生成树节点到生成树的距离（即更新`minDist`数组）

如果选择`int minDistance = INT_MAX;`，那么第一次找未加入MST且距离最小的节点时就会将 cur 设置为 1，此时才把节点1加入到树中。

## 代码实现

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int v, e, v1, v2, val;
    cin >> v >> e;
    vector<vector<int>> gird(v + 1, vector<int>(v + 1, 10001));
    while (e--) {
        cin >> v1 >> v2 >> val;
        gird[v1][v2] = val;
        gird[v2][v1] = val;
    }
    vector<bool> isTree(v + 1, false);
    vector<int> minDist(v + 1, 10001);

    // 初始化：选择节点1作为起始节点
    isTree[1] = true;
    for (int i = 1; i <= v; i++) {
        minDist[i] = gird[1][i];
    }

    // Prim算法主循环：需要添加v-1个节点
    for (int k = 1; k < v; k++) {
        int cur = -1; // 初始化为无效值
        int minDistance = 10001;

        // 找到未加入MST且距离最小的节点
        for (int i = 1; i <= v; i++) { 
            if (isTree[i] == false && minDist[i] < minDistance) {
                minDistance = minDist[i];
                cur = i;
            }
        }

        // 将选中的节点加入MST
        isTree[cur] = true;

        // 更新剩余节点到MST的最短距离
        for (int i = 1; i <= v; i++) { 
            if (isTree[i] == false && gird[cur][i] < minDist[i]) {
                minDist[i] = gird[cur][i];
            }
        }
    }

    // 计算MST的总权重
    int result = 0;
    for (int i = 2; i <= v; i++) { 
        result += minDist[i];
    }
    cout << result << endl;
    return 0;
}
```