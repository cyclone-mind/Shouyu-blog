---
title: 'Docker快速实践'
description: 'Docker容器化技术快速入门，包括安装、核心命令、网络模式和Docker Compose'
pubDate: '2025-12-21'
authors:
  - shouyu
toc: true
tags:
  - Web开发
  - 容器
  - Docker
---

## 摘要
docker 实践

## 正文
> 📺 内容来源：本文内容根据 B站UP主 40分钟的Docker实战攻略，一期视频精通Docker 整理总结而来。

## 概述

Docker是目前最成熟、高效的软件部署技术。它通过容器化技术为应用程序提供独立的运行环境，每个环境就是一个容器。运行容器的计算机被称为宿主机。Docker容器与虚拟机的最大区别在于，Docker容器之间共享同一个系统内核，而每个虚拟机都包含一个操作系统的完整内核。因此，Docker容器比虚拟机更轻、更小，启动速度更快。

Docker的另一个核心概念是**镜像**。镜像是容器的母板。我们可以将镜像类比为软件安装包，而容器则是安装出来的软件。例如，Docker镜像就像是模具，而容器就像是糕点。我们可以使用一个模具制作出多个糕点，也可以将模具分享给其他人使用。Docker仓库就是用来存放和分享镜像的地方。每个人都可以将自己的镜像上传到仓库中，其他人则可以下载并使用。Docker的官方仓库就是Docker Hub，上面存储了许多人分享的Docker镜像。

## 一、Docker的安装

Docker通常基于Linux的容器化技术。在Windows和Mac电脑上，Docker会虚拟一个Linux子系统来运行。因此，Linux系统是Docker的最佳实战环境。

### 1. 在Linux系统上安装Docker

* 访问 get.docker.com

* 复制并执行该网站上提供的安装步骤中的第一步和第四步命令

* 注意在Linux系统中，如果您的用户不是root用户（例如Ubuntu用户），需要在所有Docker命令前面加上 sudo 以管理员权限执行

### 2. 在Windows系统上安装Docker

1. 在任务栏搜索功能中，点击"启用或关闭Windows功能"

1. 勾选 Wor Machine Platform (或"虚拟机平台") 和 适用于Linux的Windows系统 (即 WSL)

1. 按照提示重启电脑

1. 重启后，打开命令提示符（cmd），以管理员身份运行

1. 执行命令：wsl --set-default-version 2，将WSL默认版本设为2

1. 执行命令：wsl --update 安装WSL。如果处于国内网络，建议添加 --web-download 参数以减少下载失败

1. 从Docker Desktop官方地址下载并安装Docker Desktop。安装过程通常只需一路点击"下一步"

1. 注意在Windows上使用Docker时，Docker Desktop软件必须一直保持开启状态

1. 测试安装：在Windows终端中输入 docker --version，如果能打印出版本号则表示安装成功

### 3. 在Mac系统上安装Docker

* 根据您的Mac芯片（Intel或Apple Silicon）下载对应的Docker Desktop安装包，然后安装即可。这是最简单的安装方式

## 二、核心Docker命令详解

尽管Docker Desktop提供了可视化界面，但命令行在各个操作系统上具有一致性和更强的通用性，因此我们将主要通过命令行进行讲解。

### 1. 镜像管理命令

#### docker pull [镜像名称]

用于从仓库下载镜像。

一个完整的镜像名称通常包含四部分：`[registry地址]/[命名空间]/[镜像名称]:[标签名]`

* Registry地址：例如 docker.io（Docker Hub的官方仓库），官方仓库的地址可以省略

* 命名空间：通常是镜像作者的用户名或组织名。library 是Docker官方仓库的命名空间，官方镜像可以省略命名空间

* 镜像名称：例如 nginx

* 标签名：即版本号，例如 :latest（最新版，可省略）或 :1.28.0

**示例**：

```bash
docker pull nginx                    # 从Docker官方仓库下载最新版nginx镜像
docker pull quay.io/n8n/n8n         # 从私有仓库quay.io下载n8n用户的n8n镜像
```

