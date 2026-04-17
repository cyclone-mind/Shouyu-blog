---
title: 'Python f-string 进阶玩法'
description: 'python 的字符串格式化'
pubDate: '2025-11-21'
authors:
  - shouyu
toc: true
tags:
  - Web开发
  - Python
  - f-string
  - 编程技巧
---

## 摘要

python 的字符串格式化

## 正文

今天聊聊 f-string。自从 Python 3.6 之后，它基本上就成了字符串格式化的首选了，确实方便。如果你还在用老式的`%`或者`.format()`，那不妨看看 f-string 能怎么让你的代码更简洁。

走着，一起看看 f-string 除了基础用法，还能玩出哪些花样，让输出不再干巴巴。🚀

## 🎯 Trick 1：数字分隔符

遇到像`10000000000`这样的大数字，一眼看过去是不是有点晕？😵‍💫 f-string 有个小技巧能让它清爽不少。

```python
n: int = 10000000000
print(f"原始输出: {n}")   # 原始输出: 10000000000
print(f"下划线分隔: {n:_}") # 下划线分隔: 10_000_000_000
print(f"逗号分隔: {n:,}")   # 逗号分隔: 10,000,000,000
```

加上`_`或者`,`之后，易读多了，这俩是 Python 内置就支持的。想用别的符号分隔？那得用到`format()`，不过今天咱主要聊 f-string。

## 📐 Trick 2：输出对齐

写脚本或者小程序的时候，输出的几行文本长长短短，看着不舒服？f-string 的对齐功能这时候就派上用场了。

```python
var: str = "hello"
width: int = 10 # 假设我们希望 "hello" 占够10个字符的宽度

# 右对齐:'>'，内容靠右，左边补空格
print(f"'{var:>{width}}'") # 输出: '     hello'

# 左对齐:'<'，内容靠左，右边补空格 (f-string 默认就是左对齐)
print(f"'{var:<{width}}'") # 输出: 'hello     '
print(f"'{var:{width}}'")  # 输出: 'hello     ' (不写 < 也是一样的效果)

# 居中对齐:'^'，内容居中，两边动态补空格
print(f"'{var:^{width}}'") # 输出: '  hello   '
```

如果不想用单调的空格填充，也可以指定别的字符：

```python
var: str = "hello"
width: int = 10

print(f"'{var:*<{width}}'")  # 左对齐，用 '*' 填充: 'hello*****'
print(f"'{var:~>{width}}'")  # 右对齐用 '~' 填充: '~~~~~hello'
print(f"'{var:.^{width}}'") # 居中对齐，用 '.' 填充: '..hello...'
```

**✨ 来个小实战：配合**`**tqdm**`**让进度条更好看**

我平时写一些命令行工具时，喜欢用`tqdm`来显示进度。结合 f-string 的对齐和填充，能让进度条的描述信息更规整。

```python
from tqdm import tqdm
import time

tasks = ["下载资源", "解压文件", "安装程序"]
total_steps = len(tasks)

for idx, task in enumerate(tasks, 1):
    # 这里用全角空格'　'来填充，让中文描述部分宽度看起来更一致
    # task 可能只有两个字，也可能有三个字，用 :　<5 保证它至少占5个字符（大致宽度）
    desc = f"{task:　<5}步骤 {idx}/{total_steps}"
    for _ in tqdm(range(3), desc=desc, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"):
        time.sleep(0.2)
    print(f"{task} 完成！🎉")
```

输出效果大概是这样（进度条会动态更新）：

```text
下载资源　步骤 1/3: 100%|██████████| 3/3 [00:00<00:00,  4.98it/s]
下载资源 完成！🎉
解压文件　步骤 2/3: 100%|██████████| 3/3 [00:00<00:00,  4.97it/s]
解压文件 完成！🎉
安装程序　步骤 3/3: 100%|██████████| 3/3 [00:00<00:00,  4.99it/s]
安装程序 完成！🎉
```

这样看起来利索多了😎

