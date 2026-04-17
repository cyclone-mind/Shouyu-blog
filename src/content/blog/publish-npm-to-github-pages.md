---
title: '发布 npm 到 github pages'
description: 'npm 包的发布'
pubDate: '2024-03-12'
authors:
  - shouyu
toc: true
tags:
  - GitHub
  - npm
  - 前端
---

## 摘要

npm 包的发布

## 打包

```js
# index.js
console.log("hello, world!")
```

```bash
npm init
```

`npm init`命令会生成一个`package.josn`文件，例如：

```json
{
  "name": "@cyclonemind/package_exemple",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "test": "exit 0"
  },
  "author": "",
  "license": "ISC",
  "description": "",
}
```

## 推送的 action

通过 github actions 实现 【发布一个 release 时将 npm 包推送到 githubpages 的服务器】的功能。我们建立 一个 release.yml 文件：

```yaml
# release.yml
name: Node.js Package

on:
   release:
    types: [created]

jobs:

    publish-gpr:

      runs-on: ubuntu-latest

      permissions:
        contents: read
        packages: write


      steps:
        - uses: actions/checkout@v4

        - uses: actions/setup-node@v4
          with:
            node-version: '16'
            registry-url: 'https://npm.pkg.github.com/' # 生成必要的 .npmrc 文件，配置认证信息设置环境变量，这个配置会影响后续所有的 npm 命令，包括：npm ci、npm publish

        - run: npm ci

        - run: npm publish 
 
          env:
            NODE_AUTH_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

实际上 actions 中的虚拟机中生成的`.npmrc`文件里面类似于：

```plaintext
# .npmrc
//npm.pkg.github.com/:_authToken=${NODE_AUTH_TOKEN}
registry=https://npm.pkg.github.com/
always-auth=true
```

这一步完成后在`package.josn`中增加 publishconfig的配置信息：

```json
# package.josn
{
  "name": "@cyclonemind/package_exemple",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "test": "exit 0"
  },
  "author": "",
  "license": "ISC",
  "description": "",
  "publishConfig": {"@cyclonemind:registry": "https://npm.pkg.github.com"},
}
```

随后在 github 中创建一个 release， release.yml 文件就会执行。一个 package 就建立完成：

一般来说使用别人发布的包时都在 package.json 中写好

```json
{
  ...
  "dependencies": {
    "@cyclonemind/package_exemple": "1.0.0"
  },
  ...
}
```

正常情况下，这时使用`npm install`安装包只会去 npm 的官方仓库下载包或者用户自己设置的仓库下载包。我们可以在项目中增加`.npmrc`文件来设置项目的 仓库配置信息：

::: warning

这里说的项目不是这个包项目，而是其他任意一个需要使用这个包的项目！

:::

在其他项目的根目录下增加

```plaintext
# .npmrc
@cyclonemind:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=YOUR _authToken
```

这里的 _authToken 是使用者自己的，在 Settings -> Developer Settings -> Personal acess tokens -> Tokens(classic) -> Generate new token -> Generate new token(classic) -> 勾选上与 package 有关的选项即可得到_authToken>。

然后就可以正常`npm install`啦