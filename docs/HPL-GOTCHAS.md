# HPL 易错点速查

本文档集中记录 AI 生成 HPL 代码时**最容易写错**的模式。每条包含错误示例和正确示例——先看错在哪，再看怎么写。

- HPL 语言完整语法 → [HPL-参考.md](HPL-参考.md)
- 项目编码规范 → [CLAUDE.md](../CLAUDE.md)
- ExtraData 域结构 → [数据结构参考.md](数据结构参考.md)
- 复杂类型与指针操作 → [复杂类型操作指南.md](复杂类型操作指南.md)

---

## 指针与内存

> HPL 指针系统基础（生命周期、pin/finalise/release 机制、ExtraData 持久化）见 [HPL-参考.md — 指针系统](HPL-参考.md)。以下为项目代码中最常见的指针误用模式。

### 1. `maps.set` 存复杂类型 → 悬垂引用

**WRONG：** 用 `maps.set` 存 map/tuple/slice/set 指针
```hpl
innerMap = {func, maps.new(False)}
_ = {func, maps.set(outerMap, 'key', innerMap)}
// 函数返回后 innerMap 句柄释放，outerMap.key 变成悬垂引用 → 后续读取崩溃
```

**RIGHT：** 复杂类型必须用 `maps.ptr_set`
```hpl
innerMap = {func, maps.new(False)}
_ = {func, maps.ptr_set(outerMap, {func, object.ref('key')}, innerMap)}
```

### 2. `maps.get` 读不存在的 key → 直接崩溃

**WRONG：**
```hpl
value = {func, maps.get(data, 'maybeMissing')}
```

**RIGHT：** 必须先用 `maps.exist` 守卫
```hpl
if {func, maps.exist(data, 'maybeMissing')}:
  value = {func, maps.get(data, 'maybeMissing')}
fi
```

### 3. `ptrMapGet` / `queue/peek` 返回的指针忘了 finalise → 内存泄漏

`data/ptrMapGet` 和 `queue/peek` 内部调用了 `object.pin()`，返回的指针**必须** `object.finalise`。

**WRONG：**
```hpl
playerData = {func, function.call('data/ptrMapGet', 'data.player.archive', playerId)}
privilege = {func, maps.get(playerData, 'privilegeLevel')}
return True
```

**RIGHT：**
```hpl
playerData = {func, function.call('data/ptrMapGet', 'data.player.archive', playerId)}
if playerData == -2147483648:
  return True
fi
privilege = {func, maps.get(playerData, 'privilegeLevel')}
_ = {func, object.finalise(playerData)}
return True
```

### 4. `finalise(-2147483648)` → 崩溃

sentinel 值不是有效指针，传入 `object.finalise` 直接崩溃。必须先判空再 finalise。

### 5. 父 map 写入顺序反了 → 写入的是空 map

子 map 必须先填充数据，再用 `ptr_set` 写入父 map。顺序不能反。

**WRONG：**
```hpl
_ = {func, maps.ptr_set(playerData, {func, object.ref('anchors')}, anchorsMap)}
_ = {func, maps.ptr_set(anchorsMap, {func, object.ref(slot)}, posTuple)}
// anchorsMap 先存入 playerData 时还是空的，后续写入不会同步到已存入的副本
```

**RIGHT：**
```hpl
_ = {func, maps.ptr_set(anchorsMap, {func, object.ref(slot)}, posTuple)}
_ = {func, maps.ptr_set(playerData, {func, object.ref('anchors')}, anchorsMap)}
```

### 6. `maps.new` / `maps.ptr_get` 返回的指针不需要 finalise

这些函数不 pin，函数返回时自动释放。只有 `data/ptrMapGet` 和 `queue/peek` 返回的指针需要 finalise。

---

## 数据存取

### 7. 二层域和三层域用错存取函数

| 域类型 | 读取用 | 写入用 |
|---|---|---|
| 二层（value 是 int/string） | `data/mapGet` | `data/mapSet` |
| 三层（value 是 map 指针） | `data/ptrMapGet` | `data/ptrMapSet` |

**WRONG：** 对三层域用 `data/mapGet` → 拿不到指针，拿到的是 int 句柄（悬垂）

### 8. 用 `maps.set(ptr, key, -2147483648)` 伪装删除

`maps.set` 存的是 int 值，不会清理指针引用。残留的悬垂指针在后续 `ptr_get` 时崩溃。同理，对队列槽位用 `maps.ptr_set` 写入 sentinel 来"清空"也不安全，应使用 `queue/pop` 正确移除。

**用 `maps.del`（标量）或 `maps.ptr_del`（指针）正确删除；队列元素用 `queue/pop` 正确移除。**

---

