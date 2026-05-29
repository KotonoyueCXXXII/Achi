# 指令速查索引 — Minecraft HPL 表单及系统指令

> 按指令类别分组，每个条目指向对应的 API 参考文档。

## 表单类指令

| 指令组 | 核心操作 | 文档 |
|---|---|---|
| `customform` | 创建/列出/删除/展示表单，绑定回调 | [custom_form.md](custom_form.md) |
| `editlongform` + `editbutton` | 编辑长表单结构及按钮 | [long_form.md](long_form.md) |
| `editpopupform` | 编辑弹窗（信息表单）标题/内容/按钮 | [popup_form.md](popup_form.md) |
| `editmodalform` | 编辑模态表单结构 | [modal_form.md](modal_form.md) |
| `editinput` / `edittoggle` / `editdropdown` / `editslider` / `editstepslider` | 编辑模态表单控件（输入框/开关/下拉/滑块） | [modal_form.md](modal_form.md) |
| `editlabel` | 编辑长表单或模态表单中的文本元素 | [edit_label.md](edit_label.md) |

## 系统类指令

| 指令组 | 核心操作 | 文档 |
|---|---|---|
| `customfunction` | 注册/调用/删除自定义函数 | [custom_function.md](custom_function.md) |
| `systemevent` | 监听/销毁/查询服务器事件 | [system_event.md](system_event.md) |
| `compilecache` | 编译缓存管理 | [compile_cache.md](compile_cache.md) |
| `commandblockoutput` | 查询命令方块输出 | [command_block_output.md](command_block_output.md) |

## 通用约定

- `<name: string>` — 表单/函数名（全局唯一标识符）
- `<executor: target>` — 执行者（`@s` / `@p` / 玩家名）
- `<position: x y z>` — 坐标（如 `~ ~ ~`）
- `<code: string>` — HPL 代码字符串，用引号包裹
- 索引参数均从 0 开始计数
