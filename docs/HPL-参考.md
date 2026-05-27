# HPL 语言参考

NetEase Minecraft HPL（Hyper Packet Language）脚本系统的语言特性、注意事项和 API 速查。

## 语法

### 前缀表达式

```
{func, module.function, args...}
```

可用模块：`object`, `reflect`, `slices`, `maps`, `tuple`, `set`, `strings`, `json`, `math`, `world`, `entity`, `player`, `command`

### `{command, ...}` vs `world.SetCommand`

- `{command, 'cmd'}` — 在表单上下文中以 `@s` 执行
- `{func, world.SetCommand(cmd, playerId)}` — 在指定 playerId 的上下文中执行

详见 [programming/external.md](programming/external.md)。

### `{ref, bool, N}` 按钮分发

长表单 onsubmit 必须用此模式。**N 是按钮的连续序号（从 0 开始），仅计按钮，`append divider`/`label`/`header` 不消耗 N。**

**注意：`editbutton <form> <index>` 的 index 是元素统一索引（所有元素类型共享，divider 也占位），与 `{ref, bool, N}` 的按钮分发序号是两套体系。**

```
append button   ← {ref, bool, 0}  editbutton 0
append button   ← {ref, bool, 1}  editbutton 1
append divider  ← 不可点击           editbutton 2（若需编辑）
append button   ← {ref, bool, 2}  editbutton 3
```

```
if {ref, bool, 0}:
  ...
elif {ref, bool, 1}:
  ...
elif {ref, bool, 2}:
  ...
fi
```

### `{ref, str/int, N}` 输入控件取值

模态表单用 `{ref, str, N}` 获取文本输入、`{ref, int, N}` 获取下拉菜单选项索引。

