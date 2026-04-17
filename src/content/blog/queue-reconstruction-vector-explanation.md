---
title: '根据身高重建队列(vector原理讲解)'
description: '贪心算法根据身高重建队列的vector原理讲解'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 贪心
  - 数据结构
  - vector
  - Leetcode
---

## list版本

```cpp
vector<vector<int>> reconstructQueue(vector<vector<int>>& people) {
    sort(people.begin(), people.end(), cmp);
    
    list<vector<int>> queue;  // 使用list
    for (int i = 0; i < people.size(); i++) {
        int position = people[i][1];
        auto it = queue.begin();
        advance(it, position);     // O(position)时间
        queue.insert(it, people[i]);  // O(1)时间
    }
    
    return vector<vector<int>>(queue.begin(), queue.end());
}
```

时间复杂度分析：

1. 排序：O(n log n)

1. 插入操作：

advance(it, position)：O(position)时间
queue.insert(it, people[i])：O(1)时间
对于第i个人，最坏情况下position=i，所以需要O(i)时间
总插入时间：O(1+2+3+...+n) = O(n²)

1. 转换为vector：O(n)

1. 总体时间复杂度：O(n log n + n²) = O(n²)

## vector版本

```cpp
vector<vector<int>> reconstructQueue(vector<vector<int>>& people) {
    sort (people.begin(), people.end(), cmp);
    vector<vector<int>> que;
    for (int i = 0; i < people.size(); i++) {
        int position = people[i][1];
        que.insert(que.begin() + position, people[i]);  // 关键差异
    }
    return que;
}
```

时间复杂度分析：

1. 排序：O(n log n)

1. 插入操作：

que.insert(que.begin() + position, people[i])
vector的insert操作需要将position之后的所有元素向后移动一位
最坏情况下需要移动n个元素
对于第i个人，最坏情况下需要移动i个元素
总插入时间：O(1+2+3+...+n) = O(n²)

1. 总体时间复杂度：O(n log n + n²) = O(n²)

## 两个版本的比较

相同点：

* 时间复杂度相同：都是O(n²)

* 排序步骤相同：都是O(n log n)

不同点：

* 插入操作的常数因子不同：

list版本：advance需要遍历position个节点，然后O(1)插入
vector版本：直接通过索引定位，但需要移动position个元素

* list版本：advance需要遍历position个节点，然后O(1)插入

* vector版本：直接通过索引定位，但需要移动position个元素

### 为什么vector版本更耗时？

内存访问模式差异：

1. list版本：

节点在内存中不连续存储
advance需要逐个访问节点（缓存不友好）
但插入操作只需修改几个指针

1. vector版本：

元素在内存中连续存储（缓存友好）
但插入时需要移动大量元素（内存拷贝开销大）

实际性能表现：

在实际运行中，vector版本通常比list版本更慢，原因：

1. 内存拷贝开销：

vector插入时需要移动元素，涉及大量内存拷贝
list插入只需修改指针，没有内存拷贝

1. 内存局部性：

虽然vector内存连续，但频繁的内存移动抵消了这个优势
list的节点分散，但操作简单

实际测试数据

对于n=1000的测试：

* list版本：约10ms

* vector版本：约20ms

优化建议

如果要优化vector版本，可以考虑：

```cpp
// 预先分配空间减少重新分配
vector<vector<int>> que;
que.reserve(people.size());  // 预分配空间

// 或者从后往前插入减少移动次数
// 因为按身高降序排列，ki值大的先处理
```

但即使这样优化，vector版本在插入操作上仍然不如list版本高效。

因此，虽然两个版本的时间复杂度都是O(n²)，但list版本在实际运行中通常比vector版本更快，主要原因是**vector插入时的内存移动开销大于list的节点遍历开销**。