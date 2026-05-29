# HPL API 参考

> 基于 NetEase Minecraft HPL 脚本系统。所有 API 调用使用 `{func, 模块.函数(参数...)}` 格式。
> 自动生成自 `所有fuc用法➕格式2.txt`。

## 模块跳转

- [object](#object)
- [reflect](#reflect)
- [slices](#slices)
- [maps](#maps)
- [tuple](#tuple)
- [set](#set)
- [strings](#strings)
- [uuid](#uuid)
- [time](#time)
- [struct_time](#struct_time)
- [math](#math)
- [random](#random)
- [json](#json)
- [binascii](#binascii)
- [datetime_datetime](#datetime_datetime)
- [datetime_date](#datetime_date)
- [datetime_time](#datetime_time)
- [command](#command)
- [general](#general)
- [world](#world)
- [entity](#entity)
- [player](#player)
- [block](#block)
- [item](#item)

---

<a id="object"></a>

## object

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `ref` | 创建指向对象的指针，用于后续通过指针操作对象。 | <code>{func, object.ref(对象: any)}</code> | `ptr` |
| `can_deref` | 检查指针是否指向可解引用的基本类型（整数、布尔值、浮点数、字符串），返回布尔值。 | <code>{func, object.can_deref(指针: ptr)}</code> | `bool` |
| `deref` | 解引用指针，返回指针指向的基本类型值（整数、布尔值、浮点数、字符串）。若指向非基本类型则抛出异常。 | <code>{func, object.deref(指针: ptr)}</code> | `bool` |
| `release` | 释放指针所管理的资源，指针变为无效。 | <code>{func, object.release(指针: ptr)}</code> | `—` |
| `pin` | 固定对象，防止被垃圾回收。 | <code>{func, object.pin(指针: ptr)}</code> | `—` |
| `finalise` | 终结对象的固定状态，使其可被释放。 | <code>{func, object.finalise(指针: ptr)}</code> | `—` |
| `make_none` | 创建一个表示空值的 None 对象，返回其指针。 | <code>{func, object.make_none()}</code> | `ptr` |
| `is_ptr` | 判断给定整数是否为一个有效指针，返回布尔值。 | <code>{func, object.is_ptr(整数: int)}</code> | `bool` |
| `is_none` | 判断指针指向的对象是否为 None，返回布尔值。 | <code>{func, object.is_none(指针: ptr)}</code> | `bool` |
| `raw_type` | 获取基本类型对象的类型码（0=int,1=bool,2=float,3=str）。参数为原始值，不是指针。详见 [类型码速查](programming/data_type.md)。 | <code>{func, object.raw_type(原始值: int|bool|float|str)}</code> | `int` |
| `ref_type` | 获取指针指向对象的类型码（见源码中的 REF_TYPE_XXX）。原始值用 raw_type，详见 [类型码速查](programming/data_type.md)。 | <code>{func, object.ref_type(指针: ptr)}</code> | `int` |

---

<a id="reflect"></a>

## reflect

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `cast` | 将对象 A 转换为对象 B 的类型，返回指向新对象的指针，失败返回 0。 | <code>{func, reflect.cast(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `length` | 返回对象的长度，返回指向长度（整数）的指针，失败返回 0。 | <code>{func, reflect.length(指针: ptr)}</code> | `int` |
| `copy` | 返回对象的浅拷贝，返回指向新对象的指针，失败返回 0。 | <code>{func, reflect.copy(指针: ptr)}</code> | `ptr` |
| `deepcopy` | 返回对象的深拷贝，返回指向新对象的指针，失败返回 0。 | <code>{func, reflect.deepcopy(指针: ptr)}</code> | `ptr` |
| `format` | 返回对象的字符串表示，返回指向字符串的指针，失败返回 0。 | <code>{func, reflect.format(指针: ptr)}</code> | `ptr` |
| `vars` | 返回对象的属性字典，返回指向映射的指针，失败返回 0。 | <code>{func, reflect.vars(指针: ptr)}</code> | `ptr` |
| `dir` | 返回对象的属性名称列表，返回指向切片的指针，失败返回 0。 | <code>{func, reflect.dir(指针: ptr)}</code> | `ptr` |
| `hasattr` | 检查对象是否拥有指定属性，返回布尔值。 | <code>{func, reflect.hasattr(指针: ptr, 属性名: string)}</code> | `bool` |
| `getattr` | 获取对象的指定属性值，返回指向该值的指针，失败返回 0（属性受保护或错误）。 | <code>{func, reflect.getattr(指针: ptr, 属性名: string)}</code> | `ptr` |
| `setattr` | 设置对象的指定属性值，返回布尔值表示成功与否。 | <code>{func, reflect.setattr(对象指针: ptr, 属性名: string, 值指针: ptr)}</code> | `bool` |
| `delattr` | 删除对象的指定属性，返回布尔值表示成功与否。 | <code>{func, reflect.delattr(对象指针: ptr, 属性名: string)}</code> | `bool` |
| `callable` | 检查对象是否可调用，返回布尔值。 | <code>{func, reflect.callable(指针: ptr)}</code> | `bool` |
| `call` | 调用可调用对象，传入任意数量的参数指针，返回指向结果的指针；失败返回错误字符串。 | <code>{func, reflect.call(函数指针: ptr, 参数指针1: any, 参数指针2: any)}</code> | `ptr` |
| `and` | 对两个对象进行逻辑与运算，返回指向结果的指针，失败返回 0。 | <code>{func, reflect.and(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `or` | 逻辑或运算，返回指向结果的指针。 | <code>{func, reflect.or(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `inverse` | 逻辑非运算，返回指向结果的指针。 | <code>{func, reflect.inverse(指针: ptr)}</code> | `ptr` |
| `in` | 检查元素是否在容器中，返回指向结果的指针。 | <code>{func, reflect.in(容器指针: ptr, 元素指针: ptr)}</code> | `ptr` |
| `add` | 加法运算，返回指向结果的指针。 | <code>{func, reflect.add(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `remove` | 减法运算，返回指向结果的指针。 | <code>{func, reflect.remove(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `times` | 乘法运算，返回指向结果的指针。 | <code>{func, reflect.times(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `divide` | 除法运算，返回指向结果的指针。 | <code>{func, reflect.divide(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `floordiv` | 整数除法，返回指向结果的指针。 | <code>{func, reflect.floordiv(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `negative` | 取负运算，返回指向结果的指针。 | <code>{func, reflect.negative(指针: ptr)}</code> | `ptr` |
| `abs` | 绝对值，返回指向结果的指针。 | <code>{func, reflect.abs(指针: ptr)}</code> | `ptr` |
| `round` | 四舍五入，可指定小数位数，返回指向结果的指针。 | <code>{func, reflect.round(指针: ptr, 小数位数: int)}</code> | `ptr` |
| `mod` | 取模运算，返回指向结果的指针。 | <code>{func, reflect.mod(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `pow` | 幂运算，返回指向结果的指针。 | <code>{func, reflect.pow(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `powmod` | 模幂运算，返回指向结果的指针。 | <code>{func, reflect.powmod(指针A: ptr, 指针B: ptr, 指针C: ptr)}</code> | `ptr` |
| `greater` | 大于比较，返回指向结果的指针。 | <code>{func, reflect.greater(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `less` | 小于比较，返回指向结果的指针。 | <code>{func, reflect.less(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `greater_equal` | 大于等于比较，返回指向结果的指针。 | <code>{func, reflect.greater_equal(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `less_equal` | 小于等于比较，返回指向结果的指针。 | <code>{func, reflect.less_equal(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `equal` | 相等比较，返回指向结果的指针。 | <code>{func, reflect.equal(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `not_equal` | 不等比较，返回指向结果的指针。 | <code>{func, reflect.not_equal(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `bit_and` | 按位与，返回指向结果的指针。 | <code>{func, reflect.bit_and(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `bit_or` | 按位或，返回指向结果的指针。 | <code>{func, reflect.bit_or(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `bit_xor` | 按位异或，返回指向结果的指针。 | <code>{func, reflect.bit_xor(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `bit_not` | 按位取反，返回指向结果的指针。 | <code>{func, reflect.bit_not(指针: ptr)}</code> | `ptr` |
| `left_shift` | 左移位，返回指向结果的指针。 | <code>{func, reflect.left_shift(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `right_shift` | 右移位，返回指向结果的指针。 | <code>{func, reflect.right_shift(指针A: ptr, 指针B: ptr)}</code> | `ptr` |
| `max` | 返回序列中的最大值，返回指向结果的指针。 | <code>{func, reflect.max(序列指针: ptr)}</code> | `ptr` |
| `min` | 返回最小值，返回指向结果的指针。 | <code>{func, reflect.min(序列指针: ptr)}</code> | `ptr` |
| `sum` | 返回序列的和，返回指向结果的指针。 | <code>{func, reflect.sum(序列指针: ptr)}</code> | `ptr` |

---

<a id="slices"></a>

## slices

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `new` | 创建新切片，可传入初始元素。 | <code>{func, slices.new(元素1?: any, 元素2: any)}</code> | `ptr` |
| `make` | 创建指定长度和默认值的切片。 | <code>{func, slices.make(长度: int, 默认值: any)}</code> | `ptr` |
| `cast` | 将其他可迭代对象转换为切片。 | <code>{func, slices.cast(可迭代对象指针: ptr)}</code> | `ptr` |
| `length` | 返回切片长度（整数，直接值，非指针）。 | <code>{func, slices.length(切片指针: ptr)}</code> | `int` |
| `copy` | 返回切片的浅拷贝（指针）。 | <code>{func, slices.copy(切片指针: ptr)}</code> | `ptr` |
| `format` | 返回切片的字符串表示（直接字符串）。 | <code>{func, slices.format(切片指针: ptr)}</code> | `str` |
| `append` | 向切片末尾追加元素，返回布尔值 True。 | <code>{func, slices.append(切片指针: ptr, 元素: any)}</code> | `bool` |
| `ptr_append` | 追加元素并返回指向新元素的指针。 | <code>{func, slices.ptr_append(切片指针: ptr, 值指针: ptr)}</code> | `ptr` |
| `get` | 获取指定索引的元素（直接值）。 | <code>{func, slices.get(切片指针: ptr, 索引: int)}</code> | `raw` |
| `ptr_get` | 获取指向指定索引元素的指针。 | <code>{func, slices.ptr_get(切片指针: ptr, 索引: int)}</code> | `ptr` |
| `set` | 设置指定索引的元素，返回布尔值 True。 | <code>{func, slices.set(切片指针: ptr, 索引: int, 元素: any)}</code> | `bool` |
| `ptr_set` | 设置指定索引的元素（通过值指针），返回布尔值 True。 | <code>{func, slices.ptr_set(切片指针: ptr, 索引: int, 值指针: ptr)}</code> | `bool` |
| `max` | 返回切片中的最大值（直接值）。 | <code>{func, slices.max(切片指针: ptr)}</code> | `raw` |
| `min` | 返回最小值（直接值）。 | <code>{func, slices.min(切片指针: ptr)}</code> | `raw` |
| `sum` | 返回切片中数值元素的和（直接值）。 | <code>{func, slices.sum(切片指针: ptr)}</code> | `raw` |
| `sub` | 截取子切片，返回新切片指针。 | <code>{func, slices.sub(切片指针: ptr, 起始: int, 结束: int)}</code> | `ptr` |
| `insert` | 在指定位置插入元素，返回布尔值 True。 | <code>{func, slices.insert(切片指针: ptr, 索引: int, 元素: any)}</code> | `bool` |
| `ptr_insert` | 插入元素（通过值指针），返回布尔值 True。 | <code>{func, slices.ptr_insert(切片指针: ptr, 索引: int, 值指针: ptr)}</code> | `bool` |
| `pop` | 移除并返回最后一个元素（直接值）。 | <code>{func, slices.pop(切片指针: ptr)}</code> | `raw` |
| `ptr_pop` | 移除最后一个元素并返回指向它的指针。 | <code>{func, slices.ptr_pop(切片指针: ptr)}</code> | `ptr` |
| `reverse` | 反转切片，返回布尔值 True。 | <code>{func, slices.reverse(切片指针: ptr)}</code> | `bool` |
| `sort` | 对切片排序，可指定是否反向，返回布尔值 True。 | <code>{func, slices.sort(切片指针: ptr, 是否反向: bool)}</code> | `bool` |
| `concat` | 连接多个切片，返回新切片指针。 | <code>{func, slices.concat(切片指针1: any, 切片指针2: any)}</code> | `ptr` |
| `binsearch` | 二分查找元素，返回指向元组 (索引, 是否找到) 的指针。 | <code>{func, slices.binsearch(切片指针: ptr, 元素: any)}</code> | `ptr` |
| `ptr_binsearch` | 二分查找（通过值指针），返回指向元组的指针。 | <code>{func, slices.ptr_binsearch(切片指针: ptr, 值指针: ptr)}</code> | `ptr` |
| `in` | 检查元素是否存在于切片中，返回布尔值。 | <code>{func, slices.in(切片指针: ptr, 元素: any)}</code> | `bool` |
| `ptr_in` | 检查元素是否存在于切片中（通过值指针），返回布尔值。 | <code>{func, slices.ptr_in(切片指针: ptr, 值指针: ptr)}</code> | `bool` |

---

<a id="maps"></a>

## maps

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `new` | 创建新映射，可指定是否有序，并可传入键值对初始化。 | <code>{func, maps.new(是否有序: bool, 键1?: any, 值1: any, 键2: any, 值2: any)}</code> | `ptr` |
| `cast` | 将其他对象强制转换为映射，返回新映射指针。 | <code>{func, maps.cast(指针: ptr)}</code> | `ptr` |
| `length` | 返回映射中键值对数量（直接整数）。 | <code>{func, maps.length(映射指针: ptr)}</code> | `int` |
| `copy` | 返回映射的浅拷贝（指针）。 | <code>{func, maps.copy(映射指针: ptr)}</code> | `ptr` |
| `format` | 返回映射的字符串表示（直接字符串）。 | <code>{func, maps.format(映射指针: ptr)}</code> | `str` |
| `exist` | 检查键是否存在，返回布尔值。 | <code>{func, maps.exist(映射指针: ptr, 键: any)}</code> | `bool` |
| `ptr_exist` | 检查键是否存在（通过键指针），返回布尔值。 | <code>{func, maps.ptr_exist(映射指针: ptr, 键指针: ptr)}</code> | `bool` |
| `get` | 获取指定键的值（直接值），键必须存在，否则异常。 | <code>{func, maps.get(映射指针: ptr, 键: any)}</code> | `raw` |
| `ptr_get` | 获取指向指定键值的指针。 | <code>{func, maps.ptr_get(映射指针: ptr, 键指针: ptr)}</code> | `ptr` |
| `pop` | 移除指定键并返回其值（直接值）。 | <code>{func, maps.pop(映射指针: ptr, 键: any)}</code> | `raw` |
| `ptr_pop` | 移除指定键并返回指向被移除值的指针。 | <code>{func, maps.ptr_pop(映射指针: ptr, 键指针: ptr)}</code> | `ptr` |
| `set` | 设置键值对，返回布尔值 True。 | <code>{func, maps.set(映射指针: ptr, 键: any, 值: any)}</code> | `bool` |
| `ptr_set` | 设置键值对（通过键指针和值指针），返回布尔值 True。 | <code>{func, maps.ptr_set(映射指针: ptr, 键指针: ptr, 值指针: ptr)}</code> | `bool` |
| `del` | 删除指定键值对，返回布尔值 True。 | <code>{func, maps.del(映射指针: ptr, 键: any)}</code> | `bool` |
| `ptr_del` | 删除指定键值对（通过键指针），返回布尔值 True。 | <code>{func, maps.ptr_del(映射指针: ptr, 键指针: ptr)}</code> | `bool` |
| `clear` | 清空映射，返回布尔值 True。 | <code>{func, maps.clear(映射指针: ptr)}</code> | `bool` |
| `keys` | 返回所有键组成的切片指针。 | <code>{func, maps.keys(映射指针: ptr)}</code> | `ptr` |
| `values` | 返回所有值组成的切片指针。 | <code>{func, maps.values(映射指针: ptr)}</code> | `ptr` |
| `items` | 返回所有键值对组成的切片指针（每个元素为二元组）。 | <code>{func, maps.items(映射指针: ptr)}</code> | `ptr` |
| `equal` | 比较两个映射是否相等，返回布尔值。 | <code>{func, maps.equal(映射指针A: ptr, 映射指针B: ptr)}</code> | `bool` |

---

<a id="tuple"></a>

## tuple

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `new` | 创建新元组，可传入元素。 | <code>{func, tuple.new(元素1?: any, 元素2: any)}</code> | `ptr` |
| `cast` | 将其他可迭代对象转换为元组，返回指针。 | <code>{func, tuple.cast(可迭代对象指针: ptr)}</code> | `ptr` |
| `length` | 返回元组长度（直接整数）。 | <code>{func, tuple.length(元组指针: ptr)}</code> | `int` |
| `format` | 返回元组的字符串表示（直接字符串）。 | <code>{func, tuple.format(元组指针: ptr)}</code> | `str` |
| `get` | 获取指定索引的元素（直接值）。 | <code>{func, tuple.get(元组指针: ptr, 索引: int)}</code> | `raw` |
| `ptr_get` | 获取指向指定索引元素的指针。 | <code>{func, tuple.ptr_get(元组指针: ptr, 索引: int)}</code> | `ptr` |
| `sub` | 截取子元组，返回新元组指针。 | <code>{func, tuple.sub(元组指针: ptr, 起始: int, 结束: int)}</code> | `ptr` |
| `max` | 返回元组中的最大值（直接值）。 | <code>{func, tuple.max(元组指针: ptr)}</code> | `raw` |
| `min` | 返回最小值（直接值）。 | <code>{func, tuple.min(元组指针: ptr)}</code> | `raw` |
| `sum` | 返回元组中数值元素的和（直接值）。 | <code>{func, tuple.sum(元组指针: ptr)}</code> | `raw` |
| `in` | 检查元素是否存在于元组中，返回布尔值。 | <code>{func, tuple.in(元组指针: ptr, 元素: any)}</code> | `bool` |
| `ptr_in` | 检查元素是否存在于元组中（通过值指针），返回布尔值。 | <code>{func, tuple.ptr_in(元组指针: ptr, 值指针: ptr)}</code> | `bool` |

---

<a id="set"></a>

## set

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `new` | 创建新集合，可传入初始元素。 | <code>{func, set.new(元素1?: any, 元素2: any)}</code> | `ptr` |
| `cast` | 将其他可迭代对象转换为集合，返回指针。 | <code>{func, set.cast(可迭代对象指针: ptr)}</code> | `ptr` |
| `length` | 返回集合中元素个数（直接整数）。 | <code>{func, set.length(集合指针: ptr)}</code> | `int` |
| `copy` | 返回集合的浅拷贝（指针）。 | <code>{func, set.copy(集合指针: ptr)}</code> | `ptr` |
| `format` | 返回集合的字符串表示（直接字符串）。 | <code>{func, set.format(集合指针: ptr)}</code> | `str` |
| `exist` | 检查元素是否存在于集合中，返回布尔值。 | <code>{func, set.exist(集合指针: ptr, 元素: any)}</code> | `bool` |
| `ptr_exist` | 检查元素是否存在于集合中（通过值指针），返回布尔值。 | <code>{func, set.ptr_exist(集合指针: ptr, 值指针: ptr)}</code> | `bool` |
| `add` | 向集合添加元素，返回布尔值 True。 | <code>{func, set.add(集合指针: ptr, 元素: any)}</code> | `bool` |
| `ptr_add` | 添加元素（通过值指针），返回布尔值 True。 | <code>{func, set.ptr_add(集合指针: ptr, 值指针: ptr)}</code> | `bool` |
| `remove` | 移除指定元素，若不存在则异常，返回布尔值 True。 | <code>{func, set.remove(集合指针: ptr, 元素: any)}</code> | `bool` |
| `ptr_remove` | 移除元素（通过值指针），返回布尔值 True。 | <code>{func, set.ptr_remove(集合指针: ptr, 值指针: ptr)}</code> | `bool` |
| `discard` | 移除指定元素（不存在时忽略），返回布尔值 True。 | <code>{func, set.discard(集合指针: ptr, 元素: any)}</code> | `bool` |
| `ptr_discard` | 移除元素（通过值指针），返回布尔值 True。 | <code>{func, set.ptr_discard(集合指针: ptr, 值指针: ptr)}</code> | `bool` |
| `pop` | 随机移除并返回一个元素（直接值）。 | <code>{func, set.pop(集合指针: ptr)}</code> | `raw` |
| `ptr_pop` | 随机移除并返回指向被移除元素的指针。 | <code>{func, set.ptr_pop(集合指针: ptr)}</code> | `ptr` |
| `clear` | 清空集合，返回布尔值 True。 | <code>{func, set.clear(集合指针: ptr)}</code> | `bool` |
| `max` | 返回集合中的最大值（直接值）。 | <code>{func, set.max(集合指针: ptr)}</code> | `raw` |
| `min` | 返回最小值（直接值）。 | <code>{func, set.min(集合指针: ptr)}</code> | `raw` |
| `sum` | 返回集合中数值元素的和（直接值）。 | <code>{func, set.sum(集合指针: ptr)}</code> | `raw` |
| `difference` | 返回两个集合的差集（新集合指针）。 | <code>{func, set.difference(集合指针A: ptr, 集合指针B: ptr)}</code> | `ptr` |
| `symmetric_difference` | 返回对称差集（新集合指针）。 | <code>{func, set.symmetric_difference(集合指针A: ptr, 集合指针B: ptr)}</code> | `ptr` |
| `intersection` | 返回交集（新集合指针）。 | <code>{func, set.intersection(集合指针A: ptr, 集合指针B: ptr)}</code> | `ptr` |
| `union` | 返回并集（新集合指针）。 | <code>{func, set.union(集合指针A: ptr, 集合指针B: ptr)}</code> | `ptr` |
| `isdisjoint` | 判断两个集合是否不相交，返回布尔值。 | <code>{func, set.isdisjoint(集合指针A: ptr, 集合指针B: ptr)}</code> | `bool` |
| `issubset` | 判断一个集合是否为另一个的子集，返回布尔值。 | <code>{func, set.issubset(集合指针A: ptr, 集合指针B: ptr)}</code> | `bool` |
| `issuperset` | 判断一个集合是否为另一个的超集，返回布尔值。 | <code>{func, set.issuperset(集合指针A: ptr, 集合指针B: ptr)}</code> | `bool` |

---

<a id="strings"></a>

## strings

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `cast` | 将指针指向的对象转换为字符串，返回直接字符串。 | <code>{func, strings.cast(指针: ptr)}</code> | `str` |
| `length` | 返回字符串长度（直接整数）。 | <code>{func, strings.length(字符串: string)}</code> | `int` |
| `sub` | 截取子字符串，返回直接字符串。 | <code>{func, strings.sub(字符串: string, 起始: int, 结束: int)}</code> | `str` |
| `ord` | 返回字符的 Unicode 码点（整数），返回整数（Unicode 码点）。 | <code>{func, strings.ord(字符: string)}</code> | `int` |
| `chr` | 返回码点对应的字符（字符串）。 | <code>{func, strings.chr(码点: int)}</code> | `str` |
| `capitalize` | 首字母大写，返回字符串。 | <code>{func, strings.capitalize(字符串: string)}</code> | `str` |
| `center` | 居中填充，返回字符串。 | <code>{func, strings.center(字符串: string, 宽度: int, 填充字符: string)}</code> | `str` |
| `startswith` | 判断是否以指定前缀开头，返回布尔值。 | <code>{func, strings.startswith(字符串: string, 前缀: string, 起始: int, 结束: int)}</code> | `bool` |
| `endswith` | 判断是否以指定后缀结尾，返回布尔值。 | <code>{func, strings.endswith(字符串: string, 后缀: string, 起始: int, 结束: int)}</code> | `bool` |
| `find` | 查找子串首次出现位置，返回索引，找不到返回 -1。 | <code>{func, strings.find(字符串: string, 子串: string, 起始: int, 结束: int)}</code> | `int` |
| `rfind` | 从右侧查找，返回索引。 | <code>{func, strings.rfind(字符串: string, 子串: string, 起始: int, 结束: int)}</code> | `int` |
| `index` | 类似 find，但找不到时抛出异常，返回整数（索引）。 | <code>{func, strings.index(字符串: string, 子串: string, 起始: int, 结束: int)}</code> | `int` |
| `rindex` | 类似 rfind，但找不到时抛出异常，返回整数（索引）。 | <code>{func, strings.rindex(字符串: string, 子串: string, 起始: int, 结束: int)}</code> | `int` |
| `isalnum` | 判断是否全为字母或数字，返回布尔值。 | <code>{func, strings.isalnum(字符串: string)}</code> | `bool` |
| `isalpha` | 判断是否全为字母，返回布尔值。 | <code>{func, strings.isalpha(字符串: string)}</code> | `bool` |
| `isdigit` | 判断是否全为数字，返回布尔值。 | <code>{func, strings.isdigit(字符串: string)}</code> | `bool` |
| `islower` | 判断是否全小写，返回布尔值。 | <code>{func, strings.islower(字符串: string)}</code> | `bool` |
| `isspace` | 判断是否全空白，返回布尔值。 | <code>{func, strings.isspace(字符串: string)}</code> | `bool` |
| `istitle` | 判断是否为标题格式，返回布尔值。 | <code>{func, strings.istitle(字符串: string)}</code> | `bool` |
| `isupper` | 判断是否全大写，返回布尔值。 | <code>{func, strings.isupper(字符串: string)}</code> | `bool` |
| `join` | 用当前字符串连接切片中的字符串元素，返回结果字符串。 | <code>{func, strings.join(分隔符: string, 切片指针: ptr)}</code> | `str` |
| `ljust` | 左对齐填充，返回字符串。 | <code>{func, strings.ljust(字符串: string, 宽度: int, 填充字符: string)}</code> | `str` |
| `rjust` | 右对齐填充，返回字符串。 | <code>{func, strings.rjust(字符串: string, 宽度: int, 填充字符: string)}</code> | `str` |
| `lower` | 转换为小写，返回字符串。 | <code>{func, strings.lower(字符串: string)}</code> | `str` |
| `upper` | 转换为大写，返回字符串。 | <code>{func, strings.upper(字符串: string)}</code> | `str` |
| `lstrip` | 去除左侧空白（或指定字符），返回字符串。 | <code>{func, strings.lstrip(字符串: string, 要去除的字符集: string)}</code> | `str` |
| `rstrip` | 去除右侧空白，返回字符串。 | <code>{func, strings.rstrip(字符串: string, 要去除的字符集: string)}</code> | `str` |
| `strip` | 去除两侧空白，返回字符串。 | <code>{func, strings.strip(字符串: string, 要去除的字符集: string)}</code> | `str` |
| `replace` | 替换子串，返回字符串。 | <code>{func, strings.replace(字符串: string, 旧子串: string, 新子串: string, 替换次数: int)}</code> | `str` |
| `split` | 按分隔符分割字符串，返回指向字符串列表的指针。 | <code>{func, strings.split(字符串: string, 分隔符: string, 最大分割次数: int)}</code> | `ptr` |
| `rsplit` | 从右侧开始分割，返回切片指针。 | <code>{func, strings.rsplit(字符串: string, 分隔符: string, 最大分割次数: int)}</code> | `ptr` |
| `swapcase` | 大小写互换，返回字符串。 | <code>{func, strings.swapcase(字符串: string)}</code> | `str` |
| `title` | 转换为标题格式，返回字符串。 | <code>{func, strings.title(字符串: string)}</code> | `str` |
| `zfill` | 左侧用零填充至指定宽度，返回字符串。 | <code>{func, strings.zfill(字符串: string, 宽度: int)}</code> | `str` |
| `equalfold` | 不区分大小写比较两个字符串，返回布尔值。 | <code>{func, strings.equalfold(字符串A: string, 字符串B: string)}</code> | `bool` |

---

<a id="uuid"></a>

## uuid

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `new` | 生成一个新的随机 UUID，返回指针。 | <code>{func, uuid.new()}</code> | `ptr` |
| `format` | 返回 UUID 的标准字符串表示，如 "123e4567-e89b-12d3-a456-426614174000"。 | <code>{func, uuid.format(UUID指针: ptr)}</code> | `str` |
| `string` | 同 format，返回字符串。 | <code>{func, uuid.string(UUID指针: ptr)}</code> | `str` |
| `bytes` | 返回 UUID 的字节表示，可能返回指针或字符串（需根据返回值类型处理）。 | <code>{func, uuid.bytes(UUID指针: ptr)}</code> | `str` |
| `bytes_le` | 返回 UUID 的小端字节序表示，返回字符串。 | <code>{func, uuid.bytes_le(UUID指针: ptr)}</code> | `str` |
| `hex` | 返回 UUID 的 32 字符十六进制字符串。 | <code>{func, uuid.hex(UUID指针: ptr)}</code> | `str` |
| `from_string` | 从标准字符串创建 UUID，返回指针。 | <code>{func, uuid.from_string(字符串: string)}</code> | `str` |
| `from_bytes` | 从字节表示创建 UUID，参数可为指针或字符串，返回指向新 UUID 的指针。 | <code>{func, uuid.from_bytes(字节串指针或字符串: ptr|string)}</code> | `ptr` |
| `from_bytes_le` | 从小端字节序创建 UUID，参数可为指针或字符串，返回指向新 UUID 的指针。 | <code>{func, uuid.from_bytes_le(字节串指针或字符串: ptr|string)}</code> | `ptr` |
| `from_hex` | 从十六进制字符串创建 UUID，返回指向新 UUID 的指针。 | <code>{func, uuid.from_hex(十六进制字符串: string)}</code> | `ptr` |

---

<a id="time"></a>

## time

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `time` | 返回当前时间戳（浮点数），返回浮点数。 | <code>{func, time.time()}</code> | `float` |
| `ctime` | 将时间戳转换为本地时间字符串，默认为当前时间。 | <code>{func, time.ctime(时间戳?: float)}</code> | `str` |
| `asctime` | 将时间元组转换为字符串，若无参数则使用当前时间。 | <code>{func, time.asctime(时间元组指针?: ptr)}</code> | `str` |
| `gmtime` | 将时间戳转换为 UTC 时间元组，返回指针。 | <code>{func, time.gmtime(时间戳?: float)}</code> | `ptr` |
| `localtime` | 将时间戳转换为本地时间元组，返回指针。 | <code>{func, time.localtime(时间戳?: float)}</code> | `ptr` |
| `mktime` | 将本地时间元组转换为时间戳，返回浮点数。 | <code>{func, time.mktime(时间元组指针: ptr)}</code> | `float` |
| `strftime` | 按格式将时间元组格式化为字符串，若无时间元组则使用当前时间。 | <code>{func, time.strftime(格式: string, 时间元组指针?: ptr)}</code> | `str` |
| `strptime` | 将字符串解析为时间元组，返回指针。 | <code>{func, time.strptime(字符串: string, 格式: string)}</code> | `str` |
| `timezone` | 返回本地时区与 UTC 的偏移秒数（整数），返回整数。 | <code>{func, time.timezone()}</code> | `int` |
| `tzname` | 返回本地时区名称元组 (标准时区名, 夏令时名)，返回指向元组的指针。 | <code>{func, time.tzname()}</code> | `ptr` |

---

<a id="struct_time"></a>

## struct_time

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `cast` | 将其他可迭代对象转换为 struct_time，返回指针。 | <code>{func, struct_time.cast(可迭代对象指针: ptr)}</code> | `ptr` |
| `length` | 返回 struct_time 的长度（固定9），返回整数。 | <code>{func, struct_time.length(时间元组指针: ptr)}</code> | `int` |
| `format` | 返回 struct_time 的字符串表示，返回字符串。 | <code>{func, struct_time.format(时间元组指针: ptr)}</code> | `str` |
| `tm_year` | 获取年份（整数），返回整数。 | <code>{func, struct_time.tm_year(时间元组指针: ptr)}</code> | `int` |
| `tm_mon` | 获取月份（1-12），返回整数。 | <code>{func, struct_time.tm_mon(时间元组指针: ptr)}</code> | `int` |
| `tm_mday` | 获取日（1-31），返回整数。 | <code>{func, struct_time.tm_mday(时间元组指针: ptr)}</code> | `int` |
| `tm_hour` | 获取小时（0-23），返回整数。 | <code>{func, struct_time.tm_hour(时间元组指针: ptr)}</code> | `int` |
| `tm_min` | 获取分钟（0-59），返回整数。 | <code>{func, struct_time.tm_min(时间元组指针: ptr)}</code> | `int` |
| `tm_sec` | 获取秒（0-61），返回整数。 | <code>{func, struct_time.tm_sec(时间元组指针: ptr)}</code> | `int` |
| `tm_wday` | 获取星期几（0-6，0为周一），返回整数。 | <code>{func, struct_time.tm_wday(时间元组指针: ptr)}</code> | `int` |
| `tm_yday` | 获取一年中的第几天（1-366），返回整数。 | <code>{func, struct_time.tm_yday(时间元组指针: ptr)}</code> | `int` |
| `tm_isdst` | 获取夏令时标志（0否，1是，-1未知），返回整数。 | <code>{func, struct_time.tm_isdst(时间元组指针: ptr)}</code> | `int` |

---

<a id="math"></a>

## math

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `format` | 将数字格式化为字符串，可指定精度，返回字符串。 | <code>{func, math.format(数字: number, 精度?: int)}</code> | `str` |
| `round` | 四舍五入，返回数字。 | <code>{func, math.round(数字: number, 小数位数: int)}</code> | `raw` |
| `floordiv` | 整数除法，返回整数。 | <code>{func, math.floordiv(a: number, b: number)}</code> | `int` |
| `mod` | 取模，返回数字。 | <code>{func, math.mod(a: number, b: number)}</code> | `raw` |
| `abs` | 绝对值，返回数字。 | <code>{func, math.abs(数字: number)}</code> | `raw` |
| `max` | 返回两个数中的较大值，返回数字。 | <code>{func, math.max(a: number, b: number)}</code> | `raw` |
| `min` | 返回较小值，返回数字。 | <code>{func, math.min(a: number, b: number)}</code> | `raw` |
| `bit_and` | 按位与，返回整数。 | <code>{func, math.bit_and(a: int, b: int)}</code> | `int` |
| `bit_or` | 按位或，返回整数。 | <code>{func, math.bit_or(a: int, b: int)}</code> | `int` |
| `bit_xor` | 按位异或，返回整数。 | <code>{func, math.bit_xor(a: int, b: int)}</code> | `int` |
| `bit_not` | 按位取反，返回整数。 | <code>{func, math.bit_not(a: int)}</code> | `int` |
| `left_shift` | 左移位，返回整数。 | <code>{func, math.left_shift(a: int, 位数: int)}</code> | `int` |
| `right_shift` | 右移位，返回整数。 | <code>{func, math.right_shift(a: int, 位数: int)}</code> | `int` |
| `acos` | 反余弦，返回弧度，返回浮点数（弧度）。 | <code>{func, math.acos(x: float)}</code> | `float` |
| `acosh` | 反双曲余弦，返回浮点数。 | <code>{func, math.acosh(x: float)}</code> | `float` |
| `asin` | 反正弦，返回浮点数。 | <code>{func, math.asin(x: float)}</code> | `float` |
| `asinh` | 反双曲正弦，返回浮点数。 | <code>{func, math.asinh(x: float)}</code> | `float` |
| `atan` | 反正切，返回浮点数。 | <code>{func, math.atan(x: float)}</code> | `float` |
| `atan2` | 双参数反正切，返回浮点数。 | <code>{func, math.atan2(y: float, x: float)}</code> | `float` |
| `atanh` | 反双曲正切，返回浮点数。 | <code>{func, math.atanh(x: float)}</code> | `float` |
| `ceil` | 向上取整，返回整数。 | <code>{func, math.ceil(x: float)}</code> | `int` |
| `cos` | 余弦，返回浮点数。 | <code>{func, math.cos(x: float)}</code> | `float` |
| `cosh` | 双曲余弦，返回浮点数。 | <code>{func, math.cosh(x: float)}</code> | `float` |
| `degrees` | 弧度转角度，返回浮点数。 | <code>{func, math.degrees(弧度: float)}</code> | `float` |
| `e` | 返回自然常数 e（浮点数）。 | <code>{func, math.e()}</code> | `float` |
| `erf` | 误差函数，返回浮点数。 | <code>{func, math.erf(x: float)}</code> | `float` |
| `erfc` | 互补误差函数，返回浮点数。 | <code>{func, math.erfc(x: float)}</code> | `float` |
| `exp` | 指数 e^x，返回浮点数。 | <code>{func, math.exp(x: float)}</code> | `float` |
| `expm1` | e^x - 1，返回浮点数。 | <code>{func, math.expm1(x: float)}</code> | `float` |
| `fabs` | 浮点绝对值，返回浮点数。 | <code>{func, math.fabs(x: float)}</code> | `float` |
| `factorial` | 阶乘，返回整数。 | <code>{func, math.factorial(x: int)}</code> | `int` |
| `floor` | 向下取整，返回整数。 | <code>{func, math.floor(x: float)}</code> | `int` |
| `fmod` | 浮点取模，返回浮点数。 | <code>{func, math.fmod(x: float, y: float)}</code> | `float` |
| `frexp` | 将浮点数分解为尾数和指数，返回指向元组 (m, e) 的指针。 | <code>{func, math.frexp(x: float)}</code> | `ptr` |
| `fsum` | 对指针指向的浮点数列表精确求和，返回浮点数。 | <code>{func, math.fsum(列表指针: ptr)}</code> | `float` |
| `gamma` | 伽马函数，返回浮点数。 | <code>{func, math.gamma(x: float)}</code> | `float` |
| `hypot` | 计算 sqrt(x^2 + y^2)，返回浮点数。 | <code>{func, math.hypot(x: float, y: float)}</code> | `float` |
| `isinf` | 判断是否为无穷大，返回布尔值。 | <code>{func, math.isinf(x: float)}</code> | `bool` |
| `isnan` | 判断是否为非数，返回布尔值。 | <code>{func, math.isnan(x: float)}</code> | `bool` |
| `ldexp` | 计算 x * 2^i，返回浮点数。 | <code>{func, math.ldexp(x: float, i: int)}</code> | `float` |
| `lgamma` | 伽马函数的自然对数，返回浮点数。 | <code>{func, math.lgamma(x: float)}</code> | `float` |
| `log` | 自然对数，可指定底数，返回浮点数。 | <code>{func, math.log(x: float, 底数: float)}</code> | `float` |
| `log10` | 以10为底的对数，返回浮点数。 | <code>{func, math.log10(x: float)}</code> | `float` |
| `log1p` | 计算 log(1+x)，返回浮点数。 | <code>{func, math.log1p(x: float)}</code> | `float` |
| `modf` | 将浮点数分解为整数和小数部分，返回指向元组 (frac, int) 的指针。 | <code>{func, math.modf(x: float)}</code> | `ptr` |
| `pi` | 返回圆周率 π，返回浮点数。 | <code>{func, math.pi()}</code> | `float` |
| `pow` | 幂运算，返回浮点数。 | <code>{func, math.pow(x: float, y: float)}</code> | `float` |
| `powmod` | 模幂运算 (x^y) % mod，返回整数。 | <code>{func, math.powmod(x: int, y: int, mod: int)}</code> | `int` |
| `radians` | 角度转弧度，返回浮点数。 | <code>{func, math.radians(角度: float)}</code> | `float` |
| `sin` | 正弦，返回浮点数。 | <code>{func, math.sin(x: float)}</code> | `float` |
| `sinh` | 双曲正弦，返回浮点数。 | <code>{func, math.sinh(x: float)}</code> | `float` |
| `sqrt` | 平方根，返回浮点数。 | <code>{func, math.sqrt(x: float)}</code> | `float` |
| `tan` | 正切，返回浮点数。 | <code>{func, math.tan(x: float)}</code> | `float` |
| `tanh` | 双曲正切，返回浮点数。 | <code>{func, math.tanh(x: float)}</code> | `float` |
| `trunc` | 截断取整，返回整数。 | <code>{func, math.trunc(x: float)}</code> | `int` |

---

<a id="random"></a>

## random

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `betavariate` | 返回 Beta 分布的随机浮点数。 | <code>{func, random.betavariate(alpha: float, beta: float)}</code> | `float` |
| `choice` | 从序列中随机选择一个元素，返回指向该元素的指针。 | <code>{func, random.choice(序列指针: ptr)}</code> | `ptr` |
| `expovariate` | 返回指数分布的随机数，返回浮点数。 | <code>{func, random.expovariate(lambd?: float)}</code> | `float` |
| `gammavariate` | 返回 Gamma 分布的随机数，返回浮点数。 | <code>{func, random.gammavariate(alpha: float, beta: float)}</code> | `float` |
| `gauss` | 返回高斯分布的随机数，返回浮点数。 | <code>{func, random.gauss(mu?: float, sigma: float)}</code> | `float` |
| `lognormvariate` | 返回对数正态分布的随机数，返回浮点数。 | <code>{func, random.lognormvariate(mu: float, sigma: float)}</code> | `float` |
| `normalvariate` | 返回正态分布的随机数，返回浮点数。 | <code>{func, random.normalvariate(mu?: float, sigma: float)}</code> | `float` |
| `paretovariate` | 返回 Pareto 分布的随机数，返回浮点数。 | <code>{func, random.paretovariate(alpha: float)}</code> | `float` |
| `randint` | 返回闭区间内的随机整数。 | <code>{func, random.randint(a: int, b: int)}</code> | `int` |
| `random` | 返回 [0.0, 1.0) 内的随机浮点数。 | <code>{func, random.random()}</code> | `float` |
| `randrange` | 从 range 中随机选取一个整数，返回整数。 | <code>{func, random.randrange(start: int, stop: int, step: int)}</code> | `int` |
| `sample` | 从总体中随机抽取 k 个不重复元素，返回新列表指针。 | <code>{func, random.sample(总体指针: ptr, k: int)}</code> | `ptr` |
| `shuffle` | 随机打乱列表（原地），返回布尔值 True。 | <code>{func, random.shuffle(列表指针: ptr)}</code> | `bool` |
| `triangular` | 返回三角分布的随机数，返回浮点数。 | <code>{func, random.triangular(low?: float, high: float, mode: float)}</code> | `float` |
| `uniform` | 返回均匀分布的随机数，返回浮点数。 | <code>{func, random.uniform(a: float, b: float)}</code> | `float` |
| `vonmisesvariate` | 返回 von Mises 分布的随机数，返回浮点数。 | <code>{func, random.vonmisesvariate(mu: float, kappa: float)}</code> | `float` |
| `weibullvariate` | 返回 Weibull 分布的随机数，返回浮点数。 | <code>{func, random.weibullvariate(alpha: float, beta: float)}</code> | `float` |
| `seed` | 设置随机种子，返回布尔值 True。 | <code>{func, random.seed(种子?: int|float|str|None)}</code> | `bool` |
| `getstate` | 返回随机数生成器状态指针。 | <code>{func, random.getstate()}</code> | `ptr` |
| `setstate` | 恢复随机数生成器状态，返回布尔值 True。 | <code>{func, random.setstate(状态指针: ptr)}</code> | `bool` |

---

<a id="json"></a>

## json

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `dumps` | 将指针指向的对象序列化为 JSON 字符串，返回字符串。 | <code>{func, json.dumps(对象指针: ptr, skipkeys?: bool, ensure_ascii: bool, check_circular: bool, allow_nan: bool, indent: int|string, separators_ptr: ptr, sort_keys: bool)}</code> | `str` |
| `fast_dumps` | 快速序列化（不转义非ASCII），参数为直接对象（非指针），返回字符串。 | <code>{func, json.fast_dumps(直接对象: any)}</code> | `str` |
| `loads` | 将 JSON 字符串解析为对象，返回指针。 | <code>{func, json.loads(JSON字符串: string)}</code> | `str` |
| `fast_loads` | 快速解析，返回直接对象（非指针）。 | <code>{func, json.fast_loads(JSON字符串: string)}</code> | `ptr` |

---

<a id="binascii"></a>

## binascii

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `a2b_base64` | 将 Base64 字符串解码为二进制数据，返回指向字节串的指针（可能返回字符串，需判断）。 | <code>{func, binascii.a2b_base64(Base64字符串: string)}</code> | `ptr` |
| `a2b_hex` | 将十六进制字符串解码为二进制数据，返回指针。 | <code>{func, binascii.a2b_hex(十六进制字符串: string)}</code> | `str` |
| `b2a_base64` | 将二进制数据编码为 Base64 字符串，参数可为指针或字符串，返回字符串。 | <code>{func, binascii.b2a_base64(字节串指针或字符串: ptr|string)}</code> | `str` |
| `b2a_hex` | 将二进制数据编码为十六进制字符串，参数同上，返回字符串。 | <code>{func, binascii.b2a_hex(字节串指针或字符串: ptr|string)}</code> | `str` |
| `hexlify` | 同 b2a_hex，返回字符串。 | <code>{func, binascii.hexlify(字节串指针或字符串: ptr|string)}</code> | `str` |

---

<a id="datetime_datetime"></a>

## datetime_datetime

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `new` | 创建 datetime 对象，年、月、日必选，时、分、秒、微秒可选，返回指针。 | <code>{func, datetime_datetime.new(年: int, 月: int, 日: int, 时?: int, 分: int, 秒: int, 微秒: int)}</code> | `ptr` |
| `now` | 返回当前本地日期时间的指针。 | <code>{func, datetime_datetime.now()}</code> | `ptr` |
| `format` | 返回 datetime 的字符串表示，返回字符串。 | <code>{func, datetime_datetime.format(datetime指针: ptr)}</code> | `str` |
| `combine` | 将日期和时间合并为 datetime，返回指针。 | <code>{func, datetime_datetime.combine(date指针: ptr, time指针: ptr)}</code> | `ptr` |
| `ctime` | 返回 C 风格时间字符串。 | <code>{func, datetime_datetime.ctime(datetime指针: ptr)}</code> | `str` |
| `date` | 返回日期部分，返回 date 指针。 | <code>{func, datetime_datetime.date(datetime指针: ptr)}</code> | `ptr` |
| `day` | 返回日（整数）。 | <code>{func, datetime_datetime.day(datetime指针: ptr)}</code> | `int` |
| `fromordinal` | 从 Gregorian 序数创建 datetime，返回指针。 | <code>{func, datetime_datetime.fromordinal(序数: int)}</code> | `int` |
| `fromtimestamp` | 从时间戳创建本地 datetime，返回指针。 | <code>{func, datetime_datetime.fromtimestamp(时间戳: float)}</code> | `ptr` |
| `hour` | 返回小时（整数）。 | <code>{func, datetime_datetime.hour(datetime指针: ptr)}</code> | `int` |
| `isocalendar` | 返回 ISO 日历元组 (年,周,周几) 的指针。 | <code>{func, datetime_datetime.isocalendar(datetime指针: ptr)}</code> | `ptr` |
| `isoformat` | 返回 ISO 格式字符串，可指定分隔符。 | <code>{func, datetime_datetime.isoformat(datetime指针: ptr, 分隔符: string)}</code> | `str` |
| `isoweekday` | 返回 ISO 星期几（1-7）。 | <code>{func, datetime_datetime.isoweekday(datetime指针: ptr)}</code> | `int` |
| `max` | 返回最大可能的 datetime 指针。 | <code>{func, datetime_datetime.max()}</code> | `ptr` |
| `microsecond` | 返回微秒（整数）。 | <code>{func, datetime_datetime.microsecond(datetime指针: ptr)}</code> | `int` |
| `min` | 返回最小可能的 datetime 指针。 | <code>{func, datetime_datetime.min()}</code> | `ptr` |
| `minute` | 返回分钟（整数）。 | <code>{func, datetime_datetime.minute(datetime指针: ptr)}</code> | `int` |
| `month` | 返回月份（整数）。 | <code>{func, datetime_datetime.month(datetime指针: ptr)}</code> | `int` |
| `replace` | 替换部分字段，返回新 datetime 指针。 | <code>{func, datetime_datetime.replace(datetime指针: ptr, 年: int, 月: int, 日: int, 时?: int, 分: int, 秒: int, 微秒: int)}</code> | `ptr` |
| `second` | 返回秒（整数）。 | <code>{func, datetime_datetime.second(datetime指针: ptr)}</code> | `int` |
| `strftime` | 按格式化为字符串。 | <code>{func, datetime_datetime.strftime(datetime指针: ptr, 格式: string)}</code> | `str` |
| `strptime` | 从字符串解析为 datetime，返回指针。 | <code>{func, datetime_datetime.strptime(日期字符串: string, 格式: string)}</code> | `str` |
| `time` | 返回时间部分，返回 time 指针。 | <code>{func, datetime_datetime.time(datetime指针: ptr)}</code> | `ptr` |
| `timetuple` | 返回时间元组指针。 | <code>{func, datetime_datetime.timetuple(datetime指针: ptr)}</code> | `ptr` |
| `today` | 返回今天日期（时间部分为0）的 datetime 指针。 | <code>{func, datetime_datetime.today()}</code> | `ptr` |
| `toordinal` | 返回 Gregorian 序数。 | <code>{func, datetime_datetime.toordinal(datetime指针: ptr)}</code> | `int` |
| `weekday` | 返回星期几（0-6）。 | <code>{func, datetime_datetime.weekday(datetime指针: ptr)}</code> | `int` |
| `greater` | 比较大于，返回布尔值。 | <code>{func, datetime_datetime.greater(指针A: ptr, 指针B: ptr)}</code> | `bool` |
| `less` | 小于，返回布尔值。 | <code>{func, datetime_datetime.less(指针A: ptr, 指针B: ptr)}</code> | `bool` |
| `greater_equal` | 大于等于，返回布尔值。 | <code>{func, datetime_datetime.greater_equal(指针A: ptr, 指针B: ptr)}</code> | `bool` |
| `less_equal` | 小于等于，返回布尔值。 | <code>{func, datetime_datetime.less_equal(指针A: ptr, 指针B: ptr)}</code> | `bool` |
| `equal` | 相等，返回布尔值。 | <code>{func, datetime_datetime.equal(指针A: ptr, 指针B: ptr)}</code> | `bool` |
| `add_delta` | 加 timedelta，返回新 datetime 指针。 | <code>{func, datetime_datetime.add_delta(datetime指针: ptr, timedelta指针: ptr)}</code> | `ptr` |
| `remove_delta` | 减 timedelta，返回新 datetime 指针。 | <code>{func, datetime_datetime.remove_delta(datetime指针: ptr, timedelta指针: ptr)}</code> | `ptr` |
| `remove_datetime` | 两 datetime 相减，返回 timedelta 指针。 | <code>{func, datetime_datetime.remove_datetime(指针A: ptr, 指针B: ptr)}</code> | `ptr` |

---

<a id="datetime_date"></a>

## datetime_date

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `new` | 创建 date 对象，年、月、日必选，返回指针。 | <code>{func, datetime_date.new(年: int, 月: int, 日: int)}</code> | `ptr` |
| `format` | 返回 date 的字符串表示。 | <code>{func, datetime_date.format(date指针: ptr)}</code> | `str` |
| `ctime` | 返回 C 风格日期字符串。 | <code>{func, datetime_date.ctime(date指针: ptr)}</code> | `str` |
| `day` | 返回日，返回整数。 | <code>{func, datetime_date.day(date指针: ptr)}</code> | `int` |
| `fromordinal` | 从序数创建 date，返回指针。 | <code>{func, datetime_date.fromordinal(序数: int)}</code> | `int` |
| `fromtimestamp` | 从时间戳创建 date，返回指针。 | <code>{func, datetime_date.fromtimestamp(时间戳: float)}</code> | `ptr` |
| `isocalendar` | 返回 ISO 日历元组指针。 | <code>{func, datetime_date.isocalendar(date指针: ptr)}</code> | `ptr` |
| `isoformat` | 返回 ISO 格式字符串。 | <code>{func, datetime_date.isoformat(date指针: ptr)}</code> | `str` |
| `isoweekday` | 返回 ISO 星期几，返回整数。 | <code>{func, datetime_date.isoweekday(date指针: ptr)}</code> | `int` |
| `max` | 返回最大 date 指针。 | <code>{func, datetime_date.max()}</code> | `ptr` |
| `min` | 返回最小 date 指针。 | <code>{func, datetime_date.min()}</code> | `ptr` |
| `month` | 返回月份，返回整数。 | <code>{func, datetime_date.month(date指针: ptr)}</code> | `int` |
| `replace` | 替换字段，返回新 date 指针。 | <code>{func, datetime_date.replace(date指针: ptr, 年: int, 月: int, 日: int)}</code> | `ptr` |
| `strftime` | 格式化，返回字符串。 | <code>{func, datetime_date.strftime(date指针: ptr, 格式: string)}</code> | `str` |
| `timetuple` | 返回时间元组指针。 | <code>{func, datetime_date.timetuple(date指针: ptr)}</code> | `ptr` |
| `today` | 返回今天日期指针。 | <code>{func, datetime_date.today()}</code> | `ptr` |
| `toordinal` | 返回序数。 | <code>{func, datetime_date.toordinal(date指针: ptr)}</code> | `int` |
| `weekday` | 返回星期几（0-6）。 | <code>{func, datetime_date.weekday(date指针: ptr)}</code> | `int` |
| `year` | 返回年份，返回整数。 | <code>{func, datetime_date.year(date指针: ptr)}</code> | `int` |
| `greater` | 比较大于，返回布尔值。 | <code>{func, datetime_date.greater(指针A: ptr, 指针B: ptr)}</code> | `bool` |
| `less` | 小于，返回布尔值。 | <code>{func, datetime_date.less(指针A: ptr, 指针B: ptr)}</code> | `bool` |
| `greater_equal` | 大于等于，返回布尔值。 | <code>{func, datetime_date.greater_equal(指针A: ptr, 指针B: ptr)}</code> | `bool` |
| `less_equal` | 小于等于，返回布尔值。 | <code>{func, datetime_date.less_equal(指针A: ptr, 指针B: ptr)}</code> | `bool` |
| `equal` | 相等，返回布尔值。 | <code>{func, datetime_date.equal(指针A: ptr, 指针B: ptr)}</code> | `bool` |
| `add_delta` | 加 timedelta，返回新 date 指针。 | <code>{func, datetime_date.add_delta(date指针: ptr, timedelta指针: ptr)}</code> | `ptr` |
| `remove_delta` | 减 timedelta，返回新 date 指针。 | <code>{func, datetime_date.remove_delta(date指针: ptr, timedelta指针: ptr)}</code> | `ptr` |
| `remove_date` | 两 date 相减，返回 timedelta 指针。 | <code>{func, datetime_date.remove_date(指针A: ptr, 指针B: ptr)}</code> | `ptr` |

---

<a id="datetime_time"></a>

## datetime_time

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `new` | 创建 time 对象，时、分、秒、微秒可选，返回指针。 | <code>{func, datetime_time.new(时?: int, 分: int, 秒: int, 微秒: int)}</code> | `ptr` |
| `format` | 返回 time 的字符串表示。 | <code>{func, datetime_time.format()}</code> | `str` |

---

<a id="command"></a>

## command

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `set_executor` | 设置命令的执行者实体ID，返回布尔值。 | <code>{func, command.set_executor(实体ID: string)}</code> | `bool` |
| `get_executor` | 获取当前命令执行者的实体ID（字符串）。 | <code>{func, command.get_executor()}</code> | `str` |
| `set_position` | 设置命令执行点的三维坐标，返回布尔值。 | <code>{func, command.set_position(x: float, y: float, z: float)}</code> | `bool` |
| `get_position` | 获取当前命令执行点的坐标，返回指向三元组 (x,y,z) 的指针。 | <code>{func, command.get_position()}</code> | `ptr` |
| `set_dimension` | 设置命令执行的维度ID，返回布尔值。 | <code>{func, command.set_dimension(维度ID: int)}</code> | `bool` |
| `get_dimension` | 获取当前命令执行的维度ID（整数）。 | <code>{func, command.get_dimension()}</code> | `int` |
| `dimension_name` | 获取当前命令执行维度的英文名称（字符串）。 | <code>{func, command.dimension_name()}</code> | `str` |
| `fast_set` | 快速将命令执行上下文切换到指定实体（通过选择器或实体ID）。若 is_selector=True（默认），则第一个参数为目标选择器字符串，必须唯一匹配一个实体；若为 False，则第一个参数为实体ID字符串，返回布尔值。 | <code>{func, command.fast_set(选择器或实体ID: string, 是否为选择器: bool)}</code> | `bool` |

---

<a id="general"></a>

## general

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `BroadcastEvent` | 在本地服务端广播事件。事件数据必须是指针，返回布尔值。 | <code>{func, general.BroadcastEvent(事件名: string, 事件数据指针: ptr)}</code> | `bool` |
| `BroadcastToAllClient` | 广播事件到所有客户端。事件数据必须是指针，返回布尔值。 | <code>{func, general.BroadcastToAllClient(事件名: string, 事件数据指针: ptr)}</code> | `bool` |
| `GetEngineNamespace` | 获取引擎命名空间，返回指向字符串的指针。 | <code>{func, general.GetEngineNamespace()}</code> | `ptr` |
| `GetEngineSystemName` | 获取引擎系统名称，返回指向字符串的指针。 | <code>{func, general.GetEngineSystemName()}</code> | `ptr` |
| `NotifyToClient` | 发送事件到指定客户端。事件数据必须是指针，返回布尔值。 | <code>{func, general.NotifyToClient(玩家ID: string, 事件名: string, 事件数据指针: ptr)}</code> | `bool` |
| `NotifyToMultiClients` | 发送事件到多个客户端。玩家ID列表必须是指针，事件数据也须是指针，返回布尔值。 | <code>{func, general.NotifyToMultiClients(玩家ID列表指针: ptr, 事件名: string, 事件数据指针: ptr)}</code> | `bool` |
| `GetMinecraftVersion` | 获取游戏版本，返回指向字符串的指针。 | <code>{func, general.GetMinecraftVersion()}</code> | `ptr` |
| `GetPlatform` | 获取运行平台，返回指向字符串的指针。 | <code>{func, general.GetPlatform()}</code> | `ptr` |
| `GetHostPlayerId` | 获取主机玩家ID，返回指向字符串的指针。 | <code>{func, general.GetHostPlayerId()}</code> | `ptr` |
| `GetServerTickTime` | 获取服务器当前tick时间（毫秒），返回指向浮点数的指针。 | <code>{func, general.GetServerTickTime()}</code> | `ptr` |

---

<a id="world"></a>

## world

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `CanSee` | 检查一个实体是否能看见另一个实体。返回指向布尔值的指针。 | <code>{func, world.CanSee(源实体ID: string, 目标实体ID: string, 视距?: float, 仅固体?: bool, 水平角?: float, 垂直角?: float)}</code> | `ptr` |
| `CheckBlockToPos` | 检查从起点到终点的方块碰撞。返回指向布尔值的指针。 | <code>{func, world.CheckBlockToPos(起点位置指针: ptr, 终点位置指针: ptr, 维度ID?: int)}</code> | `ptr` |
| `CheckChunkState` | 检查指定区块的加载状态。返回指向布尔值的指针。 | <code>{func, world.CheckChunkState(维度ID: int, 区块位置指针: ptr)}</code> | `ptr` |
| `GetAllAreaKeys` | 获取所有常加载区域键列表，返回指向字符串列表的指针。 | <code>{func, world.GetAllAreaKeys()}</code> | `ptr` |
| `GetBiomeInfo` | 获取生物群系信息，参数为生物群系名称，返回指向信息映射的指针。 | <code>{func, world.GetBiomeInfo(生物群系名称: string)}</code> | `ptr` |
| `GetBiomeName` | 获取指定位置的生物群系名称，返回指向字符串的指针。 | <code>{func, world.GetBiomeName(位置指针: ptr, 维度ID?: int)}</code> | `ptr` |
| `GetBlockLightLevel` | 获取指定方块位置的光照等级，返回指向整数的指针。 | <code>{func, world.GetBlockLightLevel(位置指针: ptr, 维度ID?: int)}</code> | `ptr` |
| `GetChunkEntites` | 获取指定区块内的所有实体ID列表，返回指向列表的指针。 | <code>{func, world.GetChunkEntites(维度ID: int, 区块位置指针: ptr)}</code> | `ptr` |
| `GetChunkMobNum` | 获取指定区块内的怪物数量，返回指向整数的指针。 | <code>{func, world.GetChunkMobNum(维度ID: int, 区块位置指针: ptr)}</code> | `ptr` |
| `GetEntitiesAround` | 获取指定实体周围的实体列表（可带过滤器），返回指向实体ID列表的指针。 | <code>{func, world.GetEntitiesAround(实体ID: string, 半径: float, 过滤器指针: ptr)}</code> | `ptr` |
| `GetEntitiesAroundByType` | 获取指定实体周围指定类型的实体列表，返回指向实体ID列表的指针。 | <code>{func, world.GetEntitiesAroundByType(实体ID: string, 半径: float, 实体类型: string)}</code> | `ptr` |
| `GetEntitiesInSquareArea` | 获取正方形区域内的所有实体，返回指向实体ID列表的指针。 | <code>{func, world.GetEntitiesInSquareArea(起点位置指针: ptr, 终点位置指针: ptr, 维度ID?: int)}</code> | `ptr` |
| `GetLevelId` | 获取当前世界ID，返回指向字符串的指针。 | <code>{func, world.GetLevelId()}</code> | `ptr` |
| `GetSpawnPosition` | 获取世界出生点坐标，返回指向位置元组的指针。 | <code>{func, world.GetSpawnPosition()}</code> | `ptr` |
| `GetStructureSize` | 获取指定结构的尺寸，返回指向尺寸映射的指针。 | <code>{func, world.GetStructureSize(结构名称: string)}</code> | `ptr` |
| `IsChunkGenerated` | 检查指定区块是否已生成，返回指向布尔值的指针。 | <code>{func, world.IsChunkGenerated(维度ID: int, 区块位置指针: ptr)}</code> | `ptr` |
| `IsSlimeChunk` | 检查指定区块是否为史莱姆区块，返回指向布尔值的指针。 | <code>{func, world.IsSlimeChunk(维度ID: int, 区块位置指针: ptr)}</code> | `ptr` |
| `LocateStructureFeature` | 定位最近的结构特征，返回指向位置元组的指针。 | <code>{func, world.LocateStructureFeature(结构类型: string, 维度ID: int, 搜索中心位置指针: ptr, 仅新区块?: bool)}</code> | `ptr` |
| `MayPlace` | 检查是否可以在指定位置放置方块，返回指向布尔值的指针。 | <code>{func, world.MayPlace(方块标识符: string, 放置位置指针: ptr, 朝向: int, 维度ID?: int)}</code> | `ptr` |
| `MayPlaceOn` | 检查是否可以在指定方块上放置另一个方块，返回指向布尔值的指针。 | <code>{func, world.MayPlaceOn(玩家ID: string, 方块标识符: string, 附加值: int, 放置位置指针: ptr, 朝向: int)}</code> | `ptr` |
| `PlaceFeature` | 在指定位置放置一个地物，返回指向布尔值的指针。 | <code>{func, world.PlaceFeature(特征名称: string, 维度ID: int, 位置指针: ptr)}</code> | `ptr` |
| `SetMergeSpawnItemRadius` | 设置掉落物合并半径，返回指向布尔值的指针。 | <code>{func, world.SetMergeSpawnItemRadius(半径: float)}</code> | `ptr` |
| `CreateExperienceOrb` | 创建经验球实体，返回指向新实体ID的指针。 | <code>{func, world.CreateExperienceOrb(实体ID: string, 经验值: int, 位置指针: ptr, 是否特殊: bool)}</code> | `ptr` |
| `CreateProjectileEntity` | 创建抛射物实体，返回指向新实体ID的指针。 | <code>{func, world.CreateProjectileEntity(发射者ID: string, 抛射物标识符: string, 参数映射指针?: ptr)}</code> | `ptr` |
| `DestroyEntity` | 销毁指定实体，返回指向布尔值的指针。 | <code>{func, world.DestroyEntity(实体ID: string)}</code> | `ptr` |
| `GetDroppedItem` | 获取掉落物实体的物品数据，返回指向物品字典的指针。 | <code>{func, world.GetDroppedItem(物品实体ID: string, 获取用户数据?: bool)}</code> | `ptr` |
| `GetPlayerList` | 获取当前所有玩家的ID列表，返回指向字符串列表的指针。 | <code>{func, world.GetPlayerList()}</code> | `ptr` |
| `IsEntityAlive` | 检查实体是否存活，返回指向布尔值的指针。 | <code>{func, world.IsEntityAlive(实体ID: string)}</code> | `ptr` |
| `KillEntity` | 杀死指定实体，返回指向布尔值的指针。 | <code>{func, world.KillEntity(实体ID: string)}</code> | `ptr` |
| `GetBlockClip` | 获取方块的剪裁框，返回指向剪裁框信息的指针（具体结构需参考Mod SDK）。 | <code>{func, world.GetBlockClip(位置指针: ptr, 维度ID?: int)}</code> | `ptr` |
| `GetBlockCollision` | 获取方块的碰撞箱，返回指向碰撞箱信息的指针。 | <code>{func, world.GetBlockCollision(位置指针: ptr, 维度ID?: int)}</code> | `ptr` |
| `GetBlockNew` | 获取指定位置的方块对象，返回指向方块信息的指针。 | <code>{func, world.GetBlockNew(位置指针: ptr, 维度ID?: int)}</code> | `ptr` |
| `GetLiquidBlock` | 获取液体方块信息，返回指向液体信息的指针。 | <code>{func, world.GetLiquidBlock(位置指针: ptr, 维度ID?: int)}</code> | `ptr` |
| `GetTopBlockHeight` | 获取指定列最高非空气方块的高度，返回指向整数的指针。 | <code>{func, world.GetTopBlockHeight(列位置指针: ptr, 维度?: int)}</code> | `ptr` |
| `GetEntityLimit` | 获取当前实体数量上限，返回指向整数的指针。 | <code>{func, world.GetEntityLimit()}</code> | `ptr` |
| `SetEntityLimit` | 设置实体数量上限，返回指向布尔值的指针。 | <code>{func, world.SetEntityLimit(上限: int)}</code> | `ptr` |
| `IsRaining` | 检查当前是否下雨，返回指向布尔值的指针。 | <code>{func, world.IsRaining()}</code> | `ptr` |
| `IsThunder` | 检查当前是否打雷，返回指向布尔值的指针。 | <code>{func, world.IsThunder()}</code> | `ptr` |
| `GetLevelGravity` | 获取世界重力值，返回指向浮点数的指针。 | <code>{func, world.GetLevelGravity()}</code> | `ptr` |
| `GetPistonMaxInteractionCount` | 获取活塞最大推动方块数量，返回指向整数的指针。 | <code>{func, world.GetPistonMaxInteractionCount()}</code> | `ptr` |
| `SetHurtCD` | 设置实体受伤冷却时间，返回指向布尔值的指针。 | <code>{func, world.SetHurtCD(冷却时间tick: int)}</code> | `ptr` |
| `SetLevelGravity` | 设置世界重力值，返回指向布尔值的指针。 | <code>{func, world.SetLevelGravity(重力值: float)}</code> | `ptr` |
| `SetPistonMaxInteractionCount` | 设置活塞最大推动方块数量，返回指向布尔值的指针。 | <code>{func, world.SetPistonMaxInteractionCount(数量: int)}</code> | `ptr` |
| `SetCommand` | 执行一条命令（非设置命令方块），返回指向命令执行结果的指针。 | <code>{func, world.SetCommand(命令字符串: string, 执行者实体ID: string, 是否显示输出?: bool)}</code> | `ptr` |

---

<a id="entity"></a>

## entity

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `GetEngineType` | 获取实体的引擎类型ID，返回指向整数的指针。 | <code>{func, entity.GetEngineType(实体ID: string)}</code> | `ptr` |
| `GetEngineTypeStr` | 获取实体的引擎类型名称，返回指向字符串的指针。 | <code>{func, entity.GetEngineTypeStr(实体ID: string)}</code> | `ptr` |
| `GetEntityDefinitions` | 获取实体的定义标识符列表，返回指向字符串列表的指针。 | <code>{func, entity.GetEntityDefinitions(实体ID: string)}</code> | `ptr` |
| `GetEntityNBTTags` | 获取实体的NBT标签数据，返回指向NBT映射的指针。 | <code>{func, entity.GetEntityNBTTags(实体ID: string)}</code> | `ptr` |
| `GetAuxValue` | 获取实体的附加值（如羊的颜色），返回指向整数的指针。 | <code>{func, entity.GetAuxValue(实体ID: string)}</code> | `ptr` |
| `ChangeEntityDimension` | 将实体传送到指定维度，返回指向布尔值的指针。 | <code>{func, entity.ChangeEntityDimension(实体ID: string, 目标维度ID: int, 位置指针: ptr)}</code> | `ptr` |
| `GetAllComponentsName` | 获取实体所有组件的名称列表，返回指向字符串列表的指针。 | <code>{func, entity.GetAllComponentsName(实体ID: string)}</code> | `ptr` |
| `GetAttrMaxValue` | 获取实体属性的最大值，返回指向浮点数的指针。 | <code>{func, entity.GetAttrMaxValue(实体ID: string, 属性类型: string)}</code> | `ptr` |
| `GetAttrValue` | 获取实体属性的当前值，返回指向浮点数的指针。 | <code>{func, entity.GetAttrValue(实体ID: string, 属性类型: string)}</code> | `ptr` |
| `GetCurrentAirSupply` | 获取实体当前氧气值，返回指向整数的指针。 | <code>{func, entity.GetCurrentAirSupply(实体ID: string)}</code> | `ptr` |
| `GetDeathTime` | 获取实体死亡时间（tick），返回指向整数的指针。 | <code>{func, entity.GetDeathTime(实体ID: string)}</code> | `ptr` |
| `GetEntitiesBySelector` | 通过目标选择器获取实体列表，需要种子实体ID，返回指向实体ID列表的指针。 | <code>{func, entity.GetEntitiesBySelector(实体ID: string, 选择器: string)}</code> | `ptr` |
| `GetEntityDamage` | 获取实体攻击伤害值，返回指向浮点数的指针。 | <code>{func, entity.GetEntityDamage(实体ID: string, 目标实体ID: string)}</code> | `ptr` |
| `GetEntityDimensionId` | 获取实体所在维度ID，返回指向整数的指针。 | <code>{func, entity.GetEntityDimensionId(实体ID: string)}</code> | `ptr` |
| `GetEntityFallDistance` | 获取实体当前下落距离，返回指向浮点数的指针。 | <code>{func, entity.GetEntityFallDistance(实体ID: string)}</code> | `ptr` |
| `GetEntityLinksTag` | 获取实体链接标签，返回指向字符串的指针。 | <code>{func, entity.GetEntityLinksTag(实体ID: string)}</code> | `ptr` |
| `GetEntityOwner` | 获取实体的拥有者ID，返回指向字符串的指针。 | <code>{func, entity.GetEntityOwner(实体ID: string)}</code> | `ptr` |
| `GetFootPos` | 获取实体脚部位置坐标，返回指向位置元组的指针。 | <code>{func, entity.GetFootPos(实体ID: string)}</code> | `ptr` |
| `GetGravity` | 获取实体重力值，返回指向浮点数的指针。 | <code>{func, entity.GetGravity(实体ID: string)}</code> | `ptr` |
| `GetMarkVariant` | 获取实体标记变体，返回指向整数的指针。 | <code>{func, entity.GetMarkVariant(实体ID: string)}</code> | `ptr` |
| `GetMaxAirSupply` | 获取实体最大氧气值，返回指向整数的指针。 | <code>{func, entity.GetMaxAirSupply(实体ID: string)}</code> | `ptr` |
| `GetMobColor` | 获取生物颜色，返回指向整数的指针。 | <code>{func, entity.GetMobColor(实体ID: string)}</code> | `ptr` |
| `GetMobStrength` | 获取生物当前力量值，返回指向浮点数的指针。 | <code>{func, entity.GetMobStrength(实体ID: string)}</code> | `ptr` |
| `GetMobStrengthMax` | 获取生物最大力量值，返回指向浮点数的指针。 | <code>{func, entity.GetMobStrengthMax(实体ID: string)}</code> | `ptr` |
| `GetName` | 获取实体自定义名称，返回指向字符串的指针。 | <code>{func, entity.GetName(实体ID: string)}</code> | `ptr` |
| `GetPos` | 获取实体位置坐标，返回指向位置元组的指针。 | <code>{func, entity.GetPos(实体ID: string)}</code> | `ptr` |
| `GetRot` | 获取实体旋转角度（俯仰, 偏航），返回指向旋转元组的指针。 | <code>{func, entity.GetRot(实体ID: string)}</code> | `ptr` |
| `GetSize` | 获取实体尺寸（宽度, 高度），返回指向尺寸元组的指针。 | <code>{func, entity.GetSize(实体ID: string)}</code> | `ptr` |
| `GetTradeLevel` | 获取村民交易等级，返回指向整数的指针。 | <code>{func, entity.GetTradeLevel(实体ID: string)}</code> | `ptr` |
| `GetTypeFamily` | 获取实体所属家族类型，返回指向字符串的指针。 | <code>{func, entity.GetTypeFamily(实体ID: string)}</code> | `ptr` |
| `GetUnitBubbleAirSupply` | 获取单位气泡氧气值，返回指向浮点数的指针。 | <code>{func, entity.GetUnitBubbleAirSupply()}</code> | `ptr` |
| `GetVariant` | 获取实体变种ID，返回指向整数的指针。 | <code>{func, entity.GetVariant(实体ID: string)}</code> | `ptr` |
| `HasChest` | 检查实体是否携带箱子，返回指向布尔值的指针。 | <code>{func, entity.HasChest(实体ID: string)}</code> | `ptr` |
| `HasComponent` | 检查实体是否拥有指定组件，返回指向布尔值的指针。 | <code>{func, entity.HasComponent(实体ID: string, 组件名: string)}</code> | `ptr` |
| `HasSaddle` | 检查实体是否装备鞍，返回指向布尔值的指针。 | <code>{func, entity.HasSaddle(实体ID: string)}</code> | `ptr` |
| `IsAngry` | 检查实体是否愤怒，返回指向布尔值的指针。 | <code>{func, entity.IsAngry(实体ID: string)}</code> | `ptr` |
| `IsBaby` | 检查实体是否为幼年，返回指向布尔值的指针。 | <code>{func, entity.IsBaby(实体ID: string)}</code> | `ptr` |
| `IsConsumingAirSupply` | 检查实体是否在消耗氧气，返回指向布尔值的指针。 | <code>{func, entity.IsConsumingAirSupply(实体ID: string)}</code> | `ptr` |
| `IsIllagerCaptain` | 检查实体是否为灾厄队长，返回指向布尔值的指针。 | <code>{func, entity.IsIllagerCaptain(实体ID: string)}</code> | `ptr` |
| `IsNaturallySpawned` | 检查实体是否自然生成，返回指向布尔值的指针。 | <code>{func, entity.IsNaturallySpawned(实体ID: string)}</code> | `ptr` |
| `IsOutOfControl` | 检查实体是否失控，返回指向布尔值的指针。 | <code>{func, entity.IsOutOfControl(实体ID: string)}</code> | `ptr` |
| `IsPregnant` | 检查实体是否怀孕，返回指向布尔值的指针。 | <code>{func, entity.IsPregnant(实体ID: string)}</code> | `ptr` |
| `IsSheared` | 检查实体是否被剪毛，返回指向布尔值的指针。 | <code>{func, entity.IsSheared(实体ID: string)}</code> | `ptr` |
| `IsSitting` | 检查实体是否坐下，返回指向布尔值的指针。 | <code>{func, entity.IsSitting(实体ID: string)}</code> | `ptr` |
| `IsTamed` | 检查实体是否被驯服，返回指向布尔值的指针。 | <code>{func, entity.IsTamed(实体ID: string)}</code> | `ptr` |
| `PromoteToIllagerCaptain` | 将实体提升为灾厄队长，返回指向布尔值的指针。 | <code>{func, entity.PromoteToIllagerCaptain(实体ID: string)}</code> | `ptr` |
| `ResetToDefaultValue` | 将实体属性重置为默认值，返回指向布尔值的指针。 | <code>{func, entity.ResetToDefaultValue(实体ID: string, 属性类型: string)}</code> | `ptr` |
| `ResetToMaxValue` | 将实体属性重置为最大值，返回指向布尔值的指针。 | <code>{func, entity.ResetToMaxValue(实体ID: string, 属性类型: string)}</code> | `ptr` |
| `SetAngry` | 设置实体愤怒状态，可指定目标ID，返回指向布尔值的指针。 | <code>{func, entity.SetAngry(实体ID: string, 是否愤怒: bool, 目标ID: string)}</code> | `ptr` |
| `SetAsAdult` | 将实体设为成年，返回指向布尔值的指针。 | <code>{func, entity.SetAsAdult(实体ID: string)}</code> | `ptr` |
| `SetAttrMaxValue` | 设置实体属性最大值，返回指向布尔值的指针。 | <code>{func, entity.SetAttrMaxValue(实体ID: string, 属性类型: string, 最大值: float)}</code> | `ptr` |
| `SetAttrValue` | 设置实体属性当前值，可指定是否设为默认值，返回指向布尔值的指针。 | <code>{func, entity.SetAttrValue(实体ID: string, 属性类型: string, 值: float, set_default: int)}</code> | `ptr` |
| `SetChest` | 设置实体是否携带箱子，返回指向布尔值的指针。 | <code>{func, entity.SetChest(实体ID: string, 是否有箱子: bool)}</code> | `ptr` |
| `SetCurrentAirSupply` | 设置实体当前氧气值，返回指向布尔值的指针。 | <code>{func, entity.SetCurrentAirSupply(实体ID: string, 氧气值: int)}</code> | `ptr` |
| `SetEntityLookAtPos` | 设置实体注视某个位置，返回指向布尔值的指针。 | <code>{func, entity.SetEntityLookAtPos(实体ID: string, 目标位置指针: ptr, 最小时间: float, 最大时间: float, 是否拒绝: bool)}</code> | `ptr` |
| `SetEntityOwner` | 设置实体的拥有者，返回指向布尔值的指针。 | <code>{func, entity.SetEntityOwner(实体ID: string, 主人ID: string)}</code> | `ptr` |
| `SetGravity` | 设置实体重力值，返回指向布尔值的指针。 | <code>{func, entity.SetGravity(实体ID: string, 重力值: float)}</code> | `ptr` |
| `SetMarkVariant` | 设置实体标记变体，返回指向布尔值的指针。 | <code>{func, entity.SetMarkVariant(实体ID: string, 变体: int)}</code> | `ptr` |
| `SetMaxAirSupply` | 设置实体最大氧气值，返回指向布尔值的指针。 | <code>{func, entity.SetMaxAirSupply(实体ID: string, 最大氧气: int)}</code> | `ptr` |
| `SetMobColor` | 设置生物颜色，返回指向布尔值的指针。 | <code>{func, entity.SetMobColor(实体ID: string, 颜色: int)}</code> | `ptr` |
| `SetMobStrength` | 设置生物力量值，返回指向布尔值的指针。 | <code>{func, entity.SetMobStrength(实体ID: string, 力量: float)}</code> | `ptr` |
| `SetMobStrengthMax` | 设置生物最大力量值，返回指向布尔值的指针。 | <code>{func, entity.SetMobStrengthMax(实体ID: string, 最大力量: float)}</code> | `ptr` |
| `SetName` | 设置实体自定义名称，返回指向布尔值的指针。 | <code>{func, entity.SetName(实体ID: string, 名称: string)}</code> | `ptr` |
| `SetOutOfControl` | 设置实体失控状态，返回指向布尔值的指针。 | <code>{func, entity.SetOutOfControl(实体ID: string, 是否失控: bool)}</code> | `ptr` |
| `SetPersistent` | 设置实体是否持久存在（不消失），返回指向布尔值的指针。 | <code>{func, entity.SetPersistent(实体ID: string, 是否持久: bool)}</code> | `ptr` |
| `SetPos` | 设置实体位置，返回指向布尔值的指针。 | <code>{func, entity.SetPos(实体ID: string, 位置指针: ptr)}</code> | `ptr` |
| `SetRecoverTotalAirSupplyTime` | 设置实体恢复全部氧气所需时间，返回指向布尔值的指针。 | <code>{func, entity.SetRecoverTotalAirSupplyTime(实体ID: string, 时间tick: int)}</code> | `ptr` |
| `SetRot` | 设置实体旋转角度，返回指向布尔值的指针。 | <code>{func, entity.SetRot(实体ID: string, 旋转指针: ptr)}</code> | `ptr` |
| `SetSheared` | 设置实体剪毛状态，返回指向布尔值的指针。 | <code>{func, entity.SetSheared(实体ID: string, 是否剪毛: bool)}</code> | `ptr` |
| `SetSitting` | 设置实体坐下状态，返回指向布尔值的指针。 | <code>{func, entity.SetSitting(实体ID: string, 是否坐下: bool)}</code> | `ptr` |
| `SetSize` | 设置实体尺寸，返回指向布尔值的指针。 | <code>{func, entity.SetSize(实体ID: string, 尺寸指针: ptr)}</code> | `ptr` |
| `SetTradeLevel` | 设置村民交易等级，返回指向布尔值的指针。 | <code>{func, entity.SetTradeLevel(实体ID: string, 等级: int)}</code> | `ptr` |
| `SetVariant` | 设置实体变种，返回指向布尔值的指针。 | <code>{func, entity.SetVariant(实体ID: string, 变种: int)}</code> | `ptr` |
| `GetAttackTarget` | 获取实体的攻击目标ID，返回指向字符串的指针。 | <code>{func, entity.GetAttackTarget(实体ID: string)}</code> | `ptr` |
| `GetBlockControlAi` | 获取实体是否被阻挡AI控制，返回指向布尔值的指针。 | <code>{func, entity.GetBlockControlAi(实体ID: string)}</code> | `ptr` |
| `GetComponents` | 获取实体的所有组件名称列表，返回指向字符串列表的指针。 | <code>{func, entity.GetComponents(实体ID: string)}</code> | `ptr` |
| `GetJumpPower` | 获取实体的跳跃力，返回指向浮点数的指针。 | <code>{func, entity.GetJumpPower(实体ID: string)}</code> | `ptr` |
| `GetLeashHolder` | 获取拴绳的主人实体ID，返回指向字符串的指针。 | <code>{func, entity.GetLeashHolder(实体ID: string)}</code> | `ptr` |
| `GetMotion` | 获取实体的运动向量，返回指向速度元组 (vx,vy,vz) 的指针。 | <code>{func, entity.GetMotion(实体ID: string)}</code> | `ptr` |
| `GetOwnerId` | 获取驯服实体的主人ID，返回指向字符串的指针。 | <code>{func, entity.GetOwnerId(实体ID: string)}</code> | `ptr` |
| `GetStepHeight` | 获取实体的步高，返回指向浮点数的指针。 | <code>{func, entity.GetStepHeight(实体ID: string)}</code> | `ptr` |
| `ImmuneDamage` | 检查实体是否对某种伤害免疫，返回指向布尔值的指针。 | <code>{func, entity.ImmuneDamage(实体ID: string, 伤害来源: string)}</code> | `ptr` |
| `IsEating` | 检查实体是否在进食，返回指向布尔值的指针。 | <code>{func, entity.IsEating(实体ID: string)}</code> | `ptr` |
| `IsEntityOnFire` | 检查实体是否着火，返回指向布尔值的指针。 | <code>{func, entity.IsEntityOnFire(实体ID: string)}</code> | `ptr` |
| `IsLootDropped` | 检查实体死亡是否掉落物品，返回指向布尔值的指针。 | <code>{func, entity.IsLootDropped(实体ID: string)}</code> | `ptr` |
| `IsPersistent` | 检查实体是否持久存在，返回指向布尔值的指针。 | <code>{func, entity.IsPersistent(实体ID: string)}</code> | `ptr` |
| `IsRoaring` | 检查实体是否在咆哮，返回指向布尔值的指针。 | <code>{func, entity.IsRoaring(实体ID: string)}</code> | `ptr` |
| `IsStunned` | 检查实体是否眩晕，返回指向布尔值的指针。 | <code>{func, entity.IsStunned(实体ID: string)}</code> | `ptr` |
| `ResetAttackTarget` | 重置攻击目标，返回指向布尔值的指针。 | <code>{func, entity.ResetAttackTarget(实体ID: string)}</code> | `ptr` |
| `ResetMotion` | 重置运动向量，返回指向布尔值的指针。 | <code>{func, entity.ResetMotion(实体ID: string)}</code> | `ptr` |
| `ResetStepHeight` | 重置步高为默认值，返回指向布尔值的指针。 | <code>{func, entity.ResetStepHeight(实体ID: string)}</code> | `ptr` |
| `SetActorCollidable` | 设置实体是否可碰撞，返回指向布尔值的指针。 | <code>{func, entity.SetActorCollidable(实体ID: string, 是否可碰撞: bool)}</code> | `ptr` |
| `SetActorPushable` | 设置实体是否可被推动，返回指向布尔值的指针。 | <code>{func, entity.SetActorPushable(实体ID: string, 是否可推动: bool)}</code> | `ptr` |
| `SetAttackTarget` | 设置攻击目标，返回指向布尔值的指针。 | <code>{func, entity.SetAttackTarget(实体ID: string, 目标ID: string)}</code> | `ptr` |
| `SetBlockControlAi` | 设置是否阻挡AI控制，返回指向布尔值的指针。 | <code>{func, entity.SetBlockControlAi(实体ID: string, 是否阻挡: bool, freeze_anim: bool)}</code> | `ptr` |
| `SetEntityOnFire` | 设置实体着火状态，返回指向布尔值的指针。 | <code>{func, entity.SetEntityOnFire(实体ID: string, 秒数: float, 燃烧伤害: int)}</code> | `ptr` |
| `SetEntityTamed` | 设置实体驯服状态，返回指向布尔值的指针。 | <code>{func, entity.SetEntityTamed(实体ID: string, 玩家ID: string)}</code> | `ptr` |
| `SetJumpPower` | 设置跳跃力，返回指向布尔值的指针。 | <code>{func, entity.SetJumpPower(实体ID: string, 跳跃力: float)}</code> | `ptr` |
| `SetLeashHolder` | 设置拴绳主人，返回指向布尔值的指针。 | <code>{func, entity.SetLeashHolder(实体ID: string, 主人ID: string)}</code> | `ptr` |
| `SetLootDropped` | 设置死亡是否掉落物品，返回指向布尔值的指针。 | <code>{func, entity.SetLootDropped(实体ID: string, 是否掉落: bool)}</code> | `ptr` |
| `SetMobKnockback` | 设置击退初始速度，返回布尔值 True（直接值，非指针）。 | <code>{func, entity.SetMobKnockback(实体ID: string, xd?: float, zd?: float, power?: float, height?: float, height_cap?: float)}</code> | `bool` |
| `SetMotion` | 设置运动向量，返回指向布尔值的指针。 | <code>{func, entity.SetMotion(实体ID: string, 运动向量指针: ptr)}</code> | `ptr` |
| `SetPersistence` | 设置实体持久化（不消失），返回布尔值 True（直接值，非指针）。 | <code>{func, entity.SetPersistence(实体ID: string, 是否持久: bool)}</code> | `bool` |
| `SetStepHeight` | 设置步高，返回指向布尔值的指针。 | <code>{func, entity.SetStepHeight(实体ID: string, 步高: float)}</code> | `ptr` |
| `AddEffectToEntity` | 为实体添加状态效果，返回指向布尔值的指针。 | <code>{func, entity.AddEffectToEntity(实体ID: string, 效果名: string, 持续时间: int, 等级: int, 是否显示粒子: bool)}</code> | `ptr` |
| `GetAllEffects` | 获取实体所有状态效果，返回指向效果列表的指针。 | <code>{func, entity.GetAllEffects(实体ID: string)}</code> | `ptr` |
| `HasEffect` | 检查实体是否有指定效果，返回指向布尔值的指针。 | <code>{func, entity.HasEffect(实体ID: string, 效果名: string)}</code> | `ptr` |
| `RemoveEffectFromEntity` | 移除实体的指定状态效果，返回指向布尔值的指针。 | <code>{func, entity.RemoveEffectFromEntity(实体ID: string, 效果名: string)}</code> | `ptr` |
| `GetEntityItem` | 获取实体手中的物品，返回指向物品字典的指针。 | <code>{func, entity.GetEntityItem(实体ID: string, 槽位类型: string, 槽位索引: int, 获取用户数据?: bool)}</code> | `ptr` |
| `GetEquItemEnchant` | 获取装备物品的附魔信息，返回指向附魔数据映射的指针。 | <code>{func, entity.GetEquItemEnchant(玩家ID: string, 槽位索引: int)}</code> | `ptr` |
| `GetEquItemModEnchant` | 获取装备物品的模组附魔信息，返回指向附魔数据映射的指针。 | <code>{func, entity.GetEquItemModEnchant(玩家ID: string, 槽位索引: int)}</code> | `ptr` |
| `CleanExtraData` | 清除实体的自定义数据（指定键），返回指向布尔值的指针。 | <code>{func, entity.CleanExtraData(实体ID: string, 键: string)}</code> | `ptr` |
| `GetExtraData` | 获取实体的自定义数据（指定键），返回指向数据值的指针。 | <code>{func, entity.GetExtraData(实体ID: string, 键: string)}</code> | `ptr` |
| `GetWholeExtraData` | 获取实体的全部自定义数据，返回指向映射的指针。 | <code>{func, entity.GetWholeExtraData(实体ID: string)}</code> | `ptr` |
| `SaveExtraData` | 保存实体的自定义数据，返回指向布尔值的指针。 | <code>{func, entity.SaveExtraData(实体ID: string)}</code> | `ptr` |
| `SetExtraData` | 设置实体的自定义数据，返回指向布尔值的指针。 | <code>{func, entity.SetExtraData(实体ID: string, 键: string, 值或指针: any, 是否为指针?: bool, 自动保存?: bool)}</code> | `ptr` |
| `AddEntityTag` | 为实体添加标签，返回指向布尔值的指针。 | <code>{func, entity.AddEntityTag(实体ID: string, 标签: string)}</code> | `ptr` |
| `EntityHasTag` | 检查实体是否有指定标签，返回指向布尔值的指针。 | <code>{func, entity.EntityHasTag(实体ID: string, 标签: string)}</code> | `ptr` |
| `GetEntityTags` | 获取实体的所有标签列表，返回指向字符串列表的指针。 | <code>{func, entity.GetEntityTags(实体ID: string)}</code> | `ptr` |
| `RemoveEntityTag` | 移除实体的指定标签，返回指向布尔值的指针。 | <code>{func, entity.RemoveEntityTag(实体ID: string, 标签: string)}</code> | `ptr` |
| `GetSourceEntityId` | 获取抛射物的发射者实体ID，返回指向字符串的指针。 | <code>{func, entity.GetSourceEntityId(抛射物实体ID: string)}</code> | `ptr` |
| `GetOrbExperience` | 获取经验球的经验值，返回指向整数的指针。 | <code>{func, entity.GetOrbExperience(经验球实体ID: string)}</code> | `ptr` |
| `SetOrbExperience` | 设置经验球的经验值，返回指向布尔值的指针。 | <code>{func, entity.SetOrbExperience(经验球实体ID: string, 经验值: int)}</code> | `ptr` |

---

<a id="player"></a>

## player

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `GetPlayerExp` | 获取玩家当前经验值（等级内进度），返回指向浮点数的指针。 | <code>{func, player.GetPlayerExp(玩家ID: string, 是否百分比: bool)}</code> | `ptr` |
| `GetPlayerHunger` | 获取玩家饥饿值，返回指向整数的指针。 | <code>{func, player.GetPlayerHunger(玩家ID: string)}</code> | `ptr` |
| `GetPlayerTotalExp` | 获取玩家总经验值（等级），返回指向整数的指针。 | <code>{func, player.GetPlayerTotalExp(玩家ID: string)}</code> | `ptr` |
| `SetPlayerHunger` | 设置玩家饥饿值，返回指向布尔值的指针。 | <code>{func, player.SetPlayerHunger(玩家ID: string, 饥饿值: int)}</code> | `ptr` |
| `SetPlayerPrefixAndSuffixName` | 设置玩家名字的前缀和后缀（带颜色），返回指向布尔值的指针。 | <code>{func, player.SetPlayerPrefixAndSuffixName(玩家ID: string, 前缀: string, 前缀颜色: string, 后缀: string, 后缀颜色: string, 名字颜色: string)}</code> | `ptr` |
| `SetPlayerTotalExp` | 设置玩家总经验值（等级），返回指向布尔值的指针。 | <code>{func, player.SetPlayerTotalExp(玩家ID: string, 经验值: int)}</code> | `ptr` |
| `ChangePlayerDimension` | 将玩家传送到指定维度，返回指向布尔值的指针。 | <code>{func, player.ChangePlayerDimension(玩家ID: string, 维度ID: int, 位置指针: ptr)}</code> | `ptr` |
| `ChangePlayerFlyState` | 更改玩家飞行状态（允许/禁止飞行），返回指向布尔值的指针。 | <code>{func, player.ChangePlayerFlyState(玩家ID: string, 是否允许飞行: bool, 是否立即起飞: bool)}</code> | `ptr` |
| `GetPlayerRespawnPos` | 获取玩家重生点坐标，返回指向位置元组的指针。 | <code>{func, player.GetPlayerRespawnPos(玩家ID: string)}</code> | `ptr` |
| `IsPlayerCanFly` | 检查玩家是否允许飞行，返回指向布尔值的指针。 | <code>{func, player.IsPlayerCanFly(玩家ID: string)}</code> | `ptr` |
| `IsPlayerFlying` | 检查玩家是否正在飞行，返回指向布尔值的指针。 | <code>{func, player.IsPlayerFlying(玩家ID: string)}</code> | `ptr` |
| `SetBanPlayerFishing` | 设置禁止玩家钓鱼，返回指向布尔值的指针。 | <code>{func, player.SetBanPlayerFishing(玩家ID: string, 是否禁止: bool)}</code> | `ptr` |
| `SetPickUpArea` | 设置玩家物品拾取范围，返回指向布尔值的指针。 | <code>{func, player.SetPickUpArea(玩家ID: string, 区域指针: ptr)}</code> | `ptr` |
| `SetPlayerAttackSpeedAmplifier` | 设置玩家攻击速度倍率，返回指向布尔值的指针。 | <code>{func, player.SetPlayerAttackSpeedAmplifier(玩家ID: string, 倍率: float)}</code> | `ptr` |
| `SetPlayerMotion` | 设置玩家运动向量，返回指向布尔值的指针。 | <code>{func, player.SetPlayerMotion(玩家ID: string, 运动向量指针: ptr)}</code> | `ptr` |
| `SetPlayerRespawnPos` | 设置玩家重生点（固定维度为0），返回指向布尔值的指针。 | <code>{func, player.SetPlayerRespawnPos(玩家ID: string, 位置指针: ptr)}</code> | `ptr` |
| `isSneaking` | 检查玩家是否潜行，返回指向布尔值的指针。 | <code>{func, player.isSneaking(玩家ID: string)}</code> | `ptr` |
| `isSwimming` | 检查玩家是否游泳，返回指向布尔值的指针。 | <code>{func, player.isSwimming(玩家ID: string)}</code> | `ptr` |
| `AddEnchantToInvItem` | 为背包物品添加附魔，返回指向布尔值的指针。 | <code>{func, player.AddEnchantToInvItem(玩家ID: string, 槽位索引: int, 附魔ID: int, 等级: int)}</code> | `ptr` |
| `AddModEnchantToInvItem` | 为背包物品添加模组附魔，返回指向布尔值的指针。 | <code>{func, player.AddModEnchantToInvItem(玩家ID: string, 槽位索引: int, 模组附魔ID: int, 等级: int)}</code> | `ptr` |
| `ChangePlayerItemTipsAndExtraId` | 修改玩家物品的提示文本和额外ID，返回指向布尔值的指针。 | <code>{func, player.ChangePlayerItemTipsAndExtraId(玩家ID: string, 槽位类型: string, 槽位索引: int, 自定义提示?: string, 额外ID?: string)}</code> | `ptr` |
| `ChangeSelectSlot` | 改变玩家当前选中的快捷栏槽位，返回指向布尔值的指针。 | <code>{func, player.ChangeSelectSlot(玩家ID: string, 新槽位: int)}</code> | `ptr` |
| `GetInvItemEnchantData` | 获取背包物品的附魔数据，返回指向附魔数据映射的指针。 | <code>{func, player.GetInvItemEnchantData(玩家ID: string, 槽位索引: int)}</code> | `ptr` |
| `GetInvItemModEnchantData` | 获取背包物品的模组附魔数据，返回指向附魔数据映射的指针。 | <code>{func, player.GetInvItemModEnchantData(玩家ID: string, 槽位索引: int)}</code> | `ptr` |
| `GetPlayerItem` | 获取玩家背包中的物品，返回指向物品字典的指针。 | <code>{func, player.GetPlayerItem(玩家ID: string, 槽位类型: string, 槽位索引: int, 获取用户数据?: bool)}</code> | `ptr` |
| `GetSelectSlotId` | 获取玩家当前选中的快捷栏槽位ID，返回指向整数的指针。 | <code>{func, player.GetSelectSlotId(玩家ID: string)}</code> | `ptr` |
| `RemoveEnchantToInvItem` | 移除背包物品的附魔，返回指向布尔值的指针。 | <code>{func, player.RemoveEnchantToInvItem(玩家ID: string, 槽位索引: int, 附魔ID: int)}</code> | `ptr` |
| `RemoveModEnchantToInvItem` | 移除背包物品的模组附魔，返回指向布尔值的指针。 | <code>{func, player.RemoveModEnchantToInvItem(玩家ID: string, 槽位索引: int, 模组附魔ID: int)}</code> | `ptr` |
| `SetInvItemExchange` | 交换背包中的两个物品，返回指向布尔值的指针。 | <code>{func, player.SetInvItemExchange(玩家ID: string, 槽位A: int, 槽位B: int)}</code> | `ptr` |
| `GetPlayerGameType` | 获取玩家的游戏模式，返回指向整数的指针。 | <code>{func, player.GetPlayerGameType(玩家ID: string)}</code> | `ptr` |
| `SetPlayerGameType` | 设置玩家的游戏模式，返回指向布尔值的指针。 | <code>{func, player.SetPlayerGameType(玩家ID: string, 游戏模式: int)}</code> | `ptr` |
| `GetPlayerAbilities` | 获取玩家能力映射，返回指向映射的指针。 | <code>{func, player.GetPlayerAbilities(玩家ID: string)}</code> | `ptr` |
| `GetPlayerOperation` | 获取玩家权限等级，返回指向整数的指针。 | <code>{func, player.GetPlayerOperation(玩家ID: string)}</code> | `ptr` |
| `SetAttackMobsAbility` | 设置玩家攻击生物的权限，返回指向布尔值的指针。 | <code>{func, player.SetAttackMobsAbility(玩家ID: string, 是否允许: bool)}</code> | `ptr` |
| `SetAttackPlayersAbility` | 设置玩家攻击玩家的权限，返回指向布尔值的指针。 | <code>{func, player.SetAttackPlayersAbility(玩家ID: string, 是否允许: bool)}</code> | `ptr` |
| `SetBuildAbility` | 设置玩家建筑权限，返回指向布尔值的指针。 | <code>{func, player.SetBuildAbility(玩家ID: string, 是否允许: bool)}</code> | `ptr` |
| `SetMineAbility` | 设置玩家挖掘权限，返回指向布尔值的指针。 | <code>{func, player.SetMineAbility(玩家ID: string, 是否允许: bool)}</code> | `ptr` |
| `SetOpenContainersAbility` | 设置玩家打开容器权限，返回指向布尔值的指针。 | <code>{func, player.SetOpenContainersAbility(玩家ID: string, 是否允许: bool)}</code> | `ptr` |
| `SetOperateDoorsAndSwitchesAbility` | 设置玩家操作门和开关权限，返回指向布尔值的指针。 | <code>{func, player.SetOperateDoorsAndSwitchesAbility(玩家ID: string, 是否允许: bool)}</code> | `ptr` |
| `SetOperatorAbility` | 设置玩家使用管理员命令权限，返回指向布尔值的指针。 | <code>{func, player.SetOperatorAbility()}</code> | `ptr` |
| `SetPermissionLevel` | 设置玩家权限等级，返回指向布尔值的指针。 | <code>{func, player.SetPermissionLevel(玩家ID: string, 权限等级: int)}</code> | `ptr` |
| `SetPlayerMute` | 设置玩家禁言状态，返回指向布尔值的指针。 | <code>{func, player.SetPlayerMute(玩家ID: string, 是否禁言: bool)}</code> | `ptr` |
| `SetTeleportAbility` | 设置玩家传送权限，返回指向布尔值的指针。 | <code>{func, player.SetTeleportAbility(玩家ID: string, 是否允许: bool)}</code> | `ptr` |

---

<a id="block"></a>

## block

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `GetBlockStates` | 获取方块的状态（如朝向、水位），返回指向状态映射的指针。 | <code>{func, block.GetBlockStates(位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `ExecuteCommandBlock` | 执行命令方块中的命令，返回指向执行结果（布尔值）的指针。 | <code>{func, block.ExecuteCommandBlock(位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `GetBlockEntityData` | 获取方块实体的数据，返回指向NBT数据的指针。 | <code>{func, block.GetBlockEntityData(维度ID: int, 位置指针: ptr)}</code> | `ptr` |
| `GetBlockTileEntityCustomData` | 获取方块实体的自定义数据（指定键），返回指向数据值的指针。 | <code>{func, block.GetBlockTileEntityCustomData(玩家ID: string, 位置指针: ptr, 键: string, 维度ID: int)}</code> | `ptr` |
| `GetBlockTileEntityWholeCustomData` | 获取方块实体的全部自定义数据，返回指向映射的指针。 | <code>{func, block.GetBlockTileEntityWholeCustomData(玩家ID: string, 位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `GetCommandBlock` | 获取命令方块的信息，返回指向信息映射的指针。 | <code>{func, block.GetCommandBlock(世界ID: string, 位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `GetFrameItem` | 获取物品展示框中的物品，返回指向物品字典的指针。 | <code>{func, block.GetFrameItem(位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `GetFrameRotation` | 获取物品展示框的旋转角度，返回指向整数的指针。 | <code>{func, block.GetFrameRotation(位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `SetCommandBlock` | 设置命令方块，返回指向布尔值的指针。 | <code>{func, block.SetCommandBlock(位置指针: ptr, 维度ID: int, 命令: string, 名称: string, 模式: int, 是否条件制约: bool, 红石模式: int)}</code> | `ptr` |
| `SetFrameRotation` | 设置物品展示框的旋转角度，返回指向布尔值的指针。 | <code>{func, block.SetFrameRotation(位置指针: ptr, 维度ID: int, 旋转角度: int)}</code> | `ptr` |
| `GetBrewingStandSlotItem` | 获取酿造台指定槽位的物品，返回指向物品字典的指针。 | <code>{func, block.GetBrewingStandSlotItem(玩家ID: string, 槽位: int, 位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `GetChestBoxSize` | 获取箱子的槽位总数（容量），返回指向整数的指针。 | <code>{func, block.GetChestBoxSize(位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `GetChestPairedPosition` | 获取双联箱子的配对箱子坐标，返回指向位置元组的指针（若无配对则指向None）。 | <code>{func, block.GetChestPairedPosition(玩家ID: string, 位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `GetContainerItem` | 获取容器指定槽位的物品，返回指向物品字典的指针。 | <code>{func, block.GetContainerItem(位置指针: ptr, 槽位: int, 维度ID: int, 获取用户数据: bool)}</code> | `ptr` |
| `GetContainerSize` | 获取容器的槽位总数，返回指向整数的指针。 | <code>{func, block.GetContainerSize(位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `GetEnderChestItem` | 获取末影箱指定槽位的物品（每个玩家独立），返回指向物品字典的指针。 | <code>{func, block.GetEnderChestItem(玩家ID: string, 槽位: int, 获取用户数据: bool)}</code> | `ptr` |
| `GetInputSlotItem` | 获取工作台、熔炉等容器的输入槽物品，返回指向物品字典的指针。 | <code>{func, block.GetInputSlotItem(位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `GetOutputSlotItem` | 获取熔炉、高炉等容器的输出槽物品，返回指向物品字典的指针。 | <code>{func, block.GetOutputSlotItem(位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `SetChestBoxItemExchange` | 交换箱子中的两个物品，返回指向布尔值的指针。 | <code>{func, block.SetChestBoxItemExchange(玩家ID: string, 位置指针: ptr, 槽位A: int, 槽位B: int)}</code> | `ptr` |
| `GetBlockPoweredState` | 获取方块的充能状态（是否被红石激活），返回指向布尔值的指针。 | <code>{func, block.GetBlockPoweredState(位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `GetStrength` | 获取红石信号的强度，返回指向整数的指针。 | <code>{func, block.GetStrength(位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `GetSignBlockText` | 获取告示牌上的文字，返回指向字符串的指针。 | <code>{func, block.GetSignBlockText(位置指针: ptr, 维度ID: int, 侧面: int)}</code> | `ptr` |
| `GetSignTextStyle` | 获取告示牌文字的样式（颜色、照明），返回指向样式映射的指针。 | <code>{func, block.GetSignTextStyle(位置指针: ptr, 维度ID: int, 侧面: int)}</code> | `ptr` |
| `SetSignBlockText` | 设置告示牌文字，返回指向布尔值的指针。 | <code>{func, block.SetSignBlockText(玩家ID: string, 位置指针: ptr, 文本: string, 维度ID: int, 侧面: int)}</code> | `ptr` |
| `SetSignTextStyle` | 设置告示牌文字样式，返回指向布尔值的指针。 | <code>{func, block.SetSignTextStyle(位置指针: ptr, 维度ID: int, 颜色: int, 照明: bool, 侧面: int)}</code> | `ptr` |
| `GetBedColor` | 获取床的颜色，返回指向整数的指针。 | <code>{func, block.GetBedColor(玩家ID: string, 位置指针: ptr, 维度ID: int)}</code> | `ptr` |
| `SetBedColor` | 设置床的颜色，返回指向布尔值的指针。 | <code>{func, block.SetBedColor(玩家ID: string, 位置指针: ptr, 颜色: int, 维度ID: int)}</code> | `ptr` |

---

<a id="item"></a>

## item

| 函数 | 描述 | 签名 | 返回值 |
|---|---|---|---|
| `GetAllEnchantsInfo` | 获取所有附魔信息，返回指向附魔列表的指针。 | <code>{func, item.GetAllEnchantsInfo()}</code> | `ptr` |
| `GetItemDurability` | 获取物品的当前耐久度，返回指向整数的指针。 | <code>{func, item.GetItemDurability(玩家ID: string, 槽位类型: string, 槽位索引: int)}</code> | `ptr` |
| `GetItemInfoByBlockName` | 通过方块名称获取对应的物品信息，返回指向物品信息映射的指针。 | <code>{func, item.GetItemInfoByBlockName(方块名称: string, 附加值: int, 是否传统: bool)}</code> | `ptr` |
| `GetItemMaxDurability` | 获取物品的最大耐久度，返回指向整数的指针。 | <code>{func, item.GetItemMaxDurability(玩家ID: string, 槽位类型: string, 槽位索引: int, 是否用户数据: bool)}</code> | `ptr` |
| `SetItemDurability` | 设置物品的耐久度，返回指向布尔值的指针。 | <code>{func, item.SetItemDurability(玩家ID: string, 槽位类型: string, 槽位索引: int, 耐久度: int)}</code> | `ptr` |

---

