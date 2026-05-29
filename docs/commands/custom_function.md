# 自定义函数指令 — 添加、调用和管理 HPL 自定义函数
> Prerequisite: [HPL 编程基础](../programming/overview.md)

# 指令概览
```mcfunction
customfunction add <name: string> <code: string>
customfunction call <executor: target> <position: x y z> <name: string>
customfunction list [name: string]
customfunction remove <name: string>
```

# 添加自定义函数
## 语法
```mcfunction
customfunction add <name: string> <code: string>
```
`<code: string>` 必须在执行完毕前 `return` 一个值。

## 示例
```mcfunction
customfunction add func1 "return True"

customfunction add func2 "return {command, 'say Hello!'} > 0"

customfunction add shallow "total = 0
for i, 100:
  total = total + i
rof
return total"
```

# 调用（执行）自定义函数
## 语法
```mcfunction
customfunction call <executor: target> <position: x y z> <name: string>
```
以指定执行者和执行点调用函数，维度自动继承当前执行维度。执行者至多一个。其他命令执行上下文（如朝向）会丢失。

## 示例
```mcfunction
customfunction call @e[tag=abc,c=1] ~ ~ ~ main
execute as @e[tag=abc,c=1] at @s run customfunction call @s ~ ~ ~ main
```

## 函数间调用与传参
通过 `function.call` 在代码内部调用其他自定义函数并传参：

```mcfunction
customfunction add math_compute "arg1 = {func, tuple.get(args, 0)}
arg2 = {func, tuple.get(args, 1)}
return {command, 'say arg1=' + str(arg1) + ', arg2=' + str(arg2)}"

customfunction add main "result = {func, function.call('math_compute', 'a_a_a', 23)}
return {command, 'say result=' + str(result)}"
```

未传入任何参数时 `args` 变量不存在，`tuple.get(args, 0)` 会报错。设计函数时应确保参数数量和类型固定。

# 列出自定义函数
## 语法
```mcfunction
customfunction list [name: string]
```

# 移除自定义函数
## 语法
```mcfunction
customfunction remove <name: string>
```
## 示例
```mcfunction
customfunction remove abc
customfunction remove "233233666"
```
