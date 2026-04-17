---
title: '岛屿的最大面积'
description: '岛屿的最大面积算法题解，使用DFS或BFS解决'
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

给定一个由 1（陆地）和 0（水）组成的矩阵，计算岛屿的最大面积。岛屿面积的计算方式为组成岛屿的陆地的总数。岛屿由水平方向或垂直方向上相邻的陆地连接而成，并且四周都是水域。你可以假设矩阵外均被水包围。

[题目链接](https://kamacoder.com/problempage.php?pid=1172)

[文章链接](https://programmercarl.com/kamacoder/0100.%E5%B2%9B%E5%B1%BF%E7%9A%84%E6%9C%80%E5%A4%A7%E9%9D%A2%E7%A7%AF.html)

## 思路

岛屿最大面积可以用深搜也可以广搜，相比较于**岛屿数量问题**只需要更换少量代码。

需要遍历网格时每踏上一个新岛屿，就 设置一个 count 然后再遍历该岛屿，遍历的时候count++计算岛屿面积，遍历完之后比较一下最大面积和count即可。

## 代码实现

### 广搜版

```cpp
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int dir[4][2] = {{0,1},{1,0},{-1,0},{0,-1}};

void bfs(const vector<vector<int>>& gird,vector<vector<bool>>& visited,int x,int y,int& count){
    queue<pair<int,int>> que;
    que.push({x,y});
    while(!que.empty()){
        pair<int,int> cur = que.front();
        que.pop();
        int curx = cur.first, cury = cur.second;
        for(int i = 0;i < 4;i++){
            int nextx = curx + dir[i][0];
            int nexty = cury + dir[i][1];
            if(nextx < 0 || nexty < 0 || nextx >= gird.size() || nexty >= gird[0].size()) continue;
            if(gird[nextx][nexty] == 1 && visited[nextx][nexty] == false){
                que.push({nextx,nexty});
                count++;
                visited[nextx][nexty] = true;
            }
        }
    }
}

int main(){
    int N, M;
    cin >> N >> M;

    vector<vector<int>> gird(N,vector<int>(M,0));
    for(int i = 0;i < N;i++){
        for(int j = 0;j < M;j++){
            int s;
            cin >> s;
            gird[i][j] =s;
        }
    }
    int maxArea = 0;
    vector<vector<bool>> visited(N,vector<bool>(M,false));
    for(int i = 0;i < N;i++){
        for(int j = 0;j < M;j++){
            if(gird[i][j] == 1 && visited[i][j] == false){
                int count = 1;
                visited[i][j] = true;
                bfs(gird,visited,i,j,count);
                maxArea = maxArea > count ? maxArea : count;
            }
        }
    }
    cout << maxArea << endl;
}
```