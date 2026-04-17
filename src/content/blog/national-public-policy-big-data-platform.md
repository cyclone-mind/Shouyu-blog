---
title: '全国公共政策大数据平台'
description: '全国公共政策大数据平台的JS逆向实战'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - JS逆向
---

## 摘要

大数据平台的JS逆向

## 正文

网址：aHR0cHM6Ly93d3cuc3BvbGljeS5jb20v

## 思路分析

### 反调试

该网站F12打不开，右键检查可以打开。打开后是虚拟机形式的无限debugger。采用hook debugger的形式过掉反调试

```js
AAA = Function.prototype.constructor;

Function.prototype.constructor = function(a) {
    if (a === 'debugger') {
        return function(){}
    } else {
        return AAA(a);
    }
}
```

### 接口参数

点击不同的政策类型切换接口，找到 showPolicyType 接口。发现请求载荷是进制流参数。

打开堆栈，断点到最后一步，找到请求参数其实是一个 Array Buffer。

继续断点往前找，断在第一个 promise 前。发现`e`是请求对象。`e.data`还是未加密的参数。

那么参数就一定是在 promise.then 之后进行加密的。i 数组有6个方法。

我们先进去这个`i`的数组中第一个，挨个看看。

axios...函数接受 e 函数，返回了 a 值。这是就要盯着 a 值。分别在函数中打三个断点，注意 e 和 a 的变化。发现请求载荷 e 显示赋值了 r ， r 再赋值 a ，后期对 a 进行了加密，a.data 成了加密后的参数。

划线的就是加密入口，经过字符串的显示：

```js
a["data"] = d["encode"](a["data"])["finish"]()['slice']()
```

悬浮进入`d["encode"]`方法，发现是一个VM文件。VM不是一个真实的文件，这里会有一个bug。打上断点，悬浮进去后是：

`Winter.create()`执行结果是一个已有的对象。找不到原始的来源。找不到 Winter 是从哪里生成的。

这时搜索Winter关键字发现 Winter 的定义的地方，

这段代码其实是在一个 webpack 的模块里，webpack 加载器自执行初始化的时候生成了 Winter 对象，存放在加载器对象中。

接着去找 webpack 的入口：加载器，i2

然后copy整个自执行函数。

新建一个loader.js文件，将 webpack 放进去，执行一下，发现`commonjsGlobal`未定义。这时想在网页中断点到 webpack 刚开始的地方，发现由于网站反调试的原因，无法断住。那么就在本地调试。将`commonjsGlobal`定义为全局对象Window。就不再报错。

本地调试过程中发现 Winter 对象就存放在 i2 加载器对象之中。

随后吧加载器赋值给一个全局对象，就可以得到 Winter 对象。随后便全部完成了。