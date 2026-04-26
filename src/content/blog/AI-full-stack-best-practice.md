---
title: AI全栈最佳实践-1
description: AI全栈开发的最佳实践指南，涵盖框架选择、组件开发、Supabase使用、Chrome插件开发和支付集成等核心内容。
pubDate: '2026-4-25'
authors:
  - shouyu
toc: true
tags:
  - AI全栈
  - Next.js
  - Supabase
  - Chrome插件
  - 支付集成
---

## AI全栈最佳实践

框架选择 next.js 或 [nuxt.js](https://nuxt.com/)。这里推荐 [next.js](https://nextjs.org/)。理由：

1. 底层基于 React，现在大模型对 React 支持明显比 Vue 好；
2. 由 Vercel 公司开发，方便部署在 vercel 上。并且，路由系统、构建优化、图像处理等都已集成；
3. 全栈框架；
4. 强大的生态系统；

Next.js拥有丰富的生态系统，这些工具和库可以大大简化开发过程，特别是对于使用AI辅助开发的新手。

## 一、UI和组件 

[shadcn/ui](https://ui.shadcn.com/)：高度可定制的组件集合，不是传统组件库，而是可以直接复制到项目中的代码

[Tailwind CSS](https://tailwindcss.com/)：Next.js默认支持的实用优先CSS框架，可快速构建现代界面

[Radix UI](https://www.radix-ui.com/)：无样式、可访问性优先的组件原语，与Next.js配合得很好

## 二、开发工具和核心扩展 

[Vercel](https://vercel.com/)：Next.js的创建者开发的部署平台，为Next.js项目优化

[NextAuth.js](https://next-auth.js.org/)：专为Next.js设计的身份验证解决方案

[SWR](https://swr.vercel.app/zh-CN)：由Vercel团队开发的数据获取库，完美配合Next.js使用

## 三、常用启动模板 

c[reate-t3-app](https://create.t3.gg/)：包含TypeScript、Tailwind、Prisma等工具的现代Next.js启动模板

[next-enterprise](https://next-enterprise.vercel.app/)：企业级Next.js启动器，包含常用配置和最佳实践

[Next.js starter](https://vercel.com/templates/next.js?utm_source=next-site&utm_medium=navbar&utm_campaign=next_site_nav_templates)：nextjs官方启动器。

[template0](https://template0.com/): 模板导航站

[saasboilerplates](https://saasboilerplates.dev/)：付费模板集合

尽量使用这些启动模板，而不是让AI帮你从0搭脚手架，因为你可能遇到各种各样的版本兼容、包兼容问题。

## 四、Next.js 

1. next.js的默认环境为`.env.local`而不是 `.env` ，且统一以 `NEXT_`开头
   ```
   NEXT_PUBLIC_EXAMPLE=https://example.com/api
   SECRET_API_KEY=xxxxxxxxxxxxxxxxxxxx
   ```

   - NEXT_PUBLIC_开头的变量是公开的，前端可访问
   - 不带NEXT_PUBLIC_的变量仅用于服务端，前端无法访问。
   - 部署到 Vercel 等平台时，必须在平台控制台中配置相同名称的环境变量。也就是手动在平台控制台再设置一次。

### 1. Next.js的基本目录结构 

Next.js提供了两种组织项目的方式：App Router（app/目录）和Pages Router（pages/目录）。从Next.js 13开始，App Router是官方推荐的新方式，本章将主要介绍这种模式。

#### App Router 结构（官方推荐） 

```
my-nextjs-project/
├── app/                 # 应用主目录
│   ├── favicon.ico      # 网站图标
│   ├── globals.css      # 全局样式
│   ├── layout.tsx       # 根布局组件（应用于所有页面）
│   ├── page.tsx         # 首页组件
│   └── about/           # 关于页面目录
│       └── page.tsx     # 关于页面组件
├── components/          # 可复用组件目录（自创建）
├── public/              # 静态资源目录
└── ...                  # 其他配置文件
```

#### 核心文件说明 

app/page.tsx: 网站首页，对应路径 /

app/layout.tsx: 根布局，包含所有页面共享的结构

app/globals.css: 全局CSS样式

app/[目录名]/page.tsx: 子页面，对应路径 /[目录名]

#### Pages Router 结构（不推荐） 

虽然不再是推荐方式，但你可能在许多现有项目中看到这种结构：

```
my-nextjs-project/
├── pages/               # 页面目录
│   ├── _app.js          # 全局App组件
│   ├── _document.js     # 自定义文档
│   ├── index.js         # 首页
│   └── about.js         # 关于页面
├── styles/              # 样式目录
├── public/              # 静态资源目录
└── ...                  # 其他配置文件
```

对于新项目，建议使用App Router（app/目录）结构，它提供了更好的性能和更丰富的功能。

### 2. 文件系统路由：自动URL映射 

Next.js的一个核心特点是文件系统路由。这意味着你的项目文件结构直接决定了网站的URL路径，不需要额外的路由配置。

#### 基本路由规则 

在App Router中，路由遵循以下规则：

1 文件命名：特殊文件有特定用途：

page.tsx: 定义路由的主要内容

layout.tsx: 定义共享UI

loading.tsx: 加载UI

error.tsx: 错误UI

not-found.tsx: 404 UI

2 目录映射：目录名直接映射到URL路径：

```powershell
app/page.tsx              → /
app/about/page.tsx        → /about
app/blog/page.tsx         → /blog
app/blog/post/page.tsx    → /blog/post
```

3 嵌套路由：子目录创建嵌套路由，共享父布局：

```powershell
app/layout.tsx            → 应用于所有页面
app/blog/layout.tsx       → 应用于所有/blog/*页面
```

#### 示例 

一个简单网站的文件结构：

```powershell
app/
├── page.tsx         # 首页 (/)
├── layout.tsx       # 根布局
├── about/
│   └── page.tsx     # 关于页 (/about)
└── blog/
    ├── page.tsx     # 博客列表页 (/blog)
    └── [slug]/
        └── page.tsx # 博客文章页 (/blog/article-1)
```

### 3. 创建页面和页面导航 

#### 创建基本页面 

在Next.js中创建新页面很简单：

1 在app目录下创建新文件夹

2 在该文件夹中创建page.tsx文件

3 添加基本内容：

```jsx
export default function AboutPage() {
  return (
    <div>
      <h1>关于我们</h1>
      <p>这是一个简单的Next.js示例页面。</p>
    </div>
  );
}
```

现在可以通过访问/about来查看这个页面。

#### 页面间导航 

Next.js提供了Link组件用于页面导航，它比普通HTML的<a>标签更高效：

```jsx
import Link from 'next/link';

export default function HomePage() {jsx
  return (
    <div>
      <h1>欢迎来到我的网站</h1>
      <nav>
        <ul>
          <li>
            <Link href="/">首页</Link>
          </li>
          <li>
            <Link href="/about">关于</Link>
          </li>
          <li>
            <Link href="/blog">博客</Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}
```

Link组件优点：

- 客户端导航，无需完全刷新页面
- 自动代码分割，只加载需要的代码
- 预加载可见链接的页面，提升速度

#### 创建共享导航组件 

对于多个页面共享的导航栏，最好创建一个可复用组件：

```jsx
// components/Navbar.jsx
import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between">
        <Link href="/" className="font-bold">我的网站</Link>
        <ul className="flex space-x-4">
          <li><Link href="/">首页</Link></li>
          <li><Link href="/about">关于</Link></li>
          <li><Link href="/blog">博客</Link></li>
        </ul>
      </div>
    </nav>
  );
}
```

在布局文件中使用导航组件：

```jsx
// app/layout.jsx
import Navbar from '@/components/Navbar';
import './globals.css';

export default function RootLayout({ children }) {
  return (
    <html lang="zh">
      <body>
        <Navbar />
        <main className="container mx-auto p-4">
          {children}
        </main>
        <footer className="text-center p-4">
          © 2025 我的网站
        </footer>
      </body>
    </html>
  );
}
```

### 4. 静态资源管理 

Next.js的public目录用于存放静态资源，如图片、字体、图标等，这些文件可以直接通过URL路径访问。

#### 使用静态资源 

图片：

```powershell
public/
└── images/
    ├── logo.png
    └── banner.jpg
```

在代码中引用：

```jsx
// 使用普通img标签
<img src="/images/logo.png" alt="Logo" />

// 使用Next.js优化的Image组件（推荐）
import Image from 'next/image';

<Image 
  src="/images/banner.jpg" 
  alt="Banner" 
  width={800} 
  height={400} 
  className="rounded"
/>
```

#### Next.js Image组件优势 

next/image组件相比普通<img>标签有许多优势：

- 自动优化图像大小
- 延迟加载（图像只在进入视口时加载）
- 防止布局偏移(CLS)
- 支持现代图像格式

#### 其他静态资源 

- 字体文件：放在public/fonts/
- 网站图标：public/favicon.ico
- 网站清单：public/manifest.json（用于PWA）

### 5. 高级路由特性 

#### 动态路由 

动态路由允许你创建基于变量的路径，例如博客文章页面：

```jsx
app/blog/[slug]/page.jsx → /blog/hello-world, /blog/next-js-tutorial
```

实现方式：

```jsx
// app/blog/[slug]/page.jsx
export default function BlogPost({ params }) {
  // params.slug 包含URL中的动态部分
  return (
    <div>
      <h1>博客文章: {params.slug}</h1>
      <div className="content">
        {/* 文章内容 */}
        <p>这是文章内容...</p>
      </div>
    </div>
  );
}
```

#### 路由组和布局组 

你可以使用括号命名的文件夹来创建路由组，这些不会影响URL路径，但可以组织代码：

```jsx
app/(marketing)/page.jsx → /
app/(marketing)/about/page.jsx → /about
app/(dashboard)/dashboard/page.jsx → /dashboard
```

这对于共享布局特别有用，例如不同区域的页面可能有不同的布局：

```jsx
// app/(dashboard)/layout.jsx
export default function DashboardLayout({ children }) {
  return (
    <div className="flex">
      <div className="w-64 bg-gray-100 min-h-screen p-4">
        {/* 侧边栏导航 */}
        <nav>
          <ul>
            <li>仪表盘</li>
            <li>设置</li>
            <li>用户</li>
          </ul>
        </nav>
      </div>
      <div className="flex-1 p-6">{children}</div>
    </div>
  );
}
```

#### 404页面和错误处理 

创建自定义404页面：

```jsx
// app/not-found.jsx
import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="text-center py-10">
      <h1 className="text-4xl font-bold">404</h1>
      <p className="text-xl mt-4">找不到这个页面</p>
      <p className="mt-6">
        <Link href="/">返回首页</Link>
      </p>
    </div>
  );
}
```

错误处理页面：

```jsx
// app/error.jsx
'use client';

export default function Error({ error, reset }) {
  return (
    <div className="text-center py-10">
      <h1 className="text-2xl">出错了</h1>
      <p className="mt-4">{error.message}</p>
      <button
        onClick={reset}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
      >
        重试
      </button>
    </div>
  );
}
```

以上示例展示了如何使用Next.js创建基本的页面结构和路由，这些知识可以作为构建各种应用的基础。

### 6. 服务端组件与客户端组件 

Next.js 13引入了React的服务器组件，这是理解现代Next.js应用的关键概念。

#### 服务端组件 (默认) 

在App Router中，所有组件默认都是服务端组件，除非你明确指定它们是客户端组件。

服务端组件的特点：

- 在服务器上渲染，将HTML发送给浏览器
- 不包含任何JavaScript交互代码
- 可以直接访问服务器资源（数据库、文件系统等）
- 不能使用浏览器API、事件处理器或React hooks

适用场景：

- 数据获取和处理
- 访问服务器资源
- 保持敏感信息在服务器
- 大型依赖库仅在服务器加载，减小前端包大小

一个简单的服务端组件示例：

```jsx
// app/products/page.jsx - 服务端组件
import ProductCard from '@/components/ProductCard';

async function getProducts() {
  const res = await fetch('https://api.example.com/products');
  return res.json();
}

export default async function ProductsPage() {
  // 直接在服务端组件中获取数据
  const products = await getProducts();
  
  return (
    <div>
      <h1>产品列表</h1>
      <div className="grid grid-cols-3 gap-4">
        {products.map(product => (
          <ProductCard 
            key={product.id}
            name={product.name}
            price={product.price}
            image={product.image}
          />
        ))}
      </div>
    </div>
  );
}
```

#### 客户端组件 

要创建客户端组件，需要在文件顶部添加'use client'指令：

```jsx
// components/Counter.jsx
'use client'

import { useState } from 'react';

export default function Counter() {
  // 在客户端组件中使用状态和事件处理
  const [count, setCount] = useState(0);
  
  return (
    <div className="p-4 border rounded">
      <p className="text-xl">当前计数：{count}</p>
      <button 
        onClick={() => setCount(count + 1)}
        className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
      >
        增加
      </button>
    </div>
  );
}
```

客户端组件的特点：

- 在浏览器中运行
- 可以使用状态、效果和浏览器API
- 支持交互性和事件处理
- 增加客户端JavaScript包的大小

适用场景：

- 交互功能（表单、计数器等）
- 使用浏览器API（localStorage、navigator等）
- 使用React hooks（useState、useEffect等）
- 基于用户事件的UI更新

#### 组件组合模式 

一个常见的模式是：服务端组件获取数据，然后将数据传递给客户端交互组件：

```jsx
// EditForm.jsx - 客户端组件
'use client'

import { useState } from 'react';

export default function EditForm({ initialData, onSave }) {
  const [formData, setFormData] = useState(initialData);
  
  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      onSave(formData);
    }}>
      <input 
        value={formData.name}
        onChange={(e) => setFormData({...formData, name: e.target.value})}
      />
      <button type="submit">保存</button>
    </form>
  );
}

// app/product/[id]/edit/page.jsx - 服务端组件
import EditForm from '@/components/EditForm';
import { getProductById } from '@/lib/data';

export default async function EditProductPage({ params }) {
  // 在服务端获取数据
  const product = await getProductById(params.id);
  
  return (
    <div>
      <h1>编辑产品</h1>
      {/* 将服务端获取的数据传递给客户端组件 */}
      <EditForm initialData={product} />
    </div>
  );
}
```

这种模式让你可以同时利用服务端组件的数据获取能力和客户端组件的交互能力。

### 7. 组件的创建与使用 

#### 基础组件开发 

让我们创建一个基础卡片组件：

```jsx
// components/Card.jsx
import Image from 'next/image';

export default function Card({ title, description, imageUrl }) {
  return (
    <div className="bg-white border rounded-lg shadow-sm p-4">
      {imageUrl && (
        <div className="mb-4">
          <Image 
            src={imageUrl} 
            alt={title} 
            width={300} 
            height={200} 
            className="rounded"
          />
        </div>
      )}
      
      <h3 className="text-lg font-medium mb-2">{title}</h3>
      
      <p className="text-gray-600 text-sm">
        {description}
      </p>
    </div>
  );
}
```

#### 组件的复用和组合 

组件的强大之处在于可以组合形成更复杂的UI：

```jsx
// components/CardGrid.jsx
import Card from './Card';

export default function CardGrid({ items }) {
  if (items.length === 0) {
    return <p>没有找到任何项目</p>;
  }
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {items.map(item => (
        <Card
          key={item.id}
          title={item.title}
          description={item.description}
          imageUrl={item.imageUrl}
        />
      ))}
    </div>
  );
}
```

#### props和children 

React组件的两个核心概念：

- props：传递给组件的数据，类似函数参数
- children：组件标签之间的内容，允许组件包裹其他元素

```jsx
// 使用children创建一个布局组件
// components/Panel.jsx
export default function Panel({ title, children, footer }) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="px-6 py-4 bg-gray-50 border-b">
        <h3 className="text-lg font-medium">{title}</h3>
      </div>
      
      <div className="p-6">
        {children}
      </div>
      
      {footer && (
        <div className="px-6 py-3 bg-gray-50 border-t">
          {footer}
        </div>
      )}
    </div>
  );
}

// 使用Panel组件
import Panel from '@/components/Panel';
import Button from '@/components/Button';

export default function AboutPage() {
  return (
    <Panel 
      title="关于我们"
      footer={<Button text="了解更多" />}
    >
      <p>
        我们是一家专注于提供高质量web服务的公司。
        我们的团队由经验丰富的开发者和设计师组成。
      </p>
    </Panel>
  );
}
```

### 4. 组件的组织与管理 

#### 组件文件夹结构 

一个合理的组件结构：

```jsx
my-project/
├── app/                  # 页面和路由
│   ├── page.jsx          # 首页
│   ├── about/            # 关于页
│   │   └── page.jsx
│   └── products/         # 产品页
│       └── page.jsx
├── components/           # 所有共享组件
│   ├── ui/               # 基础UI组件
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   └── Card.jsx
│   ├── layout/           # 布局相关组件
│   │   ├── Navbar.jsx    # 导航栏
│   │   └── Footer.jsx    # 页脚
│   └── features/         # 功能相关组件
│       ├── ProductList.jsx
│       └── ContactForm.jsx
└── lib/                  # 工具函数和服务
```

这种结构有几个优点：

- 清晰区分不同类型的组件
- 容易找到特定组件
- 支持团队协作和代码复用

#### 组件命名约定 

良好的命名约定可以使项目更易于理解：

- 组件文件使用PascalCase：Button.jsx, NavBar.jsx
- 组件函数名与文件名相同：export default function Button() {...}

关联组件可以放在同一文件夹：

```jsx
components/products/
├── ProductCard.jsx
├── ProductList.jsx
└── ProductFilter.jsx
```

#### 特定页面组件vs共享组件 

对于只在特定页面使用的组件，可以将它们放在页面目录中：

```jsx
app/dashboard/
├── page.jsx              # 仪表盘页面
└── components/           # 仅仪表盘页面使用的组件
    ├── DashboardStats.jsx
    └── ActivityFeed.jsx
```

这种方式使页面和其依赖的组件保持在一起，有助于维护。

## 五、supabase

一定开启 RLS，结合 Supabase Auth 用户身份认证，保证每一行数据仅对授权用户可见。

#### suapbase实时功能 

进入你的数据表中，在右上角打开Realtime，确保处于打开on的状态。

我们可以创建一个 Supabase Realtime 频道并订阅 数据库表的变化。

#### 第三方登录

邮件有速率限制，所以我们开启 [MTP](https://supabase.com/dashboard/project/umenqkbhotlvskxgjrmz/auth/smtp)。

> ##### Set up custom SMTP
>
> You’re using the built-in email service. This service has rate limits and is not meant to be used for production apps. [Learn more](https://supabase.com/docs/guides/platform/going-into-prod#auth-rate-limits)

另外，开发时我们设置好的重定向的 URL 为 localhost ，但部署上线的时候就要从那转向我们自己的域名或者vercel给我们分配好的域名。点击这里设置： [Site URL](https://supabase.com/dashboard/project/umenqkbhotlvskxgjrmz/auth/url-configuration)

Redirect URLs 也要设置为类似于这样的 `https://www.myapp.com/auth/callback` 形式。因为Google只能将用户重定向到事先在Google开发者后台注册好的、且在 [Redirect URLs](https://supabase.com/dashboard/project/umenqkbhotlvskxgjrmz/auth/url-configuration) 中配置好的URL。

## 六、chrome 插件开发

[chrome-extension-boilerplate-react-vite](https://github.com/Jonghakseo/chrome-extension-boilerplate-react-vite)

我们尽量使用模板开发，这样别人已经解决了兼容性问题。

我们尽量使用 `pnpm` 包管理工具。npm 实在是有太多的遗留问题了。

```bash
npm install -g pnpm@latest-10
```

### 项目目录结构

```
chrome-extension/     ← 扩展本身的核心文件
  ├── manifest.ts     ← 生成 manifest.json（扩展的配置清单）
  ├── src/background/← 后台服务脚本
  └── public/         ← 图标等静态资源

pages/                ← 扩展的各个"页面"
  ├── content/        ← 注入到网页的脚本（可在页面控制台看到）
  ├── content-ui/      ← 注入到网页的 React 组件
  ├── popup/          ← 点击扩展图标弹出的窗口
  ├── options/        ← 右键扩展 → 选项 打开的页面
  ├── new-tab/        ← 覆盖新标签页
  ├── side-panel/     ← 侧边栏面板
  ├── devtools/       ← 开发者工具面板
  └── ...

packages/             ← 共享工具包
  ├── i18n/           ← 国际化（多语言支持）
  ├── storage/        ← 存储助手
  ├── env/            ← 环境变量
  └── ...
```

### 开发

- 我们可以通过 @pages\popup\src\Popup.tsx 提出我们的需求。
- 想修改侧边栏就 @pages\side-panel\src\SidePanel.tsx

- 如果需要对页面的元素做出读取，修改等操作，最好使用类选择器等元素选择器选择到其元素。这样定位更加精准。

- 如果我们想已进入该网页就做出一些动作，而不用主动执行，chrome 为我们提供了 content 目录。在这里面注入脚本。all 目录下对所有网址生效，其余则对指定域名生效。这个配置在 manifest.json下面。

```ts
// chrome-extension\manifest.ts

// 生成 manifest.json（扩展的配置清单）
// manifest.json 是 Chrome/Firefox 扩展的核心配置文件，定义扩展的所有行为和结构。
import { readFileSync } from 'node:fs';
import type { ManifestType } from '@extension/shared';

const packageJson = JSON.parse(readFileSync('./package.json', 'utf8'));

/**
 * @prop default_locale
 * if you want to support multiple languages, you can use the following reference
 * https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Internationalization
 *
 * @prop browser_specific_settings
 * Must be unique to your extension to upload to addons.mozilla.org
 * (you can delete if you only want a chrome extension)
 *
 * @prop permissions
 * Firefox doesn't support sidePanel (It will be deleted in manifest parser)
 *
 * @prop content_scripts
 * css: ['content.css'], // public folder
 */
const manifest = {
  manifest_version: 3,
  default_locale: 'en',
  name: '小狗爱摸鱼',
  browser_specific_settings: {
    gecko: {
      id: 'example@example.com',
      strict_min_version: '109.0',
    },
  },
  version: packageJson.version,
  description: '__MSG_extensionDescription__',
  host_permissions: ['https://www.zhihu.com/*', 'https://zhihu.com/*'],
  permissions: ['storage', 'scripting', 'tabs', 'notifications', 'sidePanel'],
  options_page: 'options/index.html',
  background: {
    service_worker: 'background.js',
    type: 'module',
  },
  action: {
    default_popup: 'popup/index.html',
    default_icon: 'icon-34.png',
  },
  icons: {
    '128': 'icon-128.png',
  },
  content_scripts: [
    {
      matches: ['https://www.zhihu.com/question/*'],
      js: ['content/all.iife.js'],
    },
    {
      matches: ['https://www.zhihu.com/question/*'],
      css: ['content.css'],
    },
  ],
  devtools_page: 'devtools/index.html',
  web_accessible_resources: [
    {
      resources: ['*.js', '*.css', '*.svg', 'icon-128.png', 'icon-34.png'],
      matches: ['https://www.zhihu.com/*'],
    },
  ],
  side_panel: {
    default_path: 'side-panel/index.html',
  },
} satisfies ManifestType;

export default manifest;

```

其中

```ts
指定知乎：：
content_scripts: [
{
  matches: ['https://www.zhihu.com/question/*'],
  js: ['content/all.iife.js'],
},
{
  matches: ['https://www.zhihu.com/question/*'],
  css: ['content.css'],
},
],
      
      
原来是这样：：：      
{
    matches: ['http://*/*', 'https://*/*', '<all_urls>'],
    js: ['content/all.iife.js'],
},
{
    matches: ['http://*/*', 'https://*/*', '<all_urls>'],
    js: ['content-ui/all.iife.js'],
},
```

指定了对知乎问题答案这个页面生效。

插件名称， @manifest.js这个文件。

```
@manifest.js 修改插件的名字叫做： 小狗爱摸鱼
```

插件的描述，@packages/i18n/locales/en/messages.json这个文件

```
@messages.json 修改这个插件的描述：用来一键对知乎进行换装，方便摸鱼！
```

### 构建

```
pnpm run build
```

### 上架

https://developer.chrome.com/docs/webstore/publish?hl=zh-cn，5美金

## 七、支付

国内可以使用 [z-pay](https://z-pay.cn/) 无需营业执照，但是有开户费用和手续费提成。

支付的两个关键接口：

1. 用户输入商品的信息，比如说要有多少个商品、商品名称、金额这些信息之后，发送到服务器。服务器先生成一条待支付的订单信息，放到数据库，随后调用z-pay API 支付接口返回支付二维码或者z-pay的收银台，也可以直接重定向到z-pay在收银台。
2. 支付结果通知。服务器异步询问 z-pay 支付结果