## 语法陷阱

> HPL 基础语法（条件语句、循环、运算符、类型转换、转义规则）见 [HPL-参考.md](HPL-参考.md) 的**控制流**、**数据类型与运算符**、**注意事项**章节。以下仅列参考文档未覆盖或 AI 仍频繁写错的项目特定陷阱。

### 9. `return -2147483648` 不写 `int()` 包装

HPL 编译器 bug：`return` 语句无法直接返回 `-2147483648` 字面量。

**WRONG：**
```hpl
return -2147483648
```

**RIGHT：**
```hpl
return int(-2147483648)
```

**注意：** `int()` 包装仅在 `return` 语句中需要。函数体内的判断、赋值、比较均使用裸值 `-2147483648`。

### 10. 字符串参数变量含特殊符号时用双引号括起，函数体内双引号用 `\` 转义

`say` 是 MC 指令，通过 `{command, ...}` 语句或 `command.set_command()` 接口执行。`say` 指令后面的字符串如果包含方括号、空格等特殊符号，必须用双引号括起，否则 HPL 解析器会将其误认为语法元素。函数体内双引号用 `\"` 转义。此规则适用于所有表单类型（长表单、模态表单、弹窗）的 onsubmit/oncancel 代码块，因为它们在编译后代码块被包装在双引号内。

**WRONG：**
```hpl
{command, 'say [提示] 你好'}
```

**RIGHT：**
```hpl
{command, 'say \"[提示] 你好\"'}
```

`feedback` 同理：

**WRONG：**
```hpl
_ = {func, function.call('entry/feedback', '[系统] 操作成功')}
```

**RIGHT：**
```hpl
_ = {func, function.call('entry/feedback', '\"[系统] 操作成功\"')}
```

---

## 构建系统

### 11. 新增事件/表单文件后忘了注册

新增 `.hpl` 文件后必须同步更新 `scripts/config.py`：
- 事件 → `EVENT_MAP` 添加映射
- 表单 → `FORM_TYPE_MAP` 添加映射

构建时 `KeyError` 即表示遗漏注册。**不编译未注册的文件。**

### 12. 多行字符串中的 `//` 注释

以 `//` 开头的行在构建时被 `compress()` 丢弃。行尾 `//`（非行首）会保留。

```hpl
customform onsubmit FORM_NAME "
// 这行会被构建时丢弃
text = text + '\\n'  // 这个行尾注释会保留
return text
"
```

### 13. `&(formName)` 自引用占位符

表单文件中指向自身的引用用 `&(formName)`，构建时自动替换。交叉引用（指向其他表单）仍用显式表单名。

```hpl
editlongform &(formName) content "..."
customform onsubmit &(formName) "..."
```

---

## 返回值约定

### 14. `queue/pop` 和 `data/mapExist` 返回 True/False，不是 sentinel

与其他函数返回 `-2147483648` 表示"不存在"不同，`queue/pop` 和 `data/mapExist` 返回布尔值。调用方不能拿 `== -2147483648` 来判断结果。

### 15. `data/mapSet`、`data/ptrMapSet` 始终返回 True，`data/mapDel`、`data/ptrMapDel` 始终返回 False

这些函数的返回值是固定的，不反映操作是否成功。调用方不应依赖其返回值判断操作结果。

### 16. 项目函数统一 sentinel

`data/mapGet`、`data/mapKeyOf`、`data/ptrMapGet`、`queue/peek`、`queue/push`、`land/getFreeIndex` 在"未找到"时统一返回 `-2147483648`。调用方以此判断是否命中。

---

## 事件与表单通用

> `customform` 指令语法、`save`/`show` 注意事项、事件回调上下文设置见 [HPL-参考.md](HPL-参考.md) 的**命令执行上下文**和**HPL 指令参考**章节。以下仅列参考文档中未强调的项目特定陷阱。

### 17. 事件回调没有自动命令上下文

`systemevent` 回调中 `command.get_executor()` 返回 `None`，**必须手动设置**：

```hpl
_ = {func, command.set_executor(playerId)}
```

（`customfunction call` 会自动传入上下文，不需要手动设置。）

---

## 模态表单（modal form）易错点

> 模态表单指令语法及控件 ref 类型见 [HPL-参考.md](HPL-参考.md) 的**表单响应读取**和**模态表单编辑**章节。以下为 AI 最常写错的模式。

### 18. 控件索引 N 是元素统一索引，label/header/divider 也占位

