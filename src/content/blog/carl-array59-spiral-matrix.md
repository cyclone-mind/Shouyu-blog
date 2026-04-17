---
title: '螺旋矩阵'
description: '模拟行走法生成螺旋矩阵，按顺时针顺序螺旋排列。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 数组
  - 模拟行走
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

力扣题目链接

给定一个正整数 n，生成一个包含 1 到 n^2 所有元素，且元素按顺时针顺序螺旋排列的正方形矩阵。
示例:
输入: 3 输出: [ [ 1, 2, 3 ], [ 8, 9, 4 ], [ 7, 6, 5 ] ]

[文章链接](https://programmercarl.com/0059.%E8%9E%BA%E6%97%8B%E7%9F%A9%E9%98%B5II.html)

## 思路

生成一个 n*n 的矩阵 显然需要一个一个填充。填充时有两个思路。

### 模拟行走

模拟行走就是顺时针路径循环填充即可。所以需要：初始化 n*n 矩阵，当前位置，下个位置，方向向量，当前方向。

什么时候改变方向？下个位置超出边界 或者下个位置是已填充过的内容。

怎么改变方向？1，2，3，4 循环。

```cpp
vector<vector<int>> generateMatrix(int n)
{
    // 初始化一个 n×n 的矩阵，所有元素初始为0
    vector<vector<int>> res(n, vector<int>(n, 0));

    // 定义四个方向：右、下、左、上
    vector<vector<int>> directions = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};

    // 当前方向索引，0表示向右
    int cur_direction = 0;

    // 当前位置
    int cur_x = 0, cur_y = 0;

    // 填充矩阵，从1开始到n²
    for (int num = 1; num <= n * n; num++)
    {
        // 在当前位置填入当前数字
        res[cur_x][cur_y] = num;

        // 计算下一个预期位置
        int next_x = cur_x + directions[cur_direction][0];
        int next_y = cur_y + directions[cur_direction][1];

        // 判断下一个位置是否越界或已被填充（不为0）
        if (next_x < 0 || next_x >= n || next_y < 0 || next_y >= n || res[next_x][next_y] != 0)
        {
            // 改变方向 (右->下->左->上 循环)
            cur_direction = (cur_direction + 1) % 4;

            // 重新计算下一个位置
            next_x = cur_x + directions[cur_direction][0];
            next_y = cur_y + directions[cur_direction][1];
        }

        // 移动到下一个位置
        cur_x = next_x;
        cur_y = next_y;
    }

    return res;
}
```

### 边界收缩法

我们依次按照右、下、左、上的边界填充。这里的边界很重要。你是把一个边界的所有元素都填充？还是最后一个不填充留到下个边界？这里我们选择所有边界都填充试试。

初始化矩阵，定义边界索引，初始化填充的数组，当边界范围合法时循环填充.

## 启发

本体的关键依然是要坚持循环不变量原则，类似于二分法。

我们思路中使用的是左闭右闭，也就是所有元素都填充，而代码随想录讲解中使用的是左闭右开，即留给小尾巴作为下一边界。

看一下示意图

```cpp
#include <vector>
vector<vector<int>> generateMatrix_boundary(int n)
{
    vector<vector<int>> res(n, vector<int>(n, 0));

    // 定义四个边界
    int top = 0, bottom = n - 1;
    int left = 0, right = n - 1;

    // 当前要填入的数字
    int num = 1;

    while (left <= right && top <= bottom)
    {
        // 从左到右填充上边界
        for (int j = left; j <= right; j++) // 边界条件左闭右闭
        {
            res[top][j] = num++;
        }
        top++; // 上边界下移

        // 从上到下填充右边界
        for (int i = top; i <= bottom; i++)// 边界条件左闭右闭
        {
            res[i][right] = num++;
        }
        right--; // 右边界左移

        // 检查是否还有剩余行和列
        if (top <= bottom)
        {
            // 从右到左填充下边界
            for (int j = right; j >= left; j--)// 边界条件左闭右闭
            {
                res[bottom][j] = num++;
            }
            bottom--; // 下边界上移
        }

        if (left <= right)
        {
            // 从下到上填充左边界
            for (int i = bottom; i >= top; i--)// 边界条件左闭右闭
            {
                res[i][left] = num++;
            }
            left++; // 左边界右移
        }
    }

    return res;
}
```