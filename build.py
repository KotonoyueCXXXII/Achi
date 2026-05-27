import os
import re
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE, 'Achi.mcfunction')

from scripts.config import EVENT_MAP, FORM_TYPE_MAP

# 这些事件在安装完成后才注册，避免干扰安装过程
DEFERRED_EVENTS = {'on_command'}


def compress(text):
    """Remove empty lines, then compress double-quoted strings (handle escaped quotes)."""
    lines = text.split('\n')
    non_empty = [l for l in lines if l.strip() != '']
    text = '\n'.join(non_empty)

    def compress_body(body):
        body_lines = body.splitlines()
        stripped = [l.strip() for l in body_lines if l.strip() and not l.strip().startswith('//')]
        return ' | '.join(stripped)

    def repl(m):
        inner = m.group(1)
        return '"' + compress_body(inner) + '"'

    return re.sub(r'"((?:[^"\\]|\\.)*)"', repl, text)


def file_path_to_form_name(rel_path):
    """Derive form name from file path relative to 04_forms/.
    E.g. ACHI/HOME/_.hpl -> ACHI_HOME (sentinel _ means use parent dir name).
    E.g. ACHI/HOME/TP/FIXED-A.hpl -> ACHI_HOME_TP_FIXED-A.
    """
    no_prefix = rel_path.replace('04_forms' + os.sep, '', 1)
    no_suffix = no_prefix[:-4] if no_prefix.endswith('.hpl') else no_prefix
    parts = no_suffix.replace(os.sep, '/').split('/')
    # filter out sentinel _ segments
    filtered = [p for p in parts if p != '_']
    return '_'.join(filtered)


def strip_comments(text):
    """Remove comment lines (starting with //) outside multi-line strings."""
    lines = text.split('\n')
    stripped = []
    inside = False
    for line in lines:
        dq = line.replace('\\"', '')
        if dq.count('"') % 2 == 1:
            inside = not inside
        if inside or not line.strip().startswith('//'):
            stripped.append(line)
    return '\n'.join(stripped)


def collect_files(subdir):
    """Return list of .hpl file paths under subdir, sorted alphabetically."""
    dirpath = os.path.join(BASE, subdir)
    files = []
    for root, dirs, filenames in os.walk(dirpath):
        for f in filenames:
            if f.endswith('.hpl'):
                files.append(os.path.join(root, f))
    files.sort()
    return files


def process_init():
    """01_init: install message + init functions registered and called at import time.
    Init functions are callable via 'init/<name>' (e.g. init/main).
    """
    parts = []

    # 编译计数器
    counter_file = os.path.join(BASE, '.build_count')
    try:
        with open(counter_file, 'r') as f:
            count = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        count = 0
    count += 1
    with open(counter_file, 'w') as f:
        f.write(str(count))

    # 统计
    init_count = len(collect_files('01_init'))
    event_count = len(collect_files('02_events'))
    func_count = len(collect_files('03_functions'))
    form_count = len(collect_files('04_forms'))
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 安装信息（# 注释占首行避免导入端首行不执行的 bug，多段合并为单条 tellraw）
    msg = (
        '§e--------------------\\n'
        '§f正在安装 §aACHI §f脚本文件……\\n'
        f'§7编译次序: §f{count}  §7编译时刻: §f{now}\\n'
        f'§7初始化: §f{init_count}  §7事件: §f{event_count}  §7函数: §f{func_count}  §7表单: §f{form_count}\\n'
        '§e--------------------'
    )
    parts.append(f'# Achi 地皮管理系统 - 编译 #{count} @ {now}')
    parts.append(f'systemevent destroy on_command')
    parts.append(f'tellraw @a {{"rawtext":[{{"text":"{msg}"}}]}}')

    # 初始化函数注册（调用推迟到 process_init_call，在所有注册完成后）
    init_dir = os.path.join(BASE, '01_init')
    for f in collect_files('01_init'):
        rel = os.path.relpath(f, init_dir)
        name = 'init/' + (rel[:-4].replace(os.sep, '/') if rel.endswith('.hpl') else rel.replace(os.sep, '/'))
        with open(f, 'r', encoding='utf-8-sig') as fh:
            body = strip_comments(fh.read().strip())
        compressed = compress(body)
        parts.append(f'customfunction remove "{name}"')
        parts.append(f'customfunction add "{name}" "{compressed}"')
    return '\n'.join(parts)


