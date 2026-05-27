# HPL API 参考

> 基于 NetEase Minecraft HPL 脚本系统。所有 API 调用使用 `{func, 模块.函数(参数...)}` 格式。

## object 模块

### `object.ref`
创建指向对象的指针，用于后续通过指针操作对象。
```hpl
{func, object.ref(<对象: any>)}
```

### `object.can_deref`
检查指针是否指向可解引用的基本类型（整数、布尔值、浮点数、字符串），返回布尔值。
```hpl
{func, object.can_deref(<指针: ptr>)}
```

### `object.deref`
解引用指针，返回指针指向的基本类型值（整数、布尔值、浮点数、字符串）。若指向非基本类型则抛出异常。
```hpl
{func, object.deref(<指针: ptr>)}
```

### `object.release`
释放指针所管理的资源，指针变为无效。
```hpl
{func, object.release(<指针: ptr>)}
```

### `object.pin`
固定对象，防止被垃圾回收。
```hpl
{func, object.pin(<指针: ptr>)}
```

### `object.finalise`
终结对象的固定状态，使其可被释放。
```hpl
{func, object.finalise(<指针: ptr>)}
```

### `object.make_none`
创建一个表示空值的 None 对象，返回其指针。
```hpl
{func, object.make_none()}
```

### `object.is_ptr`
判断给定整数是否为一个有效指针，返回布尔值。
```hpl
{func, object.is_ptr(<整数: int>)}
```

### `object.is_none`
判断指针指向的对象是否为 None，返回布尔值。
```hpl
{func, object.is_none(<指针: ptr>)}
```

### `object.raw_type`
获取基本类型对象的类型码（0=int, 1=bool, 2=float, 3=str）。参数为原始值，不是指针。
```hpl
{func, object.raw_type(<原始值: int|bool|float|str>)}
```

### `object.ref_type`
获取指针指向对象的类型码（见源码中的 REF_TYPE_XXX）。
```hpl
{func, object.ref_type(<指针: ptr>)}
```

## reflect 模块

### `reflect.cast`
将对象 A 转换为对象 B 的类型，返回指向新对象的指针，失败返回 0。
```hpl
{func, reflect.cast(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.length`
返回对象的长度，返回指向长度（整数）的指针，失败返回 0。
```hpl
{func, reflect.length(<指针: ptr>)}
```

### `reflect.copy`
返回对象的浅拷贝，返回指向新对象的指针，失败返回 0。
```hpl
{func, reflect.copy(<指针: ptr>)}
```

### `reflect.deepcopy`
返回对象的深拷贝，返回指向新对象的指针，失败返回 0。
```hpl
{func, reflect.deepcopy(<指针: ptr>)}
```

### `reflect.format`
返回对象的字符串表示，返回指向字符串的指针，失败返回 0。
```hpl
{func, reflect.format(<指针: ptr>)}
```

### `reflect.vars`
返回对象的属性字典，返回指向映射的指针，失败返回 0。
```hpl
{func, reflect.vars(<指针: ptr>)}
```

### `reflect.dir`
返回对象的属性名称列表，返回指向切片的指针，失败返回 0。
```hpl
{func, reflect.dir(<指针: ptr>)}
```

### `reflect.hasattr`
检查对象是否拥有指定属性，返回布尔值。
```hpl
{func, reflect.hasattr(<指针: ptr>, <属性名: string>)}
```

### `reflect.getattr`
获取对象的指定属性值，返回指向该值的指针，失败返回 0（属性受保护或错误）。
```hpl
{func, reflect.getattr(<指针: ptr>, <属性名: string>)}
```

### `reflect.setattr`
设置对象的指定属性值，返回布尔值表示成功与否。
```hpl
{func, reflect.setattr(<对象指针: ptr>, <属性名: string>, <值指针: ptr>)}
```

### `reflect.delattr`
删除对象的指定属性，返回布尔值表示成功与否。
```hpl
{func, reflect.delattr(<对象指针: ptr>, <属性名: string>)}
```

### `reflect.callable`
检查对象是否可调用，返回布尔值。
```hpl
{func, reflect.callable(<指针: ptr>)}
```

### `reflect.call`
调用可调用对象，传入任意数量的参数指针，返回指向结果的指针；失败返回错误字符串。
```hpl
{func, reflect.call(<函数指针: ptr>, <参数指针1>, <参数指针2>, ...)}
```

### `reflect.and`
对两个对象进行逻辑与运算，返回指向结果的指针，失败返回 0。
```hpl
{func, reflect.and(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.or`
逻辑或运算，返回指向结果的指针。
```hpl
{func, reflect.or(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.inverse`
逻辑非运算，返回指向结果的指针。
```hpl
{func, reflect.inverse(<指针: ptr>)}
```

### `reflect.in`
检查元素是否在容器中，返回指向结果的指针。
```hpl
{func, reflect.in(<容器指针: ptr>, <元素指针: ptr>)}
```

### `reflect.add`
加法运算，返回指向结果的指针。
```hpl
{func, reflect.add(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.remove`
减法运算，返回指向结果的指针。
```hpl
{func, reflect.remove(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.times`
乘法运算，返回指向结果的指针。
```hpl
{func, reflect.times(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.divide`
除法运算，返回指向结果的指针。
```hpl
{func, reflect.divide(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.floordiv`
整数除法，返回指向结果的指针。
```hpl
{func, reflect.floordiv(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.negative`
取负运算，返回指向结果的指针。
```hpl
{func, reflect.negative(<指针: ptr>)}
```

### `reflect.abs`
绝对值，返回指向结果的指针。
```hpl
{func, reflect.abs(<指针: ptr>)}
```

### `reflect.round`
四舍五入，可指定小数位数，返回指向结果的指针。
```hpl
{func, reflect.round(<指针: ptr>[, <小数位数: int>])}
```

### `reflect.mod`
取模运算，返回指向结果的指针。
```hpl
{func, reflect.mod(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.pow`
幂运算，返回指向结果的指针。
```hpl
{func, reflect.pow(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.powmod`
模幂运算，返回指向结果的指针。
```hpl
{func, reflect.powmod(<指针A: ptr>, <指针B: ptr>, <指针C: ptr>)}
```

### `reflect.greater`
大于比较，返回指向结果的指针。
```hpl
{func, reflect.greater(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.less`
小于比较，返回指向结果的指针。
```hpl
{func, reflect.less(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.greater_equal`
大于等于比较，返回指向结果的指针。
```hpl
{func, reflect.greater_equal(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.less_equal`
小于等于比较，返回指向结果的指针。
```hpl
{func, reflect.less_equal(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.equal`
相等比较，返回指向结果的指针。
```hpl
{func, reflect.equal(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.not_equal`
不等比较，返回指向结果的指针。
```hpl
{func, reflect.not_equal(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.bit_and`
按位与，返回指向结果的指针。
```hpl
{func, reflect.bit_and(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.bit_or`
按位或，返回指向结果的指针。
```hpl
{func, reflect.bit_or(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.bit_xor`
按位异或，返回指向结果的指针。
```hpl
{func, reflect.bit_xor(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.bit_not`
按位取反，返回指向结果的指针。
```hpl
{func, reflect.bit_not(<指针: ptr>)}
```

### `reflect.left_shift`
左移位，返回指向结果的指针。
```hpl
{func, reflect.left_shift(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.right_shift`
右移位，返回指向结果的指针。
```hpl
{func, reflect.right_shift(<指针A: ptr>, <指针B: ptr>)}
```

### `reflect.max`
返回序列中的最大值，返回指向结果的指针。
```hpl
{func, reflect.max(<序列指针: ptr>)}
```

### `reflect.min`
返回最小值，返回指向结果的指针。
```hpl
{func, reflect.min(<序列指针: ptr>)}
```

### `reflect.sum`
返回序列的和，返回指向结果的指针。
```hpl
{func, reflect.sum(<序列指针: ptr>)}
```

<a id="slices"></a>
## slices 模块

### `slices.new`
创建新切片，可传入初始元素。
```hpl
{func, slices.new([<元素1>, <元素2>, ...])}
```

### `slices.make`
创建指定长度和默认值的切片。
```hpl
{func, slices.make(<长度: int>, <默认值: any>)}
```

### `slices.cast`
将其他可迭代对象转换为切片。
```hpl
{func, slices.cast(<可迭代对象指针: ptr>)}
```

### `slices.length`
返回切片长度（整数，直接值，非指针）。
```hpl
{func, slices.length(<切片指针: ptr>)}
```

### `slices.copy`
返回切片的浅拷贝（指针）。
```hpl
{func, slices.copy(<切片指针: ptr>)}
```

### `slices.format`
返回切片的字符串表示（直接字符串）。
```hpl
{func, slices.format(<切片指针: ptr>)}
```

### `slices.append`
向切片末尾追加元素，返回布尔值 True。
```hpl
{func, slices.append(<切片指针: ptr>, <元素: any>)}
```

### `slices.ptr_append`
追加元素并返回指向新元素的指针。
```hpl
{func, slices.ptr_append(<切片指针: ptr>, <值指针: ptr>)}
```

### `slices.get`
获取指定索引的元素（直接值）。
```hpl
{func, slices.get(<切片指针: ptr>, <索引: int>)}
```

### `slices.ptr_get`
获取指向指定索引元素的指针。
```hpl
{func, slices.ptr_get(<切片指针: ptr>, <索引: int>)}
```

### `slices.set`
设置指定索引的元素，返回布尔值 True。
```hpl
{func, slices.set(<切片指针: ptr>, <索引: int>, <元素: any>)}
```

### `slices.ptr_set`
设置指定索引的元素（通过值指针），返回布尔值 True。
```hpl
{func, slices.ptr_set(<切片指针: ptr>, <索引: int>, <值指针: ptr>)}
```

### `slices.max`
返回切片中的最大值（直接值）。
```hpl
{func, slices.max(<切片指针: ptr>)}
```

### `slices.min`
返回最小值（直接值）。
```hpl
{func, slices.min(<切片指针: ptr>)}
```

### `slices.sum`
返回切片中数值元素的和（直接值）。
```hpl
{func, slices.sum(<切片指针: ptr>)}
```

### `slices.sub`
截取子切片，返回新切片指针。
```hpl
{func, slices.sub(<切片指针: ptr>, <起始: int>, <结束: int>)}
```

### `slices.insert`
在指定位置插入元素，返回布尔值 True。
```hpl
{func, slices.insert(<切片指针: ptr>, <索引: int>, <元素: any>)}
```

### `slices.ptr_insert`
插入元素（通过值指针），返回布尔值 True。
```hpl
{func, slices.ptr_insert(<切片指针: ptr>, <索引: int>, <值指针: ptr>)}
```

### `slices.pop`
移除并返回最后一个元素（直接值）。
```hpl
{func, slices.pop(<切片指针: ptr>)}
```

### `slices.ptr_pop`
移除最后一个元素并返回指向它的指针。
```hpl
{func, slices.ptr_pop(<切片指针: ptr>)}
```

### `slices.reverse`
反转切片，返回布尔值 True。
```hpl
{func, slices.reverse(<切片指针: ptr>)}
```

### `slices.sort`
对切片排序，可指定是否反向，返回布尔值 True。
```hpl
{func, slices.sort(<切片指针: ptr>[, <是否反向: bool>])}
```

### `slices.concat`
连接多个切片，返回新切片指针。
```hpl
{func, slices.concat(<切片指针1>, <切片指针2>, ...)}
```

### `slices.binsearch`
二分查找元素，返回指向元组 (索引, 是否找到) 的指针。
```hpl
{func, slices.binsearch(<切片指针: ptr>, <元素: any>)}
```

### `slices.ptr_binsearch`
二分查找（通过值指针），返回指向元组的指针。
```hpl
{func, slices.ptr_binsearch(<切片指针: ptr>, <值指针: ptr>)}
```

### `slices.in`
检查元素是否存在于切片中，返回布尔值。
```hpl
{func, slices.in(<切片指针: ptr>, <元素: any>)}
```

### `slices.ptr_in`
检查元素是否存在于切片中（通过值指针），返回布尔值。
```hpl
{func, slices.ptr_in(<切片指针: ptr>, <值指针: ptr>)}
```

<a id="maps"></a>
## maps 模块

### `maps.new`
创建新映射，可指定是否有序，并可传入键值对初始化。
```hpl
{func, maps.new(<是否有序: bool>, [<键1>, <值1>, <键2>, <值2>, ...])}
```

### `maps.cast`
将其他对象强制转换为映射，返回新映射指针。
```hpl
{func, maps.cast(<指针: ptr>)}
```

### `maps.length`
返回映射中键值对数量（直接整数）。
```hpl
{func, maps.length(<映射指针: ptr>)}
```

### `maps.copy`
返回映射的浅拷贝（指针）。
```hpl
{func, maps.copy(<映射指针: ptr>)}
```

### `maps.format`
返回映射的字符串表示（直接字符串）。
```hpl
{func, maps.format(<映射指针: ptr>)}
```

### `maps.exist`
检查键是否存在，返回布尔值。
```hpl
{func, maps.exist(<映射指针: ptr>, <键: any>)}
```

### `maps.ptr_exist`
检查键是否存在（通过键指针），返回布尔值。
```hpl
{func, maps.ptr_exist(<映射指针: ptr>, <键指针: ptr>)}
```

### `maps.get`
获取指定键的值（直接值），键必须存在，否则异常。
```hpl
{func, maps.get(<映射指针: ptr>, <键: any>)}
```

