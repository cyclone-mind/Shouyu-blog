---
title: '最短路问题总结'
description: '最短路问题总结：Dijkstra、Bellman_ford、SPFA 和 Floyd'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 最短路算法
  - 总结
  - Leetcode
---

## 总结

四大最短路算法，分别是Dijkstra、Bellman_ford、SPFA 和 Floyd。

到底该怎么选择？

## 判断步骤

1. 有负边吗？

❌ 没有 → 看第2步
✅ 有 → Bellman-Ford/SPFA

1. 多个起点吗？

✅ 是 → Floyd
❌ 否 → 看第3步

1. 单起点到单终点吗？

✅ 是 → Dijkstra（或BFS如果等权）
❌ 否 → Dijkstra

## 算法选择表

## 特殊情况

* A* : 工程实际应用首选（游戏、导航）

* BFS : 等权图的最简单选择

* 堆优化 : 不确定就用优化版，性能更好