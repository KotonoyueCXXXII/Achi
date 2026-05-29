# 语句参考 — HPL 变量、控制流与返回

> 所有语句语法的紧凑参考。表达式与运算见 [compute.md](compute.md) 和 [expression.md](expression.md)。

## 变量与赋值

**语法：** `变量名 = 表达式`

将右侧表达式的求值结果保存到左侧变量中。变量可存储 int、bool、float、str。

**基本类型赋值：**
```python
a = 0          # int
b = True       # bool
c = 1.5        # float
d = 'hello'    # str
```

**表达式作为值：** 任何语句的返回值都可赋值——Score、Selector、Command、Ref、Func、类型转换、算术/逻辑/字符串运算均可出现在 `=` 右侧。

```python
part_a = 'tag=回城'
scoreboard = '音效分数'
my_score = {score, '@s[' + part_a + ']', scoreboard}
my_name = {selector, '@s[' + part_a + ',tag=!op]'}
```

**变量重新赋值：** 右侧表达式可使用变量当前值，支持自更新。

```python
a = 1
a = a + 1    # a = 2
a = a + 2    # a = 4
```

**保留关键字（不可作变量名）：**
`int`, `bool`, `str`, `float`, `ref`, `selector`, `score`, `command`, `func`, `return`, `if`, `else`, `elif`, `fi`, `for`, `continue`, `break`, `rof`, `and`, `or`, `not`, `in`, `True`, `False`

变量名不可数字开头、不可含标点符号。下划线 `_` 允许（如 `command_a`），但不保证未来兼容性。

---

## 条件语句

**语法：**
```python
if 条件1:
    代码块1
elif 条件2:
    代码块2
else:
    代码块3
fi
```

- 条件按顺序检查，第一个为 `True` 的分支执行后，其余全部跳过
- `elif` = `else if`（否则如果）
- `else` 和 `elif` 均可省略
- 支持任意层级嵌套
- 必须以 `fi` 闭合

**示例：日期推算（2025/12/31 → 2026/1/1）**

```python
year = 2025
month = 12
day = 31

if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
    # 大月
    if day == 31:
        if month == 12:
            year = year + 1
            month = 1
        else:
            month = month + 1
        fi
        day = 1
    else:
        day = day + 1
    fi
elif month == 2:
    # 二月：闰年判断
    is_leap = year/4==int(year/4) and not year/100==int(year/100) or year/400==int(year/400)
    if is_leap:
        if day == 29:
            month = 3
            day = 1
        else:
            day = day + 1
        fi
    else:
        if day == 28:
            month = 3
            day = 1
        else:
            day = day + 1
        fi
    fi
else:
    # 小月（4/6/9/11）
    if day == 30:
        month = month + 1
        day = 1
    else:
        day = day + 1
    fi
fi
```

---

## 循环语句

**语法：**
```python
for 循环变量, 循环次数:
    循环体
rof
```

- `循环次数` — 表达式，求值结果必须为 int
- `循环变量` — int，从 0 开始，每轮 +1（第 k 轮 = k−1）
- `_` 作为循环变量名约定：表示循环变量不使用
- `continue` — 跳过本轮剩余代码，立即进入下一轮
- `break` — 终止整个循环，不执行剩余轮次
- `continue`/`break` 仅在所在层生效，不影响外层循环

**示例一：累加 0+1+...+24**
```python
total = 0
for i, 25:
    total = total + i
rof
# total = 300
```

**示例二：斐波那契数列 — 前 31 项偶数之和**
```python
a = 0
b = 1
total = 0

for _, 30:
    temp = a
    a = b
    b = temp + b
    if a/2 == int(a/2):
        total = total + a
    fi
rof
```

等价写法（使用 continue）：
```python
for _, 30:
    temp = a
    a = b
    b = temp + b
    if a/2 != int(a/2):
        continue
    fi
    total = total + a
rof
```

**示例三：斐波那契和首次超过 50000 时 break**
```python
a = 0
b = 1
total = 1
counter = 0

for _, 30:
    temp = a
    a = b
    b = temp + b
    total = total + a
    if total > 50000:
        break
    fi
    counter = counter + 1
rof
# counter = 最大未超过 50000 的项数
```

**示例四：嵌套循环**
```python
result = 0
for _, 10:
    for _, 10:
        result = result + 1
    rof
rof
# result = 100
```

嵌套循环中 `break` 只终止最内层循环：
```python
result = 0
for _, 10:
    for _, 20:
        result = result + 1
        break          # 只终止内层，外层仍执行 10 次
    rof
rof
# result = 10
```

---

## 返回语句

**语法：** `return 表达式`

对表达式求值，将其作为整段代码的运行结果，并立即终止代码执行。

**隐式返回：** 可将表达式单独写在一行（不加 `return`），该表达式的值会成为运行结果，但代码**不会终止**——后续代码继续执行，如遇到显式 `return` 则以它为准。

```python
# 显式 return — 代码终止，返回 28
total = 0
for i, 25:
    total = total + i
    if total > 25:
        return total
    fi
rof
```

```python
# 隐式返回 — 代码继续，最终返回 300
total = 0
for i, 25:
    total = total + i
rof
total
```

---

## 管道简写

`|` 等价于换行，可将多行代码压缩为一行：

```python
# 原始
a = 0
b = 1
c = 2

# 简写
a=0 | b=1 | c=2
```

```python
# 原始
if a==0:
    a=100
    return a+25
fi

# 简写
if a==0: | a=100 | return a+25 | fi
```

`|` 用于增强可读性的紧凑场景，不推荐将所有代码压为一行。