**解决国内网络下载问题**：

* Linux：编辑 /etc/docker/daemon.json 文件，添加或修改 registry-mirrors 配置，然后重启Docker服务

* Windows/Mac：打开Docker Desktop设置，在"Docker Engine"中编辑JSON配置文件，添加 "registry-mirrors" 配置，然后"Apply & Restart"

#### docker images

列出所有已下载的Docker镜像。

#### docker rmi [镜像名称或ID]

删除镜像。

#### --platform [CPU架构]

`docker pull`命令的参数，用于拉取特定CPU架构的镜像。

* 默认情况下，Docker会自动选择最适合当前宿主机CPU架构的镜像

* 注意Mac电脑的Docker Desktop可以通过QEMU模拟X86_64指令集来兼容部分AMD64镜像，但可能带来兼容性问题或性能开销

### 2. 容器生命周期管理与交互命令

#### docker run [镜像名称或ID]

使用指定镜像创建并运行一个新容器。

* 如果本地不存在该镜像，Docker会自动先拉取一份，然后再创建并运行容器

#### docker run -d [镜像名称]

以分离模式（detached mode）在后台运行容器，不占用当前终端。

#### docker ps

查看正在运行的容器（process status的缩写）。

#### docker ps -a

查看所有容器，包括正在运行的和已停止的。

#### docker stop [容器ID或名称]

停止一个正在运行的容器。

#### docker start [容器ID或名称]

启动一个已停止的容器。

* 使用 stop 和 start 时，之前 run 时设置的端口映射、挂载卷、环境变量等参数无需重新输入，Docker已记录并保存

#### docker rm [容器ID或名称]

删除一个容器。

* 删除正在运行的容器需要添加 -f 参数进行强制删除

* 提示：docker rm 删除容器，docker rmi 删除镜像

#### docker inspect [容器ID或名称]

检查容器的详细信息，包括其启动参数、端口映射、挂载卷等。

#### docker create [镜像名称或ID]

仅创建容器但不立即启动。若要启动，仍需使用`docker start`命令。

#### docker logs [容器ID或名称]

查看容器的日志。

#### docker logs -f [容器ID或名称]

滚动实时查看容器日志（follow模式）。

#### docker exec [容器ID或名称] [Linux命令]

在容器内部执行Linux命令。

**示例**：

```bash
docker exec [容器ID] ps -ef                    # 查看容器内部进程
docker exec -it [容器ID或名称] /bin/bash       # 进入一个正在运行的容器，获取一个交互式命令行环境
```

* 容器内部表现得像一个独立的Linux系统，你可以在其中执行Linux命令、查看文件系统、管理进程等

* 注意Docker镜像通常为了减小体积，内部可能缺失常用工具（如vi）。你可能需要在容器内自行安装，例如对于Debian系的镜像，可以使用 apt update 和 apt install [工具名]

### 3. docker run命令的重要参数

#### -p [宿主机端口]:[容器内端口]

端口映射 (port mapping)。

* 由于容器网络与宿主机隔离，此参数用于将宿主机的端口转发到容器内的端口，从而允许从宿主机访问容器内的服务

* 顺序：先外后内，即宿主机端口在前，容器端口在后

* 示例：docker run -p 80:80 nginx 将宿主机的80端口映射到容器内的80端口

#### -v [宿主机目录]:[容器内目录]

挂载卷 (volume)。

* 将宿主机的文件目录与容器内的文件目录进行绑定，实现数据共享和持久化保存

* 容器内对该目录的修改会影响宿主机，反之亦然

* 挂载卷的最大作用是数据持久化，因为容器被删除时，容器内的数据也会被删除。通过挂载卷，数据可以保存在宿主机上

**绑定挂载**：直接在`docker run`命令中指定宿主机目录。如果宿主机目录是空的，它会覆盖容器内的对应目录。

**命名卷挂载**：

