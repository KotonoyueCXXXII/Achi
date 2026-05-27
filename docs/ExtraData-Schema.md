# ExtraData 域数据存储说明

本文档是 ExtraData 域结构的**权威参考**——所有域定义、字段结构、错误码、访问函数签名均以此文档为准。

- 编码规范（如何写代码）→ [CLAUDE.md](../CLAUDE.md)
- 系统架构与构建管线 → [ARCHITECTURE.md](ARCHITECTURE.md)

## 总览

所有域均存储在 level 实体的 ExtraData 上，通过 `worldData/*` 和 `queue/*` 系列函数访问。底层调用 `entity.GetExtraData(worldId, domain)` 获取域对应的顶层 map 指针。

## 域速查

| 域 | 类型 | 结构 | 说明 |
|---|---|---|---|
| `data.player.archive` | data | 三层（map） | 玩家账户数据，key=playerId |
| `data.land.archive` | data | 三层（map） | 地皮注册表，key=landIndex |
| `data.main` | data | 两层 | 系统全局状态（nextUID, schedule） |
| `temp.player.index` | temp | 两层 | 在线玩家索引，key=slot→playerId |
| `temp.land.using` | temp | 两层 | 活跃地皮绑定，key=playerIndex→landIndex |
| `temp.land.setting` | temp | 三层（map） | 地皮创建进行中 |
| `temp.land.deleting` | temp | 两层 | 地皮删除目标 |
| `temp.menu.settingPlayer` | temp | 两层 | 选中的目标玩家 |
| `temp.menu.anchorSlot` | temp | 两层 | 选中的锚点槽位 |
| `temp.menu.playerIndexSnapshot` | temp | 三层（map） | 玩家列表快照 |
| `temp.menu.errorCode` | temp | 两层 | 错误码 |
| `queue.land.init` | queue | 三层（map，FIFO） | 地皮初始化队列 |
| `queue.land.backup` | queue | 三层（map，FIFO） | 地皮备份队列 |

## 域命名规范

所有域遵循三段式命名：**类型**（数据生命周期）`.` **模块**（所属功能模块）`.` **属性**（具体用途）。

| 类型 | 含义 |
|---|---|
| `data` | 持久数据，需跨会话保留 |
| `temp` | 临时状态，会话内有效 |
| `queue` | 任务队列，异步处理 |

模块标识用功能名（`player`、`land`、`menu` 等），属性用动词或名词（`archive`、`using`、`errorCode` 等）。新增域时在此文档中追加对应章节。

### 访问函数

以下为权威版本——所有访问函数的签名和行为规范。

| 函数 | key 类型 | 返回值 | 是否需 finalise |
|---|---|---|---|
| `data/mapGet` | 值（int/string） | 值或 `-2147483648` | 否 |
| `data/mapSet` | 值（int/string） | — | 否 |
| `data/mapExist` | 值（int/string） | bool | 否 |
| `data/mapDel` | 值（int/string） | — | 否 |
| `data/mapKeyOf` | — | 匹配的 key 或 `-2147483648` | 否 |
| `data/ptrMapGet` | 指针（`object.ref(key)`） | pinned 指针或 `-2147483648` | **是** |
| `data/ptrMapSet` | 指针（`object.ref(key)`） | — | 参数指针需 finalise |
| `data/ptrMapDel` | 指针（`object.ref(key)`） | — | 否 |
| `queue/push` | — | 槽位索引 | 否 |
| `queue/pop` | — | — | 否 |
| `queue/peek` | — | pinned 指针或 `-2147483648` | 否 |

---

## 1. `data.player.archive` — 玩家账户数据

**key 类型：** `playerId`（string，实体 UUID）

**value 类型：** map 指针

**value 结构：**

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `uid` | int | — | 全局唯一玩家 ID，注册时从 `data.main.nextUID` 分配 |
| `privilegeLevel` | int | `1` | 权限等级：0=访客, 1=成员, 2=会员, 3=管理员 |
| `saveSizeIndex` | int | — | 备份地皮的大小索引（0=20×20, 1=30×30, 2=40×40）。仅在成功备份后存在，地皮解绑时清除为 `-2147483648`。用于登录时判断是否需要恢复 |
| `anchors` | map 指针 | 懒创建 | 个人锚点。key 为 int `1`~`9`，value 为 `(x, y, z)` 坐标三元组 |
| `allowTPToMe` | bool | `False` | 是否允许其他玩家通过系统传送至自己。注册时初始化为 `False`，通过个人设置修改 |
| `playerName` | string | — | 玩家显示名称，注册时写入 |