### `maps.ptr_get`
获取指向指定键值的指针。
```hpl
{func, maps.ptr_get(<映射指针: ptr>, <键指针: ptr>)}
```

### `maps.pop`
移除指定键并返回其值（直接值）。
```hpl
{func, maps.pop(<映射指针: ptr>, <键: any>)}
```

### `maps.ptr_pop`
移除指定键并返回指向被移除值的指针。
```hpl
{func, maps.ptr_pop(<映射指针: ptr>, <键指针: ptr>)}
```

### `maps.set`
设置键值对，返回布尔值 True。
```hpl
{func, maps.set(<映射指针: ptr>, <键: any>, <值: any>)}
```

### `maps.ptr_set`
设置键值对（通过键指针和值指针），返回布尔值 True。
```hpl
{func, maps.ptr_set(<映射指针: ptr>, <键指针: ptr>, <值指针: ptr>)}
```

### `maps.del`
删除指定键值对，返回布尔值 True。
```hpl
{func, maps.del(<映射指针: ptr>, <键: any>)}
```

### `maps.ptr_del`
删除指定键值对（通过键指针），返回布尔值 True。
```hpl
{func, maps.ptr_del(<映射指针: ptr>, <键指针: ptr>)}
```

### `maps.clear`
清空映射，返回布尔值 True。
```hpl
{func, maps.clear(<映射指针: ptr>)}
```

### `maps.keys`
返回所有键组成的切片指针。
```hpl
{func, maps.keys(<映射指针: ptr>)}
```

### `maps.values`
返回所有值组成的切片指针。
```hpl
{func, maps.values(<映射指针: ptr>)}
```

### `maps.items`
返回所有键值对组成的切片指针（每个元素为二元组）。
```hpl
{func, maps.items(<映射指针: ptr>)}
```

### `maps.equal`
比较两个映射是否相等，返回布尔值。
```hpl
{func, maps.equal(<映射指针A: ptr>, <映射指针B: ptr>)}
```

<a id="tuple"></a>
## tuple 模块

### `tuple.new`
创建新元组，可传入元素。
```hpl
{func, tuple.new([<元素1>, <元素2>, ...])}
```

### `tuple.cast`
将其他可迭代对象转换为元组，返回指针。
```hpl
{func, tuple.cast(<可迭代对象指针: ptr>)}
```

### `tuple.length`
返回元组长度（直接整数）。
```hpl
{func, tuple.length(<元组指针: ptr>)}
```

### `tuple.format`
返回元组的字符串表示（直接字符串）。
```hpl
{func, tuple.format(<元组指针: ptr>)}
```

### `tuple.get`
获取指定索引的元素（直接值）。
```hpl
{func, tuple.get(<元组指针: ptr>, <索引: int>)}
```

### `tuple.ptr_get`
获取指向指定索引元素的指针。
```hpl
{func, tuple.ptr_get(<元组指针: ptr>, <索引: int>)}
```

### `tuple.sub`
截取子元组，返回新元组指针。
```hpl
{func, tuple.sub(<元组指针: ptr>, <起始: int>, <结束: int>)}
```

### `tuple.max`
返回元组中的最大值（直接值）。
```hpl
{func, tuple.max(<元组指针: ptr>)}
```

### `tuple.min`
返回最小值（直接值）。
```hpl
{func, tuple.min(<元组指针: ptr>)}
```

### `tuple.sum`
返回元组中数值元素的和（直接值）。
```hpl
{func, tuple.sum(<元组指针: ptr>)}
```

### `tuple.in`
检查元素是否存在于元组中，返回布尔值。
```hpl
{func, tuple.in(<元组指针: ptr>, <元素: any>)}
```

### `tuple.ptr_in`
检查元素是否存在于元组中（通过值指针），返回布尔值。
```hpl
{func, tuple.ptr_in(<元组指针: ptr>, <值指针: ptr>)}
```

<a id="set"></a>
## set 模块

### `set.new`
创建新集合，可传入初始元素。
```hpl
{func, set.new([<元素1>, <元素2>, ...])}
```

### `set.cast`
将其他可迭代对象转换为集合，返回指针。
```hpl
{func, set.cast(<可迭代对象指针: ptr>)}
```

### `set.length`
返回集合中元素个数（直接整数）。
```hpl
{func, set.length(<集合指针: ptr>)}
```

### `set.copy`
返回集合的浅拷贝（指针）。
```hpl
{func, set.copy(<集合指针: ptr>)}
```

### `set.format`
返回集合的字符串表示（直接字符串）。
```hpl
{func, set.format(<集合指针: ptr>)}
```

### `set.exist`
检查元素是否存在于集合中，返回布尔值。
```hpl
{func, set.exist(<集合指针: ptr>, <元素: any>)}
```

### `set.ptr_exist`
检查元素是否存在于集合中（通过值指针），返回布尔值。
```hpl
{func, set.ptr_exist(<集合指针: ptr>, <值指针: ptr>)}
```

### `set.add`
向集合添加元素，返回布尔值 True。
```hpl
{func, set.add(<集合指针: ptr>, <元素: any>)}
```

### `set.ptr_add`
添加元素（通过值指针），返回布尔值 True。
```hpl
{func, set.ptr_add(<集合指针: ptr>, <值指针: ptr>)}
```

### `set.remove`
移除指定元素，若不存在则异常，返回布尔值 True。
```hpl
{func, set.remove(<集合指针: ptr>, <元素: any>)}
```

### `set.ptr_remove`
移除元素（通过值指针），返回布尔值 True。
```hpl
{func, set.ptr_remove(<集合指针: ptr>, <值指针: ptr>)}
```

### `set.discard`
移除指定元素（不存在时忽略），返回布尔值 True。
```hpl
{func, set.discard(<集合指针: ptr>, <元素: any>)}
```

### `set.ptr_discard`
移除元素（通过值指针），返回布尔值 True。
```hpl
{func, set.ptr_discard(<集合指针: ptr>, <值指针: ptr>)}
```

### `set.pop`
随机移除并返回一个元素（直接值）。
```hpl
{func, set.pop(<集合指针: ptr>)}
```

### `set.ptr_pop`
随机移除并返回指向被移除元素的指针。
```hpl
{func, set.ptr_pop(<集合指针: ptr>)}
```

### `set.clear`
清空集合，返回布尔值 True。
```hpl
{func, set.clear(<集合指针: ptr>)}
```

### `set.max`
返回集合中的最大值（直接值）。
```hpl
{func, set.max(<集合指针: ptr>)}
```

### `set.min`
返回最小值（直接值）。
```hpl
{func, set.min(<集合指针: ptr>)}
```

### `set.sum`
返回集合中数值元素的和（直接值）。
```hpl
{func, set.sum(<集合指针: ptr>)}
```

### `set.difference`
返回两个集合的差集（新集合指针）。
```hpl
{func, set.difference(<集合指针A: ptr>, <集合指针B: ptr>)}
```

### `set.symmetric_difference`
返回对称差集（新集合指针）。
```hpl
{func, set.symmetric_difference(<集合指针A: ptr>, <集合指针B: ptr>)}
```

### `set.intersection`
返回交集（新集合指针）。
```hpl
{func, set.intersection(<集合指针A: ptr>, <集合指针B: ptr>)}
```

### `set.union`
返回并集（新集合指针）。
```hpl
{func, set.union(<集合指针A: ptr>, <集合指针B: ptr>)}
```

### `set.isdisjoint`
判断两个集合是否不相交，返回布尔值。
```hpl
{func, set.isdisjoint(<集合指针A: ptr>, <集合指针B: ptr>)}
```

### `set.issubset`
判断一个集合是否为另一个的子集，返回布尔值。
```hpl
{func, set.issubset(<集合指针A: ptr>, <集合指针B: ptr>)}
```

### `set.issuperset`
判断一个集合是否为另一个的超集，返回布尔值。
```hpl
{func, set.issuperset(<集合指针A: ptr>, <集合指针B: ptr>)}
```

## strings 模块

### `strings.cast`
将指针指向的对象转换为字符串，返回直接字符串。
```hpl
{func, strings.cast(<指针: ptr>)}
```

### `strings.length`
返回字符串长度（直接整数）。
```hpl
{func, strings.length(<字符串: string>)}
```

### `strings.sub`
截取子字符串，返回直接字符串。
```hpl
{func, strings.sub(<字符串: string>, <起始: int>, <结束: int>)}
```

### `strings.ord`
返回字符的 Unicode 码点（整数）。
```hpl
{func, strings.ord(<字符: string>)}
```

### `strings.chr`
返回码点对应的字符（字符串）。
```hpl
{func, strings.chr(<码点: int>)}
```

### `strings.capitalize`
首字母大写，返回字符串。
```hpl
{func, strings.capitalize(<字符串: string>)}
```

### `strings.center`
居中填充，返回字符串。
```hpl
{func, strings.center(<字符串: string>, <宽度: int>, <填充字符: string>)}
```

### `strings.startswith`
判断是否以指定前缀开头，返回布尔值。
```hpl
{func, strings.startswith(<字符串: string>, <前缀: string>[, <起始: int>, <结束: int>])}
```

### `strings.endswith`
判断是否以指定后缀结尾，返回布尔值。
```hpl
{func, strings.endswith(<字符串: string>, <后缀: string>[, <起始: int>, <结束: int>])}
```

### `strings.find`
查找子串首次出现位置，返回索引，找不到返回 -1。
```hpl
{func, strings.find(<字符串: string>, <子串: string>[, <起始: int>, <结束: int>])}
```

### `strings.rfind`
从右侧查找，返回索引。
```hpl
{func, strings.rfind(<字符串: string>, <子串: string>[, <起始: int>, <结束: int>])}
```

### `strings.index`
类似 find，但找不到时抛出异常。
```hpl
{func, strings.index(<字符串: string>, <子串: string>[, <起始: int>, <结束: int>])}
```

### `strings.rindex`
类似 rfind，但找不到时抛出异常。
```hpl
{func, strings.rindex(<字符串: string>, <子串: string>[, <起始: int>, <结束: int>])}
```

### `strings.isalnum`
判断是否全为字母或数字，返回布尔值。
```hpl
{func, strings.isalnum(<字符串: string>)}
```

### `strings.isalpha`
判断是否全为字母，返回布尔值。
```hpl
{func, strings.isalpha(<字符串: string>)}
```

### `strings.isdigit`
判断是否全为数字，返回布尔值。
```hpl
{func, strings.isdigit(<字符串: string>)}
```

### `strings.islower`
判断是否全小写，返回布尔值。
```hpl
{func, strings.islower(<字符串: string>)}
```

### `strings.isspace`
判断是否全空白，返回布尔值。
```hpl
{func, strings.isspace(<字符串: string>)}
```

### `strings.istitle`
判断是否为标题格式，返回布尔值。
```hpl
{func, strings.istitle(<字符串: string>)}
```

### `strings.isupper`
判断是否全大写，返回布尔值。
```hpl
{func, strings.isupper(<字符串: string>)}
```

### `strings.join`
用当前字符串连接切片中的字符串元素，返回结果字符串。
```hpl
{func, strings.join(<分隔符: string>, <切片指针: ptr>)}
```

### `strings.ljust`
左对齐填充，返回字符串。
```hpl
{func, strings.ljust(<字符串: string>, <宽度: int>, <填充字符: string>)}
```

### `strings.rjust`
右对齐填充，返回字符串。
```hpl
{func, strings.rjust(<字符串: string>, <宽度: int>, <填充字符: string>)}
```

### `strings.lower`
转换为小写，返回字符串。
```hpl
{func, strings.lower(<字符串: string>)}
```

### `strings.upper`
转换为大写，返回字符串。
```hpl
{func, strings.upper(<字符串: string>)}
```

### `strings.lstrip`
去除左侧空白（或指定字符），返回字符串。
```hpl
{func, strings.lstrip(<字符串: string>[, <要去除的字符集: string>])}
```

### `strings.rstrip`
去除右侧空白，返回字符串。
```hpl
{func, strings.rstrip(<字符串: string>[, <要去除的字符集: string>])}
```

### `strings.strip`
去除两侧空白，返回字符串。
```hpl
{func, strings.strip(<字符串: string>[, <要去除的字符集: string>])}
```

### `strings.replace`
替换子串，返回字符串。
```hpl
{func, strings.replace(<字符串: string>, <旧子串: string>, <新子串: string>[, <替换次数: int>])}
```

### `strings.split`
按分隔符分割字符串，返回指向字符串列表的指针。
```hpl
{func, strings.split(<字符串: string>[, <分隔符: string>, <最大分割次数: int>])}
```

### `strings.rsplit`
从右侧开始分割，返回切片指针。
```hpl
{func, strings.rsplit(<字符串: string>[, <分隔符: string>, <最大分割次数: int>])}
```

### `strings.swapcase`
大小写互换，返回字符串。
```hpl
{func, strings.swapcase(<字符串: string>)}
```

### `strings.title`
转换为标题格式，返回字符串。
```hpl
{func, strings.title(<字符串: string>)}
```

### `strings.zfill`
左侧用零填充至指定宽度，返回字符串。
```hpl
{func, strings.zfill(<字符串: string>, <宽度: int>)}
```

### `strings.equalfold`
不区分大小写比较两个字符串，返回布尔值。
```hpl
{func, strings.equalfold(<字符串A: string>, <字符串B: string>)}
```