不同类型表单的onsubmit下的 `{ref, <type>, N}` 中 N 所指示的元素序号是不同的。参见 [programming/external.md — 索引体系对比](programming/external.md#索引体系对比)。

### 19. onsubmit 不一定是三段式 — 纯操作表单无按钮分发

模态表单 **没有按钮列表**，onsubmit 是线性顺序执行：读取控件值 → 验证 → 执行操作 → `return True`。**不写 if/elif 分支**。

这是与长表单最本质的区别——长表单的 onsubmit 是 `if {ref, bool, 0}: ... elif {ref, bool, 1}: ... fi`，模态表单没有这个结构。

### 20. onsubmit 后不一定导航离开

提交后玩家是否留在表单上取决于操作性质：
- **可重复操作（切换开关）→ 留在表单**，`return True` 即可
- **一次性操作（清除数据）→ 导航离开**，调用 `entry/navigate`

项目 4 个模态中 3 个留在表单（PERSONAL、ADMIN、MESSAGE），仅 DEBUG 导航离开。

**WRONG：** 每个模态表单都加 `entry/navigate` → 切换开关后跳走了，用户困惑

### 21. oncancel 必须存在 — 模态表单不能没有 oncancel

每个模态表单都必须定义 `customform oncancel`，导航回父表单。长表单可以省略 oncancel，模态表单不可以。

### 22. 不要给模态表单写 button1/button2/content — 那是 popup 的

`button1`、`button2`、`content` 是 `editpopupform`（弹窗表单）的指令，不是 `editmodalform` 的。模态表单设置标题用 `editmodalform ... title`。

**WRONG：**
```hpl
editmodalform &(formName) button1 "return '发送'"
editmodalform &(formName) content "return '标题'"
```

**模态表单没有自定义按钮文字——按钮始终是"提交"和"取消"。**

---

## 长表单（long form）易错点

> 长表单指令语法及 `{ref, int, -1}` / `{ref, bool, T}` 按钮分发机制见 [HPL-参考.md](HPL-参考.md) 的**表单响应读取**和**长表单编辑**章节。以下为 AI 最常写错的模式。

### 23. 混淆 `{ref, bool, N}` 按钮序号与 `editbutton` 元素索引

长表单有两套索引体系：`{ref, bool, N}` 的 N **仅计按钮**，`editbutton <form> <index>` 的 index 是**统一元素索引**。参见 [programming/external.md — 索引体系对比](programming/external.md#索引体系对比)。

**WRONG：** 用 `editbutton` 的元素索引去填 `{ref, bool, N}` → 中间有 divider/label 时序号错位

### 24. `editlabel` 同时用于 label 和 header

长表单没有 `editheader` 指令。普通文本和标题文本都用 `editlabel`，靠最后一个参数区分：

```hpl
editlabel &(formName) 0 label "return '普通文本'"
editlabel &(formName) 1 header "return '大字文本'"
```

**WRONG：** `editheader formName index "return 'text'"` → 指令不存在

### 25. 长表单只能用 4 种元素，不能加模态控件

长表单 `append` 只接受 `button|label|header|divider`。不能添加 toggle、input、dropdown、slider、stepslider——那些是模态表单专属。

**WRONG：**
```hpl
editlongform &(formName) append toggle
```

### 26. `oncancel` 对长表单是可选的

模态表单必须定义 `customform oncancel`，长表单可以省略。需要时（如返回父表单）才加。

---

## 弹窗表单（popup form）易错点

> 弹窗指令语法及 `{ref, bool, 1}` / `{ref, bool, 0}` 按钮分发见 [HPL-参考.md](HPL-参考.md) 的**表单响应读取**和**信息表单编辑**章节。以下为 AI 最常写错的模式。

### 27. 按钮 ref 索引：button1 是索引 1，button2 是索引 0

弹窗的 `{ref, bool, N}` 索引与直觉相反——**button1（确定）的点击状态在索引 1，button2（取消）在索引 0**。

```hpl
editpopupform &(formName) button1 "return '确定'"
editpopupform &(formName) button2 "return '取消'"

customform onsubmit &(formName) "
  if {ref, bool, 1}:       // button1（确定）被点击
    // 执行确认操作
  fi
  // button2（取消）通常不写 elif，直接关闭即可
"
```

**WRONG：** 用 `{ref, bool, 0}` 判断确定按钮 → 实际读到的是取消按钮状态

### 28. 弹窗只有 4 个指令：button1、button2、content、title

弹窗结构固定，没有 `append`、没有动态元素。

**WRONG：**
```hpl
editpopupform &(formName) append button   // 弹窗没有 append
```

### 29. 弹窗 onsubmit 通常只处理 button1，忽略 button2

取消按钮（button2）被点击时直接关闭表单，不需要额外处理。onsubmit 只写 `if {ref, bool, 1}:` 处理确定逻辑即可，不用写 elif 分支。`oncancel` 也不需要定义。
