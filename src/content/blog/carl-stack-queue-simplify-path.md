---
title: '代码随想录 栈与队列：71. 简化路径'
description: '给你一个字符串path，表示指向某一文件或目录的Unix风格绝对路径，将其转化为更加简洁的规范路径。'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - 算法笔记
  - 栈和队列
  - 代码随想录
  - 数据结构与算法
  - Leetcode
---

# 代码随想录 栈与队列：简化路径

**发布日期:** 2025/12/21
**阅读时间:** 2 分钟
**标签:** 算法笔记, 栈和队列, 代码随想录, 数据结构与算法, 栈, 队列

## 正文
## 题目描述

给你一个字符串 path ，表示指向某一文件或目录的 Unix 风格 绝对路径 （以 '/' 开头），请你将其转化为 更加简洁的规范路径。

在 Unix 风格的文件系统中规则如下：

一个点 '.' 表示当前目录本身。
此外，两个点 '..' 表示将目录切换到上一级（指向父目录）。
任意多个连续的斜杠（即，'//' 或 '///'）都被视为单个斜杠 '/'。
任何其他格式的点（例如，'...' 或 '....'）均被视为有效的文件/目录名称。
返回的 简化路径 必须遵循下述格式：

始终以斜杠 '/' 开头。
两个目录名之间必须只有一个斜杠 '/' 。
最后一个目录名（如果存在）不能 以 '/' 结尾。
此外，路径仅包含从根目录到目标文件或目录的路径上的目录（即，不含 '.' 或 '..'）。
返回简化后得到的 规范路径 。

[题目链接](https://leetcode.cn/problems/simplify-path)

## 思考

逐步寻找`/`，或者说以/分割，提取出来字符，若`.`或`空`就跳过。若`..`将栈元素弹出。若其余，则推入栈。栈里面是有效的路径的字符串。

如何以`/`分割字符串？可以是 stringstream 和 getline 结合

**stringstream**

stringstream 是 C++ 标准库中的一个类，属于`<sstream>`头文件。它允许你像操作流（如 cin、cout）一样操作字符串。常见用途包括：

1. 分割字符串（如按某个分隔符拆分路径）

1. 将字符串转换为其他类型（如 int、double）

示例：

```cpp
#include <sstream>
#include <string>
using namespace std;

string s = "123 456";
stringstream ss(s);
int a, b;
ss >> a >> b; // a = 123, b = 456
```

**getline**

`getline`是一个函数，可以从输入流中读取一行内容，直到遇到指定的分隔符（默认是换行符 \n，但可以自定义）。

```cpp
while (getline(ss, segment, '/')) {
    // segment 是被 '/' 分割出来的每一段字符串
}
```

这里`getline`从`stringstream ss`中每次读取被 / 分隔的子串，赋值给`segment`

`stringstream ss(path);`：把字符串`path`包装成流，方便后续分割和读取。

`getline(ss, segment, '/')`：每次读取`path`中被 / 分隔的部分，直到读完。

这样可以很方便地处理路径、分割字符串等操作。

## 代码实现

```cpp
class Solution {
public:
    string simplifyPath(string path) {
        stack<string> st;
        stringstream ss(path);
        string segment;
        while (getline(ss, segment, '/')) {
            if (segment.empty() || segment == ".") continue;
            if (segment == "..") {
                if (!st.empty()) st.pop();
            } else {
                st.push(segment);
            }
        }
        string result;
        vector<string> res;
        while (!st.empty()) {
            res.push_back(st.top());
            st.pop();
        }
        for (auto it = res.rbegin(); it != res.rend(); ++it) {
            result += "/" + *it;
        }
        return result.empty() ? "/" : result;
    }
};
```