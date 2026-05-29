# 系统事件指令 — 侦听和处理 Minecraft 游戏事件
> Prerequisite: [HPL 编程基础](../programming/overview.md)

# 指令概览
```mcfunction
systemevent destroy <funcName: string>
systemevent list [eventName: string]
systemevent listen <eventName: string> <funcName: string> <code: string> [onCodeError: string]
systemevent query <funcName: string>
```

# 侦听游戏事件
## 语法
```mcfunction
systemevent listen <eventName: string> <funcName: string> <code: string> [onCodeError: string]
```

| 参数 | 数据类型 | 备注 |
|---|---|---|
| `<eventName: string>` | 字符串 | 要侦听的游戏事件名（参见 [ModAPI 事件索引表](https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/事件/事件索引表.html)） |
| `<funcName: string>` | 字符串 | 事件函数名 |
| `<code: string>` | 字符串 | 事件触发时执行的代码 |
| `[onCodeError: string]` | 字符串 | 选填，出错时执行的代码 |

## 命令执行上下文

事件函数没有自动的命令执行上下文，需要手动设置：

```python
command.set_executor(executor: str) -> bool
command.set_position(posx: float, posy: float, posz: float) -> bool
command.set_dimension(dim_id: int) -> bool
command.fast_set(selector_or_entity_id: str, is_selector: bool = True) -> bool
```

```python
# 将上下文切换为 @a[r=3,c=1] 指示的玩家
_ = {func, command.fast_set('@a[r=3,c=1]')}

# 或分别指定执行者、位置、维度
_ = {func, command.set_executor('-666')}
_ = {func, command.set_position(2333, 0, 201.8)}
_ = {func, command.set_dimension(4)}
```

获取当前上下文：
```python
command.get_executor() -> str
command.get_position() -> ptr@tuple[float, float, float]
command.get_dimension() -> int
command.dimension_name() -> str
```

## 维度 ID 对照

| 维度 | ID |
|---|---|
| 主世界 (overworld) | 0 |
| 下界 (nether) | 1 |
| 末地 (the_end) | 2 |
| dm3 ~ dm20 | 3 ~ 20 |

## 事件取消与 args 共享

多个事件函数侦听同一事件时共享 `args` map。修改 `args` 会影响后续执行的事件函数。执行顺序不保证。

通过以下代码阻止后续事件函数执行（若 ModAPI 支持，还能撤销事件本身）：
```python
_ = {func, maps.set(args, 'cancel', True)}
```

## 示例
为聊天消息添加 VIP 前缀（基于玩家标签）：

```mcfunction
systemevent listen ServerChatEvent add_vip_chat_prefix

"
user_name = {func, maps.get(args, 'username')}
player_id = {func, maps.get(args, 'playerId')}

if {func, object.deref({func, entity.EntityHasTag(player_id, 'mvp_plus')})}:
  user_name = '§f[§dMVP§e+§f] ' + user_name
elif {func, object.deref({func, entity.EntityHasTag(player_id, 'mvp')})}:
  user_name = '§f[§cMVP§f] ' + user_name
elif {func, object.deref({func, entity.EntityHasTag(player_id, 'vip_plus')})}:
  user_name = '§f[§bVIP§e+§f] ' + user_name
elif {func, object.deref({func, entity.EntityHasTag(player_id, 'vip')})}:
  user_name = '§f[§aVIP§f] ' + user_name
fi

return {func, maps.set(args, 'username', user_name)}
"
```

# 销毁事件函数
## 语法
```mcfunction
systemevent destroy <funcName: string>
```

# 列出事件函数
## 语法
```mcfunction
systemevent list [eventName: string]
```
列出所有事件函数，或查询侦听在指定事件下的所有函数。

# 查询事件函数
## 语法
```mcfunction
systemevent query <funcName: string>
```
查询指定事件函数侦听在哪个游戏事件下。
