---
title: 'JS逆向之某日漫网站'
description: 'JS逆向实战，记录某日漫网站的加密参数破解过程'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - JS逆向
---

## 正文

网址：aHR0cHM6Ly9zcC5tYW5nYS5uaWNvdmlkZW8uanAvd2F0Y2gvbWc5MDQ3NDM=

本来想接这个单子的，但是预算只给 25，实在蚌埠住了。不过里面有点没学过的新知识、因此发出来记录一下。

## 1 接口分析

### 1.1 frames?enable_webp=true

该接口中返回图片的 前置 url。

```json
{
    "meta": {
        "status": 200
    },
    "data": {
        "result": [
            {
                "id": 10177673,
                "meta": {
                    "resource": {
                        "bgm": null,
                        "se": null
                    },
                    "duration": 1,
                    "width": 650,
                    "height": 888,
                    "is_spread": false,
                    "source_url": "https:\/\/drm.cdn.nicomanga.jp\/image\/7f7be717754389f5e7d09d5adc5857705ec6fbee_10089\/16365004p.webp?1740533869",
                    "drm_hash": "7f7be717754389f5e7d09d5adc5857705ec6fbee_10089",
                    "link_url": null
                }
            },
            ...
        ]
    }
}
```

### 1.2 blob

按左键加载图片，触发该接口。

该接口完整 url：blob:https://sp.manga.nicovideo.jp/79bfc888-2ced-41b9-b2f8-71d8e5376ccd

此接口返回图片。分析该接口，只在地址栏有一个类似于 uuid 的加密值。通过堆栈回溯确定加密位置：

前一个接口的返回值就是这里的`e`：

```js
// e 对象
{
    "id": 10177680,
    "meta": {
        "resource": {
            "bgm": null,
            "se": null
        },
        "duration": 1,
        "width": 650,
        "height": 888,
        "is_spread": true,
        "source_url": "https://drm.cdn.nicomanga.jp/image/5b13c095b44e24928058e082a7440bfdb0d09bbc_10089/16365011p.webp?1740533876",
        "drm_hash": "5b13c095b44e24928058e082a7440bfdb0d09bbc_10089",
        "link_url": null
    }
}
```

从名称上看应该是在`decodeURLToBlob`函数中发出请求获取图片，并转为 Blob，从`URL.createObjectURL(t)`生成图片 URL 供前端预览。

`URL.createObjectURL(t)`就是我们要的结果。

::: details
Blob (Binary Large Object) 是一个表示二进制数据的对象，通常用于处理文件或图片等二进制数据。
Blob 的主要特点：

1. 可以存储任意类型的二进制数据

1. 可以设置 MIME 类型（如 image/jpeg）

1. 可以通过 arrayBuffer() 方法获取底层数据

1. 在浏览器中可以通过 URL.createObjectURL() 创建可访问的 URL
:::

## 2 扣代码

```js
class i$ {
            static xor(e, t) {
                let n = new Uint8Array(e)
                  , {length: r} = n
                  , {length: i} = t
                  , s = new Uint8Array(r);
                for (let e = 0; e < r; e += 1)
                    s[e] = n[e] ^ t[e % i];
                return s
            }
            static generateKey(e) {
                let t = e.slice(0, 16).match(/[\da-f]{2}/gi);
                return eX(t, "Failed generate key."),
                new Uint8Array(t.map(e => parseInt(e, 16)))
            }
            static decodeHashToArr(e) {
                let t = atob(e)
                  , n = [];
                for (let e = 0; e < t.length; e += 1)
                    n[e] = t.charCodeAt(e);
                return n
            }
            static async decodeURLToBlob(e, t) {
                let n = await I(e).then(e => e.blob()) // I 方法 请求获取图片转为 Blob
                  , r = await new iL().readAsArrayBuffer(n); // iL 方法 将 Blob 转为 ArrayBuffer
                return new Blob([this.xor(r, this.generateKey(t))],{ // 从 ArrayBuffer 新建一个 Blob并加密
                    type: "image/jpeg"
                })
            }
        }
iI = async e => {
            if (null != e.meta.drm_hash) {
                let t = await i$.decodeURLToBlob(e.meta.source_url, e.meta.drm_hash);
                return await iD(URL.createObjectURL(t)) 
            }
            return await iD(e.meta.source_url)
        }
```

