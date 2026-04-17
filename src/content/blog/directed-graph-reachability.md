---
title: '有向图的完全可达性'
description: '判断有向图中从节点1能否到达所有其他节点，使用DFS解决'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 深度优先搜索
  - 有向图
---

# 有向图的完全可达性

**发布日期:** 2025/12/21
**阅读时间:** 1 分钟
**标签:** 算法笔记, 图论, 数据结构, 算法, 深度优先搜索, DFS, 有向图, Leetcode

## 正文
# 有向图的完全可达性

## 题目描述

给定一个有向图，包含 N 个节点，节点编号分别为 1，2，...，N。现从 1 号节点开始，如果可以从 1 号节点的边可以到达任何节点，则输出 1，否则输出 -1。

[题目链接](https://kamacoder.com/problempage.php?pid=1177)

[文章讲解](https://programmercarl.com/kamacoder/0105.%E6%9C%89%E5%90%91%E5%9B%BE%E7%9A%84%E5%AE%8C%E5%85%A8%E5%8F%AF%E8%BE%BE%E6%80%A7.html)

## 思路

目标是判断图是否强连通（从任意节点都能到达任意其他节点）。这里进行了简化，只检查从节点1能否到达所有其他节点。

因为节点编号都从1开始，因此选择K+1、 N+1大小

```cpp
vector<list<int>> grah(N+1);  // 邻接表存储图
vector<bool> visit(N + 1, false);  // 访问标记数组
```

##### 构建图

```cpp
vector<list<int>> grah(N+1);
for(int i = 0;i < K;i++){
    cin >> s >> t;
    grah[s].push_back(t);  // 添加有向边s->t
}
```

##### 连通性检查

```cpp
for(int i = 1;i<visit.size();i++){
    if(visit[i] == false) {
        cout << -1 << endl;  // 存在未访问节点，非强连通
        return 0;
    }
}
cout << 1 << endl;  // 所有节点都被访问，强连通
```

这道题里面卡尔强调了单层递归的两种处理逻辑。和之前思考的问题是一致的。

在递归中，**我们是处理当前访问的节点，还是处理下一个要访问的节点？**

本题中处理，就是 visit 数组来记录访问过的节点，该节点默认 数组里元素都是false，把元素标记为 true 就是处理 本节点了。

如果我们是处理当前访问的节点，当前访问的节点如果是 true ，说明是访问过的节点，那就终止本层递归，如果不是true，我们就把它赋值为true，因为这是我们处理本层递归的节点。

这种就是先不管下个节点访没访问过，我先递归进去，进去了再看看有没有访问过，如果已经访问过，那我直接返回，退出当前函数就行了。如果没有访问过，那我就处理当前节点，标记为访问过。

接下来我写的这种是我先看看下一个节点访没访问过，访问过我就不递归进去，没访问过，我就处理这个下个节点（标记访问过），然后递归进去。

这种保证了只要在递归内，当前节点一定是已经标记过的。

## 代码实现

```cpp
#include <iostream>
#include <vector>
#include <list>
using namespace std;

void dfs(vector<list<int>>& grah,vector<bool>& visit,int key){
    list<int> keys = grah[key];
    for(auto k:keys){
        if(visit[k] == true) continue;
        visit[k] = true;
        dfs(grah,visit,k);
    }
}

int main(){
    int N,K,s,t;
    cin >> N >> K;
    vector<list<int>> grah(N+1);
    for(int i = 0;i < K;i++){
        cin >> s >> t;
        grah[s].push_back(t);
    }

    vector<bool> visit(N + 1, false);

    visit[1] = true;
    dfs(grah,visit,1);
    for(int i = 1;i<visit.size();i++){
        if(visit[i] == false) {
            cout << -1 << endl;
            return 0;
        }
    }
    cout << 1 << endl;

}
```