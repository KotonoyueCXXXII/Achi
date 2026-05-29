# 表单指令 — 创建、配置、显示和关闭 UI 表单
> Prerequisite: [HPL 编程基础](../programming/overview.md)

# 指令概览
```mcfunction
customform add <name: string> long|popup|modal
customform list [name: string]
customform oncancel <name: string> <code: string> [onCodeError: string]
customform onsubmit <name: string> <code: string> [onCodeError: string]
customform remove <name: string>
customform save <name: string>
customform show <executor: target> <position: x y z> <player: target> <name: string>
customform style <player: target> [speed_40|speed_35|speed_30|speed_25|speed_20|speed_15|speed_10|speed_05|speed_00]
customform close <player: target>
```



# 添加表单
## 语法
```mcfunction
customform add <name: string> long|popup|modal
```

类型：`long`（长表单）、`popup`（信息表单）、`modal`（模态表单）。

## 示例
```mcfunction
customform add ABC long
customform add test popup
customform add 你好 modal
```



# 列出表单
## 语法
```mcfunction
customform list [name: string]
```
列出所有表单的类型，或仅查询指定表单的类型。



# 当表单被关闭时
## 语法
```mcfunction
customform oncancel <name: string> <code: string> [onCodeError: string]
```

| 参数 | 数据类型 | 备注 |
|---|---|---|
| `<name: string>` | 字符串 | 目标表单名 |
| `<code: string>` | 字符串 | 关闭时执行的代码 |
| `[onCodeError: string]` | 字符串 | 选填，代码出错时执行的代码 |

## 备注
表单被关闭的原因：玩家点击叉号、玩家正忙（如打开聊天栏）、提交前退出游戏。

如果关闭是因为玩家退出游戏，`<code: string>` 和 `[onCodeError: string]` 中不应向玩家打开新表单（将导致内存泄露）。

查询关闭原因见 [编程语法 § 引用玩家对表单的响应 § 表单的关闭](../programming/external.md#表单的关闭)。

## 示例
```mcfunction
customform oncancel alice

"
reason = {ref, int, -1}
{command, 'say 表单被关闭了，原因是 ' + str(reason)}
0/0
"

"
{command, 'say 错误: ' + str(error)}
"
```



# 当表单被提交时
## 语法
```mcfunction
customform onsubmit <name: string> <code: string> [onCodeError: string]
```

| 参数 | 数据类型 | 备注 |
|---|---|---|
| `<name: string>` | 字符串 | 目标表单名 |
| `<code: string>` | 字符串 | 提交时执行的代码 |
| `[onCodeError: string]` | 字符串 | 选填，代码出错时执行的代码 |

## 备注
- 长表单：点击任何按钮（非叉号）视为提交
- 信息表单：点击"确定"或"取消"视为提交
- 模态表单：点击"提交"按钮视为提交

读取提交数据见 [编程语法 § 引用玩家对表单的响应](../programming/external.md#引用玩家对表单的响应)。



# 移除表单
## 语法
```mcfunction
customform remove <name: string>
```

移除后，已打开该表单的玩家仍可正常提交或关闭，onsubmit/oncancel 代码仍会执行。

## 示例
```mcfunction
customform remove Steve
customform remove "233"
```



# 保存表单
## 语法
```mcfunction
customform save <name: string>
```
将表单配置保存到磁盘。不保存则重进存档后新配置丢失，未保存过的表单重进后完全消失。



# 显示表单
## 语法
```mcfunction
customform show <executor: target> <position: x y z> <player: target> <name: string>
```

| 参数 | 数据类型 | 备注 |
|---|---|---|
| `<executor: target>` | 目标选择器 | 命令执行者 |
| `<position: x y z>` | 坐标 | 命令执行点 |
| `<player: target>` | 目标选择器 | 向谁显示表单 |
| `<name: string>` | 字符串 | 表单名 |

## 备注
表单内容由代码构建，需要执行上下文（如获取实体名或分数），因此需指定执行者和执行点。维度自动采用当前命令执行维度。

表单一旦构建完成即为静态，重新打开才会更新内容。

目标玩家正忙时（已打开表单、聊天栏、容器等）无法显示。应通过命令方块执行，避免在聊天栏中自行触发。短时间内频繁显示会造成卡顿。

执行者至多设置一个，多个执行者将导致失败。



# 更新表单样式
## 语法
```mcfunction
customform style <player: target> [speed_40|...|speed_00]
```
设置表单动画速度（可选，不填则恢复默认值）。速度值越大动画越慢，`speed_00` 为即时显示。设置一次性的，重进游戏恢复默认。



# 强制关闭表单
## 语法
```mcfunction
customform close <player: target>
```
强制关闭指定玩家已打开的表单。这是正常关闭，会触发 oncancel 代码。正在打开中的表单无法以此关闭。如果新表单正在打开过程中，可借此在打开前阻止。