**读：** `AGREEMENT.hpl`, `player_join.hpl`, `player_leave.hpl`, `HOME/_.hpl`, `HOME/LAND/_.hpl`, `RESTORE.hpl`, `ui/getAnchorButtonText.hpl`, `ANCHOR/SET.hpl`, `block_destroy.hpl`, `item_use.hpl`, `ADMIN.hpl`, `ACTION.hpl`, `MESSAGE.hpl`, `entry/debug.hpl`, `land/processBackup.hpl`, `PERSONAL.hpl`

**写：** `AGREEMENT.hpl`（创建账户）, `ANCHOR/SET.hpl`（锚点读写）, `ELEVATE.hpl`（提权）, `ADMIN.hpl`（改权）, `ACTION.hpl`（解绑清除 saveSizeIndex）, `land/processBackup.hpl`（备份完成写入 saveSizeIndex）, `PERSONAL.hpl`（allowTPToMe）

---

## 2. `data.land.archive` — 地皮注册表

**key 类型：** `landIndex`（int，从 0 开始的连续序号）

**value 类型：** map 指针

**value 结构：**

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `anchor_x` | int | — | 地皮西北角 X 坐标 |
| `anchor_y` | int | — | 地皮地表高度 Y |
| `anchor_z` | int | — | 地皮西北角 Z 坐标 |
| `sizeIndex` | int | — | 地皮大小：0=20×20, 1=30×30, 2=40×40（边长 = `20 + sizeIndex * 10 - 1`） |

**删除时的 swap-and-pop：** 删除地皮时，将最后一条记录移至被删位置。

**读：** `HOME/LAND/_.hpl`, `GET.hpl`, `SET.hpl`, `DEL.hpl`, `RESTORE.hpl`, `land/getFreeIndex.hpl`, `land/processBackup.hpl`

**写：** `SET.hpl`（创建）, `DEL.hpl`（删除并重排）, `GET.hpl`（绑定后标记 `landIndex`）

---

## 3. `data.main` — 系统全局状态

**key 类型：** 字符串字面量（`"nextUID"`, `"schedule"`）

**value 类型：** int（标量值）

| key | 类型 | 说明 |
|---|---|---|
| `nextUID` | int | 自增玩家 UID 计数器，注册新玩家时 `+1` |
| `schedule` | int | tick 计数器，`main` 每 tick `+1`。每 5 tick 触发备份+地皮初始化处理，每 600 tick 保存 ExtraData 并发送 speed form style |

**读：** `AGREEMENT.hpl`（nextUID）, `main.hpl`（schedule）

**写：** `AGREEMENT.hpl`（自增 nextUID）, `main.hpl`（自增 schedule）

---

## 4. `temp.player.index` — 在线玩家索引

**key 类型：** `slot`（int，0–39，共 40 个槽位）

**value 类型：** `playerId`（string）— 纯字符串，非指针

**用途：** 双向映射：`mapGet(slot)` → playerId（正向）、`mapKeyOf(domain, playerId)` → slot（反向）。

**生命周期：** 服务器空载时（最后一名玩家离开）整体清除。玩家离开时单独删除对应条目。

**读：** `player_join.hpl`, `player_leave.hpl`, `ui/createPlayerSnapshot.hpl`, `ui/validatePlayerSelection.hpl`, `ui/getSnapshotName.hpl`, `PLAYER/_.hpl`

**写：** `player_join.hpl`（分配槽位）, `player_leave.hpl`（释放槽位）

---

## 5. `temp.land.using` — 活跃地皮绑定

**key 类型：** `playerIndex`（int，玩家的槽位 0–39）

**value 类型：** `landIndex`（int）— `data.land.archive` 中对应地皮的索引

**生命周期：** 服务器空载时整体清除。玩家离开或地皮解绑/删除时单独删除。

**读：** `block_destroy.hpl`, `player_leave.hpl`, `item_use.hpl`, `player_join.hpl`, `FreeLandIndex.hpl`, `HOME/_.hpl`, `HOME/LAND/_.hpl`, `GET.hpl`, `ACTION.hpl`, `DEL.hpl`

**写：** `RESTORE.hpl`（绑定）, `GET.hpl`（绑定）, `player_leave.hpl`（解绑）, `ACTION.hpl`（解绑）, `DEL.hpl`（解绑）, `player_join.hpl`（空服清除）

---

## 6. `temp.land.setting` — 地皮创建进行中

**key 类型：** `playerIndex`（int，玩家的槽位）

**value 类型：** map 指针

**value 结构：**

