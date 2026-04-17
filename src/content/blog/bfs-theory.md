---
title: '广搜理论基础'
description: '深入理解BFS广度优先搜索的适用场景、过程和代码框架。'
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
  - Leetcode
---


## 广搜适用场景

解决两点之间最短路径问题

但是如果需要把所有节点都遍历才能完成任务，那么广搜和深搜都是可以的。例如岛屿问题，遍历所有陆地，打上标记。

## 广搜的过程

感性来看就是一圈一圈进行搜索，每次搜索一定的方向，对搜索到的节点进行处理（如染色等），接着站在搜索到的节点进行下一次搜索。

## 代码框架

我们需要一个容器保留我们遍历过的元素，以便不会重复搜索节点（因为每次搜索的方向是固定的，有可能出现重复）。

这个容器可以是队列，也可以是栈，习惯上用队列比较方便

```cpp
定义4个方向
    gird 是地图-->二维数组
    visited 标记访问过的节点,不要重复访问,就是说遍历节点时要把该节点标记一下.
    x, y 代表开始搜索节点的下标
void bfs(gird,visited,x,y){
	    定义一个队列
        把第一个节点加入到队列中
        将这个节点标记为true
        遍历队列中元素
        从队列中取出元素
        计算当前元素坐标
        在此节点基础上进行四方向搜索:
            四方向搜索后的下个节点的坐标
            下个节点不能越界,不能被访问过,然后将下个节点添加到队列中
             加入队列立刻标记
        
}
```

```cpp
int dif[4][2] = {{0,1},{1,0},{0,-1},{-1,0}};
// gird
// visited
void bfs(vector<vector<int>>& gird, vector<vector<int>>& visited,int x,int y){
	queue<pair<int,int>> que;
    que.push({x,y});
    visited[x][y] = true;
    while(!que.empty()){
        pair<int, int> node = que.top(); que.pop();
        int cur_x = node.first,cur_y = node.second;
        for(int i = 0;i < 4;i++){
            int next_x = curx + dir[i][0];
            int next_y = cury + dir[i][1];
            if(next_x < 0 || next_y < 0 || next_x >= gird.size() || next_y >= gird[0].size()) continue;
            if(visited[next_x][next_y] == false){
                que.push({next_x,next_y});
                visited[next_x][next_y] == true;
            }
        }
    }
}
```