"""Parse 所有fuc用法➕格式2.txt → generate table-format HPL-API-参考.md."""
import re
from pathlib import Path

SRC = Path(r"C:\Users\Acs\Favorites\mcfunctiom\Achi_func\所有fuc用法➕格式2.txt")
OUT = Path(__file__).parent.parent / "docs" / "HPL-API-参考.md"

MODULE_NAMES = {
    "binascii": "binascii",
    "block": "block",
    "command": "command",
    "datetime_date": "datetime_date",
    "datetime_datetime": "datetime_datetime",
    "datetime_time": "datetime_time",
    "entity": "entity",
    "general": "general",
    "item": "item",
    "json": "json",
    "maps": "maps",
    "math": "math",
    "object": "object",
    "player": "player",
    "random": "random",
    "reflect": "reflect",
    "set": "set",
    "slices": "slices",
    "strings": "strings",
    "struct_time": "struct_time",
    "time": "time",
    "tuple": "tuple",
    "uuid": "uuid",
    "world": "world",
}


def _split_params(text: str) -> list[str]:
    parts = []
    depth = 0
    current = ""
    for ch in text:
        if ch == "<":
            depth += 1
            current += ch
        elif ch == ">":
            depth -= 1
            current += ch
        elif ch == "," and depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        parts.append(current.strip())
    return parts


def infer_return(desc_line: str, full_block: str) -> str:
    combined = desc_line + " " + full_block

    no_ptr = "的指针" not in desc_line

    # Parenthetical type hints
    if "（整数）" in combined or "（直接整数）" in combined:
        return "int"
    if "（浮点数）" in combined or "（浮点）" in combined:
        return "float"
    if "（字符串）" in combined or "（直接字符串）" in combined:
        return "str"

    # bool
    if "返回" in desc_line and "布尔值" in desc_line and no_ptr:
        return "bool"
    if "返回 True" in combined or "返回True" in combined:
        return "bool"

    # int
    if "返回" in desc_line and ("整数" in desc_line or "整型" in desc_line or "整数值" in desc_line) and no_ptr:
        return "int"
    if "类型码" in desc_line:
        return "int"
    if "返回" in desc_line and ("长度" in desc_line or "数量" in desc_line) and no_ptr:
        return "int"
    if "返回" in desc_line and "索引" in desc_line and no_ptr:
        return "int"
    if "返回" in desc_line and ("随机整数" in desc_line or "序数" in desc_line):
        return "int"
    if "返回" in desc_line and re.search(r"（\d+[-–]\d+）", desc_line):
        return "int"

    # float
    if "返回" in desc_line and ("浮点" in desc_line or "浮点数" in desc_line) and no_ptr:
        return "float"

    # str
    if "返回" in desc_line and "字符串" in desc_line and no_ptr:
        return "str"
    if "返回" in desc_line and "字符串表示" in desc_line and no_ptr:
        return "str"
    if "格式化为字符串" in desc_line:
        return "str"
    if "转换为" in desc_line and "字符串" in desc_line and no_ptr:
        return "str"
    if "直接字符串" in desc_line:
        return "str"

    # raw — unwrapped/direct value, not a pointer
    if "直接值" in desc_line or "直接返回" in desc_line:
        return "raw"
    if "返回数字" in desc_line and no_ptr:
        return "raw"
    if "指针指向" in desc_line and ("值" in desc_line or "数据" in desc_line):
        return "raw"

    # ptr — returns a pointer
    if "返回指向" in combined and "的指针" in combined:
        return "ptr"
    if "获取指向" in desc_line and "指针" in desc_line:
        return "ptr"
    if "返回其指针" in combined:
        return "ptr"
    if "创建指向对象的指针" in combined:
        return "ptr"
    if "返回" in desc_line and "指针" in desc_line:
        return "ptr"
    if "//" in full_block and "指针" in full_block:
        return "ptr"
    if "指向" in desc_line and "指针" in desc_line and "返回" not in desc_line:
        return "ptr"

    return "—"


