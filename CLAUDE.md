# Achi 项目编码规范

本文档定义**如何编写代码**：格式、命名、数据存取模式、控制流风格、约定。只讲规则和模式，不列举系统参考数据。

- 项目结构、构建管线、运行时架构 → [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- ExtraData 域结构、字段详情、错误码 → [ExtraData-Schema.md](docs/ExtraData-Schema.md)
- HPL 语言语法、指针系统 → [HPL-参考.md](docs/HPL-参考.md)
- HPL API 函数签名 → [HPL-API-参考.md](docs/HPL-API-参考.md)

修改后必须运行 `uv run python build.py`。构建管线流程及各目录编译规则见 [ARCHITECTURE.md#构建管线](ARCHITECTURE.md#构建管线)。

### 章节

| # | 内容 |
|---|---|
| [源码格式](#format) | 段落分隔、控制分隔、逻辑分隔、多行文本、多行指令、函数头部注释 |
| [数据存取](#data) | 指针模型、-2147483648、域级别/对象级别存取、变量命名 |
| [控制流](#control) | 事件回调、自定义函数、表单提交范式、通用规则 |
| [入口速查](#ref) | entry/navigate、entry/showError、entry/feedback、entry/debug、ref 取值 |
| [交叉引用](#xref) | 各文档职责与链接 |

<a id="format"></a>
## 源码格式

**段落分隔**：表单定义（`edit*form` 系列）与 `customform onsubmit` 之间、`customform onsubmit` 闭引号与 `customform oncancel` 之间，各留一个空行：

```
editbutton ACHI_HOME 4 text "return '系统配置'"
                                 ← 空行
customform onsubmit ACHI_HOME "
...
"
                                 ← 空行
customform oncancel ACHI_HOME "
...
"
```

**控制分隔**：每个 `if`/`fi`、`for`/`rof` 控制块上下各空一行，与前后代码保持视觉分隔。嵌套同样遵守：

```hpl
cmd = 'tickingarea add ...'

if not {func, object.deref({func, world.SetCommand(cmd, playerId)})}:
  {command, 'say 操作失败，重试中...'}
  return True
fi

_ = {func, maps.set(taskData, 'state', 1)}
```

**逻辑分隔**：所有 `.hpl` 文件内部按逻辑边界分段，每段用空行隔开，段首用 `//` 注释标注用途。仅固定字符串返回（如 `"return '写入坐标'"`）可豁免：

1. **数据存取段** — 一连串 `maps.get`/`maps.set`/`GetExtraData`/`GetFootPos` 等数据读写操作，视为一个结构体，不拆散
2. **控制结构**（`if`/`elif`/`else`/`fi`、`for`/`rof`）— 独立成段，前后留空行
3. **命令序列** — `customform show`、`title`、`tp` 等 Minecraft 命令，按语义分组

```
// 获取玩家上下文
playerId = {func, command.get_executor()}
playerIndex = {func, function.call('data/mapKeyOf', 'temp.player.index', playerId)}

// 获取账户数据
playerData = {func, function.call('data/ptrMapGet', 'data.player.archive', playerId)}

if playerData == -2147483648:
  return True
fi

_ = {func, object.finalise(playerData)}
privilege = {func, maps.get(playerData, 'privilegeLevel')}

// 权限检查
if privilege < 3:
  _ = {func, function.call('entry/showError', 5)}
  return True
fi
```

**多行文本**：`customform onsubmit`/`oncancel`、`edit*form content` 等含多行内容的字符串，**开引号后必须换行，闭引号必须独占一行**。每行是完整的 HPL 语句，构建时 `compress()` 用 ` | ` 拼接为单行：

```
editlongform ACHI_HOME_CONFIG content "
text = '...'

// 区块注释（行首 //），构建时丢弃
text = text + '\\n'
text = text + '\\n下一段落...'

return text
"
```

- 以 `//` 开头的行仅作源文件注释，构建时被 `compress_body()` 丢弃
- 换行符通过 `\\n` 字符串拼接，不在源码中直接写物理换行
- 字符串内的**行尾** `//` 注释（非行首）会保留到编译输出中，仅作开发时参考

单行字符串（如 `editbutton X 0 text "return 'xxx'"`）不做多行要求。

**多行指令**：连续多条同类型命令调用（`world.SetCommand`、`world.SpawnEntity` 等）视为一个整体，内部不留空行，前后与上下文用空行隔开：

```hpl
// 构建草皮与角标命令
grassCmd = 'fill ... grass'
glassCmd1 = 'setblock ... green_stained_glass'
glassCmd2 = 'setblock ... green_stained_glass'
glassCmd3 = 'setblock ... green_stained_glass'
glassCmd4 = 'setblock ... green_stained_glass'

// 执行草皮与角标命令
_ = {func, world.SetCommand(grassCmd, playerId)}
_ = {func, world.SetCommand(glassCmd1, playerId)}
_ = {func, world.SetCommand(glassCmd2, playerId)}
_ = {func, world.SetCommand(glassCmd3, playerId)}
_ = {func, world.SetCommand(glassCmd4, playerId)}

return True
```

与"逻辑分隔"中的命令序列一致，但强调**同类型指令的块状排列**。

**函数头部注释**：每个 `03_functions/` 下的函数文件以 `//` 注释开头，简述职责与核心逻辑：

```hpl
//地皮初始化：清空区域 → 铺草皮 → 放置绿色玻璃标记 → 传送玩家至中心
anchor_x = {func, tuple.get(args, 0)}
...
```

状态机类函数在头部注明各 state 含义：

```hpl
//备份状态机：处理 queue.land.backup 队列任务
//state 0 = 准备阶段：读取地皮数据，计算备份坐标，创建tickingarea
//state 1 = 执行阶段：等待区块加载，执行克隆，重试超过12次则放弃
```

<a id="data"></a>
## 数据存取

### 指针即句柄

HPL 内部维护一个 `_objects` 字典：`{int句柄 → 实际对象}`。`maps.new`、`tuple.new` 等返回的"指针"本质就是一个 int 句柄。操作复杂类型只能通过 `maps.*`/`tuple.*` 等函数间接进行。

函数返回时，其内部创建的所有指针自动释放（`del _objects[ptr]`）。对象若已被 ExtraData 存入或经 `ptr_set` 写入父 map，则解引用后由目标持有，函数返回后指针释放但对象仍存在。详见 [HPL-参考.md#指针生命周期](docs/HPL-参考.md#指针生命周期)。

**复杂类型：**

| 类型 | 创建 | 操作模块 | API |
|---|---|---|---|
| map | `maps.new(False)` | `maps.get` / `set` / `exist` / `del` / `ptr_get` / `ptr_set` / `ptr_exist` / `ptr_del` | [maps](docs/HPL-API-参考.md#maps) |
| tuple | `tuple.new(...)` | `tuple.get` / `set` / `len` | [tuple](docs/HPL-API-参考.md#tuple) |
| slice | `slices.new()` | `slices.append` / `ptr_get` / `set` / `len` / `in` | [slices](docs/HPL-API-参考.md#slices) |
| set | `set.new()` | `set.add` / `in` / `len` | [set](docs/HPL-API-参考.md#set) |

四个均为指针类型——存入 map 必须用 `ptr_set`，读取用 `ptr_get`。

基于此模型，存取分为两层：**域级别**（`worldData/*`，操作 ExtraData 顶层域）、**对象级别**（`maps.*` / `tuple.*` / `slices.*` / `set.*`，操作已获取到的复杂类型）。

### 域级别存取

域遵循三段式命名 `类型.模块.属性`，完整结构见 [ExtraData-Schema.md](docs/ExtraData-Schema.md)。

所有 `worldData/*` 和 `queue/*` 为项目自定义函数，key 不存在时统一返回 `-2147483648`，调用方直接判断返回值即可。完整函数签名表见 [ExtraData-Schema.md#访问函数](ExtraData-Schema.md#访问函数)。

**域的两层与三层结构：**

所有域在 `player_join` 中已完成初始化，域本身（第 1 层）始终存在。域内 value 分两种：

- **两层域**（域 → 键 → 普通值）：value 为 int/string，用 `data/mapGet` 读。

  如 `temp.land.using → playerIndex → landIndex (int)`。

- **三层域**（域 → 键 → 子 map → 字段）：value 为 map 指针，用 `data/ptrMapGet` 读。

  如 `data.player.archive → playerId → {uid, privilegeLevel, ...}`。

完整域列表见 [ExtraData-Schema.md](docs/ExtraData-Schema.md)。

**null 检查与 finalise：**

`finalise(-2147483648)` 会崩溃，因此 `ptr_mapGet` 返回 `-2147483648` 时不能调 `finalise`。

必须检查（key 不保证存在）：
```hpl
playerData = ……

if playerData == -2147483648:
  _ = {func, function.call('entry/showError', 9)}
  return True
fi

_ = {func, object.finalise(playerData)}
```

前置条件保证存在时可跳过检查，注释说明理由：

| 可跳过的场景 | 前置条件 |
|---|---|
| 查 using 中的地皮 | using 中只存有效 landIndex |
| 查 using 中玩家的账户 | 获取地皮的前提是已注册 |
| 注册流程内查账户 | 刚创建，上下文保证存在 |

仅判断二层域 key 是否存在用 `data/mapExist`（不分配指针，无需 `finalise`）：
```hpl
if not {func, function.call('data/mapExist', 'temp.land.using', playerIndex)}:
  _ = {func, function.call('entry/navigate', 'ACHI_INFO_RESTORE')}
  return True
fi
```

**变量命名：**

从域取值时，变量名反映其来源和含义，不暴露实现细节（不出现 `Ptr`、`Has` 等前缀）。

- **二层域 `mapGet`** — 变量名 = 域属性名

  如 `mapGet('temp.land.using', playerIndex)` → `usingLandIndex`

- **二层域 `mapKeyOf`** — 变量名 = key 名 + 域属性前缀

  如 `mapKeyOf('temp.land.using', landIndex)` → `landUsingPlayerIndex`

- **三层域 `ptr_mapGet` / `queue`** — 变量名 = 对象名 + `Data`

  如 `ptr_mapGet('data.player.archive', playerId)` → `playerData`

### 对象级别存取

修改**复杂类型**字段必须区分**值类型**和**指针类型**，错用导致悬垂指针崩溃。操作速查见 [HPL-API-参考.md#maps](docs/HPL-API-参考.md#maps)，以下为核心规则：

- `maps.set` 把指针句柄（int）当普通整数存入，不解引用。函数返回时句柄被释放，存储的整数变悬垂引用→后续读取崩溃。
- 存 map、tuple 等复杂类型**必须**用 `maps.ptr_set`，读回**必须**用 `maps.ptr_get`。配套：`ptr_set` 存 → `ptr_get` 读 → `ptr_exist` 查 → `ptr_del` 删。
- `maps.get` 对不存在的 key **直接崩溃**，必须先用 `maps.exist` 检查。
- `maps.ptr_get` 对不存在的 key 返回 `None`，也需 `maps.ptr_exist` 守卫。
- `data/ptrMapGet` 内部调用了 `object.pin()`，返回的指针**必须** `object.finalise` 释放；`maps.ptr_get` / `maps.new` / `tuple.new` 等不 pin，函数返回时自动释放，**不需要** `finalise`。

**示例：嵌套 map 存取（个人锚点）**

写入——先填充子 map，再 `ptr_set` 存入父 map（顺序不能反）：

```
// 获取或创建锚点 map
if {func, maps.exist(playerData, 'anchors')}:
  anchorsMap = {func, maps.ptr_get(playerData, {func, object.ref('anchors')})}
else:
  anchorsMap = {func, maps.new(False)}
fi

posTuple = {func, tuple.new(px, py, pz)}

// 先写子 map，再存入父 map
_ = {func, maps.ptr_set(anchorsMap, {func, object.ref(slot)}, posTuple)}
_ = {func, maps.ptr_set(playerData, {func, object.ref('anchors')}, anchorsMap)}
```

读取——`ptr_exist` 守卫 + `ptr_get`：

```
if {func, maps.exist(playerData, 'anchors')}:
  anchorsMap = {func, maps.ptr_get(playerData, {func, object.ref('anchors')})}

  if {func, maps.ptr_exist(anchorsMap, {func, object.ref(slot)})}:
    posTuple = {func, maps.ptr_get(anchorsMap, {func, object.ref(slot)})}
    // 使用 posTuple
  fi

fi
```

<a id="control"></a>
## 控制流

### 事件回调（`02_events/`）

**默认拦截 + 放行**。先设 `args.cancel`（或 `args.ret`）为 `True`，条件满足时改为 `False`。不使用 guard clause，所有路径 fall-through 到末尾唯一的 `return True`。

**正向条件嵌套**。用 `if x != -2147483648:` 进入正常逻辑，不写早退。允许嵌套。

```
// 验证方块破坏是否合法
_ = {func, maps.set(args, 'cancel', True)}
playerData = {func, function.call('data/ptrMapGet', 'data.player.archive', playerId)}

// 账户存在
if playerData != -2147483648:
  // 成员及以上
  if {func, maps.get(playerData, 'privilegeLevel')} > 0:
    landIndex = {func, function.call('data/mapGet', 'temp.land.using', playerIndex)}
    // 在使用中的地皮
    if landIndex != -2147483648:
      _ = {func, maps.set(args, 'cancel', False)}
    fi
  fi
  _ = {func, object.finalise(playerData)}
fi

return True
```

### 自定义函数（`03_functions/`）

**正向条件嵌套**。同事件回调，保持层次感。

自定义函数未查找到目标时返回 `-2147483648`（与 `worldData/*` 一致），调用方以此判断是否命中。不要返回其他 sentinel 值。

#### 返回规则

`03_functions/` 下所有项目自定义函数统一返回 `-2147483648` 表示"未找到"，调用方以此判断是否命中：

| 分类 | 函数 |
|---|---|
| worldData 读 | `data/mapGet`、`data/mapKeyOf`、`data/ptrMapGet` |
| queue 操作 | `queue/peek`、`queue/push` |
| 项目查找 | `land/getFreeIndex` |

HPL 内置函数（`maps.*`、`tuple.*` 等）**不遵循此约定**，其行为见 [HPL-参考.md](docs/HPL-参考.md)。

### 表单提交（`04_forms/` onsubmit）

**扁平早退**。与事件/函数的正向条件嵌套相反，每个分支 `return True` 直接退出，不 fall-through。

```
customform onsubmit ACHI_DEMO "
// === 阶段一：获取表单展示者信息 ===
// onsubmit/oncancel 中 command.get_executor() 返回打开此表单的玩家
playerId = {func, command.get_executor()}
playerIndex = {func, function.call('data/mapKeyOf', 'temp.player.index', playerId)}
playerData = {func, function.call('data/ptrMapGet', 'data.player.archive', playerId)}
//由于使用此表单的条件是创建账户，故不进行返回值检查
_ = {func, object.finalise(playerData)}
privilege = {func, maps.get(playerData, 'privilegeLevel')}

// === 阶段二：按钮分发 ===

// 分支 A — 权限 + 校验 + 操作 + feedback
if {ref, bool, 0}:

  if privilege != 3:
    _ = {func, function.call('entry/showError', 5)}
    return True
  fi

  if {func, function.call('data/mapExist', 'temp.land.using', playerIndex)}:
    _ = {func, function.call('entry/showError', 7)}
    return True
  fi

  _ = {func, function.call('data/mapSet', 'temp.land.using', playerIndex, freeIndex)}
  _ = {func, function.call('entry/feedback', '绑定成功')}
  return True

// 分支 B — 纯导航
elif {ref, bool, 1}:
  _ = {func, function.call('entry/navigate', 'ACHI_HOME_TP')}
  return True

// 分支 C — 预留
elif {ref, bool, 2}:
fi

// === 阶段三：兜底返回 ===
return True
"

customform oncancel ACHI_DEMO "
_ = {func, function.call('entry/navigate', 'ACHI_HOME')}
"
```

- **上下文**：分发前一次性获取，不在分支内重复。`entry/navigate` 内部获取 playerId，纯导航表单可省略上下文
- **早退**：每分支 `return True`。分支内顺序：权限 → 校验 → 操作 → feedback/navigate
- **账户检查**：保证存在 → 跳过并注释；否则 `== -2147483648` → `showError` → `return True`
- **覆盖**：按钮 0..N-1 全部覆盖，空分支保留 `elif` 骨架，纯导航一行 `entry/navigate`
- **oncancel**：一行返回上级，叶子表单可省
- **模态表单**：无按钮分发，跳过阶段二，直接操作后 `return True`

**其他表单函数体：** 除 onsubmit/oncancel 外，所有 `<*Code: string>` 参数也是 HPL 函数体，在表单展示者上下文中执行（`command.get_executor()` 返回打开表单的玩家）。数据存取规则与 onsubmit 一致——按需获取上下文，遵循同样的 null 检查和 finalise 规则。差异仅在于：无按钮分发、无三段结构，返回值是表单需要的实际数据（string / bool / int / float）而非 `True`。

长表单（long）：

| 位置 | 返回类型 |
|---|---|
| `editlongform content` / `title` | string |
| `editbutton N text` / `icon` | string |
| `editlabel N header` / `label` | string |

模态表单（modal）：

| 位置 | 返回类型 |
|---|---|
| `editmodalform content` / `title` | string |
| `editinput N text` / `default` / `placeholder` / `tooltip` | string |
| `edittoggle N text` / `tooltip` | string |
| `edittoggle N default` | bool |
| `editdropdown N text` / `tooltip` | string |
| `editdropdown N append` / `insert` option | string |
| `editdropdown N default` | int |
| `editslider N text` / `tooltip` | string |
| `editslider N default` / `min` / `max` / `step` | float |
| `editstepslider N text` / `tooltip` | string |
| `editstepslider N append` / `insert` step | string |
| `editstepslider N default` | int |

信息表单（popup）：

| 位置 | 返回类型 |
|---|---|
| `editpopupform content` / `title` / `button1` / `button2` | string |

### 通用规则

**`finalise` 位置**。三种情况：

- **正向条件嵌套**（`02_events/`、`03_functions/`）：放在使用该指针的 if-block 末尾，缩进与该 block 一致。
- **跳过检查**（前置条件保证存在）：紧跟 `ptr_mapGet` 之后。
- **扁平早退**（`04_forms/` onsubmit）：放在早退结构体之后、主逻辑之前。

**权限检查**。单一等级判定用精确等值 `if privilege == 3:`，等级区间判定用比较运算符 `if privilege > 1`（会员及以上）、`if privilege < 3`（非管理员拦截）。

**遍历方式**。有数据时用 `maps.length` + `maps.items` + `slices.ptr_get`。检查存在用 `slices.in`。反查 key 用 `data/mapKeyOf`。避免 `for i, 40` 暴力扫描。

**坐标命名**。统一蛇形命名：`anchor_x`, `anchor_y`, `anchor_z`（非 `anchorX`）。

**其他**。`execute` 命令优于 HPL 玩家循环；含 `/` 的函数名必须双引号包裹（`customfunction add "data/mapGet" "..."`）；使用未知 HPL 函数前先查本地 API 文档或 [网易开发手册](https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/接口/世界/索引.html)。

<a id="ref"></a>
## 入口速查

| 入口 | 用途 | 说明 |
|---|---|---|
| `entry/navigate(formName)` | 跳转到指定表单 | 内部获取 playerId，调用方不传 |
| `entry/showError(code)` | 弹出错误提示 | 写入 errorCode 并导航至 ACHI_INFO_ERROR |
| `entry/feedback(message)` | 向当前玩家发 tellraw | 格式 `§7系统 \| ACHI > §f<message>` |
| `entry/debug(message)` | 向所有玩家广播 tellraw | 仅临时调试用 |
| `{ref, bool, N}` | 长表单按钮分发 | 详见 [HPL-参考.md#ref-bool-n-按钮分发](docs/HPL-参考.md#ref-bool-n-按钮分发) |
| `{ref, str/int, N}` | 模态表单输入取值 | 详见 [HPL-参考.md#ref-strint-n-输入控件取值](docs/HPL-参考.md#ref-strint-n-输入控件取值) |

完整错误码表见 [ExtraData-Schema.md#11-tempmenuerrorcode--错误码](ExtraData-Schema.md#11-tempmenuerrorcode--错误码)，完整函数目录见 [ARCHITECTURE.md#关键函数目录](docs/ARCHITECTURE.md#关键函数目录)。

<a id="xref"></a>
## 交叉引用

| 需要了解... | 查阅文档 |
|---|---|
| 某个域的 key/value 类型和字段结构 | [ExtraData-Schema.md](docs/ExtraData-Schema.md) |
| 错误码含义 | [ExtraData-Schema.md#11-tempmenuerrorcode--错误码](ExtraData-Schema.md#11-tempmenuerrorcode--错误码) |
| 构建命令和编译规则 | [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| 如何新增事件/表单/函数 | [ARCHITECTURE.md#注册机制](ARCHITECTURE.md#注册机制) |
| HPL 函数调用语法和指针生命周期 | [HPL-参考.md](docs/HPL-参考.md) |
| 某个 API 的参数和返回值 | [HPL-API-参考.md](docs/HPL-API-参考.md) |
| 项目自建函数调用 | 本文档 [入口速查](#ref) |
| 指针 finalise 规则 | 本文档 [数据存取](#data) |
| 变量命名约定 | 本文档 [数据存取](#data) |
| 控制流模式选择（嵌套 vs 早退） | 本文档 [控制流](#control) |