详见 [programming/external.md#引用玩家对表单的响应](programming/external.md#引用玩家对表单的响应)。

---

## 指针系统

HPL 类型系统基础见 [programming/data_type.md](programming/data_type.md)。

### 为什么有指针

HPL 只原生支持 `int`、`float`、`str`、`bool` 四种类型。`map`、`slice`、`tuple`、`set` 等复杂类型无法像普通变量那样直接赋值和传递，只能通过**指针**（整数句柄）+ 内置函数间接操作：

```
// 不存在这种写法：
a_map = {'key': 'value'}

// 实际写法：maps.new 返回一个整数指针
a_map = {func, maps.new(False, 'key', 'value')}
```

### 指针的本质

指针是一个**整数句柄**。底层实现中，所有指针指向的对象存储在一个全局 `dict<int, object>` 中——指针的整数值就是这个 dict 的 key。

```python
# 底层伪代码（lib_object.py）
_objects = {}          # 全局对象池，key=指针整数, value=实际对象
_next_handle = 0

def alloc(obj):        # 分配新指针
    global _next_handle
    h = _next_handle
    _objects[h] = obj
    _next_handle += 1
    return h

def deref(ptr):        # 解引用：通过整数句柄拿回对象
    return _objects[ptr]

def release(ptr):      # 释放指针：从对象池中删除
    del _objects[ptr]
```

### 指针生命周期

**函数返回时自动释放**：`customfunction` 执行完毕后，其内部所有通过 `maps.new`、`slices.new` 等分配的指针会被自动释放（底层即 `del _objects[ptr]`）。因此，函数不能直接将内部创建的指针作为返回值传给调用方——调用方收到时句柄已失效。

**正确做法**：在传出指针前调用 `object.pin(ptr)`，阻止自动释放。调用方使用完毕后需手动 `object.finalise(ptr)`（对应 `pin`）或 `object.release(ptr)`（对应 `slices.new` 等）。

**释放的是句柄，不是对象**：`release` 只删除 dict 中的 key，不销毁 value。如果该对象被其他地方持有（如存入了 ExtraData），它继续存在。

**同 tick 内 pin 后的指针跨函数可用**：当前实现中，pin 过的指针在同一游戏刻（整个调用栈）内不会被回收，即使外层函数未再次 pin 也能使用。**但这个特性不标准，未来可能变更，不能依赖。**

### `maps.ptr_get` 的快照特性

`maps.ptr_get(mapPtr, keyPtr)` 返回的是**调用瞬间**该 key 对应的值的整数句柄。它不是"指向对象的实时引用"。如果之后该 key 对应的值发生改变，之前获取的句柄不会反映变化，它仍指向旧对象（如果旧对象未被回收）。

### ExtraData 持久化

`entity.SetExtraData(levelId, key, valuePtr)` 内部持有对象的独立引用。因此：
- 函数返回、指针被释放后，存入 ExtraData 的对象**不会丢失**
- 下次通过 `entity.GetExtraData(levelId, key)` 读取时，会返回一个新的指针指向该持久化对象

详见 [programming/external.md](programming/external.md)。

---

## 注意事项

### 1. `int(-2147483648)` 仅用于 `return` 语句

HPL bug 导致 `return` 语句无法直接返回 `-2147483648`，必须用 `int(-2147483648)` 包裹。其他所有场景直接用 `-2147483648`。

### 2. 函数体内禁用英文中括号和双引号

`customfunction` 的 body 解析依赖双引号定界，`build.py` 的 `compress()` 正则 `r'"((?:[^"\\]|\\.)*)"'` 无法处理嵌套双引号。

- 装饰性方括号 `[]` → 用全角 `【】`
- `say`/`title` 命令避免 `""` 空字符串拼接
- 字符串中避免英文双引号

### 3. 含 `/` 的函数名必须双引号包裹

```
customfunction add "data/mapGet" "..."
```

### 4. `execute` 命令优于 HPL 玩家循环

对于需要遍历所有在线玩家的操作，优先使用 `execute as @a[条件]` 命令，避免 HPL for 循环带来的性能开销。

### 5. 常用 API 返回值

以下 API 返回的指针均未 pin，函数退出时自动释放，无需手动 `release`（仅在函数内部需提前释放时手动调用）。

- `entity.GetRot(pid)` → 指向 `(pitch, yaw)` 元组的指针
- `entity.EntityHasTag(pid, tag)` → 指向布尔值的指针，用 `object.deref` 取值
- `entity.GetFootPos(pid)` → 指向 `(x, y, z)` 元组的指针
- `world.GetPlayerList()` → 指向玩家ID列表的指针
- `world.GetLevelId()` → 指向 level ID 的指针，用 `object.deref` 取值

### 6. 指针操作速查

| 操作 | 函数 | 说明 |
|---|---|---|
| 创建 map | `{func, maps.new(False, k, v, ...)}` | False=无默认值 |
| 读字段 | `{func, maps.get(ptr, 'key')}` | **key 不存在即崩溃** |
| 写字段 | `{func, maps.set(ptr, 'key', val)}` | 自动写入 |
| 检查 key | `{func, maps.exist(ptr, 'key')}` | 返回 bool |
| 获取长度 | `{func, maps.length(ptr)}` | 返回 int |
| 固定指针 | `{func, object.pin(ptr)}` | 阻止自动释放 |
| 释放固定 | `{func, object.finalise(ptr)}` | 对应 pin |
| 释放指针 | `{func, object.release(ptr)}` | 对应 new |
| 解引用 | `{func, object.deref(ptr)}` | 取出标量值 |
| 创建引用 | `{func, object.ref(val)}` | 包装标量为指针 |
| 判空 | `{func, object.is_none(ptr)}` | 返回 bool |

---

## API 参考

使用未知的 HPL 函数前，先查本地 API 文档或网易开发手册：

- 本地 API 文档：`所有fuc用法➕格式2.txt`
- 网易开发手册：https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/接口/世界/索引.html

---

## HPL 指令参考

### 表单管理 (`customform`)

详见 [commands/custom_form.md](commands/custom_form.md)。

```
customform add <name: string> long|popup|modal
customform list [name: string]
customform oncancel <name: string> <code: string> [onCodeError: string]
customform onsubmit <name: string> <code: string> [onCodeError: string]
customform remove <name: string>
customform save <name: string>
customform show <executor: target> <position: x y z> <player: target> <name: string>
customform style <player: target> [speed_40|...|speed_00]
customform close <player: target>
```

**重要提示：**

- `customform save` **必须执行**，否则表单配置在重进存档后丢失。未保存过的表单重进后连同配置一起消失。
- `customform oncancel` 中，如果关闭原因是「玩家在提交前退出游戏」，**不得打开新表单**，否则新表单永远不会得到回应，造成内存泄露。
- `customform show` 的前提是目标玩家**不忙**（不能已打开表单、聊天栏、命令方块、容器等）。不要在聊天栏内执行向自己打开表单的命令。反复执行 `customform show` 会导致服务器和玩家卡顿。
- `customform remove` 即使玩家正在交互也是安全的——已打开的表单仍可正常提交/关闭，且 onsubmit/oncancel 回调仍会执行。
- `customform close` 属于正常关闭（非因正忙），会触发 oncancel 回调。如果某表单正在打开但尚未完全打开，此命令不会关闭它。
- `customform style` 设置表单动画速度，一次性设置，玩家重进后恢复默认值 (speed_40)。不填枚举值则重置为默认。

### 长表单编辑 (`editlongform` / `editbutton` / `editlabel`)

详见 [commands/long_form.md](commands/long_form.md)。

```
editlongform <formName: string> append [button|label|header|divider]
editlongform <formName: string> content <contentCode: string>
editlongform <formName: string> insert <index: int> [button|label|header|divider]
editlongform <formName: string> list
editlongform <formName: string> pop left|right
editlongform <formName: string> sub keep|discard <startIndex: int> <endIndex: int>
editlongform <formName: string> title <titleCode: string>

editbutton <formName: string> <index: int> icon [textureCode: string]
editbutton <formName: string> <index: int> text <textCode: string>

editlabel <formName: string> <index: int> header <headerCode: string>
editlabel <formName: string> <index: int> label <labelCode: string>
```

**提示：** 分割线（divider）添加后无需进一步编辑。所有 `<*Code: string>` 参数都是一段 HPL 代码，返回值作为对应文本。元素索引从 0 开始。

### 模态表单编辑 (`editmodalform` / `editinput` / `edittoggle` / `editdropdown` / `editslider` / `editstepslider`)

详见 [commands/modal_form.md](commands/modal_form.md)。

```
editmodalform <formName: string> append label|header|divider|input|toggle|dropdown|slider|stepslider
editmodalform <formName: string> insert <index: int> label|header|divider|input|toggle|dropdown|slider|stepslider
editmodalform <formName: string> list
editmodalform <formName: string> pop left|right
editmodalform <formName: string> sub keep|discard <startIndex: int> <endIndex: int>
editmodalform <formName: string> title <titleCode: string>

editinput <formName: string> <index: int> default <defaultCode: string>
editinput <formName: string> <index: int> placeholder <placeHolderCode: string>
editinput <formName: string> <index: int> text <textCode: string>
editinput <formName: string> <index: int> tooltip [tooltipCode: string]

edittoggle <formName: string> <index: int> default <stateCode: string>
edittoggle <formName: string> <index: int> text <textCode: string>
edittoggle <formName: string> <index: int> tooltip [tooltipCode: string]

editdropdown <formName: string> <index: int> append <optionCode: string>
editdropdown <formName: string> <index: int> default <indexCode: string>
editdropdown <formName: string> <index: int> insert <index: int> <optionCode: string>
editdropdown <formName: string> <index: int> list
editdropdown <formName: string> <index: int> pop left|right
editdropdown <formName: string> <index: int> sub keep|discard <startIndex: int> <endIndex: int>
editdropdown <formName: string> <index: int> text <textCode: string>
editdropdown <formName: string> <index: int> tooltip [tooltipCode: string]

editslider <formName: string> <index: int> default <defaultCode: string>
editslider <formName: string> <index: int> min <minCode: string>
editslider <formName: string> <index: int> max <maxCode: string>
editslider <formName: string> <index: int> step <stepCode: string>
editslider <formName: string> <index: int> text <textCode: string>
editslider <formName: string> <index: int> tooltip [tooltipCode: string]

editstepslider <formName: string> <index: int> append <stepCode: string>
editstepslider <formName: string> <index: int> default <indexCode: string>
editstepslider <formName: string> <index: int> insert <index: int> <stepCode: string>
editstepslider <formName: string> <index: int> list
editstepslider <formName: string> <index: int> pop left|right
editstepslider <formName: string> <index: int> sub keep|discard <startIndex: int> <endIndex: int>
editstepslider <formName: string> <index: int> text <textCode: string>
editstepslider <formName: string> <index: int> tooltip [tooltipCode: string]
```

**提示：**
- 下拉框必须至少有 **1 个**选项；显式步进滑块必须至少有 **2 个**选项。
- 隐式步进滑块的最小值、最大值、步进长度构成等差数列；即使默认值不可达，系统也会修正到最近的可达值。如果步进长度不足以从最小值抵达最大值，系统确保玩家仍能取到最大值。
- `tooltip` 不填参数可清空已设置的灯泡提示文本。

### 信息表单编辑 (`editpopupform`)

详见 [commands/popup_form.md](commands/popup_form.md)。

```
editpopupform <formName: string> button1 <firstButtonCode: string>
editpopupform <formName: string> button2 <secondButtonCode: string>
editpopupform <formName: string> content <contentCode: string>
editpopupform <formName: string> title <titleCode: string>
```

### 自定义函数 (`customfunction`)

详见 [commands/custom_function.md](commands/custom_function.md)。

```
customfunction add <name: string> <code: string>
customfunction call <executor: target> <position: x y z> <name: string>
customfunction list [name: string]
customfunction remove <name: string>
```

**重要提示：**
- `<code: string>` 必须显式返回值（`return` 或隐式返回）。
- `customfunction call` 的命令执行维度继承自该指令执行时的维度，而非 `<executor: target>` 所在维度。命令执行者至多设置一个。
- 内部调用：`function.call('funcName', args...)` — 参数通过 `args` 元组传入，用 `tuple.get(args, n)` 按索引取值。
- **未传入任何参数时，变量 `args` 不存在**，访问会导致 `Variable "args" used before assignment` 错误。函数应约定固定的参数数量和类型。

### 系统事件 (`systemevent`)

详见 [commands/system_event.md](commands/system_event.md)。

```
systemevent destroy <funcName: string>
systemevent list [eventName: string]
systemevent listen <eventName: string> <funcName: string> <code: string> [onCodeError: string]
systemevent query <funcName: string>
```

**重要提示：**
- 事件回调中**必须手动设置命令执行上下文**（不同于 `customfunction call` 自动传入）。使用 `command.set_executor`、`command.set_position`、`command.set_dimension`、`command.fast_set`。
- 多个事件函数可侦听同一事件，共享 `args` map。执行顺序不保证，不应依赖顺序。
- `maps.set(args, 'cancel', True)` 可阻止同一事件下剩余未执行的事件函数；若 ModAPI 有特别说明，还可撤销事件本身。
- 可直接侦听最底层服务端事件，参见 [ModAPI 事件索引表](https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/事件/事件索引表.html)。

### 编译缓存 (`compilecache`)

详见 [commands/compile_cache.md](commands/compile_cache.md)。

```
compilecache compile <code: string>
compilecache query
compilecache set [size: int]
```

- 默认最大容量 2048。缓存命中可提升执行效率 20 倍以上。
- 不填 `[size: int]` 重置为默认值。容量过小降低效率，过大增加内存占用。

### 命令方块输出 (`commandblockoutput`)

详见 [commands/command_block_output.md](commands/command_block_output.md)。

```
commandblockoutput <commandBlockPosition: x y z>
```

用于查看命令方块中 HPL 代码的完整报错信息（超出命令方块 UI 显示范围时使用）。不能查看原版指令执行日志。

---

## 表单响应读取 (`{ref}`)

详见 [programming/external.md#引用玩家对表单的响应](programming/external.md#引用玩家对表单的响应)。

### 模态表单 (modal)

```
{ref, <type>, <index>}
```

`<type>` 为 `int`/`bool`/`float`/`str`，`<index>` 为元素序号（从 0 开始）。

各元素对应的响应类型：

| 元素 | 响应类型 | 说明 |
|---|---|---|
| 普通文本/大字文本/分割线 | 空值 | 不可读取（无意义） |
| 输入框 | `str` | 用户输入内容 |
| 开关 | `bool` | True=开, False=关 |
| 下拉框 | `int` | 选中选项的索引 |
| 隐式步进滑块 | `float` | 滑块当前刻度值 |
| 显式步进滑块 | `int` | 选中选项的索引 |

类型不匹配会报错——系统会检查实际响应类型与你期望的类型是否一致。

### 长表单 (long)

```
{ref, int, -1}   — 获取被点击按钮的索引（只计按钮，不计其他元素）
{ref, bool, T}   — 检查被点击按钮索引是否等于 T
```

按钮索引仅计按钮，分割线/文本等不占序号。注意与 `editbutton` 的元素统一索引区分。

### 信息表单 (popup)

```
{ref, bool, -1}  — True=点击确定, False=点击取消
{ref, bool, 1}   — 检查是否点击确定
{ref, bool, 0}   — 检查是否点击取消
```

### 表单关闭

在 `customform oncancel` 回调中使用：

```
{ref, int, -1}   — 获取关闭原因码
{ref, bool, T}   — 检查关闭原因码是否等于 T
```

| 原因码 | 含义 |
|---|---|
| 0 | 玩家手动关闭（点叉号） |
| 1 | 玩家正忙（聊天栏等） |
| 2 | 玩家在提交前退出游戏 |

---

## 外部交互语句

详见 [programming/external.md](programming/external.md)。

### `{selector, <target: str>}` — 解析目标选择器

将目标选择器解析为实体名，返回字符串。多个实体以 `, ` 分隔。无匹配实体返回空字符串。只能以命令执行者位置为参考点选取目标。

### `{score, <player: str>, <scoreboard: str>}` — 获取记分板分数

返回整数。`<player>` 可用 `*` 或 `@s` 指代命令执行者。指向多个玩家时返回分数之和。玩家不存在或未在目标记分板有分数时返回 0。只能以命令执行者位置为参考点。

### `{command, <commandLine: str>}` — 执行命令

在当前命令执行上下文中执行命令，返回整数（命令成功次数，只可能为 0 或 1）。

限制：命令执行者必须是实体；命令执行点无法传递（采用命令执行者位置）；命令执行朝向无法传递。

---

## 命令执行上下文

详见 [programming/external.md](programming/external.md)。

### 事件中手动设置上下文

事件回调中没有自动传入的命令执行上下文，需手动设置：

```hpl
_ = {func, command.set_executor(executor: str)}         // → bool
_ = {func, command.set_position(x: float, y: float, z: float)}  // → bool
_ = {func, command.set_dimension(dim_id: int)}           // → bool
_ = {func, command.fast_set(selector_or_entity_id: str, is_selector: bool = True)}  // → bool
```

### 获取当前上下文

```hpl
command.get_executor()       // → str (实体ID)
command.get_position()       // → ptr@tuple[float, float, float]
command.get_dimension()      // → int (维度数字ID)
command.dimension_name()     // → str (维度英文ID)
```

### 维度 ID 对照

| 维度 | 英文 ID | 数字 ID |
|---|---|---|
| 主世界 | overworld | 0 |
| 下界 | nether | 1 |
| 末地 | the_end | 2 |
| dm3 ~ dm20 | dm3 ~ dm20 | 3 ~ 20 |

---

## 数据类型与运算符

详见 [programming/data_type.md](programming/data_type.md) 和 [programming/compute.md](programming/compute.md)。

### 基本类型

| 类型 | 说明 | 范围/值 |
|---|---|---|
| `int` | 整数 | -2147483648 ~ 2147483647 |
| `float` | 浮点数（小数） | — |
| `bool` | 布尔值 | `True` / `False` |
| `str` | 字符串 | 用单引号 `'` 包裹 |

### 转义规则

| 转义符 | 含义 |
|---|---|
| `\n` | 换行 |
| `\\` | 反斜杠 `\` |
| `\'` | 单引号 |
| `\"` | 双引号 |

`
` 等 Unicode 转义不支持，仅支持反斜杠后 1 个字符。

**命令方块中的双层转义：** 源代码用双引号 `"` 包裹时，内部转义需双重转义。如字符串内需表示 `\'`，命令方块中需写 `\\'`。

### 运算符优先级（高→低）

1. `in` — 成员检查
2. `not` — 取反
3. `and` — 与运算（短路：遇假即停）
4. `or` — 或运算（短路：遇真即停）

算术运算符优先级与标准四则运算一致。比较运算符（`>` `<` `>=` `<=` `==` `!=`）**不能连用**，必须用 `and`/`or` 连接（如 `1 < 10 and 10 < 100`）。

### 算术运算

| 运算符 | 说明 | 结果类型 |
|---|---|---|
| `+` `-` `*` | 加减乘 | 任一操作数为 float 则结果为 float，否则 int |
| `/` | 除 | 结果一定是 float |

### 字符串运算

| 运算符 | 说明 |
|---|---|
| `+` | 拼接 |
| `*` | 重复（`'ak' * 5` → `'akakakakak'`） |
| `==` `!=` | 相等/不等比较 |
| `in` | 包含检查（`'饭' in '吃饭了'` → `True`） |

字符串支持 `>` `<` `>=` `<=` 比较，按字典序逐字符比较。

### 强制类型转换

| 语法 | 等价简写 |
|---|---|
| `int(...)` | `{func, int(...)}` |
| `bool(...)` | `{func, bool(...)}` |
| `float(...)` | `{func, float(...)}` |
| `str(...)` | `{func, str(...)}` |

关键规则：**所有不等于 0 的值转 bool 均为 `True`**，仅 0 / 0.0 / -0 / -0.0 为 `False`。非空字符串（包括 `'False'`、`''`? 注：`''` 空字符串转 bool 为 `True`）转 bool 均为 `True`。

整数转换：`int('5.99')` 报错（不能直接转带小数的字符串），需先 `float` 再 `int`。`int(5.99)` → `5`（截断）。

---

## 控制流

详见 [programming/statement.md](programming/statement.md)。

### 变量与赋值

```hpl
变量名 = 表达式
```

变量名不能以数字开头、不能含标点符号、不能使用保留关键字。变量可储存任意基本类型，但无类型声明——类型由赋值决定，后续可赋不同类型值。

### 保留关键字

`int` `bool` `str` `float` `ref` `selector` `score` `command` `func` `return` `if` `else` `elif` `fi` `for` `continue` `break` `rof` `and` `or` `not` `in` `True` `False`

### 条件语句

```hpl
if 条件:
  代码块
elif 条件:
  代码块
else:
  代码块
fi
```

`elif` 和 `else` 可选。条件按顺序检查，命中即执行，后续不再检查。`fi` 必须闭合。

### 循环语句

```hpl
for 循环变量, 循环次数:
  循环体
  continue   // 跳过本轮剩余代码，进入下一轮
  break      // 终止整个循环
rof
```

循环变量从 0 开始，每轮递增 1。循环次数为表达式，求值结果应为整数。`continue`/`break` 只能在循环内使用，只作用于所在的那层循环。嵌套循环应注意性能。

### 返回语句

```hpl
return 表达式   // 返回表达式值并立即终止代码运行
```

**隐式返回：** 代码最后一行可以是一个单独的表达式（不带 `return`），其值作为整段代码运行结果。此方式不会终止运行（之后有 `return` 仍以 `return` 结果为准）。

```hpl
total = 0
for i, 25:
  total = total + i
rof
total            // 隐式返回 300
```

### 行内简写 (`|`)

`|` 等价于换行，可将多行代码压缩为一行：

```hpl
a = 0 | b = 1 | c = 2
```

压缩以增强可读性为目的，不应将所有代码压缩为一行。
