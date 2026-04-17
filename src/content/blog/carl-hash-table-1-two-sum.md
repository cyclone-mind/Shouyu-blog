---
title: '代码随想录 哈希表：1. 两数之和'
description: '给定一个整数数组nums和一个目标值target，请你在该数组中找出和为目标值的两个整数，并返回他们的数组下标。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 哈希表
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

[题目链接](https://leetcode.cn/problems/two-sum/description/)

[文章讲解](https://programmercarl.com/0001.%E4%B8%A4%E6%95%B0%E4%B9%8B%E5%92%8C.html)

## 题目描述

给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。

你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。

**示例:**

给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9

所以返回 [0, 1]

## 思路

最初的、最直观的想法 (暴力枚举) 💥

* 思路: 拿起第一个数，然后依次和它后面的所有数配对，看看加起来等不等于 target。如果第一个数不行，就拿起第二个数，和它后面的所有数配对... 以此类推。

* 时间: O(N²)。两层循环，N 是数组长度。

* 空间: O(1)。只用了几个变量。

暴力法的瓶颈在于，对于每个 nums[i]，我们都要线性扫描剩下的数组来找 target - nums[i] (我们称之为 complement)。

* 核心问题转化: 对于当前的 nums[i]，我们如何快速知道 complement 是否存在于数组的其他位置，并且如果存在，它的下标是什么？

是不是对味了？这不就是**"需要查询一个元素是否出现过，或者一个元素是否在集合里的时候，就要第一时间想到哈希法。"**

目前我们有两类元素，一个是遍历数，另一个是 target-遍历数。

本题，就需要一个集合来存放我们遍历过的元素，然后在遍历数组的时候去询问这个集合，某元素是否遍历过，也就是 是否出现在这个集合。

因为题目要求 返回数组下标，因此除了记录元素，还要记录元素下标。可以使用 map 合适。

* 选项 A: 使用集合 (Set) - std::unordered_set

思路: 遍历数组，对于每个 nums[i]，计算 complement = target - nums[i]。然后去 set 里查 complement 是否存在。
过程:

创建一个空的 unordered_set<int> visited_numbers;
for i from 0 to nums.length - 1:

complement = target - nums[i];
if visited_numbers.count(complement):

找到了！nums[i] 和 complement 是我们要找的两个数。
问题来了: complement 的下标是什么？set 只告诉我们它存在，不告诉我们它在原数组的哪个位置。😭


visited_numbers.insert(nums[i]);




复杂度:

时间: O(N)。平均情况下，set 的插入和查找是 O(1)。
空间: O(N)。set 最多可能存储 N 个元素。


评估: 速度很快！但解决不了"返回下标"的核心需求。此路不通。

* 思路: 遍历数组，对于每个 nums[i]，计算 complement = target - nums[i]。然后去 set 里查 complement 是否存在。

* 过程:

创建一个空的 unordered_set<int> visited_numbers;
for i from 0 to nums.length - 1:

complement = target - nums[i];
if visited_numbers.count(complement):

找到了！nums[i] 和 complement 是我们要找的两个数。
问题来了: complement 的下标是什么？set 只告诉我们它存在，不告诉我们它在原数组的哪个位置。😭


visited_numbers.insert(nums[i]);

* complement = target - nums[i];

* if visited_numbers.count(complement):

找到了！nums[i] 和 complement 是我们要找的两个数。
问题来了: complement 的下标是什么？set 只告诉我们它存在，不告诉我们它在原数组的哪个位置。😭

* 找到了！nums[i] 和 complement 是我们要找的两个数。

* 问题来了: complement 的下标是什么？set 只告诉我们它存在，不告诉我们它在原数组的哪个位置。😭

* visited_numbers.insert(nums[i]);

* 复杂度:

时间: O(N)。平均情况下，set 的插入和查找是 O(1)。
空间: O(N)。set 最多可能存储 N 个元素。

* 时间: O(N)。平均情况下，set 的插入和查找是 O(1)。

* 空间: O(N)。set 最多可能存储 N 个元素。

* 评估: 速度很快！但解决不了"返回下标"的核心需求。此路不通。

* 选项 B: 使用映射 (Map / Dictionary) - std::unordered_map


启发: Set 的问题是只存了值，没存下标。Map 可以存键值对 (key-value pair)。我们是不是可以用它来把 值和它的下标关联起来？


思路 1 (先填充 Map，再查找):

创建一个 unordered_map<int, int> num_to_index;
遍历一遍数组，把所有 (nums[k], k) 存入 num_to_index。
再遍历一遍数组，对于每个 nums[i]:

complement = target - nums[i];
if num_to_index.count(complement) AND num_to_index[complement] != i: (确保不是自身)

return [i, num_to_index[complement]];






复杂度: 两次遍历，时间 O(N) + O(N) = O(N)。空间 O(N)。
评估: 可行！比排序好。但能不能一次遍历就搞定？



思路 2 (边遍历边查找边插入 - 当前代码的思路) 🎉

创建一个空的 unordered_map<int, int> record; (这里的 record 扮演的角色是"已经遇到的数字及其下标")
for i from 0 to nums.length - 1:

current_num = nums[i];
complement = target - current_num;
关键一步: 在 record 中查找 complement。

if record.count(complement):

这意味着 complement 这个数字我们之前已经遇到过了，并且它的下标被记录在 record[complement]。
而 current_num 是我们当前遇到的数。这两个数加起来正好是 target。
并且，因为我们是先查后放，record[complement] 对应的原始元素一定是在 nums[i] 之前出现的，所以它们的下标 record[complement] 和 i 必然不同。
return [record[complement], i]; (或者 [i, record[complement]]，顺序不重要)


else: (没在 record 中找到 complement)

说明到目前为止，current_num 的"另一半"还没出现。
那么，把 current_num 和它的下标 i 存入 record，供后续的数字来配对。
record[current_num] = i;








复杂度:

时间: O(N)。一次遍历，每次 map 操作平均 O(1)。
空间: O(N)。map 最多存储 N-1 个元素（最坏情况是最后一个元素才和第一个元素配对）。


评估: 非常好！一次遍历，时间空间都满足要求。

* 启发: Set 的问题是只存了值，没存下标。Map 可以存键值对 (key-value pair)。我们是不是可以用它来把 值和它的下标关联起来？

* 思路 1 (先填充 Map，再查找):

创建一个 unordered_map<int, int> num_to_index;
遍历一遍数组，把所有 (nums[k], k) 存入 num_to_index。
再遍历一遍数组，对于每个 nums[i]:

complement = target - nums[i];
if num_to_index.count(complement) AND num_to_index[complement] != i: (确保不是自身)

return [i, num_to_index[complement]];






复杂度: 两次遍历，时间 O(N) + O(N) = O(N)。空间 O(N)。
评估: 可行！比排序好。但能不能一次遍历就搞定？

* complement = target - nums[i];

* if num_to_index.count(complement) AND num_to_index[complement] != i: (确保不是自身)

return [i, num_to_index[complement]];

* return [i, num_to_index[complement]];

* 复杂度: 两次遍历，时间 O(N) + O(N) = O(N)。空间 O(N)。

* 评估: 可行！比排序好。但能不能一次遍历就搞定？

* 思路 2 (边遍历边查找边插入 - 当前代码的思路) 🎉

创建一个空的 unordered_map<int, int> record; (这里的 record 扮演的角色是"已经遇到的数字及其下标")
for i from 0 to nums.length - 1:

current_num = nums[i];
complement = target - current_num;
关键一步: 在 record 中查找 complement。

if record.count(complement):

这意味着 complement 这个数字我们之前已经遇到过了，并且它的下标被记录在 record[complement]。
而 current_num 是我们当前遇到的数。这两个数加起来正好是 target。
并且，因为我们是先查后放，record[complement] 对应的原始元素一定是在 nums[i] 之前出现的，所以它们的下标 record[complement] 和 i 必然不同。
return [record[complement], i]; (或者 [i, record[complement]]，顺序不重要)


else: (没在 record 中找到 complement)

说明到目前为止，current_num 的"另一半"还没出现。
那么，把 current_num 和它的下标 i 存入 record，供后续的数字来配对。
record[current_num] = i;








复杂度:

时间: O(N)。一次遍历，每次 map 操作平均 O(1)。
空间: O(N)。map 最多存储 N-1 个元素（最坏情况是最后一个元素才和第一个元素配对）。


评估: 非常好！一次遍历，时间空间都满足要求。

* current_num = nums[i];

* complement = target - current_num;

* 关键一步: 在 record 中查找 complement。

if record.count(complement):

这意味着 complement 这个数字我们之前已经遇到过了，并且它的下标被记录在 record[complement]。
而 current_num 是我们当前遇到的数。这两个数加起来正好是 target。
并且，因为我们是先查后放，record[complement] 对应的原始元素一定是在 nums[i] 之前出现的，所以它们的下标 record[complement] 和 i 必然不同。
return [record[complement], i]; (或者 [i, record[complement]]，顺序不重要)


else: (没在 record 中找到 complement)

说明到目前为止，current_num 的"另一半"还没出现。
那么，把 current_num 和它的下标 i 存入 record，供后续的数字来配对。
record[current_num] = i;

* if record.count(complement):

这意味着 complement 这个数字我们之前已经遇到过了，并且它的下标被记录在 record[complement]。
而 current_num 是我们当前遇到的数。这两个数加起来正好是 target。
并且，因为我们是先查后放，record[complement] 对应的原始元素一定是在 nums[i] 之前出现的，所以它们的下标 record[complement] 和 i 必然不同。
return [record[complement], i]; (或者 [i, record[complement]]，顺序不重要)

* 这意味着 complement 这个数字我们之前已经遇到过了，并且它的下标被记录在 record[complement]。

* 而 current_num 是我们当前遇到的数。这两个数加起来正好是 target。

* 并且，因为我们是先查后放，record[complement] 对应的原始元素一定是在 nums[i] 之前出现的，所以它们的下标 record[complement] 和 i 必然不同。

* return [record[complement], i]; (或者 [i, record[complement]]，顺序不重要)

* else: (没在 record 中找到 complement)

说明到目前为止，current_num 的"另一半"还没出现。
那么，把 current_num 和它的下标 i 存入 record，供后续的数字来配对。
record[current_num] = i;

* 说明到目前为止，current_num 的"另一半"还没出现。

* 那么，把 current_num 和它的下标 i 存入 record，供后续的数字来配对。

* record[current_num] = i;

* 复杂度:

时间: O(N)。一次遍历，每次 map 操作平均 O(1)。
空间: O(N)。map 最多存储 N-1 个元素（最坏情况是最后一个元素才和第一个元素配对）。

* 时间: O(N)。一次遍历，每次 map 操作平均 O(1)。

* 空间: O(N)。map 最多存储 N-1 个元素（最坏情况是最后一个元素才和第一个元素配对）。

* 评估: 非常好！一次遍历，时间空间都满足要求。

**为什么是**`**unordered_map**`**而不是**`**map**`**?**

* std::map (基于红黑树):

优点: 元素按键有序存储。
缺点: 查找、插入、删除都是 O(log N)。

* 优点: 元素按键有序存储。

* 缺点: 查找、插入、删除都是 O(log N)。

* std::unordered_map (基于哈希表):

优点: 平均情况下，查找、插入、删除都是 O(1)。
缺点: 元素无序。哈希冲突极端情况下可能退化到 O(N)，但良好设计的哈希函数下很少见。

* 优点: 平均情况下，查找、插入、删除都是 O(1)。

* 缺点: 元素无序。哈希冲突极端情况下可能退化到 O(N)，但良好设计的哈希函数下很少见。

对于这道题：

* 我们关心的是快速查找 complement 是否存在以及获取其下标。

* 我们完全不需要元素保持任何特定的顺序。

因此，`std::unordered_map`的 O(1) 平均时间复杂度更适合我们的需求，性能更优。