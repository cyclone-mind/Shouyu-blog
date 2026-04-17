---
title: '建造最大人工岛'
description: 'DFS深度优先搜索解决最大人工岛问题，将一格水变为陆地后求最大岛屿面积。'
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

给定一个由 1（陆地）和 0（水）组成的矩阵，你最多可以将矩阵中的一格水变为一块陆地，在执行了此操作之后，矩阵中最大的岛屿面积是多少。

岛屿面积的计算方式为组成岛屿的陆地的总数。岛屿是被水包围，并且通过水平方向或垂直方向上相邻的陆地连接而成的。你可以假设矩阵外均被水包围。

[题目链接](https://kamacoder.com/problempage.php?pid=1176)

[文章讲解](https://programmercarl.com/kamacoder/0104.%E5%BB%BA%E9%80%A0%E6%9C%80%E5%A4%A7%E5%B2%9B%E5%B1%BF.html)

## 思路

直观的暴力想法，应该是遍历地图尝试 将每一个 0 改成1，然后去搜索地图中的最大的岛屿面积。

计算地图的最大面积：遍历地图 + 深搜岛屿，时间复杂度为 n * n。

每改变一个0的方格，都需要重新计算一个地图的最大面积。$O(n^4)$。

### 优化

1. 依次遍历地图，使用深搜拿到所有岛屿及对应面积，每个岛屿应有编号。记录到一个 map 中。key为岛屿编号，value为岛屿面积。

1. 随后再遍历所有海洋，找跟 0 方格相连的所有岛屿，将相连的所有岛屿面积相加。最后求一个最大值。

### 特殊情况

本题有一个特殊情况：全为陆地，这样就不需要替换海洋，直接输出 N*M 即可了。

## 代码实现

```cpp
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std;

int dir[4][2] = {{0, 1}, {1, 0}, {-1, 0}, {0, -1}};

void dfs(vector<vector<int>> &gird, vector<vector<bool>> &visited, int x, int y,
         int mark, int &count) {
    if (visited[x][y] == true)
        return;
    visited[x][y] = true;
    gird[x][y] = mark;
    count++;
    for (int i = 0; i < 4; i++) {
        int nextx = x + dir[i][0];
        int nexty = y + dir[i][1];
        if (nextx < 0 || nexty < 0 || nextx >= gird.size() ||
            nexty >= gird[0].size())
            continue;
        if (gird[nextx][nexty] == 0)
            continue;
        dfs(gird, visited, nextx, nexty, mark, count);
    }
}

int main() {
    int N, M;
    cin >> N >> M;
    vector<vector<int>> gird(N, vector<int>(M, 0));
    vector<vector<bool>> visited(N, vector<bool>(M, false));
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            cin >> gird[i][j];
        }
    }
    unordered_map<int, int> girdNum;
    int mark = 2;
    bool hasWater = false; // 标记是否有海水

    // 第一步：给每个岛屿编号并记录面积
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            if (gird[i][j] == 0) {
                hasWater = true; // 发现海水
            } else if (gird[i][j] == 1 && visited[i][j] == false) {
                int count = 0;
                dfs(gird, visited, i, j, mark, count);
                girdNum[mark] = count;
                mark++;
            }
        }
    }

    // 边界情况：如果没有海水，整个网格都是陆地
    if (!hasWater) {
        cout << N * M << endl;
        return 0;
    }

    int maxArea = 0;
    // 第二步：尝试填海造陆
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            if (gird[i][j] == 0) {
                unordered_set<int> islandNum;
                int icount = 1; // 当前位置变为陆地，面积+1
                for (int k = 0; k < 4; k++) {
                    int nextx = i + dir[k][0];
                    int nexty = j + dir[k][1];
                    if (nextx < 0 || nexty < 0 || nextx >= gird.size() ||
                        nexty >= gird[0].size())
                        continue;
                    if (islandNum.count(gird[nextx][nexty]))
                        continue;
                    islandNum.insert(gird[nextx][nexty]);
                    icount += girdNum[gird[nextx][nexty]];
                }
                maxArea = maxArea > icount ? maxArea : icount;
            }
        }
    }
    cout << maxArea << endl;
}
```