---
title: 'JS逆向-某电子税务局'
description: 'JS逆向实战，记录某电子税务局的加密参数破解过程'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - JS逆向
---

## 正文

这个案例虽然不难也没啥实用价值，但还是挺有意思的。

网址：aHR0cHM6Ly90cGFzcy5zaGFueGkuY2hpbmF0YXguZ292LmNuOjg0NDMvIy9mb3JnZXQ=

## 0 前置准备

打开无痕式窗口，清除网站数据，否则第一个接口获取不到。

## 1 接口分析

输入证件类型，身份证号（位数对即可）点击 下一步触发三个请求：getPublicKey 、sendSm4、selectMobileListByAccountNew，我们按照时间顺序一个一个来分析。

## 2 getPublicKey

### 2.1 headers

headers 中的 deviceidentyno 虽然变化，但是不影响请求，忽略即可

### 2.2 params

搜索 signature 关键字可以轻松定位到：

断点打在 signature 点击下一步断不住，刷新网页可以断住，发现这时第一个 getPublicKey 请求都没发送成功，说明断在了第一个请求。

有必要稍微阅读一下代码逻辑，这是在一个请求拦截器中：

```js
...
g = f || Object(c["b"])(),
P = g.substring(0, 8) + O,
    // 这里是一个三元运算符，根据请求的 url 是否在 X 数组中，执行不同的逻辑，前面查看三个接口的载荷都非常相似，都有 signature timestamp 这些，但三元运算这里的结果不同。
"post" === A.method && (X.includes(A.url) ? 
                        (o["encryptCode"] = "0", o.datagram = JSON.stringify(A.data)) : 
                        (l = JSON.stringify(A.data),
                        p = Object(c["d"])(l, Object(c["i"])(P)),
                        o.datagram = p,
                        o["encryptCode"] = "2")),  // 三元运算符的逻辑到这里
o["timestamp"] = (new Date).format("yyyyMMddHHmmss"),
o["access_token"] = "",
o["signtype"] = "HMacSHA256",
o["signature"] = Object(c["a"])(o["zipCode"] + o["encryptCode"] + p + o["timestamp"] + o["signtype"], g),
A.data = o
...
```

`c["a"]`中的`c`是一个 webpack，向上找到`var c = n("0b77");`刷新网页断在这个模块，然后进去扣加载器所在的文件及其所需模块即可。

接着检查`Object(c["a"])(o["zipCode"] + o["encryptCode"] + p + o["timestamp"] + o["signtype"], g)`中的个元素。

第1、2、3、5 个固定即可，nodejs 中没有`(new Date).format("yyyyMMddHHmmss")`这个方法，问 AI 实现一个即可。`g`来自`Object(c["b"])()`，初次加载时`g = f || Object(c["b"])()`中的`f`为空，但后续两个请求不为空，我们后续再看。

这样我们就完成了第一个接口：

### 2.3 参考代码

```js
require("./env");
require("./mod01")
require("./mod02")

require("./loader")
var c = window.loader("0b77")

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}${month}${day}${hours}${minutes}${seconds}`;
}

