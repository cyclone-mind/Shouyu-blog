---
title: '水流问题'
description: '水流问题：深度优先搜索岛屿问题'
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

现有一个 N × M 的矩阵，每个单元格包含一个数值，这个数值代表该位置的相对高度。矩阵的左边界和上边界被认为是第一组边界，而矩阵的右边界和下边界被视为第二组边界。

矩阵模拟了一个地形，当雨水落在上面时，水会根据地形的倾斜向低处流动，但只能从较高或等高的地点流向较低或等高并且相邻（上下左右方向）的地点。我们的目标是确定那些单元格，从这些单元格出发的水可以达到第一组边界和第二组边界。

[题目链接](https://kamacoder.com/problempage.php?pid=1175)

[文章讲解](https://programmercarl.com/kamacoder/0103.%E6%B0%B4%E6%B5%81%E9%97%AE%E9%A2%98.html)

## 思路

直观的暴力解法是遍历所有点，然后在该点的基础上深搜或广搜，看看不不能到达第一边界和第二边界。

该解法时间复杂度 $O(n^2m^2)$ ， 明显超时

优化：

采用上一题**沉没孤岛**的逆向思维，原题描述好像从每个格子上面倒水，看看能不能流下来，逆向思维就是从边界向上攀爬，只能向上不能像下，看看哪些点能从两个边界上爬上来。

从第一组边界上的节点 逆流而上，将遍历过的节点都标记上（用一个数组保存）。代表了能从第一组边界爬上去的点，也就代表了这些点能流下第一组边界。

同样从第二组边界的边上节点 逆流而上，将遍历过的节点也标记上（用一个数组保存）。

然后，**双方都标记过的节点就是既可以流向第一组边界也可以流向第二组边界的节点**

## 代码实现

```cpp
#include <iostream>
#include <vector>
using namespace std;

int dir[4][2] = {{0,1},{1,0},{-1,0},{0,-1}};

void dfs(vector<vector<int>>& gird,vector<vector<bool>>& visited,int x,int y){
    if(visited[x][y] == true) return;
    visited[x][y] = true;
    for(int i = 0;i < 4;i++){
        int nextx = x + dir[i][0];
        int nexty = y + dir[i][1];
        if(nextx < 0 || nexty < 0 || nextx >= gird.size() || nexty >= gird[0].size()) continue;
        if(gird[nextx][nexty] < gird[x][y]) continue;
        dfs(gird,visited,nextx,nexty);
    }
    return;
}

int main(){
    int N,M;
    cin>>N>>M;
    vector<vector<int>> gird(N,vector<int>(M,0));
    for(int i = 0;i < N;i++){
        for(int j = 0;j < M;j++){
            int num;
            cin >> num;
            gird[i][j] = num;
        }
    }
    vector<vector<bool>> firstborder(N,vector<bool>(M,false));
    vector<vector<bool>> secondborder(N,vector<bool>(M,false));
    for(int i = 0;i < N;i++){
        dfs(gird,firstborder,i,0);
        dfs(gird,secondborder,i,M-1);
    }
    for(int j = 0;j < M;j++){
        dfs(gird,firstborder,0,j);
        dfs(gird,secondborder,N-1,j);
    }
    for(int i = 0;i < N;i++){
        for(int j = 0;j < M;j++){
            if(firstborder[i][j] && secondborder[i][j]){
                cout << i << " " << j << endl;
            }
        }
    }
}
```