| 字段 | 类型 | 说明 |
|---|---|---|
| `sizeIndex` | int | 选择的地皮大小（0/1/2）。在 `ACHI_HOME_LAND_SET` 表单中设置 |
| `anchor_x` | int | 西北角 X。`item_use` 事件中玩家放置方块时写入 |
| `anchor_y` | int | 地表 Y。`item_use` 事件中写入 |
| `anchor_z` | int | 西北角 Z。`item_use` 事件中写入 |

**生命周期：** `ACHI_HOME_LAND_SET` 创建（仅含 sizeIndex），`item_use` 补全锚点坐标，`ACHI_INFO_LAND_SET` 读取并最终创建地皮。

**读/写：** `HOME/LAND/SET.hpl`, `item_use.hpl`, `INFO/LAND/SET.hpl`

---

## 7. `temp.land.deleting` — 地皮删除目标

**key 类型：** `playerIndex`（int，玩家的槽位）

**value 类型：** `landIndex`（int）— 待删除地皮的索引。若玩家脚下未找到地皮则为 `-2147483648`。

**读：** `INFO/LAND/DEL.hpl`

**写：** `HOME/LAND/_.hpl`（遍历所有地皮，找到玩家脚下对应的 landIndex）

---

## 8. `temp.menu.settingPlayer` — 选中的目标玩家

**key 类型：** `playerIndex`（int，操作者的槽位）

**value 类型：** `targetPlayerIndex`（int）— 目标玩家在 `temp.player.index` 中的槽位

**读：** `ui/validatePlayerSelection.hpl`, `PLAYER/ACTION.hpl`, `PLAYER/ADMIN.hpl`

**写：** `PLAYER/_.hpl`（从 40 槽位玩家列表中选择目标）

---

## 9. `temp.menu.anchorSlot` — 选中的锚点槽位

**key 类型：** `playerIndex`（int，操作者的槽位）

**value 类型：** `slot`（int，1–9）— 锚点编号

**读：** `ANCHOR/SET.hpl`（content 展示 + 三个操作分支）

**写：** `ANCHOR/_.hpl`（从 9 个锚点槽位中选择 `selectedIndex + 1`）

---

## 10. `temp.menu.playerIndexSnapshot` — 玩家列表快照

**key 类型：** `playerIndex`（int，操作者的槽位）

**value 类型：** map 指针——`temp.player.index` 的深拷贝（`reflect.deepcopy`）

**用途：** 玩家打开交互菜单时的在线列表冻结副本，用于 `ui/validatePlayerSelection` 检测目标玩家槽位是否在菜单打开后被其他玩家占用。

**读：** `ui/validatePlayerSelection.hpl`

**写：** `ui/createPlayerSnapshot.hpl`

---

## 11. `temp.menu.errorCode` — 错误码

以下为权威错误码表。`entry/showError` 和 CLAUDE.md 均引用此处。

**key 类型：** 固定字符串 `"code"`

**value 类型：** int（1–17）

**错误码对照表：**

| 码 | 含义 |
|---|---|
| 1 | 未选择目标 |
| 2 | 目标玩家状态已变更，请返回重试 |
| 3 | 快照已失效，请重新打开玩家列表 |
| 4 | 所选槽位无玩家 |
| 5 | 权限不足 |
| 6 | 暂无可用地皮，请联系管理员添加 |
| 7 | 你已拥有地皮，无法再次获取 |
| 8 | 目标玩家尚未注册 |
| 9 | 请先注册后再使用此功能 |
| 10 | 地皮初始化超时，请稍后重试 |
| 11 | 目标玩家未获取地皮 |
| 12 | 该锚点尚未设置坐标 |
| 13 | 未选择锚点槽位 |
| 14 | 没有在你脚下的位置找到地皮 |
| 15 | 密码错误 |
| 16 | 该地皮正在备份中，请稍后再试 |
| 17 | 目标玩家未开放传送权限 |
| 18 | 指定的数据域不存在 |

**读：** `INFO/ERROR.hpl`

**写：** `entry/showError.hpl`（1–17），`ACTION.hpl`（17）

**写：** `entry/showError.hpl`

---

## 12. `queue.land.init` — 地皮初始化队列

**存储方式：** 手动 FIFO 队列。写入端搜索首个空槽位（0–39）并 `ptr_mapSet`；处理端读取槽位 0 并 `queue/pop`（使后续条目自动前移）。

**key 类型：** int（槽位 0–39）

**value 类型：** map 指针

**value 结构：**

