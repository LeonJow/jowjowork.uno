#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_dates.py — 把文章日期集中到 content.json，再同步到全站所有出现位置。

设计目标（用户诉求）：
  1) 日期不再"虚拟生成"，用真实日期（本批 ai/skills 文章统一为真实诞生日 2026-08-10；
     works 作品保留各自真实年份）。
  2) 后期想改只改 content.json 这一处，跑一下本脚本即可全站生效。

同步覆盖 5 类位置：
  - 文章页 <div class="meta"><span>日期</span>...
  - ai-sharing.html  <div class="date">日期</div>
  - skills.html      <div class="yr">日期 · 整理自X</div>
  - works.html       <div class="yr">年份</div>
  - search-index.json  "date": "日期"

用法：
  python3 scripts/sync_dates.py            # 用仓库内 content.json 同步
  python3 scripts/sync_dates.py --root /tmp/jow_test   # 指定根目录（测试用）
  python3 scripts/sync_dates.py --init     # 仅（重新）生成 content.json，不写其它文件
"""
import json, re, os, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.abspath(os.path.join(HERE, ".."))

DATE_RE = r"[0-9]{4}(?:-[0-9]{2}){0,2}"   # 2021 / 2026-08 / 2026-08-10


def find_root():
    for i, a in enumerate(sys.argv):
        if a == "--root" and i + 1 < len(sys.argv):
            return os.path.abspath(sys.argv[i + 1])
    return DEFAULT_ROOT


def list_post_files(root):
    out = []
    for pat in ("ai-post-*.html", "skills-post-*.html", "works-post-*.html"):
        out += sorted(glob_pat(root, pat))
    return out


def glob_pat(root, pat):
    import glob
    return glob.glob(os.path.join(root, pat))


def current_meta_date(path):
    s = open(path, encoding="utf-8").read()
    m = re.search(r'<div class="meta">\s*<span>([^<]*)</span>', s)
    return m.group(1) if m else ""


def build_manifest(root):
    """生成 content.json：ai/skills -> 2026-08-10；works -> 保留当前年份。"""
    posts = {}
    for f in list_post_files(root):
        name = os.path.basename(f)
        if name.startswith(("ai-post-", "skills-post-")):
            posts[name] = "2026-08-10"
        else:  # works-post-*
            posts[name] = current_meta_date(f) or "2026-08-10"
    return {"posts": posts}


def write_manifest(root, manifest):
    with open(os.path.join(root, "content.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def sync_article_page(path, date):
    s = open(path, encoding="utf-8").read()
    new, n = re.subn(
        r'(<div class="meta">\s*<span>)[^<]*(</span>)',
        lambda m: m.group(1) + date + m.group(2),
        s, count=1,
    )
    if n:
        open(path, "w", encoding="utf-8").write(new)
    return n


def sync_list_page(listfile, postfile, date):
    if not os.path.exists(listfile):
        return 0
    s = open(listfile, encoding="utf-8").read()
    esc = re.escape(postfile)
    if listfile.endswith("ai-sharing.html"):
        # 结构：<div class="date">日期</div> 在 <a href> 之前；
        # 用负向预查防止 .*? 跨过下一个 <div class="item"> 吃掉别的 item 的日期
        pat = (
            r'(<div class="date">)(' + DATE_RE +
            r')(' + r'</div>(?:(?!<div class="item">).)*?<a href="' + esc + r'"[^>]*>)'
        )
        rep = lambda m: m.group(1) + date + m.group(3)
    else:
        # skills.html / works.html：<a href> 在 <div class="yr"> 之前
        pat = (
            r'(<a[^>]*href="' + esc +
            r'"[^>]*>.*?<div class="yr">)(' + DATE_RE + r')([^<]*)(</div>)'
        )
        rep = lambda m: m.group(1) + date + m.group(3) + m.group(4)
    new, n = re.subn(pat, rep, s, count=1, flags=re.S)
    if n:
        open(listfile, "w", encoding="utf-8").write(new)
    return n


def sync_search_index(root, posts):
    path = os.path.join(root, "search-index.json")
    if not os.path.exists(path):
        return 0
    s = open(path, encoding="utf-8").read()
    total = 0
    for postfile, date in posts.items():
        pat = (
            r'("url":\s*"' + re.escape(postfile) +
            r'"\s*,\s*"date":\s*")(' + DATE_RE + r')([^"]*)(")'
        )
        new, n = re.subn(pat, r'\g<1>' + date + r'\g<3>' + r'\g<4>', s)
        if n:
            s = new
            total += n
    if total:
        open(path, "w", encoding="utf-8").write(s)
    return total


def sync(root, manifest):
    posts = manifest["posts"]
    # 文章页
    for f in list_post_files(root):
        name = os.path.basename(f)
        if name in posts:
            sync_article_page(f, posts[name])
    # 列表页（按帖子精确同步到各自列表）
    for f in list_post_files(root):
        name = os.path.basename(f)
        if name not in posts:
            continue
        if name.startswith("ai-post-"):
            sync_list_page(os.path.join(root, "ai-sharing.html"), name, posts[name])
        elif name.startswith("skills-post-"):
            sync_list_page(os.path.join(root, "skills.html"), name, posts[name])
        elif name.startswith("works-post-"):
            sync_list_page(os.path.join(root, "works.html"), name, posts[name])
    # 搜索索引
    sync_search_index(root, posts)


def main():
    root = find_root()
    init_only = "--init" in sys.argv
    manifest_path = os.path.join(root, "content.json")
    if os.path.exists(manifest_path):
        manifest = json.load(open(manifest_path, encoding="utf-8"))
        print("使用已有 content.json（%d 个条目）" % len(manifest.get("posts", {})))
    else:
        manifest = build_manifest(root)
        write_manifest(root, manifest)
        print("已生成 content.json（%d 个条目）" % len(manifest["posts"]))
    if init_only:
        print("（--init 仅生成清单，未写入其它文件）")
        return
    sync(root, manifest)
    print("同步完成 ✓  后期改日期只需编辑 content.json 后重跑本脚本。")


if __name__ == "__main__":
    main()
