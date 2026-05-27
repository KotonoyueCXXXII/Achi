# Achi — 地皮管理系统

基于网易 Minecraft HPL 脚本系统的玩家地皮管理插件，支持自动分配、建筑保护、备份恢复、传送锚点、权限分级。

## 功能

- **地皮管理** — 玩家自助领取 20×20 / 30×30 / 40×40 地皮，自动清空、铺草皮、放置标记
- **建筑保护** — 权限分级（访客 / 成员 / VIP / 管理员），拦截越权破坏和放置
- **自动备份** — 玩家离线时异步备份地皮至螺旋分配区，上线自动恢复
- **传送系统** — 固定传送点 + 9 个私有锚点（坐标记忆）
- **玩家交互** — 在线玩家列表、私信、管理员提权/降权
- **UI 表单** — 26 个表单（长表单 / 模态 / 弹窗），分级菜单导航

## 快速开始

```bash
# 构建（输出单一 Achi.mcfunction，上传至 MC 服务器）
uv run python build.py
```

构建输出：`Achi.mcfunction`（~100KB），导入服务器即可运行。卸载脚本：`Achi_uninstall.mcfunction`。

## 项目结构

```
Achi_func_new/
├── build.py                    ← 构建脚本
├── scripts/
│   └── config.py               ← 事件/表单注册表
├── 01_init/                    ← 初始化函数（2 个）
├── 02_events/                  ← 系统事件监听（6 个）
├── 03_functions/               ← 自定义函数（28 个）
│   ├── main.hpl                ←  主循环入口
│   ├── entry/                  ←  入口函数（导航/反馈/错误）
│   ├── queue/                  ←  FIFO 队列
│   ├── land/                   ←  领地操作（初始化/备份/克隆）
│   ├── ui/                     ←  表单辅助
│   └── data/                   ←  ExtraData 存取层
├── 04_forms/                   ← UI 表单定义（26 个）
│   └── ACHI/
│       ├── HOME/               ←  主菜单
│       │   ├── LAND/           ←    地皮操作（领取/设置）
│       │   ├── TP/             ←    传送（定点/锚点）
│       │   ├── PLAYER/         ←    玩家交互（传送/私信/管理）
│       │   ├── ROOM/           ←    房间信息
│       │   └── SYSTEM/         ←    系统配置（权限/个人/调试）
│       └── INFO/               ←  信息提示（错误/恢复/协议）
├── docs/                       ← 文档
│   ├── ARCHITECTURE.md         ←  系统架构与构建管线
│   ├── ExtraData-Schema.md     ←  数据结构权威参考
│   ├── HPL-参考.md             ←  HPL 语言/指令参考
│   ├── HPL-API-参考.md         ←  HPL API 函数参考
│   ├── commands/               ←  指令详细文档
│   └── programming/            ←  编程语法文档
├── CLAUDE.md                   ← 编码规范（格式/命名/控制流/数据存取）
└── README.md                   ← 本文件
```

## 文档导航

| 需要... | 看这里 |
|---|---|
| 了解怎么写代码（格式、命名、模式） | [CLAUDE.md](CLAUDE.md) |
| 理解系统怎么运作（架构、构建、运行时） | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| 查某个域存了什么、怎么读 | [docs/ExtraData-Schema.md](docs/ExtraData-Schema.md) |
| 查 HPL 语法、指令、指针系统 | [docs/HPL-参考.md](docs/HPL-参考.md) |
| 查 API 函数签名 | [docs/HPL-API-参考.md](docs/HPL-API-参考.md) |

## 技术要点

- **语言**：HPL（Hyper Packet Language），网易 Minecraft 专有脚本
- **运行频率**：主循环每 tick（~20Hz）执行，耗时操作异步入队
- **数据存储**：14 个 ExtraData 域，三段式命名 `类型.模块.属性`，分为持久层（data）、临时层（temp）、队列层（queue）
- **权限模型**：0=访客、1=成员、2=VIP、3=管理员
