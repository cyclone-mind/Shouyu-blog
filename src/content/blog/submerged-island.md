---
title: '沉没孤岛'
description: '将所有孤岛沉没'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - DFS
  - 岛屿问题
  - Leetcode
---


## 题目描述

给定一个由 1（陆地）和 0（水）组成的矩阵，岛屿指的是由水平或垂直方向上相邻的陆地单元格组成的区域，且完全被水域单元格包围。孤岛是那些位于矩阵内部、所有单元格都不接触边缘的岛屿。

现在你需要将所有孤岛“沉没”，即将孤岛中的所有陆地单元格（1）转变为水域单元格（0）。

[题目链接](https://kamacoder.com/problempage.php?pid=1174)

[文章链接]https://programmercarl.com/kamacoder/0102.%E6%B2%89%E6%B2%A1%E5%AD%A4%E5%B2%9B.html

## 思考

与孤岛总面积类似，将非孤岛标记为除1和0以外的任何数，随后遍历矩阵，把剩余所有陆地（孤岛）标记为0，随后再把非孤岛标记回1即可。

## 代码实现

### 深搜版

```cpp
#include <iostream>
#include <vector>
using namespace std;
int island_count;

vector<vector<int>> dir = {{0, 1}, {1, 0}, {-1, 0}, {0, -1}};
void dfs(vector<vector<int>> &gird, int x, int y) {
  gird[x][y] = 2;
  for (int current = 0; current < 4; current++) {
    int next_x = x + dir[current][0];
    int next_y = y + dir[current][1];
    if (next_x < 0 || next_y < 0 || next_x == gird.size() ||
        next_y == gird[0].size()) {
      continue;
    }
    if (gird[next_x][next_y] == 2 || gird[next_x][next_y] == 0) {
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
  for (int i = 0; i < N; i++) {
    if (gird[i][0] == 1)
      dfs(gird, i, 0);
    if (gird[i][M - 1] == 1)
      dfs(gird, i, M - 1);
  }
  for (int j = 0; j < M; j++) {
    if (gird[0][j] == 1)
      dfs(gird, 0, j);
    if (gird[N - 1][j] == 1)
      dfs(gird, N - 1, j);
  }
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < M; j++) {
      if (gird[i][j] == 1) {
        gird[i][j] = 0;
        cout << gird[i][j] << " ";
      } else if (gird[i][j] == 2) {
        gird[i][j] = 1;
        cout << gird[i][j] << " ";
      } else {
        cout << gird[i][j] << " ";
      }
    }
    cout << endl;
  }
}
```