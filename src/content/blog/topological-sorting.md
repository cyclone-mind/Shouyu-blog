---
title: '拓扑排序'
description: '拓扑排序：解决有向无环图的线性排序问题'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 拓扑排序
  - 有向无环图
  - DAG
  - Leetcode
---

## 题目描述

某个大型软件项目的构建系统拥有 N 个文件，文件编号从 0 到 N - 1，在这些文件中，某些文件依赖于其他文件的内容，这意味着如果文件 A 依赖于文件 B，则必须在处理文件 A 之前处理文件 B （0 <= A, B <= N - 1）。请编写一个算法，用于确定文件处理的顺序。

[题目链接](https://kamacoder.com/problempage.php?pid=1191)

[文章讲解](https://programmercarl.com/kamacoder/0117.%E8%BD%AF%E4%BB%B6%E6%9E%84%E5%BB%BA.html)

## 思考

拓扑排序是经典的图论问题，用于解决复杂依赖关系中的线性顺序输出。

大学排课场景，例如 先上A课，才能上B课，上了B课才能上C课，上了A课才能上D课，等等一系列这样的依赖顺序。 问给规划出一条 完整的上课顺序。

概括来说，**给出一个 有向图，把这个有向图转成线性的排序 就叫拓扑排序**。

另外如果存在循环依赖的情况，则无法做线性输出。

所以，只要能在把**有向无环图 进行线性排序 的算法**都可以叫做**拓扑排序**。

具体实现可能是广搜，也可能是深搜。

一般只需要掌握广搜-卡恩算法即可。

从上面的例子中发现，一定是有一个节点不依赖任何节点的，也就是初始情况下一定有一个入度为0的节点，构建这个软件（节点）不需要提前构建其他软件（节点）。

拓扑排序的过程：

1. 找到入度为 0 的节点，加入结果集。

1. 将该节点从图中移除。

循环以上两步，直到所有节点都在途中被移除。

结果集的顺序，就是我们想要的拓扑排序顺序 （结果集里顺序可能不唯一）

如何判断有向环的存在？

移除的节点不是图中的所有节点，即有节点没有被处理，这时候一定存在有向环。

例如：

为了统计所有节点的入度信息，遍历所有边，记录入读信息`vector<int> inDegree(n, 0); // 记录每个文件的入度`，可以在初始化的时候做这一操作。

另外为了在移除节点的时候把该节点出边去掉，要把这出边指向的节点记录下来，因此使用`unordered_map<int, vector<int>> umap; // 记录文件依赖关系`，同样可以在初始化时做这一步。

```cpp
cin >> n >> m;
vector<int> inDegree(n, 0); // 记录每个文件的入度
vector<int> result; // 记录结果
unordered_map<int, vector<int>> umap; // 记录文件依赖关系

while (m--) {
    // s->t，先有s才能有t
    cin >> s >> t;
    inDegree[t]++; // t的入度加一
    umap[s].push_back(t); // 记录s指向哪些文件
}
```

找到一个入度为零的点后我们需要广搜，去找与它相邻的移除它之后的入度为 0  的点，因此，我们使用队列存放入度为 0 的 点。

```cpp
queue<int> que;
for (int i = 0; i < n; i++) {
    // 入度为0的节点，可以作为开头，先加入队列
    if (inDegree[i] == 0) que.push(i);
}
```

初始化之后，遍历队列里入度为 0 的节点（当然也只有入度为 0 的节点），将其放入结果集中，意味着我们输出了它，处理了它。

```cpp
while (que.size()) {
    int  cur = que.front(); // 当前选中的节点
    que.pop();
    result.push_back(cur);
    // 将该节点从图中移除 

}
```

移除的结果是要把**该节点作为出发点所连接的节点**的 入度 减一。如果减一了之后入度为 0，才是我们要选取的下一个节点，才放入队列。

## 代码实现

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
using namespace std;
int main() {
    int m, n, s, t;
    cin >> n >> m;
    vector<int> inDegree(n, 0); // 记录每个文件的入度

    unordered_map<int, vector<int>> umap;// 记录文件依赖关系
    vector<int> result; // 记录结果

    while (m--) {
        // s->t，先有s才能有t
        cin >> s >> t;
        inDegree[t]++; // t的入度加一
        umap[s].push_back(t); // 记录s指向哪些文件
    }
    queue<int> que;
    for (int i = 0; i < n; i++) {
        // 入度为0的文件，可以作为开头，先加入队列
        if (inDegree[i] == 0) que.push(i);
        //cout << inDegree[i] << endl;
    }
    // int count = 0;
    while (que.size()) {
        int  cur = que.front(); // 当前选中的文件
        que.pop();
        //count++;
        result.push_back(cur);
        vector<int> files = umap[cur]; //获取该文件指向的文件
        if (files.size()) { // cur有后续文件
            for (int i = 0; i < files.size(); i++) {
                inDegree[files[i]] --; // cur的指向的文件入度-1
                if(inDegree[files[i]] == 0) que.push(files[i]);
            }
        }
    }
    if (result.size() == n) {
        for (int i = 0; i < n - 1; i++) cout << result[i] << " ";
        cout << result[n - 1];
    } else cout << -1 << endl;
}
```