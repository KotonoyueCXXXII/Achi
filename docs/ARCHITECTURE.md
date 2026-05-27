# 项目结构

本文档描述系统的**结构、行为和编译机制**。

- 编码规范 → [CLAUDE.md](../CLAUDE.md)
- ExtraData 数据结构详情 → [ExtraData-Schema.md](ExtraData-Schema.md)

```
Achi_func_new/
├── build.py                  ← 构建脚本
├── scripts/
│   └── config.py             ← 事件/表单注册表
├── Achi.mcfunction           ← 构建输出（单一文件，上传至 MC）
├── Achi_uninstall.mcfunction ← 卸载脚本
│
├── 01_init/                  ← 初始化函数（customfunction add 包装），导入时显示安装信息
│
├── 02_events/                ← 系统事件监听（6 个）
│   ├── block_destroy.hpl
│   ├── on_command.hpl
│   ├── item_use.hpl
│   ├── player_chat.hpl
│   ├── player_join.hpl
│   └── player_leave.hpl
│
├── 03_functions/             ← 自定义函数（28 个，按功能分子目录）
│   ├── main.hpl                  ← 主循环入口
│   ├── entry/
│   │   ├── debug.hpl
│   │   ├── feedback.hpl
│   │   ├── navigate.hpl
│   │   └── showError.hpl
│   ├── queue/
│   │   ├── peek.hpl
│   │   ├── pop.hpl
│   │   └── push.hpl
│   ├── land/
│   │   ├── checkChunks.hpl
│   │   ├── cloneLand.hpl
│   │   ├── getFreeIndex.hpl
│   │   ├── initLand.hpl
│   │   ├── processBackup.hpl
│   │   ├── processInit.hpl
│   │   └── squareSpiralFill.hpl
│   ├── ui/
│   │   ├── createPlayerSnapshot.hpl
│   │   ├── getAnchorButtonText.hpl
│   │   ├── getSnapshotName.hpl
│   │   ├── openMenu.hpl
│   │   └── validatePlayerSelection.hpl
│   └── data/
│       ├── mapDel.hpl
│       ├── mapExist.hpl
│       ├── mapGet.hpl
│       ├── mapKeyOf.hpl
│       ├── mapSet.hpl
│       ├── ptrMapDel.hpl
│       ├── ptrMapGet.hpl
│       └── ptrMapSet.hpl
│
├── 04_forms/                 ← UI 表单（26 个，按功能分目录）
│   └── ACHI/
│       ├── HOME/
│       │   ├── _.hpl               → ACHI_HOME
│       │   ├── LAND/
│       │   │   ├── _.hpl           → ACHI_HOME_LAND
│       │   │   ├── GET.hpl         → ACHI_HOME_LAND_GET
│       │   │   └── SET.hpl         → ACHI_HOME_LAND_SET
│       │   ├── TP/
│       │   │   ├── _.hpl           → ACHI_HOME_TP
│       │   │   ├── FIXED-A.hpl     → ACHI_HOME_TP_FIXED-A
│       │   │   ├── FIXED-B.hpl     → ACHI_HOME_TP_FIXED-B
│       │   │   └── ANCHOR/
│       │   │       ├── _.hpl       → ACHI_HOME_TP_ANCHOR
│       │   │       └── SET.hpl     → ACHI_HOME_TP_ANCHOR_SET
│       │   ├── PLAYER/
│       │   │   ├── _.hpl           → ACHI_HOME_PLAYER
│       │   │   ├── ACTION.hpl      → ACHI_HOME_PLAYER_ACTION
│       │   │   ├── ADMIN.hpl       → ACHI_HOME_PLAYER_ADMIN
│       │   │   └── MESSAGE.hpl     → ACHI_HOME_PLAYER_MESSAGE
│       │   ├── ROOM/
│       │   │   ├── _.hpl               → ACHI_HOME_ROOM
│       │   │   ├── AGREEMENT_VIEW.hpl  → ACHI_HOME_ROOM_AGREEMENT_VIEW
│       │   │   ├── LAND_WORKFLOW.hpl   → ACHI_HOME_ROOM_LAND_WORKFLOW
│       │   │   └── PLAYER_FLOW.hpl     → ACHI_HOME_ROOM_PLAYER_FLOW
│       │   └── SYSTEM/
│       │       ├── _.hpl           → ACHI_HOME_SYSTEM
│       │       ├── PERSONAL.hpl    → ACHI_HOME_SYSTEM_PERSONAL
│       │       ├── GLOBAL.hpl      → ACHI_HOME_SYSTEM_GLOBAL
│       │       └── DEBUG.hpl           → ACHI_HOME_SYSTEM_DEBUG
│       └── INFO/
│           ├── AGREEMENT.hpl       → ACHI_INFO_AGREEMENT
│           ├── ERROR.hpl           → ACHI_INFO_ERROR
│           ├── RESTORE.hpl         → ACHI_INFO_RESTORE
│           └── LAND/
│               ├── DEL.hpl         → ACHI_INFO_LAND_DEL
│               └── SET.hpl         → ACHI_INFO_LAND_SET
│
├── CLAUDE.md                  ← 编码规范
├── README.md                  ← 项目概览
├── docs/
│   ├── ARCHITECTURE.md        ← 本文件
│   ├── ExtraData-Schema.md    ← 数据结构权威参考
│   ├── HPL-参考.md            ← HPL 语言语法 & 指令参考
│   ├── HPL-API-参考.md        ← HPL API 函数参考
│   ├── commands/              ← 指令详细文档
│   └── programming/           ← 编程语法文档
```