```bash
docker volume create [卷名称]                    # 创建一个命名卷
docker run -v [卷名称]:[容器内目录] [镜像名称]    # 在docker run命令中使用卷名称
docker volume inspect [卷名称]                   # 查看命名卷在宿主机的真实存储路径
docker volume list                              # 列出所有已创建的挂载卷
docker volume remove [卷名称]                    # 删除一个挂载卷
docker volume prune                             # 删除所有没有被任何容器使用的挂载卷
```

* 特点：命名卷在第一次使用时，Docker会将容器的文件夹同步到命名卷中进行初始化。绑定挂载没有此功能

#### -e [环境变量名]=[值]

传递环境变量 (environment)。

* 用于向容器内部传递配置信息，例如数据库的账号和密码

* 如需了解容器支持的环境变量，可查阅其在Docker Hub上的文档

* 示例：docker run -e MONGO_INITDB_ROOT_USERNAME=mosh -e MONGO_INITDB_ROOT_PASSWORD=password ...

#### --name [容器名称]

为容器指定一个自定义的、在宿主机上唯一的名称。

* 这个名称与容器ID功能等价，但更易于记忆和管理

#### -it --rm

通常一起使用，用于临时调试容器。

* -it：让你的控制台进入容器进行交互式操作

* --rm：确保容器在停止时自动删除

* 示例：docker run -it --rm alpine /bin/sh

#### --restart [策略]

配置容器停止时的重启策略。

* always：只要容器停止，无论何种原因（包括内部崩溃或宿主机断电），都会立即尝试重启

* unless-stopped：与 always 类似，但如果容器是手动停止的，就不会尝试重启。这在生产环境中非常实用，可以在意外停止时自动重启，而手动停止则保持停止状态

## 三、Docker网络模式

Docker容器化技术利用了Linux内核的Cgroups（限制和隔离进程资源使用）和Namespaces（隔离进程资源视图）两大功能。从本质上讲，容器是一个特殊的进程，但其内部看起来就像一个独立的操作系统。

Docker提供了多种网络模式：

### 1. Bridge（桥接模式）

* 这是默认的网络模式。所有容器默认都连接到这个网络，并分配一个内部IP地址（通常是 172.17.x.x 开头）

* 在同一个内部网络中，容器可以通过内部IP地址互相访问。宿主机网络与容器网络是隔离的

**自定义子网**：

```bash
docker network create [子网名称]                    # 创建自定义的Bridge模式子网
docker run --network [子网名称] [镜像名称]          # 在运行容器时指定其加入某个子网
docker network list                               # 列出所有Docker网络
docker network remove [子网名称]                   # 删除自定义的子网
```

* 优点：同一子网内的容器可以互相通信，甚至可以通过容器名称互相访问（利用Docker内部的DNS机制），而无需知道对方的IP地址

* 注意默认网络（bridge, host, none）不能被删除

### 2. Host（主机模式）

* 容器直接共享宿主机的网络命名空间

* 容器直接使用宿主机的IP地址，并且无需进行端口映射 (-p 参数)。容器内的服务直接运行在宿主机的端口上

* 通过宿主机的IP和端口即可直接访问容器服务

* 示例：docker run --network host nginx

* 此模式可以解决一些棘手的网络问题

### 3. None（无网络模式）

* 容器不连接任何网络，即不联网

## 四、Dockerfile：构建自定义镜像

Dockerfile是制作Docker镜像的"图纸"。它是一个没有后缀名的文件（文件名必须是Dockerfile，D大写），详细列出了镜像的构建步骤。

### 1. Dockerfile常用指令

#### FROM [基础镜像]

Dockerfile的第一行，指定镜像基于哪个基础镜像构建。

**示例**：`FROM python:3.13-slim`

#### WORKDIR [目录]

设置镜像内部的工作目录。后续的命令（如COPY, RUN）都会在该目录下执行。

**示例**：`WORKDIR /app`

#### COPY [源路径] [目标路径]

将宿主机（构建上下文）的文件拷贝到镜像内部。

