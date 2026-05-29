# 信息表单指令 — 编辑弹窗类型的表单
> Prerequisite: [HPL 编程基础](../programming/overview.md)

# 指令概览
```mcfunction
editpopupform <formName: string> button1 <firstButtonCode: string>
editpopupform <formName: string> button2 <secondButtonCode: string>
editpopupform <formName: string> content <contentCode: string>
editpopupform <formName: string> title <titleCode: string>
```

# 编辑确定按钮
## 语法
```mcfunction
editpopupform <formName: string> button1 <firstButtonCode: string>
```
`<firstButtonCode: string>` — 生成按钮文本的 HPL 代码。

## 示例
```mcfunction
editpopupform flowers button1 "return '|确定|'"
```

# 编辑取消按钮
## 语法
```mcfunction
editpopupform <formName: string> button2 <secondButtonCode: string>
```

## 示例
```mcfunction
editpopupform flowers button2 "return '<取消>'"
```

# 编辑内容文本
## 语法
```mcfunction
editpopupform <formName: string> content <contentCode: string>
```

## 示例
```mcfunction
editpopupform flowers content "
ret = ''
for i, 25:
    ret = ret + str(i) + '\\n'
rof
return {func, strings.strip(ret)}
"
```

# 编辑标题文本
## 语法
```mcfunction
editpopupform <formName: string> title <titleCode: string>
```

## 示例
```mcfunction
editpopupform flowers title "return 'CB'*5"
```