## uuid 模块

### `uuid.new`
生成一个新的随机 UUID，返回指针。
```hpl
{func, uuid.new()}
```

### `uuid.format`
返回 UUID 的标准字符串表示，如 `"123e4567-e89b-12d3-a456-426614174000"`。
```hpl
{func, uuid.format(<UUID指针: ptr>)}
```

### `uuid.string`
同 format，返回字符串。
```hpl
{func, uuid.string(<UUID指针: ptr>)}
```

### `uuid.bytes`
返回 UUID 的字节表示，可能返回指针或字符串。
```hpl
{func, uuid.bytes(<UUID指针: ptr>)}
```

### `uuid.bytes_le`
返回 UUID 的小端字节序表示。
```hpl
{func, uuid.bytes_le(<UUID指针: ptr>)}
```

### `uuid.hex`
返回 UUID 的 32 字符十六进制字符串。
```hpl
{func, uuid.hex(<UUID指针: ptr>)}
```

### `uuid.from_string`
从标准字符串创建 UUID，返回指针。
```hpl
{func, uuid.from_string(<字符串: string>)}
```

### `uuid.from_bytes`
从字节表示创建 UUID，参数可为指针或字符串。
```hpl
{func, uuid.from_bytes(<字节串指针或字符串: ptr|string>)}
```

### `uuid.from_bytes_le`
从小端字节序创建 UUID，参数可为指针或字符串。
```hpl
{func, uuid.from_bytes_le(<字节串指针或字符串: ptr|string>)}
```

### `uuid.from_hex`
从十六进制字符串创建 UUID。
```hpl
{func, uuid.from_hex(<十六进制字符串: string>)}
```

## time 模块

### `time.time`
返回当前时间戳（浮点数）。
```hpl
{func, time.time()}
```

### `time.ctime`
将时间戳转换为本地时间字符串，默认为当前时间。
```hpl
{func, time.ctime([<时间戳: float>])}
```

### `time.asctime`
将时间元组转换为字符串，若无参数则使用当前时间。
```hpl
{func, time.asctime([<时间元组指针: ptr>])}
```

### `time.gmtime`
将时间戳转换为 UTC 时间元组，返回指针。
```hpl
{func, time.gmtime([<时间戳: float>])}
```

### `time.localtime`
将时间戳转换为本地时间元组，返回指针。
```hpl
{func, time.localtime([<时间戳: float>])}
```

### `time.mktime`
将本地时间元组转换为时间戳，返回浮点数。
```hpl
{func, time.mktime(<时间元组指针: ptr>)}
```

### `time.strftime`
按格式将时间元组格式化为字符串，若无时间元组则使用当前时间。
```hpl
{func, time.strftime(<格式: string>, [<时间元组指针: ptr>])}
```

### `time.strptime`
将字符串解析为时间元组，返回指针。
```hpl
{func, time.strptime(<字符串: string>, <格式: string>)}
```

### `time.timezone`
返回本地时区与 UTC 的偏移秒数（整数）。
```hpl
{func, time.timezone()}
```

### `time.tzname`
返回本地时区名称元组 (标准时区名, 夏令时名)，返回指向元组的指针。
```hpl
{func, time.tzname()}
```

## struct_time 模块

### `struct_time.cast`
将其他可迭代对象转换为 struct_time，返回指针。
```hpl
{func, struct_time.cast(<可迭代对象指针: ptr>)}
```

### `struct_time.length`
返回 struct_time 的长度（固定 9），返回整数。
```hpl
{func, struct_time.length(<时间元组指针: ptr>)}
```

### `struct_time.format`
返回 struct_time 的字符串表示，返回字符串。
```hpl
{func, struct_time.format(<时间元组指针: ptr>)}
```

### `struct_time.tm_year`
获取年份（整数）。
```hpl
{func, struct_time.tm_year(<时间元组指针: ptr>)}
```

### `struct_time.tm_mon`
获取月份（1-12）。
```hpl
{func, struct_time.tm_mon(<时间元组指针: ptr>)}
```

### `struct_time.tm_mday`
获取日（1-31）。
```hpl
{func, struct_time.tm_mday(<时间元组指针: ptr>)}
```

### `struct_time.tm_hour`
获取小时（0-23）。
```hpl
{func, struct_time.tm_hour(<时间元组指针: ptr>)}
```

### `struct_time.tm_min`
获取分钟（0-59）。
```hpl
{func, struct_time.tm_min(<时间元组指针: ptr>)}
```

### `struct_time.tm_sec`
获取秒（0-61）。
```hpl
{func, struct_time.tm_sec(<时间元组指针: ptr>)}
```

### `struct_time.tm_wday`
获取星期几（0-6，0 为周一）。
```hpl
{func, struct_time.tm_wday(<时间元组指针: ptr>)}
```

### `struct_time.tm_yday`
获取一年中的第几天（1-366）。
```hpl
{func, struct_time.tm_yday(<时间元组指针: ptr>)}
```

### `struct_time.tm_isdst`
获取夏令时标志（0 否，1 是，-1 未知）。
```hpl
{func, struct_time.tm_isdst(<时间元组指针: ptr>)}
```

## math 模块

### `math.format`
将数字格式化为字符串，可指定精度，返回字符串。
```hpl
{func, math.format(<数字: number>, [<精度: int>])}
```

### `math.round`
四舍五入，返回数字。
```hpl
{func, math.round(<数字: number>[, <小数位数: int>])}
```

### `math.floordiv`
整数除法，返回整数。
```hpl
{func, math.floordiv(<a: number>, <b: number>)}
```

### `math.mod`
取模，返回数字。
```hpl
{func, math.mod(<a: number>, <b: number>)}
```

### `math.abs`
绝对值，返回数字。
```hpl
{func, math.abs(<数字: number>)}
```

### `math.max`
返回两个数中的较大值。
```hpl
{func, math.max(<a: number>, <b: number>)}
```

### `math.min`
返回较小值。
```hpl
{func, math.min(<a: number>, <b: number>)}
```

### `math.bit_and`
按位与，返回整数。
```hpl
{func, math.bit_and(<a: int>, <b: int>)}
```

### `math.bit_or`
按位或，返回整数。
```hpl
{func, math.bit_or(<a: int>, <b: int>)}
```

### `math.bit_xor`
按位异或，返回整数。
```hpl
{func, math.bit_xor(<a: int>, <b: int>)}
```

### `math.bit_not`
按位取反，返回整数。
```hpl
{func, math.bit_not(<a: int>)}
```

### `math.left_shift`
左移位，返回整数。
```hpl
{func, math.left_shift(<a: int>, <位数: int>)}
```

### `math.right_shift`
右移位，返回整数。
```hpl
{func, math.right_shift(<a: int>, <位数: int>)}
```

### `math.acos`
反余弦，返回弧度。
```hpl
{func, math.acos(<x: float>)}
```

### `math.acosh`
反双曲余弦。
```hpl
{func, math.acosh(<x: float>)}
```

### `math.asin`
反正弦。
```hpl
{func, math.asin(<x: float>)}
```

### `math.asinh`
反双曲正弦。
```hpl
{func, math.asinh(<x: float>)}
```

### `math.atan`
反正切。
```hpl
{func, math.atan(<x: float>)}
```

### `math.atan2`
双参数反正切。
```hpl
{func, math.atan2(<y: float>, <x: float>)}
```

### `math.atanh`
反双曲正切。
```hpl
{func, math.atanh(<x: float>)}
```

### `math.ceil`
向上取整，返回整数。
```hpl
{func, math.ceil(<x: float>)}
```

### `math.cos`
余弦。
```hpl
{func, math.cos(<x: float>)}
```

### `math.cosh`
双曲余弦。
```hpl
{func, math.cosh(<x: float>)}
```

### `math.degrees`
弧度转角度。
```hpl
{func, math.degrees(<弧度: float>)}
```

### `math.e`
返回自然常数 e（浮点数）。
```hpl
{func, math.e()}
```

### `math.erf`
误差函数。
```hpl
{func, math.erf(<x: float>)}
```

### `math.erfc`
互补误差函数。
```hpl
{func, math.erfc(<x: float>)}
```

### `math.exp`
指数 e^x。
```hpl
{func, math.exp(<x: float>)}
```

### `math.expm1`
e^x - 1。
```hpl
{func, math.expm1(<x: float>)}
```

### `math.fabs`
浮点绝对值。
```hpl
{func, math.fabs(<x: float>)}
```

### `math.factorial`
阶乘，返回整数。
```hpl
{func, math.factorial(<x: int>)}
```

### `math.floor`
向下取整，返回整数。
```hpl
{func, math.floor(<x: float>)}
```

### `math.fmod`
浮点取模。
```hpl
{func, math.fmod(<x: float>, <y: float>)}
```

### `math.frexp`
将浮点数分解为尾数和指数，返回指向元组 (m, e) 的指针。
```hpl
{func, math.frexp(<x: float>)}
```

### `math.fsum`
对指针指向的浮点数列表精确求和，返回浮点数。
```hpl
{func, math.fsum(<列表指针: ptr>)}
```

### `math.gamma`
伽马函数。
```hpl
{func, math.gamma(<x: float>)}
```

### `math.hypot`
计算 sqrt(x^2 + y^2)。
```hpl
{func, math.hypot(<x: float>, <y: float>)}
```

### `math.isinf`
判断是否为无穷大，返回布尔值。
```hpl
{func, math.isinf(<x: float>)}
```

### `math.isnan`
判断是否为非数，返回布尔值。
```hpl
{func, math.isnan(<x: float>)}
```

### `math.ldexp`
计算 x * 2^i。
```hpl
{func, math.ldexp(<x: float>, <i: int>)}
```

### `math.lgamma`
伽马函数的自然对数。
```hpl
{func, math.lgamma(<x: float>)}
```

### `math.log`
自然对数，可指定底数。
```hpl
{func, math.log(<x: float>[, <底数: float>])}
```

### `math.log10`
以 10 为底的对数。
```hpl
{func, math.log10(<x: float>)}
```

### `math.log1p`
计算 log(1+x)。
```hpl
{func, math.log1p(<x: float>)}
```

### `math.modf`
将浮点数分解为整数和小数部分，返回指向元组 (frac, int) 的指针。
```hpl
{func, math.modf(<x: float>)}
```

### `math.pi`
返回圆周率 π。
```hpl
{func, math.pi()}
```

### `math.pow`
幂运算。
```hpl
{func, math.pow(<x: float>, <y: float>)}
```

### `math.powmod`
模幂运算 (x^y) % mod，返回整数。
```hpl
{func, math.powmod(<x: int>, <y: int>, <mod: int>)}
```

### `math.radians`
角度转弧度。
```hpl
{func, math.radians(<角度: float>)}
```

### `math.sin`
正弦。
```hpl
{func, math.sin(<x: float>)}
```

### `math.sinh`
双曲正弦。
```hpl
{func, math.sinh(<x: float>)}
```

### `math.sqrt`
平方根。
```hpl
{func, math.sqrt(<x: float>)}
```

### `math.tan`
正切。
```hpl
{func, math.tan(<x: float>)}
```

### `math.tanh`
双曲正切。
```hpl
{func, math.tanh(<x: float>)}
```

### `math.trunc`
截断取整，返回整数。
```hpl
{func, math.trunc(<x: float>)}
```

## random 模块

### `random.betavariate`
返回 Beta 分布的随机浮点数。
```hpl
{func, random.betavariate(<alpha: float>, <beta: float>)}
```

### `random.choice`
从序列中随机选择一个元素，返回指向该元素的指针。
```hpl
{func, random.choice(<序列指针: ptr>)}
```

### `random.expovariate`
返回指数分布的随机数。
```hpl
{func, random.expovariate([<lambd: float>])}
```

### `random.gammavariate`
返回 Gamma 分布的随机数。
```hpl
{func, random.gammavariate(<alpha: float>, <beta: float>)}
```

### `random.gauss`
返回高斯分布的随机数。
```hpl
{func, random.gauss([<mu: float>, <sigma: float>])}
```

### `random.lognormvariate`
返回对数正态分布的随机数。
```hpl
{func, random.lognormvariate(<mu: float>, <sigma: float>)}
```

### `random.normalvariate`
返回正态分布的随机数。
```hpl
{func, random.normalvariate([<mu: float>, <sigma: float>])}
```

### `random.paretovariate`
返回 Pareto 分布的随机数。
```hpl
{func, random.paretovariate(<alpha: float>)}
```

### `random.randint`
返回闭区间内的随机整数。
```hpl
{func, random.randint(<a: int>, <b: int>)}
```

### `random.random`
返回 [0.0, 1.0) 内的随机浮点数。
```hpl
{func, random.random()}
```

### `random.randrange`
从 range 中随机选取一个整数。
```hpl
{func, random.randrange(<start: int>[, <stop: int>, <step: int>])}
```

### `random.sample`
从总体中随机抽取 k 个不重复元素，返回新列表指针。
```hpl
{func, random.sample(<总体指针: ptr>, <k: int>)}
```

### `random.shuffle`
随机打乱列表（原地），返回布尔值 True。
```hpl
{func, random.shuffle(<列表指针: ptr>)}
```

### `random.triangular`
返回三角分布的随机数。
```hpl
{func, random.triangular([<low: float>, <high: float>, <mode: float>])}
```

### `random.uniform`
返回均匀分布的随机数。
```hpl
{func, random.uniform(<a: float>, <b: float>)}
```

