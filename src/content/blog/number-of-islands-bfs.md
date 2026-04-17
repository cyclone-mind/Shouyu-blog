---
title: '岛屿数量-广搜'
description: '岛屿数量算法题解，使用广度优先搜索(BFS)解决'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 数据结构
  - 广度优先搜索
  - BFS
  - 岛屿问题
  - Leetcode
---

## 题目描述

给定一个由 1（陆地）和 0（水）组成的矩阵，你需要计算岛屿的数量。岛屿由水平方向或垂直方向上相邻的陆地连接而成，并且四周都是水域。你可以假设矩阵外均被水包围。

具体描述见题目链接

[题目链接](https://kamacoder.com/problempage.php?pid=1171)

[文章讲解](https://programmercarl.com/kamacoder/0099.%E5%B2%9B%E5%B1%BF%E7%9A%84%E6%95%B0%E9%87%8F%E5%B9%BF%E6%90%9C.html)

## 思路

广搜版岛屿的数量。

遇到一个没有遍历过的节点陆地，计数器就加一，然后把该节点陆地所能遍历到的陆地都标记上。

再遇到标记过的陆地节点和海洋节点的时候直接跳过。 这样计数器就是最终岛屿的数量。

那么如果**把节点陆地所能遍历到的陆地都标记上**呢，就可以使用 DFS，BFS或者并查集。

本体存在一个超时写法，就是把节点从队列中取出再标记。

超时写法

```cpp
int dir[4][2] = {0, 1, 1, 0, -1, 0, 0, -1}; // 四个方向
void bfs(vector<vector<char>>& grid, vector<vector<bool>>& visited, int x, int y) {
    queue<pair<int, int>> que;
    que.push({x, y});
    while(!que.empty()) {
        pair<int ,int> cur = que.front(); que.pop();
        int curx = cur.first;
        int cury = cur.second;
        visited[curx][cury] = true; // 从队列中取出在标记走过
        for (int i = 0; i < 4; i++) {
            int nextx = curx + dir[i][0];
            int nexty = cury + dir[i][1];
            if (nextx < 0 || nextx >= grid.size() || nexty < 0 || nexty >= grid[0].size()) continue;  // 越界了，直接跳过
            if (!visited[nextx][nexty] && grid[nextx][nexty] == '1') {
                que.push({nextx, nexty});
            }
        }
    }

}
```

正确写法

```cpp
int dir[4][2] = {0, 1, 1, 0, -1, 0, 0, -1}; // 四个方向
void bfs(vector<vector<char>>& grid, vector<vector<bool>>& visited, int x, int y) {
    queue<pair<int, int>> que;
    que.push({x, y});
    visited[x][y] = true; // 只要加入队列，立刻标记。这里也可以写到主函数中。见代码实现
    while(!que.empty()) {
        pair<int ,int> cur = que.front(); que.pop();
        int curx = cur.first;
        int cury = cur.second;
        for (int i = 0; i < 4; i++) {
            int nextx = curx + dir[i][0];
            int nexty = cury + dir[i][1];
            if (nextx < 0 || nextx >= grid.size() || nexty < 0 || nexty >= grid[0].size()) continue;  // 越界了，直接跳过
            if (!visited[nextx][nexty] && grid[nextx][nexty] == '1') {
                que.push({nextx, nexty});
                visited[nextx][nexty] = true; // 只要加入队列立刻标记
            }
        }
    }

}
```

## 代码实现

```cpp
#include <iostream>
#include <queue>
#include <utility>
#include <vector>

using namespace std;
vector<vector<int>> dir = {{0, 1}, {1, 0}, {-1, 0}, {0, -1}};
// 广搜
void bfs(const vector<vector<int>> &gird, vector<vector<bool>> &visited, int x,
         int y) {
  queue<pair<int, int>> que;
  que.push({x, y});
  while (!que.empty()) {
    pair<int, int> cur = que.front();
    que.pop();
    for (int i = 0; i < 4; i++) {
      int next_x = cur.first + dir[i][0];
      int next_y = cur.second + dir[i][1];
      if (next_x < 0 || next_y < 0 || next_x == gird.size() ||
          next_y == gird[0].size()) {
        continue;
      }
      if (visited[next_x][next_y] == false && gird[next_x][next_y] == 1) {
        que.push({next_x, next_y}); 
        visited[next_x][next_y] = true;
      }
    }
  }
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
  vector<vector<bool>> visited(N, vector<bool>(M, false));
  int result = 0;
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < M; j++) {
      if (gird[i][j] == 1 && visited[i][j] == false) { // 是陆地，且没有访问过
        result++;
        visited[i][j] = true;
        bfs(gird, visited, i, j); // 以这个陆地为起点进行搜索，做什么？
      }
    }
  }
  cout << result << endl;
  return 0;
}
```