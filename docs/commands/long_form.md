# 长表单指令 — 编辑长表单及其按钮元素
> Prerequisite: [HPL 编程基础](../programming/overview.md)
> 索引从 0 开始。`{ref, bool, N}` 中的 N 是按钮序号（仅计 button，label/header/divider 不占位），与元素统一索引是两套体系。

# 指令概览
## 编辑长表单
```mcfunction
editlongform <formName: string> append [button|label|header|divider]
editlongform <formName: string> content <contentCode: string>
editlongform <formName: string> title <titleCode: string>
```

## 编辑长表单中的按钮
```mcfunction
editbutton <formName: string> <index: int> icon [textureCode: string]
editbutton <formName: string> <index: int> text <textCode: string>
```

# 编辑长表单
## 添加元素
### 语法
```mcfunction
editlongform <formName: string> append [button|label|header|divider]
```

| 元素 ID | 名称 |
|---|---|
| button | 按钮 |
| label | 普通文本 |
| header | 大字文本 |
| divider | 分割线 |

元素添加后处于默认状态（按钮无文本无图标，文本为空），需通过其他指令进一步编辑。分割线无需后续编辑。

### 示例
```mcfunction
editlongform Happy append button
editlongform abc append label
editlongform hello append header
editlongform "123" append divider
```

## 设置内容文本
### 语法
```mcfunction
editlongform <formName: string> content <contentCode: string>
```
### 示例
```mcfunction
editlongform i_am_a_boy content "return '你好'"
```

## 设置标题文本
### 语法
```mcfunction
editlongform <formName: string> title <titleCode: string>
```
### 示例
```mcfunction
editlongform bds title "return {selector, '@s'}"
```

# 编辑长表单中的按钮
## 设置图标
### 语法
```mcfunction
editbutton <formName: string> <index: int> icon [textureCode: string]
```
`[textureCode: string]` 返回图标材质贴图路径的字符串。不填则清除图标。

### 示例
```mcfunction
editbutton abc 1 icon "return 'textures/painting/baroque'"
```

## 设置文字
### 语法
```mcfunction
editbutton <formName: string> <index: int> text <textCode: string>
```
### 示例
```mcfunction
editbutton abc 2 text "return 'aabbcc'"
```
