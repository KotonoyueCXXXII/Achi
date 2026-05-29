# 外部交互参考 — selector、score、command、ref、func 语句

外部交互通过 `selector`、`score`、`command`、`ref`、`func` 实现。

- 均是表达式，有返回值，可直接嵌入任何需要值的位置
- `selector`/`score`/`command` 仅在能获取命令执行上下文的场合可用（onsubmit/oncancel/事件回调），`func`/`ref` 在所有 HPL 代码中可用
- `func` 是接口调用，其余四种是逗号分隔参数

详见 [expression.md](expression.md)。

# selector — 解析目标选择器

```
{selector, <target: str>}
```
将目标选择器解析为实体名字符串。多个实体以 `, ` 分隔，无匹配则返回空字符串。受限于网易接口，只能以命令执行者位置为参考点。

```python
{selector, '@p'}
{selector, '@e[type=zombie]'}
{selector, 'Alex'}
```

# score — 获取记分板分数

```
{score, <player: str>, <scoreboard: str>}
```
返回整数。`<player: str>` 支持目标选择器，`*` 或 `@s` 均指代命令执行者。无分数或玩家不存在时返回 0。指向多个玩家时返回分数之和。

```python
{score, '@s', 'coin'}
{score, '@a[r=10]', 'abc'}
```

# command — 执行 MC 指令

```
{command, <commandLine: str>}
```
在当前命令执行上下文中执行指令，返回成功次数（0 或 1）。执行者必须是实体，执行点和朝向无法传递。

```python
{command, 'say hello'}
{command, 'execute as @s at @s run say hello'}
```

## command vs world.SetCommand

| | `{command, cmd}` | `world.SetCommand(cmd, entityId, showOutput)` |
|---|---|---|
| 执行上下文 | 自动注入当前上下文 | 全部根据传入的 entityId |
| 底层实现 | 自动包装为 `execute as @s at @s in <dim> positioned <x> <y> <z> run <cmd>` | 原样执行 |
| 返回值 | int（0 或 1） | ptr（需 deref → bool） |
| 释放 | 无需 | 需 `object.release(ptr)` |

`command` 必须在已设置执行者（通过 `command.set_executor`）的上下文中使用，否则报错。

# ref — 读取表单响应

在 `onsubmit` 中获取玩家提交的数据，在 `oncancel` 中获取关闭原因。

## 索引体系对比

| 表单类型 | 语法 | N 的含义 |
|---|---|---|
| 模态表单 (modal) | `{ref, <type>, N}` | 元素统一索引（label/header/divider 都占位） |
| 长表单 (long) | `{ref, bool, N}` | 按钮序号（仅计 button） |
| 长表单 (long) | `{ref, int, -1}` | 获取被点击按钮的序号 |
| 信息表单 (popup) | `{ref, bool, -1}` | True=确定, False=取消 |
| 信息表单 (popup) | `{ref, bool, 1}` | 是否点击确定 |
| 信息表单 (popup) | `{ref, bool, 0}` | 是否点击取消 |
| 表单关闭 (oncancel) | `{ref, int, -1}` | 关闭原因：0=手动关闭, 1=正忙, 2=退出游戏 |
| 表单关闭 (oncancel) | `{ref, bool, T}` | 关闭原因是否等于 T |

`editbutton <form> <index>` 的 index 是元素统一索引，与长表单 `{ref, bool, N}` 的按钮序号是两套独立体系。

## 模态表单

元素有序存储，各类型对应的 ref 数据类型：

| 元素 | ref 类型 | 返回值 |
|---|---|---|
| label, header, divider | — | 不可获取 |
| input | `str` | 用户输入内容 |
| toggle | `bool` | True=开, False=关 |
| dropdown | `int` | 选中选项的索引 |
| slider | `float` | 滑块当前刻度值 |
| stepslider | `int` | 选中选项的索引 |

```python
{ref, bool, 4}   # 第5个元素（开关）
{ref, str, 7}    # 第8个元素（输入框）
{ref, float, 5}  # 第6个元素（隐式滑块）
{ref, int, 8}    # 第9个元素（下拉框/显式滑块）
```

## 长表单

仅按钮可点击。`{ref, int, -1}` 返回被点击按钮的序号（仅计按钮）。`{ref, bool, T}` 检查按钮序号是否等于 T。

## 信息表单

仅两个按钮。`{ref, bool, -1}` 获取点击结果。`{ref, bool, 1}` 检查是否确定。

# func — 接口调用

```
{func, funcName(arg1, arg2, ..., argN)}
```

调用内置 API 或自定义函数。函数名直接写出，参数是 HPL 支持的数据类型。

```python
{func, math.sqrt(4)}
{func, math.pow(2, 3)}
{func, function.call('my_func', arg1, arg2)}
```