| 字段 | 类型 | 说明 |
|---|---|---|
| `landIndex` | int | 要初始化的地皮索引 |
| `sizeIndex` | int | 地皮大小（0/1/2） |
| `playerId` | string | 所有者 ID（用于 `world.SetCommand` 上下文） |
| `anchor_x` | int | 西北角 X |
| `anchor_y` | int | 地表高度 Y |
| `anchor_z` | int | 西北角 Z |
| `retryCount` | int | 倒计时，起始 5。每周期减 1，归零则超时弹出 |

**处理流程：** `land/processInit.hpl` 每 5 tick 查看槽位 0。若 `retryCount` 归零则弹出放弃；否则递减并检查区块加载，加载完成后初始化地皮（清空→草皮→绿玻璃角标→传送玩家）并弹出。

**读：** `land/processInit.hpl`

**写：** `HOME/LAND/GET.hpl`

---

## 13. `queue.land.backup` — 地皮备份队列

**存储方式：** 标准 FIFO 队列，使用 `queue/push` / `queue/pop` / `queue/peek`。

**key 类型：** int（槽位 0–63，由 `queue/push` 自动分配）

**value 类型：** map 指针

**value 结构：**

| 字段 | 类型 | 阶段 | 说明 |
|---|---|---|---|
| `playerUID` | int | 创建时 | 玩家 UID，用于 `land/squareSpiralFill` 计算备份坐标 |
| `playerId` | string | 创建时 | 所有者 ID（离线恢复时为 `-2147483648`） |
| `mode` | int | 创建时 | 0=存档（地皮→备份区），1=恢复（备份区→地皮） |
| `landIndex` | int | 创建时 | 地皮索引 |
| `state` | int | 创建时 | 0=准备（计算坐标、创建 tickingarea），1=执行（等待区块、clone） |
| `retry` | int | 创建时 | 重试计数，起始 0。state 1 中递增，最多 12 次（约 3 秒） |
| `src_x` | int | state 0 | clone 源 X |
| `src_z` | int | state 0 | clone 源 Z |
| `dst_x` | int | state 0 | clone 目标 X |
| `dst_z` | int | state 0 | clone 目标 Z |
| `sizeIndex` | int | state 0 | 地皮大小（从地皮档案复制） |

**处理流程（`land/processBackup.hpl` 状态机）：**
- **State 0（准备）：** 读取 landIndex → 获取地皮数据 → `land/squareSpiralFill(playerUID)` 计算螺旋偏移 → 坐标偏移基值 `(1048576, 1048576)` → 在源/目标创建 tickingarea → 写入 `src_*`/`dst_*`/`sizeIndex` → 进入 state 1
- **State 1（执行）：** `retry++` → 等待区块加载 → `land/cloneLand` 纵向分段 clone → 成功后清理 tickingarea（mode 0 同时写 `saveSizeIndex` 到账户） → `queue/pop`

**读：** `land/processBackup.hpl`

**写：** `player_leave.hpl`（mode=0 存档）, `player_join.hpl`（空服启动时批量 mode=0）, `RESTORE.hpl`（mode=1 恢复）

---

## 数据流总览

从玩家视角的地皮生命周期流程见 [ARCHITECTURE.md#地皮生命周期](ARCHITECTURE.md#地皮生命周期)。

```
玩家加入
  └─ temp.player.index[slot] = playerId
  └─ 若服务器原为空：
       ├─ 遍历 temp.land.using → 逐个 queue.land.backup.push(mode=0)
       ├─ CleanExtraData temp.player.index
       └─ CleanExtraData temp.land.using

玩家注册
  └─ data.main.nextUID++
  └─ data.player.archive[playerId] = {uid, privilegeLevel=1}

玩家获取地皮
  └─ FreeLandIndex 扫描 data.land.archive vs temp.land.using
  └─ data.land.archive[freeIndex].landIndex = freeIndex
  └─ temp.land.using[playerIndex] = landIndex
  └─ queue.land.init 写入任务

地皮初始化（每 5 tick）
  └─ queue.land.init[0]: 检查区块 → land/initLand → queue/pop

地皮备份（每 5 tick）
  └─ queue.land.backup[0]:
       state 0: 计算螺旋坐标 → 创建 tickingarea → state 1
       state 1: 等待区块 → land/cloneLand → account.saveSizeIndex = sizeIndex → queue/pop

玩家离开
  └─ queue.land.backup.push(mode=0)
  └─ temp.land.using.del(slot)
  └─ temp.player.index.del(slot)

玩家返回（有 saveSizeIndex）
  └─ FreeLandIndex 找到空闲地皮
  └─ temp.land.using[playerIndex] = landIndex
  └─ queue.land.backup.push(mode=1)
```