**示例**：`COPY . .`，第一个`.`代表宿主机的当前目录，第二个`.`代表镜像内的当前工作目录

#### RUN [命令]

在镜像构建过程中执行的命令。通常用于安装依赖、编译代码等。

**示例**：`RUN pip install -r requirements.txt`

#### EXPOSE [端口]

声明镜像提供的服务端口。这是一个声明性指令，仅作提示，不强制端口映射。实际使用时仍需依靠`docker run -p`进行端口映射。

#### CMD [命令]

容器启动时的默认执行命令。当容器启动时，容器内部会自动执行此命令。一个Dockerfile中只能有一个CMD指令。

**示例**：`CMD ["python", "main.py"]`。建议使用数组形式，避免空格问题。

#### ENTRYPOINT

与CMD类似，但优先级更高，且不易被覆盖。

### 2. 构建与推送镜像

#### 构建镜像

```bash
docker build -t [镜像名称]:[版本号] .    # 在当前目录（.）下根据Dockerfile构建镜像。-t用于给镜像打标签（名称和版本号）
```

**示例**：`docker build -t my-python-app:1.0 .`

#### 推送镜像到Docker Hub

1. docker login：登录Docker Hub账户。按照提示在浏览器中完成认证

1. docker tag [本地镜像名称]:[版本号] [你的用户名]/[镜像名称]:[版本号]：为镜像打上带有你用户名的标签，这是推送到Docker Hub的必要步骤

1. docker push [你的用户名]/[镜像名称]:[版本号]：将镜像推送到Docker Hub

## 五、Docker Compose：轻量级容器编排

当一个完整的应用包含多个模块（如前端、后端、数据库）时，将每个模块打包成独立的容器是最佳实践。然而，管理多个容器会增加使用成本。Docker Compose是应对这种场景的轻量级容器编排技术。它使用YAML文件来管理多个容器的创建、配置和协同工作。

### 1. Docker Compose文件结构

* Compose文件可以简单理解为将多个 docker run 命令按照特定格式组织到一个YAML文件中

* 最顶层元素是 services

* 每个服务（service）对应一个容器

* Compose文件中的服务名称，对应于 docker run 命令中的容器名称 (--name)

**常用配置项与docker run参数对应关系**：

* image：镜像名称 (docker run [image])

* environment：环境变量 (-e)

* volumes：挂载卷 (-v)

* ports：端口映射 (-p)

**网络**：Docker Compose会自动为每个Compose文件创建一个子网。同一个Compose文件中定义的所有容器会自动加入到这个子网中，并可以通过服务名称互相访问。

**depends_on**：用于定义容器的启动顺序。例如，`depends_on: - db`表示当前服务依赖db服务，会先启动db容器。

在AI时代，你可以直接向AI描述你的Docker容器需求，让它生成等价的Docker Compose文件。

### 2. Docker Compose常用命令

```bash
docker compose up                    # 启动Compose文件中定义的所有服务（容器）
docker compose up -d                 # 在后台启动所有服务
docker compose down                  # 停止并删除Compose文件定义的所有服务及相关网络
docker compose stop                  # 只停止服务，但不删除容器
docker compose start                 # 启动通过docker compose stop命令停止的服务
docker compose -f [文件名] up        # 如果Compose文件使用了非标准名称（默认为docker-compose.yml），需要使用-f参数指定文件名
```

## 总结

本篇攻略带你了解了Docker的核心概念，包括容器、镜像和镜像仓库。我们学习了如何在主流操作系统上安装Docker，掌握了`docker pull`、`docker run`等基础镜像和容器管理命令，以及端口映射、挂载卷、环境变量等重要参数。此外，我们还探讨了Docker的几种网络模式，了解了如何使用Dockerfile构建自定义镜像并推送到Docker Hub。最后，我们深入了解了轻量级容器编排技术Docker Compose，学习了如何使用它来管理复杂的多容器应用。掌握这些干货，你就能自信地使用Docker进行软件部署和管理了！ 🚀