### `random.vonmisesvariate`
返回 von Mises 分布的随机数。
```hpl
{func, random.vonmisesvariate(<mu: float>, <kappa: float>)}
```

### `random.weibullvariate`
返回 Weibull 分布的随机数。
```hpl
{func, random.weibullvariate(<alpha: float>, <beta: float>)}
```

### `random.seed`
设置随机种子，返回布尔值 True。
```hpl
{func, random.seed([<种子: int|float|str|None>])}
```

### `random.getstate`
返回随机数生成器状态指针。
```hpl
{func, random.getstate()}
```

### `random.setstate`
恢复随机数生成器状态，返回布尔值 True。
```hpl
{func, random.setstate(<状态指针: ptr>)}
```

## json 模块

### `json.dumps`
将指针指向的对象序列化为 JSON 字符串，返回字符串。
```hpl
{func, json.dumps(<对象指针: ptr>, [<skipkeys: bool>, <ensure_ascii: bool>, <check_circular: bool>, <allow_nan: bool>, <indent: int|string>, <separators_ptr: ptr>, <sort_keys: bool>])}
```

### `json.fast_dumps`
快速序列化（不转义非 ASCII），参数为直接对象（非指针），返回字符串。
```hpl
{func, json.fast_dumps(<直接对象: any>)}
```

### `json.loads`
将 JSON 字符串解析为对象，返回指针。
```hpl
{func, json.loads(<JSON字符串: string>)}
```

### `json.fast_loads`
快速解析，返回直接对象（非指针）。
```hpl
{func, json.fast_loads(<JSON字符串: string>)}
```

## binascii 模块

### `binascii.a2b_base64`
将 Base64 字符串解码为二进制数据，返回指向字节串的指针。
```hpl
{func, binascii.a2b_base64(<Base64字符串: string>)}
```

### `binascii.a2b_hex`
将十六进制字符串解码为二进制数据，返回指针。
```hpl
{func, binascii.a2b_hex(<十六进制字符串: string>)}
```

### `binascii.b2a_base64`
将二进制数据编码为 Base64 字符串，参数可为指针或字符串，返回字符串。
```hpl
{func, binascii.b2a_base64(<字节串指针或字符串: ptr|string>)}
```

### `binascii.b2a_hex`
将二进制数据编码为十六进制字符串，参数同上，返回字符串。
```hpl
{func, binascii.b2a_hex(<字节串指针或字符串: ptr|string>)}
```

### `binascii.hexlify`
同 b2a_hex，返回字符串。
```hpl
{func, binascii.hexlify(<字节串指针或字符串: ptr|string>)}
```

## datetime_datetime 模块

### `datetime_datetime.new`
创建 datetime 对象，年、月、日必选，时、分、秒、微秒可选，返回指针。
```hpl
{func, datetime_datetime.new(<年: int>, <月: int>, <日: int>, [<时: int>, <分: int>, <秒: int>, <微秒: int>])}
```

### `datetime_datetime.now`
返回当前本地日期时间的指针。
```hpl
{func, datetime_datetime.now()}
```

### `datetime_datetime.format`
返回 datetime 的字符串表示，返回字符串。
```hpl
{func, datetime_datetime.format(<datetime指针: ptr>)}
```

### `datetime_datetime.combine`
将日期和时间合并为 datetime，返回指针。
```hpl
{func, datetime_datetime.combine(<date指针: ptr>, <time指针: ptr>)}
```

### `datetime_datetime.ctime`
返回 C 风格时间字符串。
```hpl
{func, datetime_datetime.ctime(<datetime指针: ptr>)}
```

### `datetime_datetime.date`
返回日期部分，返回 date 指针。
```hpl
{func, datetime_datetime.date(<datetime指针: ptr>)}
```

### `datetime_datetime.day`
返回日（整数）。
```hpl
{func, datetime_datetime.day(<datetime指针: ptr>)}
```

### `datetime_datetime.fromordinal`
从 Gregorian 序数创建 datetime，返回指针。
```hpl
{func, datetime_datetime.fromordinal(<序数: int>)}
```

### `datetime_datetime.fromtimestamp`
从时间戳创建本地 datetime，返回指针。
```hpl
{func, datetime_datetime.fromtimestamp(<时间戳: float>)}
```

### `datetime_datetime.hour`
返回小时（整数）。
```hpl
{func, datetime_datetime.hour(<datetime指针: ptr>)}
```

### `datetime_datetime.isocalendar`
返回 ISO 日历元组 (年, 周, 周几) 的指针。
```hpl
{func, datetime_datetime.isocalendar(<datetime指针: ptr>)}
```

### `datetime_datetime.isoformat`
返回 ISO 格式字符串，可指定分隔符。
```hpl
{func, datetime_datetime.isoformat(<datetime指针: ptr>[, <分隔符: string>])}
```

### `datetime_datetime.isoweekday`
返回 ISO 星期几（1-7）。
```hpl
{func, datetime_datetime.isoweekday(<datetime指针: ptr>)}
```

### `datetime_datetime.max`
返回最大可能的 datetime 指针。
```hpl
{func, datetime_datetime.max()}
```

### `datetime_datetime.microsecond`
返回微秒（整数）。
```hpl
{func, datetime_datetime.microsecond(<datetime指针: ptr>)}
```

### `datetime_datetime.min`
返回最小可能的 datetime 指针。
```hpl
{func, datetime_datetime.min()}
```

### `datetime_datetime.minute`
返回分钟（整数）。
```hpl
{func, datetime_datetime.minute(<datetime指针: ptr>)}
```

### `datetime_datetime.month`
返回月份（整数）。
```hpl
{func, datetime_datetime.month(<datetime指针: ptr>)}
```

### `datetime_datetime.replace`
替换部分字段，返回新 datetime 指针。
```hpl
{func, datetime_datetime.replace(<datetime指针: ptr>, <年: int>, <月: int>, <日: int>, [<时: int>, <分: int>, <秒: int>, <微秒: int>])}
```

### `datetime_datetime.second`
返回秒（整数）。
```hpl
{func, datetime_datetime.second(<datetime指针: ptr>)}
```

### `datetime_datetime.strftime`
按格式化为字符串。
```hpl
{func, datetime_datetime.strftime(<datetime指针: ptr>, <格式: string>)}
```

### `datetime_datetime.strptime`
从字符串解析为 datetime，返回指针。
```hpl
{func, datetime_datetime.strptime(<日期字符串: string>, <格式: string>)}
```

### `datetime_datetime.time`
返回时间部分，返回 time 指针。
```hpl
{func, datetime_datetime.time(<datetime指针: ptr>)}
```

### `datetime_datetime.timetuple`
返回时间元组指针。
```hpl
{func, datetime_datetime.timetuple(<datetime指针: ptr>)}
```

### `datetime_datetime.today`
返回今天日期（时间部分为 0）的 datetime 指针。
```hpl
{func, datetime_datetime.today()}
```

### `datetime_datetime.toordinal`
返回 Gregorian 序数。
```hpl
{func, datetime_datetime.toordinal(<datetime指针: ptr>)}
```

### `datetime_datetime.weekday`
返回星期几（0-6）。
```hpl
{func, datetime_datetime.weekday(<datetime指针: ptr>)}
```

### `datetime_datetime.greater`
比较大于，返回布尔值。
```hpl
{func, datetime_datetime.greater(<指针A: ptr>, <指针B: ptr>)}
```

### `datetime_datetime.less`
小于，返回布尔值。
```hpl
{func, datetime_datetime.less(<指针A: ptr>, <指针B: ptr>)}
```

### `datetime_datetime.greater_equal`
大于等于，返回布尔值。
```hpl
{func, datetime_datetime.greater_equal(<指针A: ptr>, <指针B: ptr>)}
```

### `datetime_datetime.less_equal`
小于等于，返回布尔值。
```hpl
{func, datetime_datetime.less_equal(<指针A: ptr>, <指针B: ptr>)}
```

### `datetime_datetime.equal`
相等，返回布尔值。
```hpl
{func, datetime_datetime.equal(<指针A: ptr>, <指针B: ptr>)}
```

### `datetime_datetime.add_delta`
加 timedelta，返回新 datetime 指针。
```hpl
{func, datetime_datetime.add_delta(<datetime指针: ptr>, <timedelta指针: ptr>)}
```

### `datetime_datetime.remove_delta`
减 timedelta，返回新 datetime 指针。
```hpl
{func, datetime_datetime.remove_delta(<datetime指针: ptr>, <timedelta指针: ptr>)}
```

### `datetime_datetime.remove_datetime`
两 datetime 相减，返回 timedelta 指针。
```hpl
{func, datetime_datetime.remove_datetime(<指针A: ptr>, <指针B: ptr>)}
```

## datetime_date 模块

### `datetime_date.new`
创建 date 对象，年、月、日必选，返回指针。
```hpl
{func, datetime_date.new(<年: int>, <月: int>, <日: int>)}
```

### `datetime_date.format`
返回 date 的字符串表示。
```hpl
{func, datetime_date.format(<date指针: ptr>)}
```

### `datetime_date.ctime`
返回 C 风格日期字符串。
```hpl
{func, datetime_date.ctime(<date指针: ptr>)}
```

### `datetime_date.day`
返回日。
```hpl
{func, datetime_date.day(<date指针: ptr>)}
```

### `datetime_date.fromordinal`
从序数创建 date，返回指针。
```hpl
{func, datetime_date.fromordinal(<序数: int>)}
```

### `datetime_date.fromtimestamp`
从时间戳创建 date，返回指针。
```hpl
{func, datetime_date.fromtimestamp(<时间戳: float>)}
```

### `datetime_date.isocalendar`
返回 ISO 日历元组指针。
```hpl
{func, datetime_date.isocalendar(<date指针: ptr>)}
```

### `datetime_date.isoformat`
返回 ISO 格式字符串。
```hpl
{func, datetime_date.isoformat(<date指针: ptr>)}
```

### `datetime_date.isoweekday`
返回 ISO 星期几。
```hpl
{func, datetime_date.isoweekday(<date指针: ptr>)}
```

### `datetime_date.max`
返回最大 date 指针。
```hpl
{func, datetime_date.max()}
```

### `datetime_date.min`
返回最小 date 指针。
```hpl
{func, datetime_date.min()}
```

### `datetime_date.month`
返回月份。
```hpl
{func, datetime_date.month(<date指针: ptr>)}
```

### `datetime_date.replace`
替换字段，返回新 date 指针。
```hpl
{func, datetime_date.replace(<date指针: ptr>, <年: int>, <月: int>, <日: int>)}
```

### `datetime_date.strftime`
格式化。
```hpl
{func, datetime_date.strftime(<date指针: ptr>, <格式: string>)}
```

### `datetime_date.timetuple`
返回时间元组指针。
```hpl
{func, datetime_date.timetuple(<date指针: ptr>)}
```

### `datetime_date.today`
返回今天日期指针。
```hpl
{func, datetime_date.today()}
```

### `datetime_date.toordinal`
返回序数。
```hpl
{func, datetime_date.toordinal(<date指针: ptr>)}
```

### `datetime_date.weekday`
返回星期几（0-6）。
```hpl
{func, datetime_date.weekday(<date指针: ptr>)}
```

### `datetime_date.year`
返回年份。
```hpl
{func, datetime_date.year(<date指针: ptr>)}
```

### `datetime_date.greater`
比较大于，返回布尔值。
```hpl
{func, datetime_date.greater(<指针A: ptr>, <指针B: ptr>)}
```

### `datetime_date.less`
小于，返回布尔值。
```hpl
{func, datetime_date.less(<指针A: ptr>, <指针B: ptr>)}
```

### `datetime_date.greater_equal`
大于等于，返回布尔值。
```hpl
{func, datetime_date.greater_equal(<指针A: ptr>, <指针B: ptr>)}
```

### `datetime_date.less_equal`
小于等于，返回布尔值。
```hpl
{func, datetime_date.less_equal(<指针A: ptr>, <指针B: ptr>)}
```

### `datetime_date.equal`
相等，返回布尔值。
```hpl
{func, datetime_date.equal(<指针A: ptr>, <指针B: ptr>)}
```

### `datetime_date.add_delta`
加 timedelta，返回新 date 指针。
```hpl
{func, datetime_date.add_delta(<date指针: ptr>, <timedelta指针: ptr>)}
```

### `datetime_date.remove_delta`
减 timedelta，返回新 date 指针。
```hpl
{func, datetime_date.remove_delta(<date指针: ptr>, <timedelta指针: ptr>)}
```

### `datetime_date.remove_date`
两 date 相减，返回 timedelta 指针。
```hpl
{func, datetime_date.remove_date(<指针A: ptr>, <指针B: ptr>)}
```

## datetime_time 模块

### `datetime_time.new`
创建 time 对象，时、分、秒、微秒可选，返回指针。
```hpl
{func, datetime_time.new([<时: int>, <分: int>, <秒: int>, <微秒: int>])}
```

### `datetime_time.format`
返回 time 的字符串表示。
```hpl
{func, datetime_time.format(<time指针: ptr>)}
```

## 命令执行上下文

### `command.set_executor`
设置命令的执行者实体 ID。
```hpl
{func, command.set_executor(<实体ID: string>)}
```

### `command.get_executor`
获取当前命令执行者的实体 ID（字符串）。
```hpl
{func, command.get_executor()}
```