def parse():
    text = SRC.read_text(encoding="utf-8-sig")

    # Split into module sections: —————— name[ 模块] ——————
    sections = re.split(r"(?:^|\n)—————— (.+?)(?: 模块)? ——————\n", text)
    # sections[0] = preamble, then alternating [module_cn, content, ...]

    modules = []

    i = 1
    while i < len(sections) - 1:
        module_cn = sections[i].strip()
        content = sections[i + 1]
        i += 2

        # module_cn is now the English module ID (e.g. "object", "general", "world")
        module_id = module_cn

        apis = []

        # Split into API blocks: each starts with ''name'' on its own logical line
        api_blocks = re.split(r"\n(?=''[a-zA-Z_][\w.]*'')", content)

        for block in api_blocks:
            block = block.strip()
            if not block:
                continue

            # Extract: ''module.method'' description
            name_match = re.match(r"''([a-zA-Z_][\w.]*)''\s*(.*)", block)
            if not name_match:
                continue

            full_name = name_match.group(1)
            desc_line = name_match.group(2).strip()

            # Extract signature: {func, module.method(params)}
            sig_match = re.search(r"\{func,\s*" + re.escape(full_name) + r"\(([^)]*)\)\}", block)
            if sig_match:
                params_str = sig_match.group(1).strip()
            else:
                # Try short name with module prefix: e.g. get_executor → command.get_executor
                sig_match = re.search(r"\{func,\s*([a-zA-Z_][\w.]*\." + re.escape(full_name) + r")\(([^)]*)\)\}", block)
                if sig_match:
                    full_name = sig_match.group(1)
                    params_str = sig_match.group(2).strip()
                else:
                    params_str = ""

            # Build simplified signature string for display
            params = []
            if params_str:
                for p in _split_params(params_str):
                    p = p.strip()
                    inner = p.strip("[] ")
                    m = re.match(r"<([^:]+)(?::\s*(.+?))?>$", inner)
                    if m:
                        opt = "?" if p.strip().startswith("[") else ""
                        params.append(f"{m.group(1).strip()}{opt}: {m.group(2).strip() if m.group(2) else 'any'}")

            sig_display = f"{{func, {full_name}({', '.join(params)})}}"

            ret = infer_return(desc_line, block)

            # Clean description
            desc = desc_line if desc_line else ""
            # Remove trailing newlines/whitespace for table cell
            desc = desc.replace("\n", " ").strip()

            short = full_name.split(".", 1)[1] if "." in full_name else full_name

            apis.append({
                "short": short,
                "desc": desc,
                "sig": sig_display,
                "ret": ret,
            })

        modules.append({"id": module_id, "name": MODULE_NAMES.get(module_id, module_cn + " 模块"), "apis": apis})

    return modules


def build(modules):
    lines = [
        "# HPL API 参考",
        "",
        "> 基于 NetEase Minecraft HPL 脚本系统。所有 API 调用使用 `{func, 模块.函数(参数...)}` 格式。",
        "> 自动生成自 `所有fuc用法➕格式2.txt`。",
        "",
        "## 模块跳转",
        "",
    ]

    for mod in modules:
        lines.append(f'- [{mod["name"]}](#{mod["id"]})')

    lines.append("")
    lines.append("---")
    lines.append("")

    for mod in modules:
        lines.append(f'<a id="{mod["id"]}"></a>')
        lines.append("")
        lines.append(f'## {mod["name"]}')
        lines.append("")
        lines.append("| 函数 | 描述 | 签名 | 返回值 |")
        lines.append("|---|---|---|---|")

        for api in mod["apis"]:
            sig_html = api["sig"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            lines.append(f'| `{api["short"]}` | {api["desc"]} | <code>{sig_html}</code> | `{api["ret"]}` |')

        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines) + "\n"


def main():
    modules = parse()
    total = sum(len(m["apis"]) for m in modules)
    output = build(modules)
    OUT.write_text(output, encoding="utf-8")
    print(f"Done: {total} APIs across {len(modules)} modules → {OUT}")
    for mod in modules:
        print(f"  {mod['id']}: {len(mod['apis'])} functions")


if __name__ == "__main__":
    main()
