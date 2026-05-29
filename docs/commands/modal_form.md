# 模态表单指令 — 编辑模态表单及其输入控件
> Prerequisite: [HPL 编程基础](../programming/overview.md)
> 索引从 0 开始（元素统一索引）。`{ref, str/int, N}` 中的 N 即此索引。

# 指令概览
## 编辑模态表单
```mcfunction
editmodalform <formName: string> append label|header|divider|input|toggle|dropdown|slider|stepslider
editmodalform <formName: string> title <titleCode: string>
```

## 编辑模态表单中的输入框
```mcfunction
editinput <formName: string> <index: int> default <defaultCode: string>
editinput <formName: string> <index: int> placeholder <placeHolderCode: string>
editinput <formName: string> <index: int> text <textCode: string>
editinput <formName: string> <index: int> tooltip [tooltipCode: string]
```

## 编辑模态表单中的开关
```mcfunction
edittoggle <formName: string> <index: int> default <stateCode: string>
edittoggle <formName: string> <index: int> text <textCode: string>
edittoggle <formName: string> <index: int> tooltip [tooltipCode: string]
```

## 编辑模态表单中的下拉框
```mcfunction
editdropdown <formName: string> <index: int> append <optionCode: string>
editdropdown <formName: string> <index: int> default <indexCode: string>
editdropdown <formName: string> <index: int> text <textCode: string>
editdropdown <formName: string> <index: int> tooltip [tooltipCode: string]
```

## 编辑模态表单中的隐式步进滑块
```mcfunction
editslider <formName: string> <index: int> default <defaultCode: string>
editslider <formName: string> <index: int> min <minCode: string>
editslider <formName: string> <index: int> max <maxCode: string>
editslider <formName: string> <index: int> step <stepCode: string>
editslider <formName: string> <index: int> text <textCode: string>
editslider <formName: string> <index: int> tooltip [tooltipCode: string]
```

## 编辑模态表单中的显式步进滑块
```mcfunction
editstepslider <formName: string> <index: int> append <stepCode: string>
editstepslider <formName: string> <index: int> default <indexCode: string>
editstepslider <formName: string> <index: int> text <textCode: string>
editstepslider <formName: string> <index: int> tooltip [tooltipCode: string]
```

# 编辑模态表单
## 添加元素
### 语法
```mcfunction
editmodalform <formName: string> append label|header|divider|input|toggle|dropdown|slider|stepslider
```

| 元素 ID | 名称 | 默认状态 |
|---|---|---|
| label | 普通文本 | 空文本 |
| header | 大字文本 | 空文本 |
| divider | 分割线 | 无需后续编辑 |
| input | 输入框 | 空标题、空提示语、空默认内容、空 tooltip |
| toggle | 开关 | 空标题、默认关闭、空 tooltip |
| dropdown | 下拉框 | 空标题、空 tooltip、**无选项** |
| slider | 隐式步进滑块 | 空标题、min=0.0、max=1.0、step=1.0、default=0.0、空 tooltip |
| stepslider | 显式步进滑块 | 空标题、空 tooltip、**无选项** |

下拉框必须至少有 1 个选项，显式步进滑块至少 2 个，否则展示时报错。

## 设置标题文本
### 语法
```mcfunction
editmodalform <formName: string> title <titleCode: string>
```

# 编辑输入框
## 语法
```mcfunction
editinput <formName: string> <index: int> default <defaultCode: string>     ← 已输入内容
editinput <formName: string> <index: int> placeholder <placeHolderCode: string> ← 提示文本
editinput <formName: string> <index: int> text <textCode: string>            ← 标题文本
editinput <formName: string> <index: int> tooltip [tooltipCode: string]      ← 灯泡提示（不填则清除）
```

## 示例
```mcfunction
editinput ohhh 0 text "return '您的生日是什么时候？'"
editinput ohhh 0 placeholder "return '1990-01-01'"
editinput ohhh 0 tooltip "return '生日是您的出生日期'"
editinput ohhh 0 default "return '2000-12-31'"
```

# 编辑开关
## 语法
```mcfunction
edittoggle <formName: string> <index: int> default <stateCode: string>  ← 返回 True/False
edittoggle <formName: string> <index: int> text <textCode: string>
edittoggle <formName: string> <index: int> tooltip [tooltipCode: string]
```

## 示例
```mcfunction
edittoggle abc 2 default "return False"
edittoggle abc 2 text "return '你好'"
```

# 编辑下拉框
## 语法
```mcfunction
editdropdown <formName: string> <index: int> append <optionCode: string>  ← 添加选项
editdropdown <formName: string> <index: int> default <indexCode: string>   ← 默认选项索引
editdropdown <formName: string> <index: int> text <textCode: string>
editdropdown <formName: string> <index: int> tooltip [tooltipCode: string]
```

## 示例
```mcfunction
editdropdown abc 1 append "return 'a'"
editdropdown abc 1 append "return 'b'"
editdropdown abc 1 text "return 'c'"
editdropdown abc 1 default "return 1"
editdropdown abc 1 tooltip "return '我是一个提示文本'"
```

# 编辑隐式步进滑块
## 语法
```mcfunction
editslider <formName: string> <index: int> default <defaultCode: string>  ← 默认值（数字）
editslider <formName: string> <index: int> min <minCode: string>          ← 最小值
editslider <formName: string> <index: int> max <maxCode: string>          ← 最大值
editslider <formName: string> <index: int> step <stepCode: string>        ← 步进长度
editslider <formName: string> <index: int> text <textCode: string>
editslider <formName: string> <index: int> tooltip [tooltipCode: string]
```

滑块可取值为从 min 到 max 的等差数列（步长 = step）。若 max 在正常步进下不可达，系统仍确保玩家可取得 max。默认值不可达时自动修正到最近可达值。

## 示例
```mcfunction
editslider app 0 text "return 'aaa'"
editslider app 0 min "return -5.0"
editslider app 0 max "return 5"
editslider app 0 step "return 0.5"
editslider app 0 default "return 3.5"
editslider app 0 tooltip "return '666'"
```

# 编辑显式步进滑块
## 语法
子命令用法与下拉框基本一致：

```mcfunction
editstepslider <formName: string> <index: int> append <stepCode: string>   ← 添加选项
editstepslider <formName: string> <index: int> default <indexCode: string>  ← 默认选项索引
editstepslider <formName: string> <index: int> text <textCode: string>
editstepslider <formName: string> <index: int> tooltip [tooltipCode: string]
```

## 示例
```mcfunction
editstepslider ggb 0 text "return 'Hello, World!'"
editstepslider ggb 0 append "return 'a'"
editstepslider ggb 0 append "return 'b'"
editstepslider ggb 0 append "return 'c'"
editstepslider ggb 0 default "return 2"
editstepslider ggb 0 tooltip "return '献给机械の花束'"
```