### `command.set_position`
设置命令执行点的三维坐标。
```hpl
{func, command.set_position(<x: float>, <y: float>, <z: float>)}
```

### `command.get_position`
获取当前命令执行点的坐标，返回指向三元组 (x, y, z) 的指针。
```hpl
{func, command.get_position()}
```

### `command.set_dimension`
设置命令执行的维度 ID。
```hpl
{func, command.set_dimension(<维度ID: int>)}
```

### `command.get_dimension`
获取当前命令执行的维度 ID（整数）。
```hpl
{func, command.get_dimension()}
```

### `command.dimension_name`
获取当前命令执行维度的英文名称（字符串）。
```hpl
{func, command.dimension_name()}
```

### `command.fast_set`
快速将命令执行上下文切换到指定实体（通过选择器或实体 ID）。若 `is_selector=True`（默认），则第一个参数为目标选择器字符串，必须唯一匹配一个实体；若为 False，则第一个参数为实体 ID 字符串。
```hpl
{func, command.fast_set(<选择器或实体ID: string>[, <是否为选择器: bool>])}
```

## 通用模块

### `general.BroadcastEvent`
在本地服务端广播事件。事件数据必须是指针。
```hpl
{func, general.BroadcastEvent(<事件名: string>, <事件数据指针: ptr>)}
```

### `general.BroadcastToAllClient`
广播事件到所有客户端。事件数据必须是指针。
```hpl
{func, general.BroadcastToAllClient(<事件名: string>, <事件数据指针: ptr>)}
```

### `general.GetEngineNamespace`
获取引擎命名空间，返回指向字符串的指针。
```hpl
{func, general.GetEngineNamespace()}
```

### `general.GetEngineSystemName`
获取引擎系统名称，返回指向字符串的指针。
```hpl
{func, general.GetEngineSystemName()}
```

### `general.NotifyToClient`
发送事件到指定客户端。事件数据必须是指针。
```hpl
{func, general.NotifyToClient(<玩家ID: string>, <事件名: string>, <事件数据指针: ptr>)}
```

### `general.NotifyToMultiClients`
发送事件到多个客户端。玩家 ID 列表必须是指针，事件数据也须是指针。
```hpl
{func, general.NotifyToMultiClients(<玩家ID列表指针: ptr>, <事件名: string>, <事件数据指针: ptr>)}
```

### `general.GetMinecraftVersion`
获取游戏版本，返回指向字符串的指针。
```hpl
{func, general.GetMinecraftVersion()}
```

### `general.GetPlatform`
获取运行平台，返回指向字符串的指针。
```hpl
{func, general.GetPlatform()}
```

### `general.GetHostPlayerId`
获取主机玩家 ID，返回指向字符串的指针。
```hpl
{func, general.GetHostPlayerId()}
```

### `general.GetServerTickTime`
获取服务器当前 tick 时间（毫秒），返回指向浮点数的指针。
```hpl
{func, general.GetServerTickTime()}
```

## 世界模块

### 地图

#### `world.CanSee`
检查一个实体是否能看见另一个实体。返回指向布尔值的指针。
```hpl
{func, world.CanSee(<源实体ID: string>, <目标实体ID: string>, [<视距: float>], [<仅固体: bool>], [<水平角: float>], [<垂直角: float>])}
```

#### `world.CheckBlockToPos`
检查从起点到终点的方块碰撞。返回指向布尔值的指针。
```hpl
{func, world.CheckBlockToPos(<起点位置指针: ptr>, <终点位置指针: ptr>, [<维度ID: int>])}
```

#### `world.CheckChunkState`
检查指定区块的加载状态。返回指向布尔值的指针。
```hpl
{func, world.CheckChunkState(<维度ID: int>, <区块位置指针: ptr>)}
```

#### `world.GetAllAreaKeys`
获取所有常加载区域键列表，返回指向字符串列表的指针。
```hpl
{func, world.GetAllAreaKeys()}
```

#### `world.GetBiomeInfo`
获取生物群系信息，参数为生物群系名称，返回指向信息映射的指针。
```hpl
{func, world.GetBiomeInfo(<生物群系名称: string>)}
```

#### `world.GetBiomeName`
获取指定位置的生物群系名称，返回指向字符串的指针。
```hpl
{func, world.GetBiomeName(<位置指针: ptr>, [<维度ID: int>])}
```

#### `world.GetBlockLightLevel`
获取指定方块位置的光照等级，返回指向整数的指针。
```hpl
{func, world.GetBlockLightLevel(<位置指针: ptr>, [<维度ID: int>])}
```

#### `world.GetChunkEntites`
获取指定区块内的所有实体 ID 列表，返回指向列表的指针。
```hpl
{func, world.GetChunkEntites(<维度ID: int>, <区块位置指针: ptr>)}
```

#### `world.GetChunkMobNum`
获取指定区块内的怪物数量，返回指向整数的指针。
```hpl
{func, world.GetChunkMobNum(<维度ID: int>, <区块位置指针: ptr>)}
```

#### `world.GetEntitiesAround`
获取指定实体周围的实体列表（可带过滤器），返回指向实体 ID 列表的指针。
```hpl
{func, world.GetEntitiesAround(<实体ID: string>, <半径: float>, <过滤器指针: ptr>)}
```

#### `world.GetEntitiesAroundByType`
获取指定实体周围指定类型的实体列表，返回指向实体 ID 列表的指针。
```hpl
{func, world.GetEntitiesAroundByType(<实体ID: string>, <半径: float>, <实体类型: string>)}
```

#### `world.GetEntitiesInSquareArea`
获取正方形区域内的所有实体，返回指向实体 ID 列表的指针。
```hpl
{func, world.GetEntitiesInSquareArea(<起点位置指针: ptr>, <终点位置指针: ptr>, [<维度ID: int>])}
```

#### `world.GetLevelId`
获取当前世界 ID，返回指向字符串的指针。
```hpl
{func, world.GetLevelId()}
```

#### `world.GetSpawnPosition`
获取世界出生点坐标，返回指向位置元组的指针。
```hpl
{func, world.GetSpawnPosition()}
```

#### `world.GetStructureSize`
获取指定结构的尺寸，返回指向尺寸映射的指针。
```hpl
{func, world.GetStructureSize(<结构名称: string>)}
```

#### `world.IsChunkGenerated`
检查指定区块是否已生成，返回指向布尔值的指针。
```hpl
{func, world.IsChunkGenerated(<维度ID: int>, <区块位置指针: ptr>)}
```

#### `world.IsSlimeChunk`
检查指定区块是否为史莱姆区块，返回指向布尔值的指针。
```hpl
{func, world.IsSlimeChunk(<维度ID: int>, <区块位置指针: ptr>)}
```

#### `world.LocateStructureFeature`
定位最近的结构特征，返回指向位置元组的指针。
```hpl
{func, world.LocateStructureFeature(<结构类型: string>, <维度ID: int>, <搜索中心位置指针: ptr>, [<仅新区块: bool>])}
```

#### `world.MayPlace`
检查是否可以在指定位置放置方块，返回指向布尔值的指针。
```hpl
{func, world.MayPlace(<方块标识符: string>, <放置位置指针: ptr>, <朝向: int>, [<维度ID: int>])}
```

#### `world.MayPlaceOn`
检查是否可以在指定方块上放置另一个方块，返回指向布尔值的指针。
```hpl
{func, world.MayPlaceOn(<玩家ID: string>, <方块标识符: string>, <附加值: int>, <放置位置指针: ptr>, <朝向: int>)}
```

#### `world.PlaceFeature`
在指定位置放置一个地物，返回指向布尔值的指针。
```hpl
{func, world.PlaceFeature(<特征名称: string>, <维度ID: int>, <位置指针: ptr>)}
```

#### `world.SetMergeSpawnItemRadius`
设置掉落物合并半径，返回指向布尔值的指针。
```hpl
{func, world.SetMergeSpawnItemRadius(<半径: float>)}
```

### 实体管理

#### `world.CreateExperienceOrb`
创建经验球实体，返回指向新实体 ID 的指针。
```hpl
{func, world.CreateExperienceOrb(<实体ID: string>, <经验值: int>, <位置指针: ptr>, <是否特殊: bool>)}
```

#### `world.CreateProjectileEntity`
创建抛射物实体，返回指向新实体 ID 的指针。
```hpl
{func, world.CreateProjectileEntity(<发射者ID: string>, <抛射物标识符: string>, [<参数映射指针: ptr>])}
```

#### `world.DestroyEntity`
销毁指定实体，返回指向布尔值的指针。
```hpl
{func, world.DestroyEntity(<实体ID: string>)}
```

#### `world.GetDroppedItem`
获取掉落物实体的物品数据，返回指向物品字典的指针。
```hpl
{func, world.GetDroppedItem(<物品实体ID: string>, [<获取用户数据: bool>])}
```

#### `world.GetPlayerList`
获取当前所有玩家的 ID 列表，返回指向字符串列表的指针。
```hpl
{func, world.GetPlayerList()}
```

#### `world.IsEntityAlive`
检查实体是否存活，返回指向布尔值的指针。
```hpl
{func, world.IsEntityAlive(<实体ID: string>)}
```

#### `world.KillEntity`
杀死指定实体，返回指向布尔值的指针。
```hpl
{func, world.KillEntity(<实体ID: string>)}
```

### 方块管理

#### `world.GetBlockClip`
获取方块的剪裁框，返回指向剪裁框信息的指针。
```hpl
{func, world.GetBlockClip(<位置指针: ptr>, [<维度ID: int>])}
```

#### `world.GetBlockCollision`
获取方块的碰撞箱，返回指向碰撞箱信息的指针。
```hpl
{func, world.GetBlockCollision(<位置指针: ptr>, [<维度ID: int>])}
```

#### `world.GetBlockNew`
获取指定位置的方块对象，返回指向方块信息的指针。
```hpl
{func, world.GetBlockNew(<位置指针: ptr>, [<维度ID: int>])}
```

#### `world.GetLiquidBlock`
获取液体方块信息，返回指向液体信息的指针。
```hpl
{func, world.GetLiquidBlock(<位置指针: ptr>, [<维度ID: int>])}
```

#### `world.GetTopBlockHeight`
获取指定列最高非空气方块的高度，返回指向整数的指针。
```hpl
{func, world.GetTopBlockHeight(<列位置指针: ptr>, [<维度: int>])}
```

### 生物生成

#### `world.GetEntityLimit`
获取当前实体数量上限，返回指向整数的指针。
```hpl
{func, world.GetEntityLimit()}
```

#### `world.SetEntityLimit`
设置实体数量上限，返回指向布尔值的指针。
```hpl
{func, world.SetEntityLimit(<上限: int>)}
```

### 天气

#### `world.IsRaining`
检查当前是否下雨，返回指向布尔值的指针。
```hpl
{func, world.IsRaining()}
```

#### `world.IsThunder`
检查当前是否打雷，返回指向布尔值的指针。
```hpl
{func, world.IsThunder()}
```

### 游戏规则

#### `world.GetLevelGravity`
获取世界重力值，返回指向浮点数的指针。
```hpl
{func, world.GetLevelGravity()}
```

#### `world.GetPistonMaxInteractionCount`
获取活塞最大推动方块数量，返回指向整数的指针。
```hpl
{func, world.GetPistonMaxInteractionCount()}
```

#### `world.SetHurtCD`
设置实体受伤冷却时间，返回指向布尔值的指针。
```hpl
{func, world.SetHurtCD(<冷却时间tick: int>)}
```

#### `world.SetLevelGravity`
设置世界重力值，返回指向布尔值的指针。
```hpl
{func, world.SetLevelGravity(<重力值: float>)}
```

#### `world.SetPistonMaxInteractionCount`
设置活塞最大推动方块数量，返回指向布尔值的指针。
```hpl
{func, world.SetPistonMaxInteractionCount(<数量: int>)}
```

### 指令

#### `world.SetCommand`
执行一条命令（非设置命令方块），返回指向命令执行结果的指针。
```hpl
{func, world.SetCommand(<命令字符串: string>, <执行者实体ID: string>, [<是否显示输出: bool>])}
```

## 实体模块

### 实体类型

#### `entity.GetEngineType`
获取实体的引擎类型 ID，返回指向整数的指针。
```hpl
{func, entity.GetEngineType(<实体ID: string>)}
```

#### `entity.GetEngineTypeStr`
获取实体的引擎类型名称，返回指向字符串的指针。
```hpl
{func, entity.GetEngineTypeStr(<实体ID: string>)}
```

#### `entity.GetEntityDefinitions`
获取实体的定义标识符列表，返回指向字符串列表的指针。
```hpl
{func, entity.GetEntityDefinitions(<实体ID: string>)}
```

#### `entity.GetEntityNBTTags`
获取实体的 NBT 标签数据，返回指向 NBT 映射的指针。
```hpl
{func, entity.GetEntityNBTTags(<实体ID: string>)}
```

### 附加值

#### `entity.GetAuxValue`
获取实体的附加值（如羊的颜色），返回指向整数的指针。
```hpl
{func, entity.GetAuxValue(<实体ID: string>)}
```

### 属性

#### `entity.ChangeEntityDimension`
将实体传送到指定维度，返回指向布尔值的指针。
```hpl
{func, entity.ChangeEntityDimension(<实体ID: string>, <目标维度ID: int>, <位置指针: ptr>)}
```

