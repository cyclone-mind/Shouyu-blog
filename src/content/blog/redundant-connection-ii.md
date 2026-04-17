---
title: '冗余连接II'
description: '有向图的冗余连接问题'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 并查集
  - 有向图
  - 环检测
  - Leetcode
---

## 题目描述

有一种有向树,该树只有一个根节点，所有其他节点都是该根节点的后继。该树除了根节点之外的每一个节点都有且只有一个父节点，而根节点没有父节点。有向树拥有 n 个节点和 n - 1 条边。如图：

现在有一个有向图，有向图是在有向树中的两个没有直接链接的节点中间添加一条有向边。如图：

输入一个有向图，该图由一个有着 n 个节点(节点编号 从 1 到 n)，n 条边，请返回一条可以删除的边，使得删除该条边之后该有向图可以被当作一颗有向树。

[题目链接](https://kamacoder.com/problempage.php?pid=1182)

[文章讲解](https://programmercarl.com/kamacoder/0109.%E5%86%97%E4%BD%99%E8%BF%9E%E6%8E%A5II.html)

## 思考

题目本质：找到冗余的边删除它，这条 冗余的边 使原本的一颗有向树不再是有向树了。

另外有题目要求：“**若有多条边可以删除，请输出标准输入中最后出现的一条边**”。这意味着如果这条冗余的边不唯一，则输出标准输入中最后出现的那条。

上一句话有个要点，即冗余的边只有一条，但是可能不唯一。

因为图有向，因此在有向树中，除根节点以外其他所有节点入度为1，但是一旦加上一条冗余的边，则可能有节点入度为2。

所以情况一：找到入度为2的点，删一条指向该节点的边就行了。

这种情况删 1 -> 3 或者 2 -> 3 都行，选择删标准输入中顺序靠后的那个。

但是入度为2还有一种情况：

这种情况下，只能删1->3这条边。

所以如果发现存在入度为2的节点，那么一定有两条待选的冗余的边，如果删除了靠后的那条边后能成为有向树，说明我们删对了，如果不能成为有向树，就说明冗余的边是前面的那条边。

情况三：没有入度为2的节点，而是形成了有向环。

对于有向环，和**冗余的边**类似，直接删除形成环的边

## 易错点

1. 存储所有边时不要预分配大小

1. 判断待选的边是否冗余时需要初始化并查集。因为判断是否冗余就是要看其余边是都在同一集合。

## 代码实现

```cpp
#include <iostream>
#include <vector>

using namespace std;

vector<int> father(1001, 0);

// 初始化并查集
void init(int n) {
    for (int i = 1; i <= n; i++) {
        father[i] = i;
    }
}

// 查找根节点（路径压缩）
int find(int u) { return father[u] == u ? u : father[u] = find(father[u]); }

// 判断两个节点是否在同一连通分量
bool isSame(int u, int v) {
    u = find(u);
    v = find(v);
    return u == v;
}

// 合并两个连通分量
void join(int u, int v) {
    u = find(u);
    v = find(v);
    if (u == v)
        return;
    father[v] = u;
}

// 检查删除指定边后是否能形成有向树
bool isRedundant(vector<pair<int, int>> &edges, int skipIndex, int n) {
    init(n); // 重新初始化并查集
    for (int i = 0; i < edges.size(); i++) {
        if (i == skipIndex)
            continue; // 跳过指定边
        if (isSame(edges[i].first, edges[i].second)) {
            return false; // 发现环，不能形成树
        } else {
            join(edges[i].first, edges[i].second);
        }
    }
    return true; // 能形成树
}

int main() {
    int n, s, t;
    cin >> n;
    vector<pair<int, int>> edges;   // 不预分配大小
    vector<int> indegree(n + 1, 0); // 入度数组

    // 读取边并计算入度
    for (int i = 0; i < n; i++) {
        cin >> s >> t;
        edges.push_back({s, t});
        indegree[t]++;
    }

    // 查找入度为2的节点对应的边
    vector<int> redundant_edges;
    for (int i = 0; i < n; i++) {
        if (indegree[edges[i].second] == 2) {
            redundant_edges.push_back(i);
        }
    }

    // 情况1：存在入度为2的节点
    if (redundant_edges.size() > 0) {
        // 优先删除后出现的边
        if (redundant_edges.size() >= 2) {
            if (isRedundant(edges, redundant_edges[1], n)) {
                cout << edges[redundant_edges[1]].first << " "
                     << edges[redundant_edges[1]].second << endl;
                return 0;
            } else {
                cout << edges[redundant_edges[0]].first << " "
                     << edges[redundant_edges[0]].second << endl;
                return 0;
            }
        } else {
            // 只有一条边指向入度为2的节点
            cout << edges[redundant_edges[0]].first << " "
                 << edges[redundant_edges[0]].second << endl;
            return 0;
        }
    }

    // 情况2：没有入度为2的节点，直接查找形成环的边
    init(n);
    for (int i = 0; i < edges.size(); i++) {
        if (isSame(edges[i].first, edges[i].second)) {
            cout << edges[i].first << " " << edges[i].second << endl;
            return 0;
        } else {
            join(edges[i].first, edges[i].second);
        }
    }

    return 0;
}
```