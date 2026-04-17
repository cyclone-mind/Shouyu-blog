---
title: '孤岛总面积'
description: '所有孤岛的总面积'
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
  - 岛屿问题
  - Leetcode
---

## 题目描述

给定一个由 1（陆地）和 0（水）组成的矩阵，岛屿指的是由水平或垂直方向上相邻的陆地单元格组成的区域，且完全被水域单元格包围。孤岛是那些位于矩阵内部、所有单元格都不接触边缘的岛屿。

现在你需要计算所有**孤岛的总面积**，岛屿面积的计算方式为组成岛屿的陆地的总数。

[题目链接](https://kamacoder.com/problempage.php?pid=1173)

[文章链接](https://programmercarl.com/kamacoder/0101.%E5%AD%A4%E5%B2%9B%E7%9A%84%E6%80%BB%E9%9D%A2%E7%A7%AF.html)

## 思考

不找到孤岛，而是把所有非孤岛（靠边的岛屿）找到，标记为海洋。类似于“沉没”，之后再正常找到所有的陆地总面积就是所有的孤岛总面积了

靠边的岛屿很好找，这道题目中不再需要 visited 数组来判断陆地是否已经遍历过了，因为我们最终要找到的是所有的孤岛。这些孤岛，在沉没非孤岛的时候不会被沉没，因此只需要`if (gird[i][j] == 1)`就可以判断。

至于在沉没的时候也不需要 visited ，因为在扩展整个岛屿时，沉没这个动作就已经替代了 visited 的作用。

```cpp
if (gird[next_x][next_y] == 0) {
    continue;
}
dfs(gird, next_x, next_y);
```

扩展遍历至海洋的时候跳过，而原来是 visited 为 true 的时候跳过

## 代码实现

##### 深搜版

```cpp
#include <iostream>
#include <vector>
using namespace std;
int island_count;

vector<vector<int>> dir = {{0, 1}, {1, 0}, {-1, 0}, {0, -1}};
void dfs(vector<vector<int>> &gird, int x,
         int y) {
            gird[x][y] = 0;
    for (int current = 0; current < 4; current++) {
        int next_x = x + dir[current][0];
        int next_y = y + dir[current][1];
        if (next_x < 0 || next_y < 0 || next_x == gird.size() ||
            next_y == gird[0].size()) {
            continue;
        }
        if (gird[next_x][next_y] == 0) {
            continue;        
        }
        dfs(gird, next_x, next_y);
    }
    return;
}

int main() {
    int N, M;
    cin >> N >> M;
    vector<vector<int>> gird(N, vector<int>(M, 0));
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            cin >> gird[i][j];
        }
    }
    for(int i = 0;i < N;i++){
        if(gird[i][0] == 1) dfs(gird,i,0);
        if(gird[i][M-1] == 1) dfs(gird,i,M-1);
    }
    for(int j = 0;j < M;j++){
        if(gird[0][j] == 1) dfs(gird,0,j);
        if(gird[N-1][j] == 1) dfs(gird,N-1,j);
    }
    int S = 0;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            if (gird[i][j] == 1) {
                S++;
            }
        }
    }
    cout << S << endl;
}
```