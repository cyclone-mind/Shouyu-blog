---
title: '上海弈智交互初面'
description: '上海弈智交互初面'
date: '2026-04-17'
authors:
  - shouyu
toc: true
tags:
  - 面试
---


## 1. Agent 框架代码 Review

### 选定框架与代码段

我选择了 [claude code] 的 [tool] 模块，核心代码位于 `services/tools/toolOrchestration.t`。

### 代码核心逻辑

```typescript
// services/tools/toolOrchestration.ts — 工具执行编排
function getMaxToolUseConcurrency(): number {
  return parseInt(process.env.CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY || '', 10) || 10
}

...

function partitionToolCalls(toolUseMessages, toolUseContext): Batch[] {
  return toolUseMessages.reduce((acc, toolUse) => {
    const tool = findToolByName(toolUseContext.options.tools, toolUse.name)
    const parsedInput = tool?.inputSchema.safeParse(toolUse.input)
    const isConcurrencySafe = parsedInput?.success
      ? (() => {
          try {
            return Boolean(tool?.isConcurrencySafe(parsedInput.data))
          } catch {
            return false  // 抛异常也当不安全，又是 fail-closed
          }
        })()
      : false  // 解析失败也当不安全

    if (isConcurrencySafe && acc[acc.length - 1]?.isConcurrencySafe) {
      acc[acc.length - 1].blocks.push(toolUse)  // 合并到并发批次
    } else {
      acc.push({ isConcurrencySafe, blocks: [toolUse] })  // 新开一个批次
    }
    return acc
  }, [])
}
...

runTools 函数
if (isConcurrencySafe) {
const queuedContextModifiers = {}
forawait (const update of runToolsConcurrently(blocks, ...)) {
    if (update.contextModifier) {
      // 先排队，不立即应用
      queuedContextModifiers[toolUseID].push(modifyContext)
    }
  }
// 全部跑完后，按工具调用顺序依次应用
for (const block of blocks) {
    for (const modifier of queuedContextModifiers[block.id]) {
      currentContext = modifier(currentContext)
    }
  }
}
```

### 设计优点

- **优点1**：工具编排的读写分离，连续几个只读工具可以一起跑，但一旦遇到写操作，就得排队等前面的都完成了才行。这种读读并行、读写互斥设计思维处处应用
- **优点2**：默认最多 10 个工具同时并发，还可以通过环境变量调整

### 设计缺点

- **缺点1**：`contextModifier`延迟应用破坏了批次内的上下文一致性，**并发执行的多个工具共享同一份初始上下文快照，但各自可能产生不同的修改意图**。比如：
  - Tool A（并发安全但修改了工作目录的副作用）修改了 `cwd` 为 `/project/src`
  - Tool B（同为并发安全）修改了 `cwd` 为 `/project/test`

## 2. AI 工具解决 Bug / 框架踩坑复盘

### 背景

我的博客 用的 astro-schloar框架GitHub Actions 部署失败，`npm ci` / `npm install` 均报错：

npm error code EINTEGRITY
npm error sha512-... integrity checksum failed

影响所有 main 分支推送，网站无法部署到 GitHub Pages

### 排查过程

1. — 认为是 GitHub Actions 的 npm 缓存损坏，在 `npm ci` 前添加了 `npm cache clean --force`，但**无效**。
2. — 错误信息中的 `wanted sha512-... but got sha512-...` **wanted 和 got 的值完全相同**，说明不是本地缓存问题，而是 **npm registry 返回的包本身 checksum 就与声明不符**。`setup-node` 的 `cache: 'npm'` 会恢复旧缓存，掩盖了问题。
3. **解决方案** — 切换到 **pnpm**，其使用独立的全局 store（不在 npm 缓存路径内），绕过了损坏的 npm 缓存问题

### 根因

`remark-gfm@4.0.1` 在 npm registry 端的 tarball 文件损坏（ checksum 与 package.json 声明不一致）。这是**npm registry 基础设施问题**，非项目代码或配置引入。`remark-gfm` 自项目初始提交起就是传递依赖，一直正常工作，只是 registry 偶尔出现了这个损坏的包版本。

### 反思

- **AI 最有价值的地方**：识别出 `setup-node` 的 npm 缓存是掩盖根因的帮凶，以及建议完全绕过 npm 换用 pnpm。
- **AI 最容易误导的地方**：一开始就接受了"本地缓存损坏"的假设，导致连续尝试了多种缓存清理方案才转向换包管理器的正确方向。
- **如果重来**：看到 `wanted sha512-xxx but got sha512-xxx（两者相同）` 这个关键信号时，应立即判断是 registry 端问题，第一时间尝试换 pnpm，而不是继续在 npm 缓存清理上打转。

## 3. 最近编写的 Skills 展示