## ⏰ Trick 3：时间格式化(Time Formatting)

`datetime`对象直接打出来那一长串，一般都不是我们想要的最终展示格式。f-string 配合一些格式化指令，就能让时间显示得明明白白。

```python
from datetime import datetime

now: datetime = datetime.now() # 当前时间

# 比较常用的年月日时分秒
print(f"当前时间: {now:%Y-%m-%d %H:%M:%S}")
# 输出类似: 当前时间: 2025-05-10 10:30:45

# 本地化的日期和时间格式，用 %c
print(f"本地格式: {now:%c}")
# 输出可能类似 (看你系统语言环境): 本地格式: Sat May 10 10:30:45 2025

# 如果你习惯 AM/PM，这样来：
print(f"12小时制: {now:%Y-%m-%d %I:%M:%S %p}")
# 输出类似: 12小时制: 2025-05-10 10:30:45 AM

# 只显示时分和AM/PM
print(f"简约时分: {now:%I:%M %p}")
# 输出类似: 简约时分: 10:30 AM
```

这些`%Y`,`%m`,`%d`之类的都是标准指令，需要啥格式可以查查 strftime 的文档，挺全的。🗓️

## 🔢 Trick 4：控制小数精度？f-string 说了算

处理浮点数，我们经常要控制显示几位小数，比如显示金额的时候。

```python
n: float = 1234.56789

# Python 内置的 round() 能四舍五入取整，但不够灵活
print(f"round(n) 的结果: {round(n)}") # round(n) 的结果: 1235

# f-string 控制小数位数更方便
print(f"保留两位小数: {n:.2f}") # 保留两位小数: 1234.57 (四舍五入)
print(f"不保留小数 (取整): {n:.0f}") # 不保留小数 (取整): 1235
```

**✨ 组合技：数字分隔符 + 精度控制**

还记得第一个技巧里的数字分隔符不？它们可以和精度控制一起用，比如格式化金额：

```python
price: float = 1234567.89123
print(f"商品总价: {price:,.2f} 元") # 商品总价: 1,234,567.89 元
```

这样看起来就规范多了。💰

## 🐞 Trick 5：表达式调试输出(f-string debug feature)   Python 3.8+

写代码免不了要打印些变量看看中间状态。以前可能得这么写：

```python
a: int = 5
b: int = 10
print(f"a 的值是 {a}, b 的值是 {b}, 它俩的和是 {a + b}")
# 输出: a 的值是 5, b 的值是 10, 它俩的和是 15
```

有点繁琐。Python 3.8 之后，f-string 加了个很贴心的小功能：在变量或表达式后面直接跟个`=`，它就能把名字和值都给你打出来。

```python
a: int = 5
b: int = 10
var_str: str = "Python"

# 看看这个神奇的等号！
print(f"{a = }")         # 输出: a = 5
print(f"{b = }")         # 输出: b = 10
print(f"{a + b = }")     # 输出: a + b = 15
print(f"{var_str = }")   # 输出: var_str = 'Python'
print(f"{len(var_str*2) = }") # 输出: len(var_str*2) = 12
```

这在调试的时候是真方便，能少打不少字，代码也看着清爽。墙裂推荐！👍

## 🎉 小结一下

好了，今天分享了 f-string 的几个实用小技巧：

1. 数字分隔符 (_ 或 ,)：让长数字不费眼。

1. 对齐与填充 (<, >, ^, 加填充字符)：让输出排版更好看。

1. 时间格式化 (配合 % 指令)：按需显示日期时间。

1. 数字精度控制 (.nf)：控制小数位数。

1. 表达式调试 ({表达式=})：Python 3.8+ 的调试快捷方式。

f-string 的花样其实还挺多的，比如在`{}`里面可以直接写表达式、调函数什么的。希望这些技巧能帮到你，让你用 Python 写东西的时候更顺手。💪

不妨现在就在你的代码里试试这些技巧吧！😉 祝编码愉快!