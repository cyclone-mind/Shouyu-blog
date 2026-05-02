---
title: 'vibecoding---一天时间落地一个真实可支付的 Sass，地图制作课程。'
description: '使用 Next.js + Supabase + Vercel + Z-Pay 从零搭建一个可支付的 Sass 地图制作课程平台，包含完整支付流程、订阅逻辑和部署方案。'
pubDate: '2026-05-01'
updatedDate: 'May 02 2026'
authors:
  - shouyu
toc: true
tags:
  - vibecoding
  - z-pay
  - supabase
  - vercel
---

> 本文章不记录如何从零实现这么一个地图制作课程的 Sass，而是记录在这个过程中遇到的细节。

项目地址：[地图制作课程](https://mapcourse.microcyclone.cloud)

## 1. 选择技术栈

next.js + supabase + vercel + z-pay

## 初始化项目

使用了 [B站熠辉](https://space.bilibili.com/39930228) 的起始模板。

---

我们设置环境变量

```text
# Supabase 配置
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# 应用基础配置
NEXT_PUBLIC_BASE_URL=http://localhost:3000

# Z-Pay 支付网关配置
ZPAY_PID=
ZPAY_KEY=
```

你需要从 supabase 获取 `NEXT_PUBLIC_SUPABASE_URL` 和 `NEXT_PUBLIC_SUPABASE_ANON_KEY`，以及从 z-pay 获取 `ZPAY_PID` 和 `ZPAY_KEY`。z-pay 是一个第三方支付平台，z-pay 的接口非常简单，提供了支付宝和微信支付的接口，适合我们快速集成支付功能，且无需营业执照。

---

## 支付设置

`NEXT_PUBLIC_BASE_URL` 是我们应用的基础 URL，在开发环境中是 `http://localhost:3000`，在生产环境中需要替换成你的实际域名。另外提前说明，z-pay 的回调接口需要公网地址，无法访问到 vercel 的域名，这也是为什么我们需要自己的域名。

对于支付，核心的流程是：

1. 用户点击购买按钮，前端调用后端接口创建订单。
2. 后端接口使用 z-pay 的 SDK 创建支付订单，并返回支付链接给前端。
3. 用户使用支付链接完成支付，z-pay 会回调我们的后端接口通知支付结果。
4. 后端接口处理支付结果，更新订单状态，并根据需要给用户提供访问权限。
5. 前端根据支付结果给用户反馈。

这个过程中最关键的是有两个接口。一个是创建订单的接口，另一个是处理支付回调的接口。

接口1：​​​`​/api/checkout/providers/zpay/url​​​​`，用于前端获取支付链接

接口2：​​​`​/api/checkout/providers/zpay/webhook`​​​​，用户支付平台通知我们的后端服务
​​
用户点击购买按钮后，前端会调用接口1获取支付链接，这个支付链接是 z-pay 的付款二维码网址。我们采取了 [z-pay页面跳转支付](https://member.z-pay.cn/member/doc.html)接口。

用户支付完成后，z-pay 会回调接口2，通知我们支付结果。我们需要在接口2中验证回调数据的真实性，并根据支付结果更新订单状态。

<div class="callout" data-callout="info">
  <p><strong>Info:</strong> 本地开发时需要手动模拟支付回调，上线后则需要公网可访问的域名来接收 z-pay 的回调请求。</p>
</div>

### 本地开发：模拟 z-pay 回调

本地开发时，z-pay 无法回调你的 `localhost` 地址，需要手动模拟回调请求来测试接口2。

我们发现，用户支付完成后的跳转页面是这样：

```
return_url?pid=xxx&trade_no=xxx&out_trade_no=xxx&type=alipay&name=xxx&money=1.00&trade_status=TRADE_SUCCESS&sign=xxx&sign_type=MD5
```

那么这个请求的参数就是 `pid`、`trade_no`、`out_trade_no`、`type`、`name`、`money`、`trade_status`、`sign` 和 `sign_type`。

**方法一：Postman**

在 Postman 中构造 POST 请求：

```
POST http://localhost:3000/api/checkout/providers/zpay/webhook
Content-Type: application/x-www-form-urlencoded
```

**Body 参数：**

| 参数 | 说明 | 示例 |
| :-- | :-- | :-- |
| `pid` | 商户 ID | `xxx` |
| `trade_no` | z-pay 交易号 | `202604050000` |
| `out_trade_no` | 你的订单号 | `order_xxx` |
| `type` | 支付方式 | `alipay` |
| `name` | 商品名称 | `课程名称` |
| `money` | 支付金额 | `1.00` |
| `trade_status` | 交易状态 | `TRADE_SUCCESS` |
| `sign` | 签名 | `xxx` |
| `sign_type` | 签名方式 | `MD5` |

**方法二：浏览器直接访问**

直接在浏览器地址栏访问（GET 请求）：

```
http://localhost:3000/api/checkout/providers/zpay/webhook?pid=xxx&trade_no=xxx&out_trade_no=xxx&type=alipay&name=xxx&money=1.00&trade_status=TRADE_SUCCESS&sign=xxx&sign_type=MD5
```

你也可以在 [z-pay 订单后台](https://member.z-pay.cn/member/orders.html) 查看订单详情和回调日志，获取实际的回调参数。

### 上线部署：配置公网回调

上线后，z-pay 的回调接口需要公网可访问的地址。Vercel 分配的域名无法被外网访问，因此你需要配置自己的域名来接收回调。

<div class="callout" data-callout="warning">
  <p><strong>Warning:</strong> 涉及到支付的逻辑一定要认真测试，尤其是订阅的逻辑，过期时间的计算逻辑，重复订阅的处理逻辑等，这些都是比较容易出问题的地方。</p>
</div>

可能有用的提示词

```text
现在请你帮我开发两个支付接口：

- 接口1： `/api/checkout/providers/zpay/url`，用于前端获取支付链接

- 接口2：`/api/checkout/providers/zpay/webhook`，用于支付平台通知我们的后端服务

我使用的是zpay支付实现支付

1. 关于前端获取支付链接的接口`/api/checkout/providers/zpay/url`，需要拼接成为的支付链接如下[文档](https://member.z-pay.cn/member/doc.html)
2. 关于/api/checkout/providers/zpay/webhook`，用于支付平台通知我们的后端服务的webhook，[接口文档](https://member.z-pay.cn/member/doc.html)

请你帮我实现这两个接口，要求：

1. 服务端操作数据库的相关操作，请使用createServerAdminClient实现
2. 在webhook中需要检查对应业务的状态，避免重复调用数据库或者插入数据
3. 支付结果通知的内容一定要做签名验证,并校验返回的订单金额是否与商户侧的订单金额一致，防止数据泄漏导致出现“假通知”，造成资金损失。
4. 请你给到我supabase需要创建的表sql，并且保存在项目中，表名叫做`zpay_transactions`
5. 我们的环境变量中字段包括NEXT_PUBLIC_SUPABASE_URL、NEXT_PUBLIC_SUPABASE_ANON_KEY、SUPABASE_SERVICE_ROLE_KEY、NEXT_PUBLIC_BASE_URL、ZPAY_PID、ZPAY_KEY

同时请你帮我实现 @pricing.tsx 接入请求获取购买链接的接口，包括一次性购买逻辑 + 订阅模式，要求：

1. 订阅模式需要设置过期时间等信息，而且订阅需要考虑重复订阅的情况，例如用户在2025-03-15订阅了一个月，那么过期时间是2025-04-15，但是用户在2025-04-01又订阅了一个一个月，此时用户的开始订阅时间需要从2025-04-15开始计算，过期时间是2025-05-15，这一定要注意
2. 用户需要登陆后才能请求获取购买链接，因为要获取用的uid，如果用户没有登陆点击支付，跳转登录页/signin
​
```

<div class="callout" data-callout="tip">
  <p><strong>Tip:</strong> 一方面你可以使用 <a href="https://supabase.com/docs/guides/getting-started/mcp">Supabase 的 MCP 功能</a>连接到你的项目，这样你就可以使 Agent 直接操作你的数据库创建表之类的。另一方面你也可以将创建表的 SQL 语句保存在项目中，例如在 <code>db/schema.sql</code> 文件中，这样你就可以在需要的时候执行这个 SQL 文件来创建表。</p>
</div>


---

## 个人页面

<div class="callout" data-callout="note">
  <p><strong>Note:</strong> 以下是封装购买历史组件时使用的提示词参考。</p>
</div>

提示词

```text
1. 请你在 @layout.tsx 中获取本人的订阅信息，并在邮箱下面显示
2. 请你在 @components/PurchaseHistory.tsx 中封装一个购买历史，并在/dashboard这个页面显示，要求显示产品名称、购买日期、价格、状态和操作按钮。如果是待支付状态，那么点击后用户去跳转支付；如果支付成功，点击后alert相关的购买订单的详细信息
```

这里我们需要注意的就是 用户支付的月订阅的过期时间的计算逻辑，用户可能会在订阅过期前再次订阅，这时候新的订阅应该从当前订阅的过期时间开始计算，而不是从当前时间开始计算。

---

<div class="callout" data-callout="tip">
  <p><strong>Tip:</strong> 在前端，用户的订阅信息我们可以使用轮询的方式来获取，或者使用 Supabase 的 Real-time 功能来实时更新用户的订阅状态，这样用户在支付完成后可以立即看到自己的订阅状态更新。</p>
</div>

---

## 部署至 Vercel

部署到 Vercel 非常简单，你只需要将你的代码 push 到 GitHub 上，然后在 Vercel 上连接你的 GitHub 仓库，选择你要部署的分支，Vercel 会自动构建和部署你的应用。在部署之前，记得在 Vercel 的环境变量设置中添加你在本地使用的环境变量，这样你的应用在 Vercel 上也能正常运行。

还有 `pnpm dev` 不同于 `pnpm build` 和 `pnpm start`，前者是开发模式，会启动一个热更新的开发服务器，适合本地开发和调试；后者是生产模式，会先构建应用，然后启动一个优化过的生产服务器，适合部署到生产环境。所以我们最好在本地 `pnpm build` 来测试一下生产模式下的构建和运行，确保没有问题后再部署到 Vercel。

<div class="callout" data-callout="info">
  <p><strong>Info:</strong> 本地开发的时候我们可以自己模拟 z-pay 的回调请求来测试支付逻辑，但上线部署后由于 z-pay 的回调接口需要公网地址，需要配置自己的域名来接收回调。</p>
</div>