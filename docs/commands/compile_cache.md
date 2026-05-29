# 编译缓存指令 — 管理 HPL 代码编译缓存
> Prerequisite: [HPL 编程基础](../programming/overview.md)

```mcfunction
compilecache compile <code: string>
compilecache query
compilecache set [size: int]
```

# 概述
缓存系统存储已编译的代码产物（AST → 字节码），跳过重复解析翻译，执行效率提高二十倍以上。默认最大容量 2048。

# 编译代码
## 语法
```mcfunction
compilecache compile <code: string>
```

## 示例
```mcfunction
compilecache compile "total = -2018
for i, 32:
  total = total + 10*i
rof
return total"
```

# 查询缓存状态
## 语法
```mcfunction
compilecache query
```

# 设置最大容量
## 语法
```mcfunction
compilecache set [size: int]
```
不填参数则重置为默认值 2048。无特别需要请勿手动调整——过小降低效率，过大占用内存。