```js
let $ = fetch
          , D = e => {
            if (!e.ok)
                throw new L(e,"Network response was not ok.");
            return e
        }
          , I = async (...e) => $(...e).then(D) // I 方法 
// 这有 JavaScript 中的展开运算符（Spread Operator）和剩余参数（Rest Parameters）的写法。
// ...e 在函数参数中表示"收集所有传入的参数到一个数组中"
// $(...e) 表示"将这个数组展开成单独的参数传递给 $ 函数"，也就是发送请求获取图片了
```

::: tip
在浏览器环境中，`fetch`是内置的全局对象 ，作为是一个现代的 HTTP 请求 API，比传统的`XMLHttpRequest`更易用。在 Node.js v18+ 版本中，fetch 是内置的。`e.blob()`是`fetch`响应对象的一个方法，用于将响应数据转换为`Blob`对象。
:::

对于 iL 函数，nodejs 环境中并没有 FileReader 对象，我们自己写一个类来替代这个 iL，实现将 Blob 对象转为 ArrayBuffer

```js
class iL {
  async readAsArrayBuffer(e) {
    try {
      if (e instanceof Blob) {
        return await e.arrayBuffer();
      } else {
        const buffer = await fs.readFile(e);
        return buffer.buffer;
      }
    } catch (error) {
      throw new Error("Failed to read data.");
    }
  }
}
```

还有 iI， 因为我们已经有了 Blob了，所以不需要从 Blob 生成图片 URL 供前端预览。我们直接将 Blob 转换为 Buffer 并保存到文件就行

```js
iI = async e => {
            if (null != e.meta.drm_hash) {
                let t = await i$.decodeURLToBlob(e.meta.source_url, e.meta.drm_hash);
                // return await iD(URL.createObjectURL(t)) 
                const buffer = Buffer.from(await t.arrayBuffer());
                const filename = `decrypted_${e.id}.jpg`;
                await fs.writeFile(filename, buffer);
                return filename;
            }
            return await iD(e.meta.source_url)
        }
```

到此 我们已经完成。

## 3 参考代码

```js
const fs = require("fs").promises;
const { Blob } = require("buffer");

class iL {
  async readAsArrayBuffer(e) {
    try {
      if (e instanceof Blob) {
        return await e.arrayBuffer();
      } else {
        const buffer = await fs.readFile(e);
        return buffer.buffer;
      }
    } catch (error) {
      throw new Error("Failed to read data.");
    }
  }
}
class i$ {
  static xor(e, t) {
    let n = new Uint8Array(e),
      { length: r } = n,
      { length: i } = t,
      s = new Uint8Array(r);
    for (let e = 0; e < r; e += 1) s[e] = n[e] ^ t[e % i];
    return s;
  }
  static generateKey(e) {
    let t = e.slice(0, 16).match(/[\da-f]{2}/gi);
    return new Uint8Array(t.map((e) => parseInt(e, 16)));
  }
  static decodeHashToArr(e) {
    let t = Buffer.from(e, "base64"),
      n = [];
    for (let e = 0; e < t.length; e += 1) n[e] = t[e];
    return n;
  }
  static async decodeURLToBlob(e, t) {
    let n = await I(e).then((e) => e.blob()),
      r = await new iL().readAsArrayBuffer(n);
    return new Blob([this.xor(r, this.generateKey(t))], {
      type: "image/jpeg",
    });
  }
}

let $ = fetch,
  D = (e) => {
    if (!e.ok)
      throw new L(e,"Network response was not ok.");
    return e;
  },
  I = async (...e) => $(...e).then(D);

iI = async (e) => {
  if (null != e.meta.drm_hash) {
    let t = await i$.decodeURLToBlob(e.meta.source_url, e.meta.drm_hash);
    // 将 Blob 转换为 Buffer 并保存到文件
    const buffer = Buffer.from(await t.arrayBuffer());
    const filename = `decrypted_${e.id}.jpg`;
    await fs.writeFile(filename, buffer);
    return filename;
  }
};

let data = {
  id: 10285844,
  meta: {
    resource: {
      bgm: null,
      se: null,
    },
    duration: 1,
    width: 650,
    height: 889,
    is_spread: false,
    source_url:
      "https://drm.cdn.nicomanga.jp/image/4b048448d946e0afc205b73dd76e2365d52ceeea_10089/16483464p.webp?1743145040",
    drm_hash: "4b048448d946e0afc205b73dd76e2365d52ceeea_10089",
    link_url: null,
  },
};

iI(data).then((e) => console.log(e));
```