#### `entity.GetAllComponentsName`
获取实体所有组件的名称列表，返回指向字符串列表的指针。
```hpl
{func, entity.GetAllComponentsName(<实体ID: string>)}
```

#### `entity.GetAttrMaxValue`
获取实体属性的最大值，返回指向浮点数的指针。
```hpl
{func, entity.GetAttrMaxValue(<实体ID: string>, <属性类型: string>)}
```

#### `entity.GetAttrValue`
获取实体属性的当前值，返回指向浮点数的指针。
```hpl
{func, entity.GetAttrValue(<实体ID: string>, <属性类型: string>)}
```

#### `entity.GetCurrentAirSupply`
获取实体当前氧气值，返回指向整数的指针。
```hpl
{func, entity.GetCurrentAirSupply(<实体ID: string>)}
```

#### `entity.GetDeathTime`
获取实体死亡时间（tick），返回指向整数的指针。
```hpl
{func, entity.GetDeathTime(<实体ID: string>)}
```

#### `entity.GetEntitiesBySelector`
通过目标选择器获取实体列表，需要种子实体 ID，返回指向实体 ID 列表的指针。
```hpl
{func, entity.GetEntitiesBySelector(<实体ID: string>, <选择器: string>)}
```

#### `entity.GetEntityDamage`
获取实体攻击伤害值，返回指向浮点数的指针。
```hpl
{func, entity.GetEntityDamage(<实体ID: string>[, <目标实体ID: string>])}
```

#### `entity.GetEntityDimensionId`
获取实体所在维度 ID，返回指向整数的指针。
```hpl
{func, entity.GetEntityDimensionId(<实体ID: string>)}
```

#### `entity.GetEntityFallDistance`
获取实体当前下落距离，返回指向浮点数的指针。
```hpl
{func, entity.GetEntityFallDistance(<实体ID: string>)}
```

#### `entity.GetEntityLinksTag`
获取实体链接标签，返回指向字符串的指针。
```hpl
{func, entity.GetEntityLinksTag(<实体ID: string>)}
```

#### `entity.GetEntityOwner`
获取实体的拥有者 ID，返回指向字符串的指针。
```hpl
{func, entity.GetEntityOwner(<实体ID: string>)}
```

#### `entity.GetFootPos`
获取实体脚部位置坐标，返回指向位置元组的指针。
```hpl
{func, entity.GetFootPos(<实体ID: string>)}
```

#### `entity.GetGravity`
获取实体重力值，返回指向浮点数的指针。
```hpl
{func, entity.GetGravity(<实体ID: string>)}
```

#### `entity.GetMarkVariant`
获取实体标记变体，返回指向整数的指针。
```hpl
{func, entity.GetMarkVariant(<实体ID: string>)}
```

#### `entity.GetMaxAirSupply`
获取实体最大氧气值，返回指向整数的指针。
```hpl
{func, entity.GetMaxAirSupply(<实体ID: string>)}
```

#### `entity.GetMobColor`
获取生物颜色，返回指向整数的指针。
```hpl
{func, entity.GetMobColor(<实体ID: string>)}
```

#### `entity.GetMobStrength`
获取生物当前力量值，返回指向浮点数的指针。
```hpl
{func, entity.GetMobStrength(<实体ID: string>)}
```

#### `entity.GetMobStrengthMax`
获取生物最大力量值，返回指向浮点数的指针。
```hpl
{func, entity.GetMobStrengthMax(<实体ID: string>)}
```

#### `entity.GetName`
获取实体自定义名称，返回指向字符串的指针。
```hpl
{func, entity.GetName(<实体ID: string>)}
```

#### `entity.GetPos`
获取实体位置坐标，返回指向位置元组的指针。
```hpl
{func, entity.GetPos(<实体ID: string>)}
```

#### `entity.GetRot`
获取实体旋转角度（俯仰, 偏航），返回指向旋转元组的指针。
```hpl
{func, entity.GetRot(<实体ID: string>)}
```

#### `entity.GetSize`
获取实体尺寸（宽度, 高度），返回指向尺寸元组的指针。
```hpl
{func, entity.GetSize(<实体ID: string>)}
```

#### `entity.GetTradeLevel`
获取村民交易等级，返回指向整数的指针。
```hpl
{func, entity.GetTradeLevel(<实体ID: string>)}
```

#### `entity.GetTypeFamily`
获取实体所属家族类型，返回指向字符串的指针。
```hpl
{func, entity.GetTypeFamily(<实体ID: string>)}
```

#### `entity.GetUnitBubbleAirSupply`
获取单位气泡氧气值，返回指向浮点数的指针。
```hpl
{func, entity.GetUnitBubbleAirSupply()}
```

#### `entity.GetVariant`
获取实体变种 ID，返回指向整数的指针。
```hpl
{func, entity.GetVariant(<实体ID: string>)}
```

#### `entity.HasChest`
检查实体是否携带箱子，返回指向布尔值的指针。
```hpl
{func, entity.HasChest(<实体ID: string>)}
```

#### `entity.HasComponent`
检查实体是否拥有指定组件，返回指向布尔值的指针。
```hpl
{func, entity.HasComponent(<实体ID: string>, <组件名: string>)}
```

#### `entity.HasSaddle`
检查实体是否装备鞍，返回指向布尔值的指针。
```hpl
{func, entity.HasSaddle(<实体ID: string>)}
```

#### `entity.IsAngry`
检查实体是否愤怒，返回指向布尔值的指针。
```hpl
{func, entity.IsAngry(<实体ID: string>)}
```

#### `entity.IsBaby`
检查实体是否为幼年，返回指向布尔值的指针。
```hpl
{func, entity.IsBaby(<实体ID: string>)}
```

#### `entity.IsConsumingAirSupply`
检查实体是否在消耗氧气，返回指向布尔值的指针。
```hpl
{func, entity.IsConsumingAirSupply(<实体ID: string>)}
```

#### `entity.IsIllagerCaptain`
检查实体是否为灾厄队长，返回指向布尔值的指针。
```hpl
{func, entity.IsIllagerCaptain(<实体ID: string>)}
```

#### `entity.IsNaturallySpawned`
检查实体是否自然生成，返回指向布尔值的指针。
```hpl
{func, entity.IsNaturallySpawned(<实体ID: string>)}
```

#### `entity.IsOutOfControl`
检查实体是否失控，返回指向布尔值的指针。
```hpl
{func, entity.IsOutOfControl(<实体ID: string>)}
```

#### `entity.IsPregnant`
检查实体是否怀孕，返回指向布尔值的指针。
```hpl
{func, entity.IsPregnant(<实体ID: string>)}
```

#### `entity.IsSheared`
检查实体是否被剪毛，返回指向布尔值的指针。
```hpl
{func, entity.IsSheared(<实体ID: string>)}
```

#### `entity.IsSitting`
检查实体是否坐下，返回指向布尔值的指针。
```hpl
{func, entity.IsSitting(<实体ID: string>)}
```

#### `entity.IsTamed`
检查实体是否被驯服，返回指向布尔值的指针。
```hpl
{func, entity.IsTamed(<实体ID: string>)}
```

#### `entity.PromoteToIllagerCaptain`
将实体提升为灾厄队长，返回指向布尔值的指针。
```hpl
{func, entity.PromoteToIllagerCaptain(<实体ID: string>)}
```

#### `entity.ResetToDefaultValue`
将实体属性重置为默认值，返回指向布尔值的指针。
```hpl
{func, entity.ResetToDefaultValue(<实体ID: string>, <属性类型: string>)}
```

#### `entity.ResetToMaxValue`
将实体属性重置为最大值，返回指向布尔值的指针。
```hpl
{func, entity.ResetToMaxValue(<实体ID: string>, <属性类型: string>)}
```

#### `entity.SetAngry`
设置实体愤怒状态，可指定目标 ID，返回指向布尔值的指针。
```hpl
{func, entity.SetAngry(<实体ID: string>, <是否愤怒: bool>[, <目标ID: string>])}
```

#### `entity.SetAsAdult`
将实体设为成年，返回指向布尔值的指针。
```hpl
{func, entity.SetAsAdult(<实体ID: string>)}
```

#### `entity.SetAttrMaxValue`
设置实体属性最大值，返回指向布尔值的指针。
```hpl
{func, entity.SetAttrMaxValue(<实体ID: string>, <属性类型: string>, <最大值: float>)}
```

#### `entity.SetAttrValue`
设置实体属性当前值，可指定是否设为默认值，返回指向布尔值的指针。
```hpl
{func, entity.SetAttrValue(<实体ID: string>, <属性类型: string>, <值: float>[, <set_default: int>])}
```

#### `entity.SetChest`
设置实体是否携带箱子，返回指向布尔值的指针。
```hpl
{func, entity.SetChest(<实体ID: string>, <是否有箱子: bool>)}
```

#### `entity.SetCurrentAirSupply`
设置实体当前氧气值，返回指向布尔值的指针。
```hpl
{func, entity.SetCurrentAirSupply(<实体ID: string>, <氧气值: int>)}
```

#### `entity.SetEntityLookAtPos`
设置实体注视某个位置，返回指向布尔值的指针。
```hpl
{func, entity.SetEntityLookAtPos(<实体ID: string>, <目标位置指针: ptr>, <最小时间: float>, <最大时间: float>, <是否拒绝: bool>)}
```

#### `entity.SetEntityOwner`
设置实体的拥有者，返回指向布尔值的指针。
```hpl
{func, entity.SetEntityOwner(<实体ID: string>, <主人ID: string>)}
```

#### `entity.SetGravity`
设置实体重力值，返回指向布尔值的指针。
```hpl
{func, entity.SetGravity(<实体ID: string>, <重力值: float>)}
```

#### `entity.SetMarkVariant`
设置实体标记变体，返回指向布尔值的指针。
```hpl
{func, entity.SetMarkVariant(<实体ID: string>, <变体: int>)}
```

#### `entity.SetMaxAirSupply`
设置实体最大氧气值，返回指向布尔值的指针。
```hpl
{func, entity.SetMaxAirSupply(<实体ID: string>, <最大氧气: int>)}
```

#### `entity.SetMobColor`
设置生物颜色，返回指向布尔值的指针。
```hpl
{func, entity.SetMobColor(<实体ID: string>, <颜色: int>)}
```

#### `entity.SetMobStrength`
设置生物力量值，返回指向布尔值的指针。
```hpl
{func, entity.SetMobStrength(<实体ID: string>, <力量: float>)}
```

#### `entity.SetMobStrengthMax`
设置生物最大力量值，返回指向布尔值的指针。
```hpl
{func, entity.SetMobStrengthMax(<实体ID: string>, <最大力量: float>)}
```

#### `entity.SetName`
设置实体自定义名称，返回指向布尔值的指针。
```hpl
{func, entity.SetName(<实体ID: string>, <名称: string>)}
```

#### `entity.SetOutOfControl`
设置实体失控状态，返回指向布尔值的指针。
```hpl
{func, entity.SetOutOfControl(<实体ID: string>, <是否失控: bool>)}
```

#### `entity.SetPersistent`
设置实体是否持久存在（不消失），返回指向布尔值的指针。
```hpl
{func, entity.SetPersistent(<实体ID: string>, <是否持久: bool>)}
```

#### `entity.SetPos`
设置实体位置，返回指向布尔值的指针。
```hpl
{func, entity.SetPos(<实体ID: string>, <位置指针: ptr>)}
```

#### `entity.SetRecoverTotalAirSupplyTime`
设置实体恢复全部氧气所需时间，返回指向布尔值的指针。
```hpl
{func, entity.SetRecoverTotalAirSupplyTime(<实体ID: string>, <时间tick: int>)}
```

#### `entity.SetRot`
设置实体旋转角度，返回指向布尔值的指针。
```hpl
{func, entity.SetRot(<实体ID: string>, <旋转指针: ptr>)}
```

#### `entity.SetSheared`
设置实体剪毛状态，返回指向布尔值的指针。
```hpl
{func, entity.SetSheared(<实体ID: string>, <是否剪毛: bool>)}
```

#### `entity.SetSitting`
设置实体坐下状态，返回指向布尔值的指针。
```hpl
{func, entity.SetSitting(<实体ID: string>, <是否坐下: bool>)}
```

#### `entity.SetSize`
设置实体尺寸，返回指向布尔值的指针。
```hpl
{func, entity.SetSize(<实体ID: string>, <尺寸指针: ptr>)}
```

#### `entity.SetTradeLevel`
设置村民交易等级，返回指向布尔值的指针。
```hpl
{func, entity.SetTradeLevel(<实体ID: string>, <等级: int>)}
```

#### `entity.SetVariant`
设置实体变种，返回指向布尔值的指针。
```hpl
{func, entity.SetVariant(<实体ID: string>, <变种: int>)}
```

### 行为

#### `entity.GetAttackTarget`
获取实体的攻击目标 ID，返回指向字符串的指针。
```hpl
{func, entity.GetAttackTarget(<实体ID: string>)}
```

#### `entity.GetBlockControlAi`
获取实体是否被阻挡 AI 控制，返回指向布尔值的指针。
```hpl
{func, entity.GetBlockControlAi(<实体ID: string>)}
```

#### `entity.GetComponents`
获取实体的所有组件名称列表，返回指向字符串列表的指针。
```hpl
{func, entity.GetComponents(<实体ID: string>)}
```

#### `entity.GetJumpPower`
获取实体的跳跃力，返回指向浮点数的指针。
```hpl
{func, entity.GetJumpPower(<实体ID: string>)}
```