function get_signature(){
    let f = Object(c["b"])()
    let g = f || Object(c["b"])()
    let p = ""
    let o = {}
    o["zipCode"] = "0"
    o["encryptCode"] = "0"
    o["timestamp"] = formatDate(new Date())
    o["access_token"] = ""
    o["signtype"] = "HMacSHA256"
    o["signature"] = Object(c["a"])(o["zipCode"] + o["encryptCode"] + p + o["timestamp"] + o["signtype"], g)

    return o
}
```

## 3 sendSm4

### 3.1 headers

第二个请求多了一个`x-temp-info`，断住后发现是一个 uuid， 经过比对，正是来自于 getPublicKey 返回的 uuid：

### 3.2 params

datagram 中的 uuid 是来自于 getPublicKey 返回的 uuid。

进一步分析 secret，来自于`A.data`。

看结构组成 A 是一个请求对象。全局搜索 secret 定位到：

n 就是 secret,`_utils_getUuid__WEBPACK_IMPORTED_MODULE_5__["c"]`向上可以找到就是原来的 webpack：`n("0b77")`, naturepublicKey 是 getPublicKey 返回的 publicKey。A 就也有了。

扣代码

```js
// 注意只扣必要的。
A = Object(_utils_getUuid__WEBPACK_IMPORTED_MODULE_5__["b"])(),
// localStorage.getItem("new_key16") && (js_cookie__WEBPACK_IMPORTED_MODULE_8___default.a.get("token") || "/secondCertificate" == _router__WEBPACK_IMPORTED_MODULE_9__["b"].history.current.path) && (A = localStorage.getItem("new_key16")),      这部分的localStorage.getItem("new_key16")为false，因此不要扣下来
n = Object(_utils_getUuid__WEBPACK_IMPORTED_MODULE_5__["c"])(A, localStorage.getItem("naturepublicKey"), 1),
/* Object(_api_login__WEBPACK_IMPORTED_MODULE_4__["a"])({
    uuid: localStorage.getItem("natureuuid") || "",
    secret: n
    }).then((function(e) {
        localStorage.setItem("new_key16", A)
    }
    )).catch((function() {}
    ));    
    我们已然得到了secret，这部分的逻辑就不要再扣了 尤其是这个多出来的_api_login__WEBPACK_IMPORTED_MODULE_4__就不要了，没有用，还会导致非常多的补环境。
    注意这里把 A 赋给了 new_key16，我们需要导出这个值，后面还有用
*/
```

完成第二个接口

### 3.3 参考代码

```js
function sendSm4(natureuuid, naturepublicKey){
    let A = Object(c["b"])(),
    n = Object(c["c"])(A, naturepublicKey, 1)
    let g = Object(c["b"])()
    let o = {}
    let p = ""
    o["encryptCode"] = "0"
    o["zipCode"] = "0"
    let AA = {
        data:{
            "secret": n,
            "uuid": natureuuid
        }
    }
    o.datagram = JSON.stringify(AA.data)
    o["timestamp"] = formatDate(new Date()),
    o["access_token"] = "",
    o["signtype"] = "HMacSHA256",
    o["signature"] = Object(c["a"])(o["zipCode"] + o["encryptCode"] + p + o["timestamp"] + o["signtype"], g)
    return {new_key16:A,o}
}
```

## 4 selectMobileListByAccountNew

### 4.1 headers

`deviceidentyno`和`x-temp-info`同上

### 4.2 params

`datagram`成了一个加密值，走的是三元运算符的后半部分。

A.data 正是我们的身份证号和证件类型，扣下来对应的逻辑即可。

需要注意`Object(c["a"])(o["zipCode"] + o["encryptCode"] + p + o["timestamp"] + o["signtype"], g)`中的`g`正是来自第二个接口逻辑中生成的 new_key16。

完成第三个接口

### 4.3 参考代码

```js
let O = "dt!P^bfrR6LhHTUutGk3GwdKdewgdewgjfekqwgfgfjg".substring(0, 4) + "fwejkfjqfgjgfhewvfvq^R4qd^VLrf^2^ujqgM2Rpb9t".substring("fwejkfjqfgjgfhewvfvq^R4qd^VLrf^2^ujqgM2Rpb9t".length - 4)
function selectMobileListByAccountNew(idcard,new_key16){
    let f = new_key16
    let g = f || Object(c["b"])()
    let A = {}
    A.data = {
        "idCard": idcard,
        "idCardType": "201"
    }
    let P = g.substring(0, 8) + O
    let o = {}
    o["zipCode"] = "0"
    l = JSON.stringify(A.data)
    p = Object(c["d"])(l, Object(c["i"])(P))
    o.datagram = p
    o["encryptCode"] = "2"
    o["timestamp"] = formatDate(new Date())
    o["access_token"] = ""
    o["signtype"] = "HMacSHA256"
    o["signature"] = Object(c["a"])(o["zipCode"] + o["encryptCode"] + p + o["timestamp"] + o["signtype"], g)
    return o
}
// let idcard = "410782199303229536"
// console.log(selectMobileListByAccountNew(idcard));
```

## 5 python封装

python 封装很简单，这里就不贴了，注意三个接口的 headers 略有不同，不要全部套用即可。