## 构建管线

```
源文件 (.hpl)                  build.py                          Achi.mcfunction
─────────────                  ────────                          ──────────────
01_init/*.hpl     ──→ 安装信息（tellraw）+ customfunction add + call（函数名 init/...）
02_events/*.hpl   ──→ 包装为 systemevent listen 指令
03_functions/*.hpl──→ 包装为 customfunction add 指令             全部拼接 → 二次压缩 → 输出
04_forms/*.hpl    ──→ 包装为 customform add + UI + save 序列
```

**构建命令：** `uv run python build.py`

**处理步骤：**
1. `strip_comments()` — 移除 `//` 注释行（字符串外的行首注释）
2. `replace_form_refs()` — 将 `&(formName)` 替换为当前表单的实际表单名（仅在 `process_forms` 中）
3. `compress()` — 移除空行，双引号字符串内部用 `|` 连接为一行
4. 最终输出时再对整个文件执行一次 `compress()`

## 运行时架构

系统由 `main` 函数驱动，每游戏 tick 执行一次，通过 `schedule` 计数器调度不同频率的任务。

**启动流程：** `.mcfunction` 导入时输出安装信息（`tellraw`），随即注册 `init/main` 并通过 `customfunction call` 执行，完成 ExtraData 域的初始化。首位玩家加入时，`player_join` 检测到服务器为空，遍历 `temp.land.using` 备份异常关闭残留的地皮，随后清理并重建临时域。

```
每 tick（~20Hz）：
  main
  ├── titleraw @a[tag=isSettingLand]     ← 显示地皮设置提示
  ├── execute ... ui/openMenu          ← 检测低头玩家，弹出菜单
  └── schedule++

每 5 tick（~4Hz）：
  ├── land/processBackup                     ← 驱动备份队列（状态机，最多1个任务）
  └── land/processInit                   ← 驱动地皮初始化队列（检查槽位0）

每 600 tick（~30秒）：
  ├── entity.SaveExtraData               ← 持久化存档
  └── customform style @a speed_00       ← 刷新表单样式
```

**队列模式：** 耗时操作（地皮初始化、备份）不阻塞主循环，而是入队后由 `land/*` 函数逐 tick 推进。队列任务完整字段结构见 [ExtraData-Schema.md](ExtraData-Schema.md)。

| 队列域 | 处理函数 | 模式 | 超时 |
|---|---|---|---|
| `queue.land.init` | `land/processInit` | 取槽位 0 → 递减 retryCount → 等区块加载 → 执行 land/initLand | ~15 tick（~3.75s） |
| `queue.land.backup` | `land/processBackup` | Peek 槽位 0 → state 0 创建 tickingarea → state 1 等区块并 land/cloneLand | ~12 retry（~3s） |

**状态机模式：** `land/processBackup.hpl` 和 `land/processInit.hpl` 在多次调用间通过 taskMap 的 `state` 字段推进。

