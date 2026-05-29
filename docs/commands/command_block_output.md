# 命令方块输出指令 — 查看命令方块的完整报错信息
> Prerequisite: [HPL 编程基础](../programming/overview.md)

# 概述
当命令方块中的报错信息超出显示范围时，使用 `commandblockoutput` 查看完整输出。

# 语法
```mcfunction
commandblockoutput <commandBlockPosition: x y z>
```

# 示例
```mcfunction
commandblockoutput ~ ~-1 ~
```

# 备注
- 不能用于查看原版指令执行日志
- 大多数模组命令执行日志可用此查看，但不确保兼容性
