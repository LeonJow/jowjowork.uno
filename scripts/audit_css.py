#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_css.py — 全站内联 CSS 一致性审计

扫描全部 *.html 的 <style>...</style> 块，输出:
  - 每个 style 块的字数、行数、是否单行大段
  - 哪些文件含 .nav-search / .top-nav
  - 单/多行混用统计

用法:
  python3 scripts/audit_css.py
"""
import os
import re
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith(".html") and not f.startswith("."))
    rows = []
    single_long_blocks = []
    nav_search_issues = []

    for f in files:
        path = os.path.join(ROOT, f)
        try:
            with open(path, encoding="utf-8") as fh:
                html = fh.read()
        except Exception as e:
            continue
        styles = re.findall(r"<style[^>]*>(.*?)</style>", html, re.S)
        for idx, css in enumerate(styles, 1):
            raw_lines = css.split("\n")
            non_empty = [l for l in raw_lines if l.strip()]
            # "单行大段": 非空行 <=1 且字符数 >120
            single_long = len(non_empty) <= 1 and len(css) > 120
            has_nav_search = ".nav-search" in css
            has_top_nav = ".top-nav" in css
            has_position_abs = "position:absolute" in css
            row = {
                "file": f,
                "block": idx,
                "chars": len(css),
                "lines": len(raw_lines),
                "single_long": single_long,
                "has_nav_search": has_nav_search,
                "has_top_nav": has_top_nav,
                "position_absolute": has_position_abs,
            }
            rows.append(row)
            if single_long:
                single_long_blocks.append(row)
            if has_nav_search:
                # 检查 nav-search 段是否单行：取 .nav-search 所在行数
                # 简化: 看 .nav-search 附近有没有分号+换行
                snippet = css[css.find(".nav-search"):css.find(".nav-search")+300]
                if snippet and "\n" not in snippet:
                    nav_search_issues.append({"file": f, "issue": "nav-search 段为单行格式"})

    summary = {
        "total_files": len(files),
        "total_style_blocks": len(rows),
        "single_long_blocks": len(single_long_blocks),
        "files_with_position_absolute": len({r["file"] for r in rows if r["position_absolute"]}),
        "files_with_top_nav": len({r["file"] for r in rows if r["has_top_nav"]}),
        "files_with_nav_search": len({r["file"] for r in rows if r["has_nav_search"]}),
        "nav_search_format_issues": len(nav_search_issues),
    }

    report_path = os.path.join(ROOT, "css-audit-report.json")
    with open(report_path, "w", encoding="utf-8") as fh:
        json.dump({
            "summary": summary,
            "single_long_blocks": single_long_blocks,
            "nav_search_format_issues": nav_search_issues,
            "details": rows,
        }, fh, ensure_ascii=False, indent=2)

    print("=== 全站 CSS 一致性审计报告 ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
    if single_long_blocks:
        print("\n[单行大段 style 块] 建议展开多行:")
        for r in single_long_blocks[:10]:
            print(f"  - {r['file']} 块{r['block']} ({r['chars']} 字符, {r['lines']} 行)")
    if nav_search_issues:
        print("\n[nav-search 格式不一致]:")
        for it in nav_search_issues[:10]:
            print(f"  - {it['file']}: {it['issue']}")
    print(f"\n详细报告已保存: {report_path}")

if __name__ == "__main__":
    main()