```
Backup 状态流转：
  Push(任务) → state=0（准备）→ 计算坐标、创建tickingarea → state=1
  → state=1（执行）→ 等区块加载 → land/cloneLand → rate>=1 时 Pop 出队
                   → retry>12 超时 → 清理 + Pop
```

**槽位复用：** 队列函数（`queue/push`、`queue/pop`、`queue/peek`）在固定长度 map（64 槽位）上线性扫描空位，不维护头尾指针。`Pop` 将后续元素前移填充空位。

## 地皮生命周期

```
[玩家选择尺寸]  GET.hpl
      │
      ▼
[获取地皮]  GET.hpl onsubmit
  ├── FreeLandIndex          ← 查找匹配尺寸的空闲地皮
  ├── mapSet temp.land.using ← 绑定玩家
  ├── tp 传送至中心
  └── Push queue.land.init   ← 入队初始化任务（retryCount=15）
      │
      ▼
[初始化]  land/processInit → land/initLand
  ├── 逐段 fill air          ← 清空地皮上方空间
  ├── fill grass             ← 铺设草皮地面
  ├── setblock 绿色玻璃      ← 放置角标 + 中心十字
  └── Pop 出队 → 完成
      │
      ▼
[正常使用]  block_destroy / item_use 拦截
  ├── 管理员（privilege>1）→ 放行全局
  ├── 会员（privilege>0）  → 仅放行自己地皮内
  └── 访客（privilege=0）  → 全拦截
      │
      ▼
[玩家离开]  player_leave
  ├── 备份入队 queue.land.backup          ← 保护地皮数据
  └── 删除 temp.player.index[slot]        ← 释放槽位
      │
      ▼
[备份]  land/processBackup
  ├── state 0：计算备份坐标（land/squareSpiralFill）、创建 tickingarea
  ├── state 1：等区块加载 → land/cloneLand（逐段 clone）
  ├── 成功：写入 account.saveSizeIndex → 释放 temp.land.using → Pop
  └── 超时（retry>12）：放弃 → 释放锁 → Pop
      │
      ▼
[玩家重新加入]  player_join
  ├── 分配空闲槽位至 temp.player.index
  ├── 检测 account.saveSizeIndex → 恢复地皮
  └── 清理孤立数据（CleanExtraData）
```

**关键设计：** `temp.land.using` 在玩家离开时不删除，作为备份期间的预留锁，防止 `FreeLandIndex` 将正在备份的地皮分配给新玩家。备份完成或超时后才释放。