#### `entity.GetLeashHolder`
获取拴绳的主人实体 ID，返回指向字符串的指针。
```hpl
{func, entity.GetLeashHolder(<实体ID: string>)}
```

#### `entity.GetMotion`
获取实体的运动向量，返回指向速度元组 (vx, vy, vz) 的指针。
```hpl
{func, entity.GetMotion(<实体ID: string>)}
```

#### `entity.GetOwnerId`
获取驯服实体的主人 ID，返回指向字符串的指针。
```hpl
{func, entity.GetOwnerId(<实体ID: string>)}
```

#### `entity.GetStepHeight`
获取实体的步高，返回指向浮点数的指针。
```hpl
{func, entity.GetStepHeight(<实体ID: string>)}
```

#### `entity.ImmuneDamage`
检查实体是否对某种伤害免疫，返回指向布尔值的指针。
```hpl
{func, entity.ImmuneDamage(<实体ID: string>, <伤害来源: string>)}
```

#### `entity.IsEating`
检查实体是否在进食，返回指向布尔值的指针。
```hpl
{func, entity.IsEating(<实体ID: string>)}
```

#### `entity.IsEntityOnFire`
检查实体是否着火，返回指向布尔值的指针。
```hpl
{func, entity.IsEntityOnFire(<实体ID: string>)}
```

#### `entity.IsLootDropped`
检查实体死亡是否掉落物品，返回指向布尔值的指针。
```hpl
{func, entity.IsLootDropped(<实体ID: string>)}
```

#### `entity.IsPersistent`
检查实体是否持久存在，返回指向布尔值的指针。
```hpl
{func, entity.IsPersistent(<实体ID: string>)}
```

#### `entity.IsRoaring`
检查实体是否在咆哮，返回指向布尔值的指针。
```hpl
{func, entity.IsRoaring(<实体ID: string>)}
```

#### `entity.IsStunned`
检查实体是否眩晕，返回指向布尔值的指针。
```hpl
{func, entity.IsStunned(<实体ID: string>)}
```

#### `entity.ResetAttackTarget`
重置攻击目标，返回指向布尔值的指针。
```hpl
{func, entity.ResetAttackTarget(<实体ID: string>)}
```

#### `entity.ResetMotion`
重置运动向量，返回指向布尔值的指针。
```hpl
{func, entity.ResetMotion(<实体ID: string>)}
```

#### `entity.ResetStepHeight`
重置步高为默认值，返回指向布尔值的指针。
```hpl
{func, entity.ResetStepHeight(<实体ID: string>)}
```

#### `entity.SetActorCollidable`
设置实体是否可碰撞，返回指向布尔值的指针。
```hpl
{func, entity.SetActorCollidable(<实体ID: string>, <是否可碰撞: bool>)}
```

#### `entity.SetActorPushable`
设置实体是否可被推动，返回指向布尔值的指针。
```hpl
{func, entity.SetActorPushable(<实体ID: string>, <是否可推动: bool>)}
```

#### `entity.SetAttackTarget`
设置攻击目标，返回指向布尔值的指针。
```hpl
{func, entity.SetAttackTarget(<实体ID: string>, <目标ID: string>)}
```

#### `entity.SetBlockControlAi`
设置是否阻挡 AI 控制，返回指向布尔值的指针。
```hpl
{func, entity.SetBlockControlAi(<实体ID: string>, <是否阻挡: bool>[, <freeze_anim: bool>])}
```

#### `entity.SetEntityOnFire`
设置实体着火状态，返回指向布尔值的指针。
```hpl
{func, entity.SetEntityOnFire(<实体ID: string>, <秒数: float>[, <燃烧伤害: int>])}
```

#### `entity.SetEntityTamed`
设置实体驯服状态，返回指向布尔值的指针。
```hpl
{func, entity.SetEntityTamed(<实体ID: string>, <玩家ID: string>)}
```

#### `entity.SetJumpPower`
设置跳跃力，返回指向布尔值的指针。
```hpl
{func, entity.SetJumpPower(<实体ID: string>, <跳跃力: float>)}
```

#### `entity.SetLeashHolder`
设置拴绳主人，返回指向布尔值的指针。
```hpl
{func, entity.SetLeashHolder(<实体ID: string>, <主人ID: string>)}
```

#### `entity.SetLootDropped`
设置死亡是否掉落物品，返回指向布尔值的指针。
```hpl
{func, entity.SetLootDropped(<实体ID: string>, <是否掉落: bool>)}
```

#### `entity.SetMobKnockback`
设置击退初始速度，返回布尔值 True（直接值，非指针）。
```hpl
{func, entity.SetMobKnockback(<实体ID: string>, [<xd: float>], [<zd: float>], [<power: float>], [<height: float>], [<height_cap: float>])}
```

#### `entity.SetMotion`
设置运动向量，返回指向布尔值的指针。
```hpl
{func, entity.SetMotion(<实体ID: string>, <运动向量指针: ptr>)}
```

#### `entity.SetPersistence`
设置实体持久化（不消失），返回布尔值 True（直接值，非指针）。
```hpl
{func, entity.SetPersistence(<实体ID: string>, <是否持久: bool>)}
```

#### `entity.SetStepHeight`
设置步高，返回指向布尔值的指针。
```hpl
{func, entity.SetStepHeight(<实体ID: string>, <步高: float>)}
```

### 状态效果

#### `entity.AddEffectToEntity`
为实体添加状态效果，返回指向布尔值的指针。
```hpl
{func, entity.AddEffectToEntity(<实体ID: string>, <效果名: string>, <持续时间: int>, <等级: int>, <是否显示粒子: bool>)}
```

#### `entity.GetAllEffects`
获取实体所有状态效果，返回指向效果列表的指针。
```hpl
{func, entity.GetAllEffects(<实体ID: string>)}
```

#### `entity.HasEffect`
检查实体是否有指定效果，返回指向布尔值的指针。
```hpl
{func, entity.HasEffect(<实体ID: string>, <效果名: string>)}
```

#### `entity.RemoveEffectFromEntity`
移除实体的指定状态效果，返回指向布尔值的指针。
```hpl
{func, entity.RemoveEffectFromEntity(<实体ID: string>, <效果名: string>)}
```

### 背包

#### `entity.GetEntityItem`
获取实体手中的物品，返回指向物品字典的指针。
```hpl
{func, entity.GetEntityItem(<实体ID: string>, <槽位类型: string>, <槽位索引: int>, [<获取用户数据: bool>])}
```

#### `entity.GetEquItemEnchant`
获取装备物品的附魔信息，返回指向附魔数据映射的指针。
```hpl
{func, entity.GetEquItemEnchant(<玩家ID: string>, <槽位索引: int>)}
```

#### `entity.GetEquItemModEnchant`
获取装备物品的模组附魔信息，返回指向附魔数据映射的指针。
```hpl
{func, entity.GetEquItemModEnchant(<玩家ID: string>, <槽位索引: int>)}
```

### 自定义数据

#### `entity.CleanExtraData`
清除实体的自定义数据（指定键），返回指向布尔值的指针。
```hpl
{func, entity.CleanExtraData(<实体ID: string>, <键: string>)}
```

#### `entity.GetExtraData`
获取实体的自定义数据（指定键），返回指向数据值的指针。
```hpl
{func, entity.GetExtraData(<实体ID: string>, <键: string>)}
```

#### `entity.GetWholeExtraData`
获取实体的全部自定义数据，返回指向映射的指针。
```hpl
{func, entity.GetWholeExtraData(<实体ID: string>)}
```

#### `entity.SaveExtraData`
保存实体的自定义数据，返回指向布尔值的指针。
```hpl
{func, entity.SaveExtraData(<实体ID: string>)}
```

#### `entity.SetExtraData`
设置实体的自定义数据，返回指向布尔值的指针。
```hpl
{func, entity.SetExtraData(<实体ID: string>, <键: string>, <值或指针: any>, [<是否为指针: bool>], [<自动保存: bool>])}
```

### 标签

#### `entity.AddEntityTag`
为实体添加标签，返回指向布尔值的指针。
```hpl
{func, entity.AddEntityTag(<实体ID: string>, <标签: string>)}
```

#### `entity.EntityHasTag`
检查实体是否有指定标签，返回指向布尔值的指针。
```hpl
{func, entity.EntityHasTag(<实体ID: string>, <标签: string>)}
```

#### `entity.GetEntityTags`
获取实体的所有标签列表，返回指向字符串列表的指针。
```hpl
{func, entity.GetEntityTags(<实体ID: string>)}
```

#### `entity.RemoveEntityTag`
移除实体的指定标签，返回指向布尔值的指针。
```hpl
{func, entity.RemoveEntityTag(<实体ID: string>, <标签: string>)}
```

### 抛射物

#### `entity.GetSourceEntityId`
获取抛射物的发射者实体 ID，返回指向字符串的指针。
```hpl
{func, entity.GetSourceEntityId(<抛射物实体ID: string>)}
```

### 经验球

#### `entity.GetOrbExperience`
获取经验球的经验值，返回指向整数的指针。
```hpl
{func, entity.GetOrbExperience(<经验球实体ID: string>)}
```

#### `entity.SetOrbExperience`
设置经验球的经验值，返回指向布尔值的指针。
```hpl
{func, entity.SetOrbExperience(<经验球实体ID: string>, <经验值: int>)}
```

## 玩家模块

### 属性

#### `player.GetPlayerExp`
获取玩家当前经验值（等级内进度），返回指向浮点数的指针。
```hpl
{func, player.GetPlayerExp(<玩家ID: string>[, <是否百分比: bool>])}
```

#### `player.GetPlayerHunger`
获取玩家饥饿值，返回指向整数的指针。
```hpl
{func, player.GetPlayerHunger(<玩家ID: string>)}
```

#### `player.GetPlayerTotalExp`
获取玩家总经验值（等级），返回指向整数的指针。
```hpl
{func, player.GetPlayerTotalExp(<玩家ID: string>)}
```

#### `player.SetPlayerHunger`
设置玩家饥饿值，返回指向布尔值的指针。
```hpl
{func, player.SetPlayerHunger(<玩家ID: string>, <饥饿值: int>)}
```

#### `player.SetPlayerPrefixAndSuffixName`
设置玩家名字的前缀和后缀（带颜色），返回指向布尔值的指针。
```hpl
{func, player.SetPlayerPrefixAndSuffixName(<玩家ID: string>, <前缀: string>, <前缀颜色: string>, <后缀: string>, <后缀颜色: string>[, <名字颜色: string>])}
```

#### `player.SetPlayerTotalExp`
设置玩家总经验值（等级），返回指向布尔值的指针。
```hpl
{func, player.SetPlayerTotalExp(<玩家ID: string>, <经验值: int>)}
```

### 行为

#### `player.ChangePlayerDimension`
将玩家传送到指定维度，返回指向布尔值的指针。
```hpl
{func, player.ChangePlayerDimension(<玩家ID: string>, <维度ID: int>, <位置指针: ptr>)}
```

#### `player.ChangePlayerFlyState`
更改玩家飞行状态（允许/禁止飞行），返回指向布尔值的指针。
```hpl
{func, player.ChangePlayerFlyState(<玩家ID: string>, <是否允许飞行: bool>[, <是否立即起飞: bool>])}
```

#### `player.GetPlayerRespawnPos`
获取玩家重生点坐标，返回指向位置元组的指针。
```hpl
{func, player.GetPlayerRespawnPos(<玩家ID: string>)}
```

#### `player.IsPlayerCanFly`
检查玩家是否允许飞行，返回指向布尔值的指针。
```hpl
{func, player.IsPlayerCanFly(<玩家ID: string>)}
```

#### `player.IsPlayerFlying`
检查玩家是否正在飞行，返回指向布尔值的指针。
```hpl
{func, player.IsPlayerFlying(<玩家ID: string>)}
```

#### `player.SetBanPlayerFishing`
设置禁止玩家钓鱼，返回指向布尔值的指针。
```hpl
{func, player.SetBanPlayerFishing(<玩家ID: string>, <是否禁止: bool>)}
```

#### `player.SetPickUpArea`
设置玩家物品拾取范围，返回指向布尔值的指针。
```hpl
{func, player.SetPickUpArea(<玩家ID: string>, <区域指针: ptr>)}
```

#### `player.SetPlayerAttackSpeedAmplifier`
设置玩家攻击速度倍率，返回指向布尔值的指针。
```hpl
{func, player.SetPlayerAttackSpeedAmplifier(<玩家ID: string>, <倍率: float>)}
```

#### `player.SetPlayerMotion`
设置玩家运动向量，返回指向布尔值的指针。
```hpl
{func, player.SetPlayerMotion(<玩家ID: string>, <运动向量指针: ptr>)}
```

#### `player.SetPlayerRespawnPos`
设置玩家重生点（固定维度为 0），返回指向布尔值的指针。
```hpl
{func, player.SetPlayerRespawnPos(<玩家ID: string>, <位置指针: ptr>)}
```

#### `player.isSneaking`
检查玩家是否潜行，返回指向布尔值的指针。
```hpl
{func, player.isSneaking(<玩家ID: string>)}
```

#### `player.isSwimming`
检查玩家是否游泳，返回指向布尔值的指针。
```hpl
{func, player.isSwimming(<玩家ID: string>)}
```

### 背包

