# 文本元素指令 — 编辑长表单和模态表单中的文本元素
> Prerequisite: [HPL 编程基础](../programming/overview.md)

```mcfunction
editlabel <formName: string> <index: int> header <headerCode: string>
editlabel <formName: string> <index: int> label <labelCode: string>
```

# 编辑普通文本
## 语法
```mcfunction
editlabel <formName: string> <index: int> label <labelCode: string>
```

`<index: int>` 是元素统一索引（从 0 开始），label/header/divider 都占位。

## 示例
```mcfunction
editlabel aaa 2 label "return 'aobo'"
editlabel "242322" 7 label "return 'hhhhc'"
```

# 编辑大字文本
## 语法
```mcfunction
editlabel <formName: string> <index: int> header <headerCode: string>
```

## 示例
```mcfunction
editlabel 你好 0 header "return 'ababac'"
editlabel labelheader 0 header "ptr = {func, datetime_datetime.now()}
month = {func, datetime_datetime.month(ptr)}
return '现在的时间是' + str(month) + '月'"
```
