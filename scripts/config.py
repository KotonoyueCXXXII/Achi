# 事件文件名 → Minecraft ModAPI 事件名
EVENT_MAP = {
    "block_destroy": "ServerPlayerTryDestroyBlockEvent",
    "item_use": "ServerItemUseOnEvent",
    "player_chat": "ServerChatEvent",
    "player_join": "AddServerPlayerEvent",
    "player_leave": "DelServerPlayerEvent",
    "on_command": "GlobalCommandServerEvent",
}

# 表单名 → UI 类型（long / modal / popup）
FORM_TYPE_MAP = {
    "ACHI_HOME": "long",
    "ACHI_HOME_TP": "long",
    "ACHI_HOME_TP_FIXED-A": "long",
    "ACHI_HOME_TP_FIXED-B": "long",
    "ACHI_HOME_LAND": "long",
    "ACHI_HOME_LAND_GET": "long",
    "ACHI_HOME_LAND_SET": "long",
    "ACHI_INFO_AGREEMENT": "long",
    "ACHI_HOME_ROOM": "long",
    "ACHI_HOME_ROOM_AGREEMENT_VIEW": "long",
    "ACHI_HOME_ROOM_LAND_WORKFLOW": "long",
    "ACHI_HOME_ROOM_PLAYER_FLOW": "long",
    "ACHI_HOME_SYSTEM": "long",
    "ACHI_HOME_SYSTEM_PERSONAL": "modal",
    "ACHI_HOME_SYSTEM_GLOBAL": "long",
    "ACHI_HOME_SYSTEM_DEBUG": "modal",
    "ACHI_HOME_TP_ANCHOR": "long",
    "ACHI_HOME_TP_ANCHOR_SET": "long",
    "ACHI_HOME_PLAYER": "long",
    "ACHI_HOME_PLAYER_ACTION": "long",
    "ACHI_HOME_PLAYER_ADMIN": "modal",
    "ACHI_HOME_PLAYER_MESSAGE": "modal",
    "ACHI_INFO_LAND_SET": "popup",
    "ACHI_INFO_LAND_DEL": "popup",
    "ACHI_INFO_RESTORE": "popup",
    "ACHI_INFO_ERROR": "popup",
}
