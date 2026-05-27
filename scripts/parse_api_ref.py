"""Parse HPL API reference file and extract structured function signatures."""
import re
import json
import os

REF_PATH = r"C:\Users\Acs\Favorites\mcfunctiom\Achi_func\所有fuc用法➕格式2.txt"
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "api_signatures.json")


def parse_ref(filepath: str) -> list[dict]:
    with open(filepath, "r", encoding="utf-8-sig") as f:
        text = f.read()

    # Split into module sections
    # Each section starts with —————— module 模块 ——————
    sections = re.split(r"(?:^|\n)—————— (.+?) 模块 ——————\n", text)
    # sections[0] = preamble (discard), then alternating [module_cn_name, module_content, ...]

    all_apis = []

    i = 1
    while i < len(sections) - 1:
        module_cn = sections[i].strip()
        content = sections[i + 1]
        i += 2

        # Extract individual API definitions
        # Format: ''module.method'' description line(s)
        #          {func, module.method(params)}
        api_blocks = re.split(r"\n(?=''[a-zA-Z_][\w.]*'')", content)

        for block in api_blocks:
            block = block.strip()
            if not block:
                continue

            # Extract method name: ''module.method'' or ''method'' (short form)
            name_match = re.match(r"''([a-zA-Z_][\w.]*)''\s*(.*)", block)
            if not name_match:
                continue

            short_name = name_match.group(1)
            desc_line = name_match.group(2).strip()

            # Extract the function call pattern: {func, module.method(params)}
            # First try with the short name
            call_match = re.search(
                r"\{func,\s*([a-zA-Z_][\w.]*\." + re.escape(short_name) + r")\(([^)]*)\)\}",
                block,
            )
            if call_match:
                full_name = call_match.group(1)
                params_str = call_match.group(2).strip()
            else:
                # Try with full dotted name (short_name already contains dot)
                call_match = re.search(
                    r"\{func,\s*" + re.escape(short_name) + r"\(([^)]*)\)\}",
                    block,
                )
                full_name = short_name
                params_str = call_match.group(1).strip() if call_match else ""

            # Parse individual parameters: <name: type> or [<name: type>]
            params = []
            if params_str:
                # Split by comma but respect nested <>
                param_parts = _split_params(params_str)
                for p in param_parts:
                    p = p.strip()
                    # Extract name: type from <name: type> or [<name: type>]
                    inner = p.strip("[] ")
                    m = re.match(r"<([^:]+)(?::\s*(.+?))?>$", inner)
                    if m:
                        params.append({
                            "name": m.group(1).strip(),
                            "type": m.group(2).strip() if m.group(2) else "any",
                            "optional": p.strip().startswith("["),
                        })

            # Parse return type from description line
            ret_match = re.search(r"返回(?:指向)?([^。，,\n]+?)(?:的指针|。|$)", desc_line)
            return_type = "any"
            if "返回布尔值" in desc_line or "返回 True" in desc_line:
                return_type = "bool"
            elif "返回整数" in desc_line or "返回整型" in desc_line:
                return_type = "int"
            elif "返回浮点" in desc_line:
                return_type = "float"
            elif "返回字符串" in desc_line:
                return_type = "str"
            elif "返回指向" in desc_line and "的指针" in desc_line:
                return_type = "ptr"
            elif "返回布尔值" in block:
                return_type = "bool"

            # Build signature label
            param_labels = []
            for p in params:
                opt = "?" if p["optional"] else ""
                param_labels.append(f"{p['name']}{opt}: {p['type']}")
            label = f"{full_name}({', '.join(param_labels)})"

            # Extract description
            desc = desc_line.strip() if desc_line else ""
            if len(desc) > 200:
                desc = desc[:200]

            all_apis.append({
                "name": full_name,
                "label": label,
                "params": [f"{p['name']}: {p['type']}" + ("?" if p["optional"] else "") for p in params],
                "description": desc,
                "returnType": return_type,
            })

    return all_apis


def _split_params(text: str) -> list[str]:
    """Split by top-level commas respecting nested <>."""
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


def main():
    apis = parse_ref(REF_PATH)
    # Group by module
    by_module = {}
    for api in apis:
        mod = api["name"].split(".")[0]
        by_module.setdefault(mod, []).append(api)

    output = {
        "_total": len(apis),
        "_modules": sorted(by_module.keys()),
        "signatures": {api["name"]: {k: v for k, v in api.items() if k != "name"} for api in apis},
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Extracted {len(apis)} APIs across {len(by_module)} modules")
    print(f"Written to {OUT_PATH}")
    for mod in sorted(by_module.keys()):
        print(f"  {mod}: {len(by_module[mod])} functions")


if __name__ == "__main__":
    main()