#### `player.AddEnchantToInvItem`
为背包物品添加附魔，返回指向布尔值的指针。
```hpl
{func, player.AddEnchantToInvItem(<玩家ID: string>, <槽位索引: int>, <附魔ID: int>, <等级: int>)}
```

#### `player.AddModEnchantToInvItem`
为背包物品添加模组附魔，返回指向布尔值的指针。
```hpl
{func, player.AddModEnchantToInvItem(<玩家ID: string>, <槽位索引: int>, <模组附魔ID: int>, <等级: int>)}
```

#### `player.ChangePlayerItemTipsAndExtraId`
修改玩家物品的提示文本和额外 ID，返回指向布尔值的指针。
```hpl
{func, player.ChangePlayerItemTipsAndExtraId(<玩家ID: string>, <槽位类型: string>, <槽位索引: int>, [<自定义提示: string>], [<额外ID: string>])}
```

#### `player.ChangeSelectSlot`
改变玩家当前选中的快捷栏槽位，返回指向布尔值的指针。
```hpl
{func, player.ChangeSelectSlot(<玩家ID: string>, <新槽位: int>)}
```

#### `player.GetInvItemEnchantData`
获取背包物品的附魔数据，返回指向附魔数据映射的指针。
```hpl
{func, player.GetInvItemEnchantData(<玩家ID: string>, <槽位索引: int>)}
```

#### `player.GetInvItemModEnchantData`
获取背包物品的模组附魔数据，返回指向附魔数据映射的指针。
```hpl
{func, player.GetInvItemModEnchantData(<玩家ID: string>, <槽位索引: int>)}
```

#### `player.GetPlayerItem`
获取玩家背包中的物品，返回指向物品字典的指针。
```hpl
{func, player.GetPlayerItem(<玩家ID: string>, <槽位类型: string>, <槽位索引: int>, [<获取用户数据: bool>])}
```

#### `player.GetSelectSlotId`
获取玩家当前选中的快捷栏槽位 ID，返回指向整数的指针。
```hpl
{func, player.GetSelectSlotId(<玩家ID: string>)}
```

#### `player.RemoveEnchantToInvItem`
移除背包物品的附魔，返回指向布尔值的指针。
```hpl
{func, player.RemoveEnchantToInvItem(<玩家ID: string>, <槽位索引: int>, <附魔ID: int>)}
```

#### `player.RemoveModEnchantToInvItem`
移除背包物品的模组附魔，返回指向布尔值的指针。
```hpl
{func, player.RemoveModEnchantToInvItem(<玩家ID: string>, <槽位索引: int>, <模组附魔ID: int>)}
```

#### `player.SetInvItemExchange`
交换背包中的两个物品，返回指向布尔值的指针。
```hpl
{func, player.SetInvItemExchange(<玩家ID: string>, <槽位A: int>, <槽位B: int>)}
```

### 游戏模式

#### `player.GetPlayerGameType`
获取玩家的游戏模式，返回指向整数的指针。
```hpl
{func, player.GetPlayerGameType(<玩家ID: string>)}
```

#### `player.SetPlayerGameType`
设置玩家的游戏模式，返回指向布尔值的指针。
```hpl
{func, player.SetPlayerGameType(<玩家ID: string>, <游戏模式: int>)}
```

### 权限

#### `player.GetPlayerAbilities`
获取玩家能力映射，返回指向映射的指针。
```hpl
{func, player.GetPlayerAbilities(<玩家ID: string>)}
```

#### `player.GetPlayerOperation`
获取玩家权限等级，返回指向整数的指针。
```hpl
{func, player.GetPlayerOperation(<玩家ID: string>)}
```

#### `player.SetAttackMobsAbility`
设置玩家攻击生物的权限，返回指向布尔值的指针。
```hpl
{func, player.SetAttackMobsAbility(<玩家ID: string>, <是否允许: bool>)}
```

#### `player.SetAttackPlayersAbility`
设置玩家攻击玩家的权限，返回指向布尔值的指针。
```hpl
{func, player.SetAttackPlayersAbility(<玩家ID: string>, <是否允许: bool>)}
```

#### `player.SetBuildAbility`
设置玩家建筑权限，返回指向布尔值的指针。
```hpl
{func, player.SetBuildAbility(<玩家ID: string>, <是否允许: bool>)}
```

#### `player.SetMineAbility`
设置玩家挖掘权限，返回指向布尔值的指针。
```hpl
{func, player.SetMineAbility(<玩家ID: string>, <是否允许: bool>)}
```

#### `player.SetOpenContainersAbility`
设置玩家打开容器权限，返回指向布尔值的指针。
```hpl
{func, player.SetOpenContainersAbility(<玩家ID: string>, <是否允许: bool>)}
```

#### `player.SetOperateDoorsAndSwitchesAbility`
设置玩家操作门和开关权限，返回指向布尔值的指针。
```hpl
{func, player.SetOperateDoorsAndSwitchesAbility(<玩家ID: string>, <是否允许: bool>)}
```

#### `player.SetOperatorAbility`
设置玩家使用管理员命令权限，返回指向布尔值的指针。
```hpl
{func, player.SetOperatorCommandAbility(<玩家ID: string>, <是否允许: bool>)}
```

#### `player.SetPermissionLevel`
设置玩家权限等级，返回指向布尔值的指针。
```hpl
{func, player.SetPermissionLevel(<玩家ID: string>, <权限等级: int>)}
```

#### `player.SetPlayerMute`
设置玩家禁言状态，返回指向布尔值的指针。
```hpl
{func, player.SetPlayerMute(<玩家ID: string>, <是否禁言: bool>)}
```

#### `player.SetTeleportAbility`
设置玩家传送权限，返回指向布尔值的指针。
```hpl
{func, player.SetTeleportAbility(<玩家ID: string>, <是否允许: bool>)}
```

## 方块模块

### 方块状态与附加值

#### `block.GetBlockStates`
获取方块的状态（如朝向、水位），返回指向状态映射的指针。
```hpl
{func, block.GetBlockStates(<位置指针: ptr>[, <维度ID: int>])}
```

### 方块实体

#### `block.ExecuteCommandBlock`
执行命令方块中的命令，返回指向执行结果（布尔值）的指针。
```hpl
{func, block.ExecuteCommandBlock(<位置指针: ptr>, <维度ID: int>)}
```

#### `block.GetBlockEntityData`
获取方块实体的数据，返回指向 NBT 数据的指针。
```hpl
{func, block.GetBlockEntityData(<维度ID: int>, <位置指针: ptr>)}
```

#### `block.GetBlockTileEntityCustomData`
获取方块实体的自定义数据（指定键），返回指向数据值的指针。
```hpl
{func, block.GetBlockTileEntityCustomData(<玩家ID: string>, <位置指针: ptr>, <键: string>[, <维度ID: int>])}
```

#### `block.GetBlockTileEntityWholeCustomData`
获取方块实体的全部自定义数据，返回指向映射的指针。
```hpl
{func, block.GetBlockTileEntityWholeCustomData(<玩家ID: string>, <位置指针: ptr>[, <维度ID: int>])}
```

#### `block.GetCommandBlock`
获取命令方块的信息，返回指向信息映射的指针。
```hpl
{func, block.GetCommandBlock(<世界ID: string>, <位置指针: ptr>, <维度ID: int>)}
```

#### `block.GetFrameItem`
获取物品展示框中的物品，返回指向物品字典的指针。
```hpl
{func, block.GetFrameItem(<位置指针: ptr>, <维度ID: int>)}
```

#### `block.GetFrameRotation`
获取物品展示框的旋转角度，返回指向整数的指针。
```hpl
{func, block.GetFrameRotation(<位置指针: ptr>, <维度ID: int>)}
```

#### `block.SetCommandBlock`
设置命令方块，返回指向布尔值的指针。
```hpl
{func, block.SetCommandBlock(<位置指针: ptr>, <维度ID: int>, <命令: string>, <名称: string>, <模式: int>, <是否条件制约: bool>, <红石模式: int>)}
```

#### `block.SetFrameRotation`
设置物品展示框的旋转角度，返回指向布尔值的指针。
```hpl
{func, block.SetFrameRotation(<位置指针: ptr>, <维度ID: int>, <旋转角度: int>)}
```

### 容器

#### `block.GetBrewingStandSlotItem`
获取酿造台指定槽位的物品，返回指向物品字典的指针。
```hpl
{func, block.GetBrewingStandSlotItem(<玩家ID: string>, <槽位: int>, <位置指针: ptr>, <维度ID: int>)}
```

#### `block.GetChestBoxSize`
获取箱子的槽位总数（容量），返回指向整数的指针。
```hpl
{func, block.GetChestBoxSize(<位置指针: ptr>[, <维度ID: int>])}
```

#### `block.GetChestPairedPosition`
获取双联箱子的配对箱子坐标，返回指向位置元组的指针（若无配对则指向 None）。
```hpl
{func, block.GetChestPairedPosition(<玩家ID: string>, <位置指针: ptr>[, <维度ID: int>])}
```

#### `block.GetContainerItem`
获取容器指定槽位的物品，返回指向物品字典的指针。
```hpl
{func, block.GetContainerItem(<位置指针: ptr>, <槽位: int>[, <维度ID: int>][, <获取用户数据: bool>])}
```

#### `block.GetContainerSize`
获取容器的槽位总数，返回指向整数的指针。
```hpl
{func, block.GetContainerSize(<位置指针: ptr>[, <维度ID: int>])}
```

#### `block.GetEnderChestItem`
获取末影箱指定槽位的物品（每个玩家独立），返回指向物品字典的指针。
```hpl
{func, block.GetEnderChestItem(<玩家ID: string>, <槽位: int>[, <获取用户数据: bool>])}
```

#### `block.GetInputSlotItem`
获取工作台、熔炉等容器的输入槽物品，返回指向物品字典的指针。
```hpl
{func, block.GetInputSlotItem(<位置指针: ptr>[, <维度ID: int>])}
```

#### `block.GetOutputSlotItem`
获取熔炉、高炉等容器的输出槽物品，返回指向物品字典的指针。
```hpl
{func, block.GetOutputSlotItem(<位置指针: ptr>[, <维度ID: int>])}
```

#### `block.SetChestBoxItemExchange`
交换箱子中的两个物品，返回指向布尔值的指针。
```hpl
{func, block.SetChestBoxItemExchange(<玩家ID: string>, <位置指针: ptr>, <槽位A: int>, <槽位B: int>)}
```

### 红石

#### `block.GetBlockPoweredState`
获取方块的充能状态（是否被红石激活），返回指向布尔值的指针。
```hpl
{func, block.GetBlockPoweredState(<位置指针: ptr>, <维度ID: int>)}
```

#### `block.GetStrength`
获取红石信号的强度，返回指向整数的指针。
```hpl
{func, block.GetStrength(<位置指针: ptr>[, <维度ID: int>])}
```

### 告示牌

#### `block.GetSignBlockText`
获取告示牌上的文字，返回指向字符串的指针。
```hpl
{func, block.GetSignBlockText(<位置指针: ptr>[, <维度ID: int>][, <侧面: int>])}
```

#### `block.GetSignTextStyle`
获取告示牌文字的样式（颜色、照明），返回指向样式映射的指针。
```hpl
{func, block.GetSignTextStyle(<位置指针: ptr>, <维度ID: int>[, <侧面: int>])}
```

#### `block.SetSignBlockText`
设置告示牌文字，返回指向布尔值的指针。
```hpl
{func, block.SetSignBlockText(<玩家ID: string>, <位置指针: ptr>, <文本: string>[, <维度ID: int>][, <侧面: int>])}
```

#### `block.SetSignTextStyle`
设置告示牌文字样式，返回指向布尔值的指针。
```hpl
{func, block.SetSignTextStyle(<位置指针: ptr>, <维度ID: int>, <颜色: int>, <照明: bool>[, <侧面: int>])}
```

### 床

#### `block.GetBedColor`
获取床的颜色，返回指向整数的指针。
```hpl
{func, block.GetBedColor(<玩家ID: string>, <位置指针: ptr>[, <维度ID: int>])}
```

#### `block.SetBedColor`
设置床的颜色，返回指向布尔值的指针。
```hpl
{func, block.SetBedColor(<玩家ID: string>, <位置指针: ptr>, <颜色: int>[, <维度ID: int>])}
```

## 物品模块

### `item.GetAllEnchantsInfo`
获取所有附魔信息，返回指向附魔列表的指针。
```hpl
{func, item.GetAllEnchantsInfo()}
```

### `item.GetItemDurability`
获取物品的当前耐久度，返回指向整数的指针。
```hpl
{func, item.GetItemDurability(<玩家ID: string>, <槽位类型: string>, <槽位索引: int>)}
```

### `item.GetItemInfoByBlockName`
通过方块名称获取对应的物品信息，返回指向物品信息映射的指针。
```hpl
{func, item.GetItemInfoByBlockName(<方块名称: string>[, <附加值: int>][, <是否传统: bool>])}
```

### `item.GetItemMaxDurability`
获取物品的最大耐久度，返回指向整数的指针。
```hpl
{func, item.GetItemMaxDurability(<玩家ID: string>, <槽位类型: string>, <槽位索引: int>, <是否用户数据: bool>)}
```

### `item.SetItemDurability`
设置物品的耐久度，返回指向布尔值的指针。
```hpl
{func, item.SetItemDurability(<玩家ID: string>, <槽位类型: string>, <槽位索引: int>, <耐久度: int>)}
```
