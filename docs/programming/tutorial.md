# 模式参考 — 紧凑代码参考

> 适用场景: 已了解基本语法，需要快速查阅常见编程模式。
> 语法细节见 [statement.md](statement.md)、[expression.md](expression.md)、[compute.md](compute.md)。

## 模式一：条件分支中的类型转换

**问题：** 将 0–999999 的数字补齐为 6 位（前导零补全）。

**关键规则：**

| 规则 | 说明 |
|---|---|
| 类型隔离 | `int` 与 `str` 不能比较（`10 <= "abc"` 报错）、不能拼接（`"00" + 233` 报错） |
| 结果变量分离 | 用独立变量保存结果，避免覆盖原变量后导致后续条件语句类型失败 |
| if/elif 匹配顺序 | 从上到下，先匹配先生效——范围最大的条件放最前 |
| elif 等价形式 | `elif` = 嵌套 `else { if ... }`，两者语义等同 |

**最终代码（正确形式）：**
```python
number = 233
result = ''

if 100000 <= number:
    result = str(number)
elif 10000 <= number:
    result = '0' + str(number)
elif 1000 <= number:
    result = '00' + str(number)
elif 100 <= number:
    result = '000' + str(number)
elif 10 <= number:
    result = '0000' + str(number)
elif 0 <= number:
    result = '00000' + str(number)
fi

return result
```

**常见错误：**

| 错误 | 原因 | 示例 |
|---|---|---|
| 条件顺序反转 | `0 <= number` 匹配所有值，后续分支永不执行 | 将最小范围条件放前面 |
| 修改原变量 | `number = '0' + str(number)` 后 `number` 变为 `str`，后续 `number <= 99` 报错 | 始终用独立 `result` 变量 |

---

## 模式二：字符串重复与循环生成

**核心操作符：** `*` — 字符串重复。`'*' * 3` → `***`，`' ' * 5` → `     `（5 空格）。

**核心公式（对称三角形/菱形）：**

| 变量 | 公式 | 说明 |
|---|---|---|
| `star` | `2*i + 1` | 第 i 行（0-indexed）的星号数 |
| `space` | `(total - star) / 2` | 居中所需前导空格数 |
| `total` | `2*repeat - 1` | 最宽行的星号数 |

**菱形生成（完整代码）：**
```python
repeat = 6
total = 2*repeat - 1

for i, repeat:
    star = 2*i + 1
    space = int((total-star)/2)
    line = 'say ' + ' '*space + '*'*star + ' '*space
    {command, line}
rof

for i, repeat-1:
    star = 2*(repeat-(i+1)) - 1
    space = int((total-star)/2)
    line = 'say ' + ' '*space + '*'*star + ' '*space
    {command, line}
rof
```

**常用形状速查：**

| 形状 | 循环形式 | star 变化 | 输出特征 |
|---|---|---|---|
| 上三角（左对齐） | `for _, repeat:` | `star + 2` | 第 1 行 1 个星，逐行 +2 |
| 下三角（左对齐） | `for _, repeat:` | `star - 2` | 从最宽开始，逐行 −2 |
| 上三角（居中） | `for i, repeat:` | `2*i + 1` | `space` 前导空格居中 |
| 下三角（居中） | `for i, repeat:` | `2*(repeat-i) - 1` | 同上，递减 |
| 菱形 | 上三角 + 下三角 | 上增下减 | 两个 for 循环拼接 |

**Command 语句：** `{command, line}` 将变量 `line` 的内容作为 Minecraft 指令执行（如 `say ***`）。
