---
title: '所有可达路径'
description: '使用DFS和BFS解决有向无环图中从节点1到节点N的所有路径问题。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 数据结构
  - 深度优先搜索
  - DFS
  - 路径问题
  - Leetcode
---

## 题目描述

给定一个有 n 个节点的有向无环图，节点编号从 1 到 n。请编写一个函数，找出并返回所有从节点 1 到节点 n 的路径。每条路径应以节点编号的列表形式表示。

### 输入描述

第一行包含两个整数 N，M，表示图中拥有 N 个节点，M 条边

后续 M 行，每行包含两个整数 s 和 t，表示图中的 s 节点与 t 节点中有一条路径

### 输出描述

输出所有的可达路径，路径中所有节点之间空格隔开，每条路径独占一行，存在多条路径，路径输出的顺序可任意。如果不存在任何一条路径，则输出 -1。

**注意输出的序列中，最后一个节点后面没有空格！**例如正确的答案是`1 3 5`,而不是`1 3 5`， 5后面没有空格！

### 输入示例

```bash
5 5
1 3
3 5
1 2
2 4
4 5
```

### 输出示例

```bash
1 3 5
1 2 4 5
```

[题目链接](https://kamacoder.com/problempage.php?pid=1170)

[文章讲解](https://programmercarl.com/kamacoder/0098.%E6%89%80%E6%9C%89%E5%8F%AF%E8%BE%BE%E8%B7%AF%E5%BE%84.html)

## 思路

这道题是入门图论的好题目，可以掌握 dfs 和 bfs 的基础写法。

题目要求求所有可达路径，每条路径是一个列表。

所以我们设置一个全局的表示所有可达路径的二维数组保存所有路径。`vector<vector<int>> result;`

再设置一个全局的一维数组表示伴随着遍历节点而变化的正在探索的或者说所处的路径。`vector<int> path;`

* path (全局变量): 记录当前正在探索的路径。

* result (全局变量): 存储所有已经找到的、从起点到终点的完整路径。

图的保存可以使用邻接矩阵，构建方便。构建时需要注意节点的序号是从 1 开始的，而不是 0，因此可以构建一个 N+1 大小的二维数组，这样`graph[1][2]`就表示 1 节点和 2 节点之间的边了。

## 深搜三部曲

**第一步：确定函数的目的和参数**

* 目的：找到所有路径。

* 需要什么信息？

需要知道图长什么样 -> `const vector<vector<int>> &graph`
需要知道当前在哪 -> `int currentNode`
需要知道目标在哪 -> `int targetNode`

* 需要知道图长什么样 -> `const vector<vector<int>> &graph`

* 需要知道当前在哪 -> `int currentNode`

* 需要知道目标在哪 -> `int targetNode`

* 初步函数签名：`void findPaths(const vector<vector<int>> &graph, int currentNode, int targetNode)`

**第二步：确定递归的终止条件**

* 什么时候停下来？ 当到达目的地时。

* 条件：`currentNode == targetNode`。

* 停下来做什么？ 已经找到了一条完整路径。这条路径存储在某个地方（一个全局的 path 向量）。需要把它保存到一个最终结果集里（比如 result 向量）。

* 代码实现：
* 
if (currentNode == targetNode) {
    result.push_back(path); // `path` 和 `result` 需要在函数外定义
    return;
}

**第三步：确定递归的递推关系**

* 如果没到终点，该做什么？ 遍历当前节点能到达的所有邻居节点。

* 如何遍历？ 写一个循环，从 1 到 N，检查 `graph[currentNode][neighbor]` 是否为 1。

* 对每个邻居节点做什么？

选择 (Choose)：把它加入到当前路径中。path.push_back(neighbor);
探索 (Explore)：以这个邻居为新的当前节点，递归调用函数。findPaths(graph, neighbor, targetNode);
撤销 (Unchoose / Backtrack)：当对这个邻居的探索结束后（即递归调用返回后），要把它从当前路径中移除，以便于探索当前节点的其他邻居。path.pop_back();

* 代码实现

```cpp
for (int neighbor = 1; neighbor <= N; ++neighbor) {
    if (graph[currentNode][neighbor] == 1) {
        path.push_back(neighbor);
        findPaths(graph, neighbor, targetNode);
        path.pop_back();
    }
}
```

把深搜的过程理解成**走迷宫**：

1. 起点：从节点 x 开始（第一次调用时是从节点 1 开始）。

2. 目标：目标是走到节点 n。

3. 路径记录：手上有一个本子 (path)，每走到一个新节点，你就在本子上记下它的编号。这是我们处理节点的逻辑，也就是说我们遍历到当前节点需要做什么

* 终止条件 (Base Case):
if (x == n) {
  result.push_back(path);
  return;
}

理解：如果你当前所在的节点 x 就是终点 n，找到了一条完整的路径 这时，把本子 (path) 上的完整路径放到(result)里，然后这条路的探索就到此为止，准备原路返回去尝试别的路口。

* 递归步骤 (Recursive Step): // 处理目前搜索节点出发的路径
for (int i = 1; i <= n; i++) {
  if (graph[x][i] == 1) { // 如果从当前节点x到节点i有路
    path.push_back(i);     // 1. 做出选择：往前走一步到i，并记录下来
    dfs(graph, i, n);      // 2. 继续探索：从新的节点i开始，重复整个走迷宫的过程
    path.pop_back();       // 3. 撤销选择 (回溯)：从节点i返回到节点x
  }
}

理解：站在节点 x，环顾四周，查看地图 (graph)，寻找所有能直接走到的下一个节点 i。


对于每一个可能的下一节点 i：

前进：决定先走向 i。在本子 (path) 上写下 i。
深入：把探索任务交给了“下一个你”，让他从 i 出发去寻找终点 n (这就是dfs(graph, i, n)的调用)。
回溯：当“下一个你”完成了从 i 出发的所有探索（无论找到终点与否）并返回后，你需要退回到你当前所在的节点 x。为了做到这一点，你必须把本子上刚刚记下的 i 划掉 (path.pop_back())。为什么要这么做？因为这样你才能继续尝试从 x 走向其他还没去过的节点，寻找其他可能的路径。

* 对于每一个可能的下一节点 i：

前进：决定先走向 i。在本子 (path) 上写下 i。
深入：把探索任务交给了“下一个你”，让他从 i 出发去寻找终点 n (这就是dfs(graph, i, n)的调用)。
回溯：当“下一个你”完成了从 i 出发的所有探索（无论找到终点与否）并返回后，你需要退回到你当前所在的节点 x。为了做到这一点，你必须把本子上刚刚记下的 i 划掉 (path.pop_back())。为什么要这么做？因为这样你才能继续尝试从 x 走向其他还没去过的节点，寻找其他可能的路径。

这个递归步骤有一点很重要就是**前进之前**就把 下一个节点写入到 path 中，而**不是进入到下个节点**才把下个节点写到 path 中。

### 经典的回溯算法范式

这是经典的回溯算法范式，可以分解为三步：

1. 做出选择 (Choose): path.push_back(i);

在循环中，当你决定要从当前节点 x 走向下一个节点 i 时，你把这个“选择”(i)记录下来。

1. 探索 (Explore): dfs(graph, i, n);

基于这个选择，继续向下探索所有可能性。

1. 撤销选择 (Unchoose/Backtrack): path.pop_back();

当从 i 出发的所有路径都探索完毕（即 dfs(graph, i, n) 返回后），你必须撤销刚才的选择，这样才能在下一次循环中尝试从 x 走向另一个节点。

在这个递归步骤中，path 始终代表 “到达当前节点之前的路径”。

## 代码实现

```cpp
#include <iostream>
#include <vector>

using namespace std;

vector<vector<int>> result;
vector<int> path;

void dfs(const vector<vector<int>> &graph, int x, int n) {
  if (x == n) {
    result.push_back(path);
    return;
  }
  for (int i = 1; i <= n; i++) {
    if (graph[x][i] == 1) {
      path.push_back(i);
      dfs(graph, i, n);
      path.pop_back();
    }
  }
}
int main() {
  int N, M;
  cin >> N >> M;
  vector<vector<int>> graph(N + 1, vector<int>(N + 1, 0));
  while (M--) {
    int s, t;
    cin >> s >> t;
    graph[s][t] = 1;
  }

  path.push_back(1);

  dfs(graph, 1, N);
  if (result.size() == 0)
    cout << -1 << endl;
  for (auto pa : result) {
    for (int i = 0; i < pa.size() - 1; i++) {
      cout << pa[i] << " ";
    }
    cout << pa[pa.size() - 1] << endl;
  }
}
```