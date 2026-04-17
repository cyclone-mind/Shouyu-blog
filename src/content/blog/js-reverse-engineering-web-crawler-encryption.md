---
title: 'JavaScript 逆向入门指南：爬虫的加密参数破解'
description: 'JavaScript 逆向入门，爬虫的加密参数破解教程'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - JS逆向
---

## 摘要

JavaScript 逆向入门

JS 逆向（JavaScript Reverse Engineering）指通过分析网页中 JavaScript 代码的加密逻辑，还原数据请求的加密参数生成过程。它是爬虫开发中绕过反爬机制的核心技术。JS逆向一般分为请求逆向和响应逆向。

* 请求逆向：网站通过将请求所需的动态关键字如页码、搜索关键字、账号密码等信息加密放在 headers、params、cookie 中实现，实现请求加密，这样防止爬虫者篡改请求参数爬取到页面信息。而爬虫者通过前端断点调试，找出 JavaScript 代码的加密逻辑，还原数据请求的加密参数，伪造加密参数，发出请求。

* 响应逆向：服务器返回给前端的是加密的字符串，为能够在页面正常显示信息，前端的 JavaScript 代码对字符串进行解密。爬虫者通过前端断点调试，找出 JavaScript 代码的解密逻辑，还原加密数据解密过程，拿到数据。

## 核心工具链

### 1. 调试工具

* Chrome DevTools：断点调试 JavaScript，观察变量变化

* Fiddler/Charles：篡改 JavaScript 文件

* Node.js：快速验证 JavaScript 加密函数

### 2. Python 库

* requests：模拟 HTTP 请求

* lxml bs4：解析 HTML

* PyExecJS：执行 JavaScript 代码片段

## 实战案例：破解简单加密参数

以某网站的`portal-sign`参数为例，演示逆向流程。

### 步骤 1：定位加密逻辑

1. 打开目标网页，使用 Chrome DevTools 的 Network 面板观察请求参数。

1. 搜索关键词（portal-sign），定位生成加密参数的 JavaScript 函数。

1. 定位入口：
t.headers["portal-sign"] = f.getSign(e)

function d(t) {
            for (var e in t)
                "" !== t[e] && void 0 !== t[e] || delete t[e];
            var n = r["a"] + u(t);
            return s(n).toLocaleLowerCase()
        }

### 步骤 2：提取并复现加密逻辑

理解加密逻辑，就是用MD5：

```python
from hashlib import md5
import time


def get_sign(data):
    # (1) 固定字符串
    s = 'B3978D054A72A7002063637CCDF6B2E5'
    # (2) 将参数整理成某称格式字符串
    l = sorted(data.items(), key=lambda i: i[0])
    data_str = ""
    for key, val in l:
        data_str += key + str(val)

    print("data_str:::", data_str)

    # (3)
    s = s + data_str
    md5_obj = md5()
    md5_obj.update(s.encode())

    return md5_obj.hexdigest()


sign = get_sign(json_data)
print("sign:::", sign)
```

### 步骤 3：模拟请求

将生成的参数加入请求头或表单数据：

```python
import requests

cookies = {
    'ASP.NET_SessionId': 'yia0gk1jwug2xfesgxkqoc3u',
}
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'https://ggzyfw.fj.gov.cn/index/new/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
}
json_data = {
    'type': '12',
    'IS_IMPORT': 1,
    'pageSize': 20,
    'ts': timer,
}
headers["portal-sign"] = sign
response = requests.post('https://ggzyfw.fj.gov.cn/FwPortalApi/Article/PageList', 
                         cookies=cookies, headers=headers,
                         json=json_data)

print(response.text)
```

## 进阶方向

### 1. 检测浏览器环境动态生成 Cookie（如瑞数）

* 技术核心：通过 JavaScript 检测浏览器指纹（如 navigator 对象、Canvas 渲染结果、WebGL 信息）和 TLS 握手特征，动态生成加密 Cookie（如 _umdata、__RC）。

* 示例：瑞数（River Security）通过动态执行的 JS 代码生成 前后两次的cookie。

### 2. 验证码（极验、顶象）

* 技术核心：结合行为分析（如鼠标轨迹、点击压力）、生物特征（如滑动速度）和 AI 风险评分，生成动态验证码。

* 示例：

极验（Geetest）：第三代滑块验证码需模拟人类拖动轨迹（先加速后减速），并破解 gt、challenge 参数的加密逻辑。
顶象（DingXiang）：通过 XSS 防御和 WebAssembly 实现的无感验证（如 "文字点选"），需逆向其 dx.js 中的算法。

* 极验（Geetest）：第三代滑块验证码需模拟人类拖动轨迹（先加速后减速），并破解 gt、challenge 参数的加密逻辑。

* 顶象（DingXiang）：通过 XSS 防御和 WebAssembly 实现的无感验证（如 "文字点选"），需逆向其 dx.js 中的算法。

### 3. JS 混淆或加密（Obfuscator、Wasm、JSVMP）

* 技术核心：

代码混淆：通过变量名替换、控制流平坦化（Control Flow Flattening）、字符串加密隐藏逻辑。
WebAssembly 加密：将核心算法编译为 .wasm 文件，反编译门槛高（如 wat 格式需进一步分析）。
JSVMP（虚拟机保护）：将 JS 代码编译为自定义字节码，通过虚拟机解释执行。

* 代码混淆：通过变量名替换、控制流平坦化（Control Flow Flattening）、字符串加密隐藏逻辑。

* WebAssembly 加密：将核心算法编译为 .wasm 文件，反编译门槛高（如 wat 格式需进一步分析）。

* JSVMP（虚拟机保护）：将 JS 代码编译为自定义字节码，通过虚拟机解释执行。

### 4. 字体反爬、CSS 反爬、雪碧图

* 技术核心：

字体反爬：自定义字体文件（如 woff、ttf）映射字符编码（如数字 1 显示为 A，但实际 Unicode 为 xE001）。
CSS 反爬：通过 CSS 偏移（::before 伪类）或层级覆盖隐藏真实文本（如价格显示 ￥100，但实际 DOM 中是 ￥<span class="hidden">200</span>）。
雪碧图（CSS Sprites）：合并多个图标为一张图片，通过 background-position 定位，增加 OCR 识别难度。

* 字体反爬：自定义字体文件（如 woff、ttf）映射字符编码（如数字 1 显示为 A，但实际 Unicode 为 xE001）。

* CSS 反爬：通过 CSS 偏移（::before 伪类）或层级覆盖隐藏真实文本（如价格显示 ￥100，但实际 DOM 中是 ￥<span class="hidden">200</span>）。

* 雪碧图（CSS Sprites）：合并多个图标为一张图片，通过 background-position 定位，增加 OCR 识别难度。

* 示例：猫眼电影票房数据使用自定义字体加密数字，需下载 .woff 文件并解析 cmap 表还原真实数值。

### 5. TLS 指纹检查

* 技术核心：通过分析客户端的 TLS 握手特征（如支持的加密套件、扩展字段、协议版本）生成唯一指纹（如 JA3 哈希），识别非浏览器流量。

* 示例：Cloudflare 的 cf-chl-bypass 检测会拦截 TLS 指纹异常的请求，需模拟真实浏览器指纹（如 Chrome 的 TLS_GREASE 握手特征）。

## 学习资源推荐

* 视频教程：【无逆向难爬虫】爬虫高手进阶之路

* 资源汇总：虫盒、吾爱破解

* 开源项目：learn_python3_spider、CrawlerToturial、CrawlerWorks