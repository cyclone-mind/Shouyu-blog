---
title: '并查集理论基础'
description: '并查集理论基础：动态连通性问题'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 图论
  - 并查集
  - Union-Find
  - Leetcode
---

## 并查集两个主要功能

* 将两个元素添加到一个集合中

* 判断两个元素是否在同一个集合

### 背景

为什么传统的数组、set、map方法不适合解决"动态连通性"问题

假设我们有很多元素（比如1000个），需要把它们分成若干个集合，比如：

* 集合1：(1, 3, 5, 7)

* 集合2：(2, 4, 6)

* 集合3：(8, 9, 10)

* ... 可能有几百个这样的集合

多个数组可能这样：

```cpp
vector<int> group1 = {1, 3, 5, 7};
vector<int> group2 = {2, 4, 6};
vector<int> group3 = {8, 9, 10};
// ... 需要定义成百上千个数组？这显然不现实
```

二维数组可能这样：

```cpp
vector<vector<int>> groups = {
    {1, 3, 5, 7},    // 第一个集合
    {2, 4, 6},       // 第二个集合
    {8, 9, 10}       // 第三个集合
};
```

判断两个元素是否在同一集合：

```cpp
bool inSameSet(int a, int b) {
    for (int i = 0; i < groups.size(); i++) {
        bool hasA = false, hasB = false;
        for (int j = 0; j < groups[i].size(); j++) {
            if (groups[i][j] == a) hasA = true;
            if (groups[i][j] == b) hasB = true;
        }
        if (hasA && hasB) return true;  // 都在第i个集合里
    }
    return false;
}
```

添加元素到某个集合：

```cpp
void addToSet(int element, int target) {
    // 需要先遍历所有集合，找到target在哪个集合
    for (int i = 0; i < groups.size(); i++) {
        for (int j = 0; j < groups[i].size(); j++) {
            if (groups[i][j] == target) {
                groups[i].push_back(element);  // 找到了，添加到这个集合
                return;
            }
        }
    }
}
```

以上方法的时间复杂度过高，O(n²)。

换个思路就是将三个元素A，B，C （分别是数字）放在同一个集合，其实就是将三个元素连通在一起，如何连通呢。

只需要用一个一维数组来表示，即：father[A] = B，father[B] = C 这样就表述 A 与 B 与 C连通了（有向连通图）。

把**集合的概念抽象出来**，**只要元素能连通，那就是在一个集合中**。尽管这个集合非真实存在。

### 将两个元素添加到集合中

也就是将两个元素练成的边添加到集合

```cpp
// 将v，u 这条边加入并查集
void join(int u, int v) {
    u = find(u); // 寻找u的根
    v = find(v); // 寻找v的根
    if (u == v) return; // 如果发现根相同，则说明在一个集合，不用两个节点相连直接返回
    father[v] = u;
}
```

### 寻根

```cpp
// 并查集里寻根的过程
int find(int u) {
    if (u == father[u]) return u; // 如果根就是自己，直接返回
    else return find(father[u]); // 如果根不是自己，就根据数组下标一层一层向下找
}
```

### 初始化

默认自己指向自己

```cpp
// 并查集初始化
void init() {
    for (int i = 0; i < n; ++i) {
        father[i] = i;
    }
}
```

### 判断两个元素是否在同一个集合

```cpp
// 判断 u 和 v是否找到同一个根
bool isSame(int u, int v) {
    u = find(u);
    v = find(v);
    return u == v;
}
```

### 路径压缩

find 函数的过程中，通过递归的方式，不断获取father数组下标对应的数值，最终找到这个集合的根。

如果层数过多可能会栈溢出。我们需要做的是**路径压缩**，将非根节点的所有节点直接指向根节点。

只需要在递归的过程中，让 father[u] 接住 递归函数 find(father[u]) 的返回结果。

```cpp
int find(int u){
    if(u == father[u]) return u;
    else return father[u] = find(father[u]);
}

// 精简
int find(int u) {
    return u == father[u] ? u : father[u] = find(father[u]);
}
```

### 复杂度

路径压缩后的并查集时间复杂度在O(logn)与O(1)之间，且随着查询或者合并操作的增加，时间复杂度会越来越趋于O(1)。

## 代码实现

整体并查集模板

```cpp
int n = 1005; // n根据题目中节点数量而定，一般比节点数量大一点就好
vector<int> father = vector<int> (n, 0); // C++里的一种数组结构

// 并查集初始化
void init() {
    for (int i = 0; i < n; ++i) {
        father[i] = i;
    }
}
// 并查集里寻根的过程
int find(int u) {
    return u == father[u] ? u : father[u] = find(father[u]); // 路径压缩
}

// 判断 u 和 v是否找到同一个根
bool isSame(int u, int v) {
    u = find(u);
    v = find(v);
    return u == v;
}

// 将v->u 这条边加入并查集
void join(int u, int v) {
    u = find(u); // 寻找u的根
    v = find(v); // 寻找v的根
    if (u == v) return ; // 如果发现根相同，则说明在一个集合，不用两个节点相连直接返回
    father[v] = u;
}
```

上述模板的三个功能：

1. 寻找任意节点的根节点

1. 将两个节点加入同一个集合

1. 判断两个节点是否在同一个集合

## 常见误区

isSame 和 join 函数都有，找根的代码，那能够服用吗？

错误代码

```cpp
// 判断 u 和 v是否找到同一个根
bool isSame(int u, int v) {
    u = find(u);
    v = find(v);
    return u == v;
}

// 将v->u 这条边加入并查集
void join(int u, int v) {
    if (isSame(u, v)) return ; // 如果发现根相同，则说明在一个集合，不用两个节点相连直接返回
    father[v] = u;
}
```

这样做会导致生成错误的图。举例

```cpp
join(1,2);
join(3,2);
```

如果使用错误代码构成的图是这样的

这个错误的图会导致：

当我们调用`isSame(1, 3)`的时候，find(1) 返回的是1，find(3) 返回的是3。`return 1 == 3`返回的是false，代码告诉我们 1 和 3 不在同一个集合，这明显不符合我们的预期。

而正确代码生成的图是这样的

此时我们在调用`isSame(1, 3)`的时候，find(1) 返回的是3，find(3) 返回的也是3，`return 3 == 3`返回的是true，即告诉我们 元素 1 和 元素 3 是在同一个集合里的。