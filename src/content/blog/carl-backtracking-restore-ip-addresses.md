---
title: '复原IP地址'
description: '回溯算法解决复原IP地址问题，将数字字符串分割成有效的IP地址。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 回溯算法
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

## 题目描述

**有效 IP 地址**正好由四个整数（每个整数位于`0`到`255`之间组成，且不能含有前导`0`），整数之间用`'.'`分隔。

* 例如："0.1.2.201" 和 "192.168.1.1" 是 有效 IP 地址，但是 "0.011.255.245"、"192.168.1.312" 和 "192.168@1.1" 是 无效 IP 地址。

给定一个只包含数字的字符串`s`，用以表示一个 IP 地址，返回所有可能的**有效 IP 地址**，这些地址可以通过在`s`中插入`'.'`来形成。你**不能**重新排序或删除`s`中的任何数字。你可以按**任何**顺序返回答案。

[题目链接]93

[文章讲解]93

## 思考

这道题目类似于切割问题，同样可以抽象成组合问题：**有重复数组**中选择组合，约束条件是组合中的元素每个都是**回文串**。组合元素**无数量要求**。组合中元素**不可重复选取**。

## 回溯三部曲

**1、回溯函数参数及返回值**

全局变量result存放结果，startIndex 需要，终止条件由于每个组合是一个字符串，不能再以字符串长度为终止条件，虽然是四段，但四段长度不固定。但是我们可以以插入`.`的数量，记作`pointNum`

**2、终止条件**

本题明确要求只会分成4段，所以不能用切割线切到最后作为终止条件，而是分割的段数作为终止条件。pointNum 表示逗点数量，pointNum 为3说明字符串分成了4段了。

然后验证一下第四段是否合法，如果合法就加入到结果集里

**3、单层回溯搜索逻辑**

我们已讲过如何截取子串，本题类似。

如果字串合法，就在字符串后面添加`.`表示已分割。为什么这么做，我们以往是一个一维数组path，往path里面添加元素，本题是一个字符串，往path里面添加元素当然是后面拼接`.`。

如果字符串不合法，就结束本层循环 break，剪枝。这里是break，不同于上一题的 continue

合法的情况下就要递归，回溯。

递归调用时 startIndex要从i+2 开始（因为需要在字符串中加入了分隔符`.`），同时记录分割符的数量 pointNum 要 +1。

回溯的时候，撤销选择，删掉`.`就行，并且 pointNum -1 .删掉`.`不能用`s.pop_back();`这会删掉最后一个数字，应该使用`s.erase(s.begin() + i + 1);`在指定位置删除

### 判断有效字段

主要考虑三点

* 不能有前导0

* 不大于255

* 只包含数字（题目描述了给定一个只包含数字的字符串，这一点其实可以不用考虑）

将数字字符串转换为数字可以任选一种方式

```cpp
std::string sub = s.substr(left, len);
int num = std::stoi(sub);

// 或者
int num = 0;
for(int i = left;i <= right;i++){
    num = num * 10 + s[i] - '0';
}
```

## 代码实现

```cpp
#include <string>
#include <vector>
using namespace std;
class Solution {
    public:
        bool isValid(string& s, int left, int right) {
    
            int len = right - left + 1;
            if (len <= 0 || len > 3) {
                return false;
            }
            if (len > 1 && s[left] == '0') {
                return false;
            }
            std::string sub = s.substr(left, len);
            int num = std::stoi(sub);
    
            return num <= 255;
        }
    
        vector<string> result;
        void backtracking(string& s, int startIndex, int pointNum) {
            if (pointNum == 3) {
                if (isValid(s, startIndex, s.size() - 1)) {
                    result.push_back(s);
                }
                return;
            }
            for (int i = startIndex; i < s.size(); i++) {
                if (isValid(s, startIndex, i)) {
                    s.insert(s.begin() + i + 1, '.');
                    pointNum++;
                    backtracking(s, i + 2, pointNum);
                    pointNum--;
                    s.erase(s.begin() + i + 1);
                } else {
                    break;
                }
            }
        }
        vector<string> restoreIpAddresses(string s) {
            result.clear();
            if(s.size() < 4 || s.size() > 12) return result;
            backtracking(s, 0, 0);
            return result;
        }
    };
```

## 优化

剪枝，将长度小于4，大于12的字符串去除就算剪枝了

```cpp
if (s.size() < 4 || s.size() > 12) return result; // 算是剪枝了
```