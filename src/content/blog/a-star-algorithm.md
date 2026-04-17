---
title: 'A*算法'
description: '深入理解A*启发式搜索算法，解决骑士最短路径问题。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 数据结构
  - 启发式搜索
  - A*算法
  - 路径规划
  - Leetcode
---

## 题目描述

在象棋中，马和象的移动规则分别是“马走日”和“象走田”。现给定骑士的起始坐标和目标坐标，要求根据骑士的移动规则，计算从起点到达目标点所需的最短步数。

棋盘大小 1000 x 1000（棋盘的 x 和 y 坐标均在 [1, 1000] 区间内，包含边界）

[题目链接](https://kamacoder.com/problempage.php?pid=1203)

[文章讲解](https://programmercarl.com/kamacoder/0126.%E9%AA%91%E5%A3%AB%E7%9A%84%E6%94%BB%E5%87%BBastar.html)

## 思考

这道题是给定起点和终点，计算最短步数。适用于广搜。

为什么不是 dijkstra ？

这里划分一下使用条件。

什么时候用广搜BFS？

1. 无权图或等权图

1. 单一起点到单一终点

1. 只需要最短距离，不需要具体路径。

典型场景：迷宫问题，马走日

什么时候用Dijkstra算法？

1. 带权图

1. 非负权重

1. 从单一起点到其他所有点的最短路径

1. 需要完整的最短路径树

典型场景：道路网络

## 广搜的代码

```cpp
#include<iostream>
#include<queue>
#include<string.h>
using namespace std;
int moves[1001][1001];
int dir[8][2]={-2,-1,-2,1,-1,2,1,2,2,1,2,-1,1,-2,-1,-2};
void bfs(int a1,int a2, int b1, int b2)
{
	queue<int> q;
	q.push(a1);
	q.push(a2);
	while(!q.empty())
	{
		int m=q.front(); q.pop();
		int n=q.front(); q.pop();
		if(m == b1 && n == b2)
		break;
		for(int i=0;i<8;i++)
		{
			int mm=m + dir[i][0];
			int nn=n + dir[i][1];
			if(mm < 1 || mm > 1000 || nn < 1 || nn > 1000)
			continue;
			if(!moves[mm][nn])
			{
				moves[mm][nn]=moves[m][n]+1;
				q.push(mm);
				q.push(nn);
			}
		}
	}
}

int main()
{
    int n, a1, a2, b1, b2;
    cin >> n;
    while (n--) {
        cin >> a1 >> a2 >> b1 >> b2;
        memset(moves,0,sizeof(moves));
		bfs(a1, a2, b1, b2);
		cout << moves[b1][b2] << endl;
	}
	return 0;
}
```

能够发现广搜的代码八个方向的其中未访问过的方格全部添加到队列中，不管这些方格是否离终点更远。

假使说这八个方向是上下左右、上左上右下左下右。从起点开始，起点的八个方向都未访问过，那么都要加入到队列中以便下次作为起点访问。

这时若终点在右下角，那么这八个方向当中 左上、左、上、左下这几个方向的方格加入到队列中有什么意义呢？或者说作为加入队列中作为起始节点重新搜索有什么意义呢？

因为无权值，或者说权值全部为1，左上、左、上、左下这几个方向不可能比其他方向离节点更近，不可能通过绕远路获得更低的权值，因为权值都是一样的。

那么怎么做？

那就左上、左、上、左下这几个方向的方格不加入到队列？不现实，因为这个起点，这几个方向离终点远，那下次呢，下一个方格的方向说不定不是这几个方向离终点远了，因为实际上我们不知道终点在起点的什么方位。

所以我们扔把这些方向的方格加入到队列中，只不过，队列是有顺序的，离终点远的几个方向放在队列后面，近的放在队列前面，优先取离终点近的。

对队列里节点进行排序，就需要给每一个节点权值，如何计算权值呢？

每个节点的权值为F，给出公式为：F = G + H

G：起点达到目前遍历节点的距离

H：目前遍历的节点到达终点的距离

那么目前遍历点节点到离终点的距离怎么计算？

起点达到目前遍历节点的距离 + 目前遍历的节点到达终点的距离 就是起点到达终点的距离。

**启发式函数 要影响的就是队列里元素的排序**！

这里的**目前遍历的节点到达终点的距离**就是启发式函数的结果值

本题的图是无权网格状，在计算两点距离通常有如下三种计算方式：

1. 曼哈顿距离，计算方式： d = abs(x1-x2)+abs(y1-y2)

1. 欧氏距离（欧拉距离） ，计算方式：d = sqrt( (x1-x2)^2 + (y1-y2)^2 )

1. 切比雪夫距离，计算方式：d = max(abs(x1 - x2), abs(y1 - y2))

## 代码实现

实现步骤

1. 定义一个棋盘大小的二维数组moves，作为访问标志位也作为最短步数纪录位。

1. 定义二维数组存储八个方向

1. 定义遍历的节点，节点是一个结构体，包含节点位置，从起点到该节点路径消耗，该节点到终点的预估消耗，从起点经过该节点到终点的最短步数F。因为该节点要放进优先级队列实现小顶堆，F小的放前面，因此要重载 < 运算符。

1. 定义优先级队列

1. 启发式函数，接受节点坐标和终点坐标，输出该节点到终点的预估消耗。欧拉距离，不开平方根

1. 声明Astar函数，传入一个起始节点

定义一个默认当前节点和默认下一个节点，先不声明。Knight cur, next;
把起始节点放入队列
遍历队列

队列中取头节点作为搜索节点
若已是终点则终止循环
循环八个方向

不越界，也未访问过，就更新moves，并把这个节点加入到队列中

1. 定义一个默认当前节点和默认下一个节点，先不声明。Knight cur, next;

1. 把起始节点放入队列

1. 遍历队列

队列中取头节点作为搜索节点
若已是终点则终止循环
循环八个方向

不越界，也未访问过，就更新moves，并把这个节点加入到队列中

1. 队列中取头节点作为搜索节点

1. 若已是终点则终止循环

1. 循环八个方向

不越界，也未访问过，就更新moves，并把这个节点加入到队列中

1. 不越界，也未访问过，就更新moves，并把这个节点加入到队列中

```cpp
#include<iostream>
#include<queue>
#include<string.h>
using namespace std;
int moves[1001][1001];
int dir[8][2]={-2,-1,-2,1,-1,2,1,2,2,1,2,-1,1,-2,-1,-2};
int b1, b2;
// F = G + H
// G = 从起点到该节点路径消耗
// H = 该节点到终点的预估消耗

struct Knight{
    int x,y;
    int g,h,f;
    bool operator < (const Knight & k) const{  // 重载运算符， 从小到大排序
     return k.f < f;
    }
};

priority_queue<Knight> que;

int Heuristic(const Knight& k) { // 欧拉距离
    return (k.x - b1) * (k.x - b1) + (k.y - b2) * (k.y - b2); // 统一不开根号，这样可以提高精度
}
void astar(const Knight& k)
{
    Knight cur, next;
	que.push(k);
	while(!que.empty())
	{
		cur=que.top(); que.pop();
		if(cur.x == b1 && cur.y == b2)
		break;
		for(int i = 0; i < 8; i++)
		{
			next.x = cur.x + dir[i][0];
			next.y = cur.y + dir[i][1];
			if(next.x < 1 || next.x > 1000 || next.y < 1 || next.y > 1000)
			continue;
			if(!moves[next.x][next.y])
			{
				moves[next.x][next.y] = moves[cur.x][cur.y] + 1;

                // 开始计算F
				next.g = cur.g + 5; // 统一不开根号，这样可以提高精度，马走日，1 * 1 + 2 * 2 = 5
                next.h = Heuristic(next);
                next.f = next.g + next.h;
                que.push(next);
			}
		}
	}
}

int main()
{
    int n, a1, a2;
    cin >> n;
    while (n--) {
        cin >> a1 >> a2 >> b1 >> b2;
        memset(moves,0,sizeof(moves));
        Knight start;
        start.x = a1;
        start.y = a2;
        start.g = 0;
        start.h = Heuristic(start);
        start.f = start.g + start.h;
		astar(start);
        while(!que.empty()) que.pop(); // 队列清空
		cout << moves[b1][b2] << endl;
	}
	return 0;
}
```

```cpp
#include <climits>
#include <cmath>
#include <iostream>
#include <queue>
#include <unordered_set>
#include <vector>

using namespace std;

// A*算法中的节点结构
struct Node {
    int x, y; // 当前位置
    int g;    // 从起点到当前点的实际距离
    int h;    // 启发式函数值（到终点的估计距离）
    int f;    // f = g + h，总评估值

    Node(int x, int y, int g, int h) : x(x), y(y), g(g), h(h), f(g + h) {}
};

// 自定义比较器：f值小的优先级高（小顶堆）
class NodeCompare {
  public:
    bool operator()(const Node &lhs, const Node &rhs) {
        if (lhs.f != rhs.f) {
            return lhs.f > rhs.f; // f值小的优先级高
        }
        return lhs.h > rhs.h; // f值相同时，h值小的优先级高
    }
};

// 启发式函数：计算从当前位置到目标位置的估计距离
int heuristic(int x1, int y1, int x2, int y2) {
    // 使用距离平方，避免开根号运算，提高性能
    double dx = abs(x1 - x2);
    double dy = abs(y1 - y2);
    // 直接返回距离平方除以5（因为马最大移动距离平方是5）
    return (dx * dx + dy * dy) / 5;
}

// 马的8个可能移动方向
int dx[] = {-2, -2, -1, -1, 1, 1, 2, 2};
int dy[] = {-1, 1, -2, 2, -2, 2, -1, 1};

// 检查坐标是否在棋盘范围内
bool isValid(int x, int y) {
    return x >= 1 && x <= 1000 && y >= 1 && y <= 1000;
}

// 将坐标转换为唯一的哈希值，用于visited集合
long long getHash(int x, int y) { return (long long)x * 1001 + y; }

int astar(int startX, int startY, int endX, int endY) {
    // 如果起点和终点相同，直接返回0
    if (startX == endX && startY == endY) {
        return 0;
    }

    // 优先队列，存储待探索的节点
    priority_queue<Node, vector<Node>, NodeCompare> pq;
    // 已访问的节点集合
    unordered_set<long long> visited;

    // 将起点加入队列
    int h = heuristic(startX, startY, endX, endY);
    pq.push(Node(startX, startY, 0, h));

    while (!pq.empty()) {
        Node current = pq.top();
        pq.pop();

        // 生成当前节点的哈希值
        long long currentHash = getHash(current.x, current.y);

        // 如果已经访问过，跳过
        if (visited.find(currentHash) != visited.end()) {
            continue;
        }

        // 标记为已访问
        visited.insert(currentHash);

        // 如果到达目标，返回步数
        if (current.x == endX && current.y == endY) {
            return current.g;
        }

        // 尝试马的8个可能移动
        for (int i = 0; i < 8; i++) {
            int newX = current.x + dx[i];
            int newY = current.y + dy[i];

            // 检查新位置是否有效
            if (!isValid(newX, newY)) {
                continue;
            }

            long long newHash = getHash(newX, newY);

            // 如果已经访问过，跳过
            if (visited.find(newHash) != visited.end()) {
                continue;
            }

            // 计算新节点的g值和h值
            int newG = current.g + 1;
            int newH = heuristic(newX, newY, endX, endY);

            // 将新节点加入队列
            pq.push(Node(newX, newY, newG, newH));
        }
    }

    return -1; // 理论上不会到达这里
}

int main() {
    int n;
    cin >> n;

    while (n--) {
        int a1, a2, b1, b2;
        cin >> a1 >> a2 >> b1 >> b2;

        int result = astar(a1, a2, b1, b2);
        cout << result << endl;
    }

    return 0;
}
```