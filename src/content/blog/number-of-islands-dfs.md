---
title: '岛屿数量-深搜'
description: '岛屿数量算法题解，使用深度优先搜索(DFS)解决'
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

给定一个由 1（陆地）和 0（水）组成的矩阵，你需要计算岛屿的数量。岛屿由水平方向或垂直方向上相邻的陆地连接而成，并且四周都是水域。你可以假设矩阵外均被水包围。

具体描述见题目链接

[题目链接](https://kamacoder.com/problempage.php?pid=1171)

[文章讲解](https://programmercarl.com/kamacoder/0099.%E5%B2%9B%E5%B1%BF%E7%9A%84%E6%95%B0%E9%87%8F%E6%B7%B1%E6%90%9C.html)

## 思路

要求出岛屿数量，需要知道什么时候踏上了一座全新的岛屿，之前未曾踏足过的岛屿。

这就需要我们做到一点：一旦到达某个岛屿就把这个岛屿的全陆地遍历一遍，标记为已踏足。这正是深搜或广搜可以做的事。

我们开始遍历所有节点，看该节点是否是陆地，是陆地的话看是否被踏足过，如果没有，恭喜，找到了一个岛屿。

注意，这道题目没有回溯是因为没有需要撤销的选择，即我们不需要把已经标记过的陆地撤销标记

## 代码实现

```cpp
#include <iostream>
#include <queue>
#include <utility>
#include <vector>

using namespace std;
vector<vector<int>> dir = {{0, 1}, {1, 0}, {-1, 0}, {0, -1}};
// 深搜
void dfs(const vector<vector<int>> &gird, vector<vector<bool>> &visited,
         int x, int y) {
            // 以这个x，y这个陆地为起点进行搜索，做什么？将相连的并且是陆地的并且没有访问过的陆地标记为已访问
    for (int current = 0; current < 4; current++) {
        int next_x = x + dir[current][0];
        int next_y = y + dir[current][1];
        if (next_x < 0 || next_y < 0 || next_x == gird.size() ||
            next_y == gird[0].size()) {
            continue;
        }
        if (visited[next_x][next_y] == false && gird[next_x][next_y] == 1) { 
            // 相连的并且是陆地的并且没有访问过的陆地才进入下一步搜索 
            visited[next_x][next_y] = true; 
            // 搜索之前先把陆地标记了 dfs(gird, visited, next_x, next_y);
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
            if (gird[i][j] == 1 &&
                visited[i][j] == false) { // 是陆地，且没有访问过
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

### 深搜的另一种实现

上一种深搜的代码呢是把递归的终止条件写在了`if (visited[next_x][next_y] == false && gird[next_x][next_y] == 1)`里面。进入到递归之前就将 visited 标记为 true。

这是回溯写法的经典范式：1. 做出选择/处理下个节点，2. 再进入下个节点，3. 出来后撤销选择/处理下个节点。

而还有一种写法是显式写递归的终止条件，且进入到递归之后再将 visited 标记为 true。

```cpp
// 版本二
#include <iostream>
#include <vector>
using namespace std;
int dir[4][2] = {0, 1, 1, 0, -1, 0, 0, -1}; // 四个方向
void dfs(const vector<vector<int>>& grid, vector<vector<bool>>& visited, int x, int y) {
    if (visited[x][y] || grid[x][y] == 0) return; // 终止条件：访问过的节点 或者 遇到海水
    visited[x][y] = true; // 标记访问过
    for (int i = 0; i < 4; i++) {
        int nextx = x + dir[i][0];
        int nexty = y + dir[i][1];
        if (nextx < 0 || nextx >= grid.size() || nexty < 0 || nexty >= grid[0].size()) continue;  // 越界了，直接跳过
        dfs(grid, visited, nextx, nexty);
    }
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> grid(n, vector<int>(m, 0));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> grid[i][j];
        }
    }

    vector<vector<bool>> visited(n, vector<bool>(m, false));

    int result = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (!visited[i][j] && grid[i][j] == 1) {
                result++; // 遇到没访问过的陆地，+1
                dfs(grid, visited, i, j); // 将与其链接的陆地都标记上 true
            }
        }
    }
    cout << result << endl;
}
```