def process_init_call():
    """Call init functions — must run last, after all registrations."""
    parts = []
    init_dir = os.path.join(BASE, '01_init')
    for f in collect_files('01_init'):
        rel = os.path.relpath(f, init_dir)
        name = 'init/' + (rel[:-4].replace(os.sep, '/') if rel.endswith('.hpl') else rel.replace(os.sep, '/'))
        parts.append(f'customfunction call @p ~ ~ ~ "{name}"')
    return '\n'.join(parts)


def process_events():
    """02_events: code body -> systemevent destroy + listen wrappers.
    Files listed in DEFERRED_EVENTS are skipped — they are registered last."""
    parts = []
    for f in collect_files('02_events'):
        name = os.path.splitext(os.path.basename(f))[0]
        if name in DEFERRED_EVENTS:
            continue
        mc_event = EVENT_MAP.get(name)
        if not mc_event:
            raise KeyError(f"Unknown event '{name}' — add to EVENT_MAP")
        with open(f, 'r', encoding='utf-8-sig') as fh:
            body = strip_comments(fh.read().strip())
        compressed = compress(body)
        parts.append(f'systemevent destroy {name}')
        parts.append(f'systemevent listen {mc_event} {name} "{compressed}"')
    return '\n'.join(parts)


def process_deferred_events():
    """Events that must be registered last, after all other install steps."""
    parts = []
    for f in collect_files('02_events'):
        name = os.path.splitext(os.path.basename(f))[0]
        if name not in DEFERRED_EVENTS:
            continue
        mc_event = EVENT_MAP.get(name)
        if not mc_event:
            raise KeyError(f"Unknown event '{name}' — add to EVENT_MAP")
        with open(f, 'r', encoding='utf-8-sig') as fh:
            body = strip_comments(fh.read().strip())
        compressed = compress(body)
        parts.append(f'systemevent destroy {name}')
        parts.append(f'systemevent listen {mc_event} {name} "{compressed}"')
    return '\n'.join(parts)


def process_functions():
    """03_functions: code body -> customfunction remove + add wrappers.
    Function name = relative path from 03_functions/ minus .hpl."""
    parts = []
    func_dir = os.path.join(BASE, '03_functions')
    for f in collect_files('03_functions'):
        rel = os.path.relpath(f, func_dir)
        name = rel[:-4].replace(os.sep, '/') if rel.endswith('.hpl') else rel.replace(os.sep, '/')
        with open(f, 'r', encoding='utf-8-sig') as fh:
            body = strip_comments(fh.read().strip())
        compressed = compress(body)
        parts.append(f'customfunction remove "{name}"')
        parts.append(f'customfunction add "{name}" "{compressed}"')
    return '\n'.join(parts)


def process_forms():
    """04_forms: code body -> customform remove + add + body + save wrappers.
    Form name derived from file path. Type from FORM_TYPE_MAP."""
    FORM_EDIT_PREFIX = {
        'long': 'editlongform',
        'modal': 'editmodalform',
        'popup': 'editpopupform',
    }
    parts = []
    forms_dir = os.path.join(BASE, '04_forms')
    for f in collect_files('04_forms'):
        rel = os.path.relpath(f, BASE)
        form_name = file_path_to_form_name(rel)
        form_type = FORM_TYPE_MAP.get(form_name)
        if not form_type:
            raise KeyError(f"Unknown form '{form_name}' — add to FORM_TYPE_MAP")
        with open(f, 'r', encoding='utf-8-sig') as fh:
            body = strip_comments(fh.read().strip())
            body = body.replace('&(formName)', form_name)
        edit_prefix = FORM_EDIT_PREFIX[form_type]
        if not re.search(rf'^{edit_prefix} {form_name} title ', body, re.MULTILINE):
            title_line = f'{edit_prefix} {form_name} title "return \'{form_name}\'"\n'
            body = title_line + body
        compressed = compress(body)
        parts.append(f'customform remove {form_name}')
        parts.append(f'customform add {form_name} {form_type}')
        parts.append(compressed)
        parts.append(f'customform save {form_name}')
    return '\n'.join(parts)


def main():
    sections = []
    sections.append(process_init())
    sections.append(process_events())
    sections.append(process_functions())
    sections.append(process_forms())
    sections.append(process_init_call())
    sections.append(process_deferred_events())

    output = '\n'.join(sections)
    output = compress(output)

    with open(OUTPUT, 'w', encoding='utf-8-sig') as fh:
        fh.write(output)

    print(f'Built: {OUTPUT}')
    print(f'Size: {len(output)} chars, {len(output.splitlines())} lines')


if __name__ == '__main__':
    main()