- ### Skill: MiniMax TTS — 整句英语发音快捷工具

  **用途**：一键调用 MiniMax Token Plan 的语音合成（TTS）API，将任意英文整句转为自然语音播放，解决英语学习中整句发音的需求缺口。

  #### 痛点与动机

  我在日常英语学习中，经常遇到想听整句话自然发音的场景——不是单词，而是完整句子的语调、连读和节奏。现有的词典插件和翻译工具几乎都只支持单词发音，缺少整句 TTS 能力。虽然 MiniMax Token Plan 提供了 Speech 语音模型的 API，额度充足，但每次使用都要经历一个繁琐的流程：

  1. 打开浏览器，搜索 MiniMax API 文档
  2. 找到 TTS 接口的 endpoint、参数格式、鉴权方式
  3. 手动构造请求体（音色选择、文本输入、输出格式等）
  4. 发送请求，下载音频，再播放

  整个过程打断学习心流，尤其当你在阅读一段英文、想快速听一下某句话的发音时，这个等待和切换的成本太高了。而且每次让大模型帮我调 API，它也要先查一遍文档、理解接口、再拼请求，重复劳动，效率很低。

  #### 实现要点

  核心思路是把"查文档 → 构造请求 → 调用 API → 播放结果"这整个链路**沉淀为一个 Skill**，让 Agent 遇到发音需求时直接执行标准流程，无需重新思考：

  ```markdown
  ---
  name: minimax-tts-sentence
  description: |  将英文整句通过 MiniMax Speech WebSocket API 转为语音并播放。  当用户提到"想听发音""怎么读""念一下""读一下这句"等发音需求时使用。  适用于英语学习场景中需要整句自然发音的情况。
  ---
  # MiniMax TTS — 整句英语发音
  ## 执行步骤
  1. 从用户输入中提取需要发音的英文句子
  2. 建立 WebSocket 连接：wss://api.minimax.chat/ws/v1/t2a_v2，鉴权通过 URL 参数或 Header 传递 Bearer Token（从环境变量 MINIMAX_API_KEY 读取）
  3. 收到 `connected_success` 事件后，发送 `task_start` 事件：   - model: "speech-2.8-turbo"   - language_boost: "English"   - voice_setting:     - voice_id: "male-qn-qingse"（预设音色，可通过 references/ 中的音色列表切换）     - speed: 1     - vol: 1     - pitch: 0   - audio_setting:     - sample_rate: 32000     - bitrate: 128000     - format: "mp3"     - channel: 1
  4. 收到 `task_started` 事件后，发送 `task_continue` 事件，text 字段为用户输入的英文句子
  5. 收到 `task_continued` 事件，从 data.audio 中提取音频数据（Base64 编码），同时从 extra_info 获取音频元信息（时长、格式等）
  6. 发送 `task_finish` 事件，收到 `task_finished` 事件后关闭连接
  7. 将音频数据解码后写入本地临时文件：/tmp/minimax_tts_{timestamp}.mp3
  8. 执行本地播放命令：afplay /tmp/minimax_tts_{timestamp}.mp39. 播放完成后自动清理临时文件
  ## 约束
  - 超过 50 词的句子，按逗号/分句自动拆分，分别通过多次 `task_continue` 事件发送（同一 WebSocket 连接内），无需重连- 单次 `task_continue` 后超过 120s 未发送新事件，WebSocket 连接自动断开，需注意超时处理- 如果收到 `task_failed` 事件，关闭连接，提示用户检查 Token Plan 额度- 音色和语速已预设为英语学习最优配置，无需用户额外选择
  ## References
  - references/voice_list.md — 可用音色列表及 ID（通过"查询可用音色"接口获取）- references/api_reference.md — MiniMax Speech WebSocket API 完整参数文档
  ```

  关键设计决策：

  - **预设音色和语速**：锁定一个适合英语学习的音色，语速设为 0.9 倍，避免每次都要决策这些参数。学习场景下稳定性比灵活性更重要
  - **输入极简化**：用户只需要给一句话，不需要关心 API 细节。Skill 内部处理鉴权、参数构造、错误重试
  - **输出直达播放**：音频直接本地播放，不用手动下载再打开

## 4. OpenClaw 使用经历

### 使用情况

最近使用 hermes agent。

### 使用场景

起初我只是想让他帮我查找 X 上活跃的 巨鲸 的发文，结果它主动询问我是否需要推送，是否需要定时执行，并且沉淀下来了一个 skill。这种自助进化的能力让人惊艳。

### 评价

- 亮点：长程任务执行能力强，并且会自主进化给你惊喜。

## 5. 二次元经历与社区观察

### 个人二次元经历

个人属于二次元文化中的轻度用户。国漫看得多一些，《斗破苍穹》《凡人修仙传》《灵笼》等都有追过；日番看得很少，只看过《海贼》《鬼灭之刃》《间谍过家家》这种破圈级别作品，不追番，不混圈。只是偶尔消费二次元内容的路人，而不是核心 ACG 玩家。

所以，带着边缘参与的视角。这种位置反而让我对社区中某些现象的感受更敏锐。

### 社区观察

- #### **一个观察：轻量用户的"被动消费"特征**

  作为轻度消费者，我对二次元内容的接触路径主要是被动推送——B 站首页推荐、社交媒体热搜。我不会主动搜索新番列表，只是个别会在播出日蹲更新，更不会参与角色投票和同人创作。

  虽然不够活跃，但是这部分群体贡献了播放量、付费会员和周边消费，但几乎不产出 UGC 内容。**二次元社区的内容生态实际上是由不到 10% 的核心用户驱动的，但商业化依赖的是 90% 的沉默消费者。**

  所以做好用户分层十分重要。**不要只看核心用户的反馈来定义产品方向。** 核心用户要的是深度参与感；轻度用户要的是不费力获取好内容。尽管很难完全兼顾，但是这是不得不为之的一件事。
