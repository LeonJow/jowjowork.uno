#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unify_inline_css.py — 全站内联 CSS 单/多行格式统一

规则:
  - 若某个 <style> 块为"单行大段"(非空行 <= 1 且字符数 > 120), 则自动展开为多行, 每条规则独立一行。
  - 已是多行的 <style> 块保持不动。
  - 含 @media / @keyframes 的复杂块跳过展开, 仅记录, 避免误伤嵌套结构。
  - 运行后可用 `git diff` 检查改动。

用法:
  python3 scripts/unify_inline_css.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LONG_THRESHOLD = 120  # 字符数超过此值视为需要展开


def fmt_block(css):
    """把单条规则或规则集合展开为多行。"""
    css = css.strip()
    # 先按顶层 '}' 拆分; 对 @media 这种嵌套结构, 若存在 '@' 直接原样返回
    if "@media" in css or "@keyframes" in css:
        return css

    parts = re.split(r"(?<=})\s*", css)
    out_rules = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if "{" not in part:
            # 不是普通规则, 原样保留
            out_rules.append(part)
            continue
        head, tail = part.split("{", 1)
        selector = head.strip()
        body = tail.rstrip("}").strip()
        if not body:
            out_rules.append(selector + " {}")
            continue
        props = [p.strip() for p in body.split(";") if p.strip()]
        if props:
            inner = ";\n  ".join(props) + ";"
        else:
            inner = ""
        out_rules.append(selector + " {\n  " + inner + "\n}")
    return "\n".join(out_rules)


def main():
    files = sorted(
        f for f in os.listdir(ROOT) if f.endswith(".html") and not f.startswith(".")
    )
    changed_blocks = 0
    changed_files = 0

    for f in files:
        path = os.path.join(ROOT, f)
        try:
            with open(path, encoding="utf-8") as fh:
                html = fh.read()
        except Exception:
            continue
        new_html = html
        for m in re.finditer(r"<style[^>]*>(.*?)</style>", html, re.S):
            css = m.group(1)
            non_empty = [l for l in css.split("\n") if l.strip()]
            if len(non_empty) <= 1 and len(css) > LONG_THRESHOLD:
                fmt = fmt_block(css)
                if fmt != css:
                    new_html = new_html.replace(css, fmt, 1)
                    changed_blocks += 1
        if new_html != html:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new_html)
            changed_files += 1

    print(f"统一完成: 涉及 {changed_files} 个文件, {changed_blocks} 个 style 块")
    if changed_blocks == 0:
        print("  当前全站内联 CSS 格式已统一, 无需改动")


if __name__ == "__main__":
    main()
