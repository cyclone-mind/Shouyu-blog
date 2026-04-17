---
title: '开发商购买土地'
description: '使用前缀和技巧解决土地购买问题，将城市区域分成两个子区域使价值差最小。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 数组
  - 前缀和
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

[题目链接](https://kamacoder.com/problempage.php?pid=1044)

[文章链接](https://programmercarl.com/kamacoder/0044.%E5%BC%80%E5%8F%91%E5%95%86%E8%B4%AD%E4%B9%B0%E5%9C%9F%E5%9C%B0.html)

【题目描述】

在一个城市区域内，被划分成了 n * m 个连续的区块，每个区块都拥有不同的权值，代表着其土地价值。目前，有两家开发公司，A 公司和 B 公司，希望购买这个城市区域的土地。

现在，需要将这个城市区域的所有区块分配给 A 公司和 B 公司。

然而，由于城市规划的限制，只允许将区域按横向或纵向划分成两个子区域，而且每个子区域都必须包含一个或多个区块。

为了确保公平竞争，你需要找到一种分配方式，使得 A 公司和 B 公司各自的子区域内的土地总价值之差最小。

注意区块不可再分。

【输入描述】

第一行输入两个正整数，代表 n 和 m。

接下来的 n 行，每行输出 m 个正整数。

输出描述

请输出一个整数，代表两个子区域内土地总价值之间的最小差距。

【输入示例】

3 3 1 2 3 2 1 3 1 2 3

【输出示例】

0

【提示信息】

如果将区域按照如下方式划分：

1 2 | 3 2 1 | 3 1 2 | 3

两个子区域内土地总价值之间的最小差距可以达到 0。

【数据范围】：

* 1 <= n, m <= 100；

* n 和 m 不同时为 1。

## 思路

最简单的思路是暴力解法，一个 for 循环划界限，套两个 for 循环求和。

### 前缀和

然而这不就是在数组中求区间和吗？何不利用到前缀和的思路，只不过是从一维换到二维罢了。

那么我们就先计算行的前缀和，再计算列的前缀和。

一个 for 循环画行界限，求行区间和之差，实时更新最小差值。

一个 for 循环画列界限，求列区间和之差，实时更新最小差值。

时间复杂度：O(n _ m) (输入) + O(n _ m) (行前缀和) + O(n _ m) (列前缀和) + O(n + m) (计算差值)，总体是 O(n _ m)

时间都咋读：O(n _ m) (输入) + O(n) (行前缀和) + O(m) (列前缀和) + O(1) (其他变量)，总体是 O(n _ m)

```cpp
#include <iostream>
#include <vector>
#include <climits>
using namespace std;

int main() {
	int n, m;
	cin >> n >> m;
	vector<vector<int>> nums(n, vector<int>(m,0));
	int sum = 0;
	for (int i = 0;i < n;i++) {
		for (int j = 0; j < m; j++) {
			cin >> nums[i][j];
			sum += nums[i][j];
		}
	}

	// 计算行前缀和
	vector<int> rowPrefixSum(n, 0);
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			rowPrefixSum[i] += nums[i][j];
		}
		rowPrefixSum[i] += (i > 0 ? rowPrefixSum[i - 1] : 0);
	}
	// 计算列前缀和
	vector<int> colPrefixSum(m, 0);
	for (int j = 0; j < m; j++) {
		for (int i = 0; i < n; i++) {
			colPrefixSum[j] += nums[i][j];
		}
		colPrefixSum[j] += (j > 0 ? colPrefixSum[j - 1] : 0);
	}

	// 计算差值
	int result = INT_MAX;
	for (int i = 0; i < n-1;i++) {
		result = min(result, abs(sum - 2 * rowPrefixSum[i]));
	}
	for (int i = 0; i < m-1;i++) {
		result = min(result, abs(sum - 2 * colPrefixSum[i]));
	}
	cout << result << endl;
	cin.get();
	cin.get();
	return 0;
}
```

### 优化暴力解法

因为这道题目的特殊性，只能画一条线分层，分成两个区域。那么完全可以在输入的时候遍历求出所有的和。然后一个 for 循环划线，套一个 for 求出划线的上层的和，这样下层的和就等于总和减去上层和（这一步需要在求出上层和的时候进行）。这样差值就有了。

需要注意的是代码随想录中的优化暴力解法边界条件中统计遍历行时是 int i = 0; i < n; i++ 这里会导致 i 取到 n-1，就划分了一个空区域，尽管仍能求出正确答案。但是过程可能与题意稍有不符（每个子区域都必须包含一个或多个区块）。