对应的 ExtraData 读写细节见 [ExtraData-Schema.md#数据流总览](ExtraData-Schema.md#数据流总览)。

## 各目录编译规则

### `01_init/` — 初始化

启动时负责两项工作：显示安装信息、注册初始化函数供后续调用。

| 项目 | 说明 |
|---|---|
| 输入 | `.hpl` 初始化函数代码体 |
| 编译 | 首行输出 `tellraw` 安装信息，随后每个文件包装为 `customfunction add` |
| 函数名 | `init/<相对路径去 .hpl>`（如 `01_init/main.hpl` → `init/main`） |
| 顺序 | 安装信息固定在最前，函数按文件名排序 |

**安装信息：** 构建时自动生成一条 `tellraw @a` 命令，在 `.mcfunction` 导入时向所有在线玩家展示系统名称。

**触发方式：** 初始化函数在导入时立即执行——`customfunction add` 注册后紧跟 `customfunction call` 触发。同时也保留为可调用函数，供后续需要时复用。

### `02_events/` — 系统事件

| 项目 | 说明 |
|---|---|
| 输入 | 事件回调**代码体**（不含 `systemevent` 声明） |
| 事件名 | 文件名去 `.hpl`（如 `player_join.hpl` → `player_join`） |
| MC 事件 | 在 `EVENT_MAP` 中查找（如 `player_join` → `AddServerPlayerEvent`） |
| 输出 | `systemevent destroy <名>` + `systemevent listen <MC事件> <名> "<压缩代码>"` |

**当前注册事件：**

| 文件名 | MC 事件 |
|---|---|
| `block_destroy.hpl` | `ServerPlayerTryDestroyBlockEvent` |
| `on_command.hpl` | `GlobalCommandServerEvent` |
| `item_use.hpl` | `ServerItemUseOnEvent` |
| `player_chat.hpl` | `ServerChatEvent` |
| `player_join.hpl` | `AddServerPlayerEvent` |
| `player_leave.hpl` | `DelServerPlayerEvent` |

### `03_functions/` — 自定义函数

| 项目 | 说明 |
|---|---|
| 输入 | 函数**代码体**（不含 `customfunction` 声明） |
| 函数名 | 相对 `03_functions/` 的路径去 `.hpl`（如 `land/getFreeIndex.hpl` → `land/getFreeIndex`） |
| 输出 | `customfunction remove "<名>"` + `customfunction add "<名>" "<压缩代码>"` |

**关键函数目录：**

| 函数 | 参数 | 返回值 | 用途 |
|---|---|---|---|
| `main` | — | `True` | 主循环，每 tick 驱动队列处理、菜单弹出检测、数据持久化 |
| `entry/navigate` | `formName: str` | `True` | 向当前执行玩家打开指定表单 |
| `ui/openMenu` | — | `True` | 检测低头玩家并弹出主菜单 |
| `entry/showError` | `errorCode: int` | `True` | 写入错误码并弹出 ACHI_INFO_ERROR |
| `ui/createPlayerSnapshot` | `playerIndex: int` | `True` | 深拷贝在线玩家列表作为快照 |
| `ui/validatePlayerSelection` | `playerIndex: int` | `int` | 验证选中目标有效性：0=通过，2/3/4=错误码 |
| `ui/getAnchorButtonText` | `slot: int, playerId: str` | `str` | 返回锚点按钮的动态文本 |
| `ui/getSnapshotName` | `index: int` | `str` | 返回快照中玩家的名称或 `- 无 -` |
| `entry/feedback` | `message: str` | `True` | 向当前执行玩家发送 tellraw 反馈消息 |
| `entry/debug` | `message: str` | `True` | 向所有在线玩家广播 tellraw 调试消息 |
| `land/cloneLand` | `taskData: ptr` | `float` | 从任务中的源/目标坐标逐段 clone，返回成功率 |
| `land/initLand` | `anchor_x, anchor_y, anchor_z, sizeIndex` | `True` | 地皮初始化：清空→铺草皮→玻璃标记 |
| `land/squareSpiralFill` | `uid: int` | `tuple` | 根据玩家 UID 计算螺旋分配的备份坐标偏移 |
| `land/checkChunks` | `anchor_x, anchor_z, sizeIndex` | `bool` | 检查地皮覆盖的所有区块是否已加载 |
| `land/getFreeIndex` | `sizeIndex: int` | `int` | 查找第一个匹配指定大小的空闲地皮索引 |
| `land/processBackup` | —（读取队列） | `True` | 备份状态机：state 0 准备→state 1 执行 clone |
| `land/processInit` | —（读取队列） | `True` | 初始化状态机：检查区块→调 land/initLand→出队 |

ExtraData 存取函数和队列函数的完整签名见 [ExtraData-Schema.md#访问函数](ExtraData-Schema.md#访问函数)。

### `04_forms/` — UI 表单

| 项目 | 说明 |
|---|---|
| 输入 | 表单 UI 定义（`edit*form` 系列）+ 回调代码体（`customform onsubmit/oncancel`） |
| 表单名 | 相对 `04_forms/` 的路径去 `.hpl`，`_` 被过滤，其余用 `_` 连接 |
| 表单类型 | 在 `FORM_TYPE_MAP` 中查找（`long` / `modal` / `popup`） |
| 标题 | 若源文件中没有 `edit___form X title ...` 则自动补入默认标题 |
| 输出 | `customform remove <名>` + `customform add <名> <类型>` + 压缩后的表单内容 + `customform save <名>` |

**`&(formName)` 自引用占位符：**

表单源文件中，所有指向**本表单自身**的引用统一使用 `&(formName)`。构建时 `build.py` 自动替换为实际表单名：

```hpl
editlongform &(formName) content "..."
editbutton &(formName) 0 text "..."
customform onsubmit &(formName) "..."
customform oncancel &(formName) "..."
```

表单文件移动或重命名后无需修改内部源文件，只需调整目录结构即可自动适配。
**交叉引用（指向其他表单）仍使用显式表单名**，如 `{command, 'customform show @s ~ ~ ~ @s ACHI_HOME'}`。

**表单命名示例：**

| 文件路径 | 表单名 |
|---|---|
| `ACHI/HOME/_.hpl` | `ACHI_HOME` |
| `ACHI/HOME/TP/FIXED-A.hpl` | `ACHI_HOME_TP_FIXED-A` |
| `ACHI/INFO/LAND/DEL.hpl` | `ACHI_INFO_LAND_DEL` |

## 注册机制

`build.py` 通过**遍历目录**发现 `.hpl` 文件，但 `.hpl` 文件本身不包含「MC 事件名」或「表单类型」这样的元数据。这些信息需要在注册文件中手动声明。

**核心原则：每一份 `.hpl` 源文件，都必须在对应的注册文件中有记录。文件与记录一一对应，增则增，删则删。**

事件和表单的注册统一在 `scripts/config.py` 中维护：

- **`EVENT_MAP`** — 映射「文件名 → MC 事件名」：

```python
EVENT_MAP = {
    "block_destroy": "ServerPlayerTryDestroyBlockEvent",
    "item_use":     "ServerItemUseOnEvent",
    "player_join":  "AddServerPlayerEvent",
    "player_leave": "DelServerPlayerEvent",
    "on_command":   "GlobalCommandServerEvent",
}
```

Key 就是 `02_events/` 下**文件名去掉 `.hpl`**，Value 是网易 ModAPI 的完整事件名（参见 [事件索引表](https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/事件/事件索引表.html)）。

- **`FORM_TYPE_MAP`** — 映射「表单名 → 表单类型」：

```python
FORM_TYPE_MAP = {
    "ACHI_HOME":             "long",
    "ACHI_HOME_PLAYER_ADMIN": "modal",
    "ACHI_INFO_RESTORE":     "popup",
    ...
}
```

Key 由文件路径自动推导（规则见上方「04_forms/」编译表），Value 是 `"long"` / `"modal"` / `"popup"` 之一。

### 增删文件操作

#### 新增事件

| 步骤 | 操作 |
|---|---|
| 1. 创建文件 | 在 `02_events/` 下新建 `xxx.hpl`，写入回调代码体 |
| 2. 注册 | 在 `scripts/config.py` 的 `EVENT_MAP` 中添加 `"xxx": "对应MC事件名"` |
| 3. 构建验证 | `uv run python build.py` |

#### 新增表单

| 步骤 | 操作 |
|---|---|
| 1. 创建文件 | 在 `04_forms/` 下新建 `.hpl`，写入 UI 定义 + 回调 |
| 2. 确定类型 | 三选一：`long`（按钮列表）/ `modal`（输入控件）/ `popup`（确定取消） |
| 3. 推导表单名 | 按路径命名规则推导（如 `ACHI/INFO/XXX.hpl` → `ACHI_INFO_XXX`） |
| 4. 注册 | 在 `scripts/config.py` 的 `FORM_TYPE_MAP` 中添加 `"表单名": "类型"` |
| 5. 构建验证 | `uv run python build.py` |

#### 新增函数

| 步骤 | 操作 |
|---|---|
| 1. 创建文件 | 在 `03_functions/` 下新建 `xxx.hpl`，写入函数代码体 |
| 2. 构建验证 | `uv run python build.py` |

函数不需要注册表——`build.py` 根据路径自动生成函数名。

#### 新增初始化函数

| 步骤 | 操作 |
|---|---|
| 1. 创建文件 | 在 `01_init/` 下新建 `xxx.hpl`，写入初始化函数代码体 |
| 2. 构建验证 | `uv run python build.py` |

与 `03_functions/` 规则相同，无需注册表。函数名自动生成为 `init/<路径>`（如 `01_init/main.hpl` → `init/main`）。调用时使用 `function.call('init/main')`。

#### 删除文件

删除 `.hpl` 文件时，**必须同步删除**对应注册条目，否则 `build.py` 仍会尝试编译——对于事件/表单会直接报 `KeyError` 导致构建失败；对于函数和初始化函数虽然不会报错，但会留下无用的 `customfunction` 声明。

### 忘记注册的报错

如果创建了 `.hpl` 但没有在注册文件中添加条目，`build.py` 会在编译时报错：

```
KeyError: "Unknown event 'xxx' — add to EVENT_MAP"
KeyError: "Unknown form 'XXX' — add to FORM_TYPE_MAP"
```

这就是注册机制的保障——**不编译未注册的文件，防止遗漏**。
