---
title: '岛屿周长'
description: '岛屿的周长'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 数据结构
  - 岛屿问题
  - Leetcode
---

## 题目描述

给定一个由 1（陆地）和 0（水）组成的矩阵，岛屿是被水包围，并且通过水平方向或垂直方向上相邻的陆地连接而成的。

你可以假设矩阵外均被水包围。在矩阵中恰好拥有一个岛屿，假设组成岛屿的陆地边长都为 1，请计算岛屿的周长。岛屿内部没有水域。

[题目链接](https://kamacoder.com/problempage.php?pid=1178)

[文章讲解](https://programmercarl.com/kamacoder/0106.%E5%B2%9B%E5%B1%BF%E7%9A%84%E5%91%A8%E9%95%BF.html)

## 思路

本题不用深搜或广搜，只需要遍历所有方格。某个方格对周长的贡献周长本应是 0，但陆地的四个方向，该方向上如果越界或者是海洋的话，周长就加一；

## 代码实现

```cpp
#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> grid(n, vector<int>(m, 0));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> grid[i][j];
        }
    }
    int direction[4][2] = {0, 1, 1, 0, -1, 0, 0, -1};
    int result = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (grid[i][j] == 1) {
                for (int k = 0; k < 4; k++) {       // 上下左右四个方向
                    int x = i + direction[k][0];
                    int y = j + direction[k][1];    // 计算周边坐标x,y
                    if (x < 0                       // x在边界上
                            || x >= grid.size()     // x在边界上
                            || y < 0                // y在边界上
                            || y >= grid[0].size()  // y在边界上
                            || grid[x][y] == 0) {   // x,y位置是水域
                        result++;
                    }
                }
            }
        }
    }
    cout << result << endl;

}
```