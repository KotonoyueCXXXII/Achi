# HPL 语言参考

NetEase Minecraft HPL（Hyper Packet Language）脚本系统速查。

## 导航

| 入口 | 覆盖内容 |
|---|---|
| [语法速查](programming/overview.md) | 数据类型、表达式、控制流、外部交互、常用模式 |
| [运算符速查](programming/compute.md) | 运算符优先级、算术、逻辑、类型转换 |
| [指令速查](commands/overview.md) | customform、editlongform、editmodalform、customfunction、systemevent 等所有指令 |

---

## 指针系统

HPL 只原生支持 `int`、`float`、`str`、`bool` 四种类型。`map`、`slice`、`tuple`、`set` 等复杂类型只能通过**指针**（整数句柄）+ 内置函数间接操作。

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

**函数返回时自动释放**：`customfunction` 执行完毕后，其内部所有通过 `maps.new`、`slices.new` 等分配的指针会被自动释放。函数不能直接将内部创建的指针作为返回值传给调用方。

**正确做法**：在传出指针前调用 `object.pin(ptr)`，阻止自动释放。调用方使用完毕后需手动 `object.finalise(ptr)`（对应 `pin`）或 `object.release(ptr)`（对应 `slices.new` 等）。

**释放的是句柄，不是对象**：`release` 只删除 dict 中的 key，不销毁 value。如果该对象被其他地方持有（如存入了 ExtraData），它继续存在。

**同 tick 内 pin 后的指针跨函数可用**：当前实现中，pin 过的指针在同一游戏刻内不会被回收。**但这个特性不标准，未来可能变更，不能依赖。**

### `maps.ptr_get` 的快照特性

`maps.ptr_get(mapPtr, keyPtr)` 返回的是**调用瞬间**该 key 对应的值的整数句柄，非实时引用。后续变化不反映。

### ExtraData 持久化

`entity.SetExtraData(levelId, key, valuePtr)` 内部持有对象的独立引用。函数返回、指针被释放后，存入 ExtraData 的对象不会丢失。下次读取时返回新指针指向该持久化对象。

---

## `{ref, bool, N}` 按钮分发

长表单 onsubmit 必须用此模式。**N 是按钮的连续序号（从 0 开始），仅计按钮**，`append divider`/`label`/`header` 不消耗 N。

`editbutton <form> <index>` 的 index 是元素统一索引（所有元素类型共享，divider 也占位），与 `{ref, bool, N}` 的按钮分发序号是**两套体系**。

```
append button   ← {ref, bool, 0}  editbutton 0
append button   ← {ref, bool, 1}  editbutton 1
append divider  ← 不可点击           editbutton 2
append button   ← {ref, bool, 2}  editbutton 3
```

索引体系完整对比见 [programming/external.md#索引体系对比](programming/external.md#索引体系对比)。

---

## 注意事项

- 函数体内禁用英文中括号 `[]` 和双引号 `"`，用全角 `【】` 替代
- 含 `/` 的函数名必须双引号包裹：`customfunction add "data/mapGet" "..."`
- 遍历玩家优先用 `execute as @a[条件]` 而非 HPL 循环（开发便利性建议）

---

## 速查引用

| 需要查什么 | 去哪看 |
|---|---|
| 转义规则（需转义：`n` `\` `'` `"`，不支持 `\u`） | [programming/data_type.md](programming/data_type.md) |
| 类型码速查（`ref_type` 0–8 + 0xFFFF） | [programming/data_type.md#类型码速查ref_type-返回值](programming/data_type.md#类型码速查ref_type-返回值) |
| 命令执行上下文（set_executor / get_executor / 维度 ID） | [programming/external.md](programming/external.md) |
| `{command}` vs `world.SetCommand` 对比 | [programming/external.md](programming/external.md) |
| 所有 HPL 内置函数 API（614 个函数） | [HPL-API-参考.md](HPL-API-参考.md) |
| Achi 项目 HPL 陷阱和反模式 | [HPL-GOTCHAS.md](HPL-GOTCHAS.md) |
