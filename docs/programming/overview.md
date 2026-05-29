# 语法速查索引 — HPL 编程语言参考

> 按主题分组的快速导航，每项指向对应的完整参考文档。

## 数据类型

| 类型 | 字面量示例 | 说明 |
|---|---|---|
| `int` | `42`, `-1`, `0xFF` | 整数 |
| `float` | `3.14`, `-0.5` | 浮点数 |
| `bool` | `True`, `False` | 布尔值（首字母大写） |
| `str` | `"hello"`, `'world'` | 字符串（单/双引号均可） |
| `slice` | `[1, 2, 3]` | 数组/列表 |
| `map` | `{"key": "value"}` | 键值对映射 |
| `tuple` | `(1, "two", True)` | 元组（不可变） |
| `set` | `{1, 2, 3}` | 集合（无序唯一） |
| `none` | `None` | 空值 |

## 语法主题速查

| 主题 | 内容 | 文档 |
|---|---|---|
| 外部交互 | `command` 执行MC指令、`selector` 解析选择器、`score` 读记分板、`func` 调用API、`ref` 读表单响应 | [external.md](external.md) |
| 表达式求值 | 算术、逻辑、比较 | [expression.md](expression.md) |
| 计算与运算 | 运算符详解、优先级、类型转换 | [compute.md](compute.md) |
| 语句与控制流 | 变量赋值、if/elif/else、for 循环、return | [statement.md](statement.md) |
| 指针系统与复杂类型 | `object.ref`、pin/finalise/release、ptr_set vs set、map/slice/tuple/set 操作 | [../复杂类型操作指南.md](../复杂类型操作指南.md) |
| 常用编程模式 | 条件类型转换、字符串重复与循环生成 | [tutorial.md](tutorial.md) |
| 完整 API 参考 | 24 个模块 614 个系统/SDK 函数 | [..HPL-API-参考.md](../HPL-API-参考.md) |

## 关键语法要点

- **接口调用**：`{func, module.function, args...}` 是所有内置 API 的调用方式，五个外部交互语句（`command`、`selector`、`score`、`func`、`ref`）都遵循此模式
- **无分号，有闭合**：语句不以分号结尾；`if`/`elif`/`else` 以 `fi` 闭合，`for` 以 `rof` 闭合
- **复杂类型必须 ptr_set**：存入 map/slice/tuple/set 指针必须用 `ptr_set`，用 `set` 会导致悬垂引用
- **maps.get 前先 exist**：不存在的 key 直接 `get` 会崩溃，必须先 `maps.exist` 守卫
- **字符串引号**：单引号 `'...'` 双引号 `"..."` 均可；含 `[]`、空格的内容需双引号包裹，函数体内用 `\"` 转义
- **for 循环**：`for i, count:` — `i` 从 0 到 count-1，共 count 次迭代
- **类型转换**：`str()` / `int()` / `float()` / `bool()`
