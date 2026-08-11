#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_search_index.py — 搜索索引生成 / 增强工具

用法:
  python3 scripts/build_search_index.py             # 增强模式: 以现有 search-index.json 为准, 补拼音字段 + 校验 url
  python3 scripts/build_search_index.py --from-html # 全扫描模式: 重新扫描全站 HTML 生成索引(含拼音)

说明:
  - 增强模式保留手工撰写的 title/desc/tags(质量更高), 仅自动补 py(拼音) 字段并校验链接有效性。
  - 全扫描模式按文件名前缀推断栏目(cat), 从 <title>/<meta> 提取信息, 适合从零生成。
  - 拼音搜索: 输入 lidan / ld 也能命中"李诞"。
"""
import json
import os
import re
import sys
from pypinyin import lazy_pinyin, Style

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, "search-index.json")

# 文件名前缀 -> 栏目
CAT_MAP = [
    ("ai-post", "AI经验"),
    ("ai-sharing", "AI经验"),
    ("skills-post", "SKILLS"),
    ("skills", "SKILLS"),
    ("works-post", "作品"),
    ("works", "作品"),
]

SKIP = {"search.html", "index-旧版备份.html"}


def to_pinyin(text):
    if not text:
        return ""
    full = "".join(lazy_pinyin(text))
    init = "".join(lazy_pinyin(text, style=Style.FIRST_LETTER))
    return (full + " " + init).strip()


def guess_cat(name):
    base = name.replace(".html", "")
    for prefix, cat in CAT_MAP:
        if base == prefix or base.startswith(prefix + "-"):
            return cat
    return "AI经验"


def extract(html, name):
    title_m = re.search(r"<title>(.*?)</title>", html, re.S)
    title = title_m.group(1).strip() if title_m else name
    title = re.sub(r"\s*\|\s*JowJo\s*$", "", title)
    desc = ""
    m = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html, re.S | re.I)
    if m:
        desc = m.group(1).strip()
    else:
        p = re.search(r"<p[^>]*>(.*?)</p>", html, re.S)
        if p:
            desc = re.sub(r"<[^>]+>", "", p.group(1)).strip()[:80]
    tags = []
    tm = re.findall(r'class="tags"[^>]*>(.*?)</div>', html, re.S)
    if tm:
        tags = re.findall(r">([^<]+)<", tm[0])
    date = ""
    dm = re.search(r'date["\s:]+([\d]{4}-[\d]{2}-[\d]{2})', html)
    if dm:
        date = dm.group(1)
    return title, desc, tags, date


def enhance_mode():
    if not os.path.exists(IDX):
        print("search-index.json 不存在，改用 --from-html 全扫描")
        return from_html_mode()
    with open(IDX, encoding="utf-8") as f:
        data = json.load(f)
    for d in data:
        base = d.get("title", "") + " " + " ".join(d.get("tags", [])) + " " + d.get("cat", "")
        d["py"] = to_pinyin(base)
        url = d.get("url", "")
        if url and not os.path.exists(os.path.join(ROOT, url)):
            print("  [警告] 索引 url 不存在:", url)
    with open(IDX, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("增强完成: 共", len(data), "条，已补拼音并校验链接")
    return data


def from_html_mode():
    files = [f for f in os.listdir(ROOT) if f.endswith(".html") and f not in SKIP]
    data = []
    for f in sorted(files):
        if f == "index.html":
            continue
        with open(os.path.join(ROOT, f), encoding="utf-8") as fh:
            html = fh.read()
        title, desc, tags, date = extract(html, f)
        data.append({
            "title": title,
            "url": f,
            "date": date,
            "desc": desc,
            "tags": tags,
            "cat": guess_cat(f),
            "py": to_pinyin(title + " " + " ".join(tags)),
        })
    with open(IDX, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print("全扫描完成: 共", len(data), "条")
    return data


if __name__ == "__main__":
    if "--from-html" in sys.argv:
        from_html_mode()
    else:
        enhance_mode()
