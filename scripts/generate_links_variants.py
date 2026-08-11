# -*- coding: utf-8 -*-
"""生成 4 个版式的名片页预览（links-a/b/c/d.html），供用户挑选。
统一使用：白底圆角方块 + 彩色真实 APP 图标。"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLATFORMS = [
    {"name": "抖音", "href": "https://www.douyin.com/user/MS4wLjABAAAAreuw3cVEK6Hp5cO9UyTVRpkyAs0yGbAmmy21T5seUypb1Mfq9Bc_qUqmY2ecqQWi",
     "icon": "media/social/douyin.png", "desc": "短视频日常、AI 玩法、创作心得", "id": "29568050004"},
    {"name": "B 站", "href": "https://b23.tv/EZxcvcF", "icon": "media/social/bilibili.svg",
     "desc": "读书、学习、旅行系列 · 易富体质", "id": "@O鲨鱼Oo"},
    {"name": "小红书", "href": "https://xhslink.com/m/A0GnUQ9rw0U", "icon": "media/social/xiaohongshu.svg",
     "desc": "生活方式、成长笔记、好物灵感", "id": ""},
    {"name": "微信", "href": "http://weixin.qq.com/r/mp/iRE5IU7EIRNerQpC90Sb", "icon": "media/social/wechat.svg",
     "desc": "公众号 / 个人号 · 慢聊、长文、链接", "id": ""},
]

NAV = """  <nav class="top-nav">
    <div class="nav-inner">
      <a href="ai-sharing.html" class="nav-item"><span class="label">AI经验</span><span class="sub">日常中的一些AI经验分享</span></a>
      <a href="skills.html" class="nav-item"><span class="label">SKILLS</span><span class="sub">一些好用的Skills</span></a>
      <a href="works.html" class="nav-item"><span class="label">作品</span><span class="sub">我做过的一些项目与案例</span></a>
      <a href="services.html" class="nav-item"><span class="label">商业合作</span><span class="sub">JowJo也许可以解决你的一些问题</span></a>
      <a href="about.html" class="nav-item"><span class="label">关于</span><span class="sub">关于JowJo与超认真工作室</span></a>
      <a class="nav-search" href="search.html" aria-label="搜索">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      </a>
    </div>
  </nav>"""

BASE_STYLE = r"""*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0e0e0e;color:#f2f2f2;font-family:'Noto Sans SC',-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;min-height:100vh;}
a{color:inherit;text-decoration:none;}
.top-nav{position:fixed;top:0;left:0;right:0;z-index:10;background:linear-gradient(to bottom,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 100%);}
.nav-inner{display:flex;justify-content:center;align-items:flex-start;max-width:1100px;margin:0 auto;padding:30px 24px 16px;font-family:'Noto Sans SC',-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;}
.nav-inner .nav-item{position:relative;flex:1 1 0;min-width:0;display:flex;flex-direction:column;align-items:center;color:#fff;white-space:nowrap;border-left:1px solid rgba(255,255,255,.32);}
.nav-inner .nav-item:first-child{border-left:none;}
.nav-inner .label{font-size:clamp(18px,2.2vw,25px);letter-spacing:1.5px;opacity:.82;text-shadow:0 1px 8px rgba(0,0,0,.55);transition:opacity .25s,text-shadow .25s;}
.nav-inner .nav-item:hover .label{opacity:1;text-shadow:0 0 14px rgba(255,255,255,.7);}
.nav-inner .sub{position:absolute;top:100%;left:50%;transform:translateX(-50%);margin-top:8px;font-size:12px;letter-spacing:1px;color:rgba(255,255,255,.82);opacity:0;transition:opacity .25s;pointer-events:none;white-space:nowrap;}
.nav-inner .nav-item:hover .sub{opacity:1;}
@media(max-width:600px){.nav-inner{padding:14px 8px 10px;max-width:none;}.nav-inner .label{font-size:12px;letter-spacing:.3px;}.nav-inner .sub{font-size:9px;margin-top:4px;}.top-nav .nav-item{flex:0 1 auto;min-width:auto;}.nav-inner{gap:14px;}}

.nav-search{display:flex;align-items:center;justify-content:center;color:#fff;opacity:.8;transition:opacity .25s,transform .25s;filter:drop-shadow(0 1px 6px rgba(0,0,0,.6));align-self:center;margin-left:10px;}
.nav-search:hover{opacity:1;transform:scale(1.1);}
@media(max-width:600px){.nav-search{margin-left:4px;}.nav-search svg{width:17px;height:17px;}.top-nav .nav-item{flex:0 1 auto;min-width:auto;}.nav-inner{gap:14px;}}

.wrap{max-width:980px;margin:0 auto;padding:150px 36px 60px;}
.page-title{font-size:clamp(34px,6vw,56px);text-align:center;font-weight:700;letter-spacing:2px;margin-bottom:6px;}
.page-sub{text-align:center;opacity:.6;font-size:14px;letter-spacing:3px;margin-bottom:46px;}

.icon{width:54px;height:54px;border-radius:14px;background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden;box-shadow:0 4px 14px rgba(0,0,0,.35);flex:0 0 auto;}
.icon img{width:62%;height:62%;object-fit:contain;}

.foot{text-align:center;padding:30px 0 44px;font-size:12px;opacity:.5;}
.foot a{color:inherit;text-decoration:underline;}
"""

EXTRA = {
    "A": r""".card-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px;max-width:720px;margin:0 auto;}
.card{display:flex;flex-direction:column;align-items:flex-start;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:28px;transition:transform .25s,background .25s,border-color .25s;}
.card:hover{transform:translateY(-4px);background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.22);}
.card h3{font-size:20px;font-weight:500;margin-bottom:4px;letter-spacing:1px;}
.card p{font-size:13px;opacity:.55;margin-bottom:18px;line-height:1.6;}
.card .btn{display:inline-block;font-size:13px;padding:8px 18px;border-radius:999px;background:rgba(255,255,255,.1);color:#fff;transition:background .25s;}
.card:hover .btn{background:rgba(255,255,255,.2);}
.card .id{font-size:12px;opacity:.4;margin-top:8px;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;}
@media(max-width:680px){.card-grid{grid-template-columns:1fr;}}""",
    "B": r""".list-b{max-width:680px;margin:0 auto;display:flex;flex-direction:column;gap:14px;}
.row-b{display:flex;align-items:center;gap:18px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:18px 22px;transition:background .25s,transform .2s,border-color .25s;}
.row-b:hover{background:rgba(255,255,255,.09);transform:translateX(4px);border-color:rgba(255,255,255,.25);}
.icon-circle{width:52px;height:52px;border-radius:50%;background:#fff;flex:0 0 auto;display:flex;align-items:center;justify-content:center;overflow:hidden;box-shadow:0 4px 14px rgba(0,0,0,.3);}
.icon-circle img{width:60%;height:60%;object-fit:contain;}
.meta{flex:1 1 auto;}
.meta h3{font-size:19px;font-weight:500;margin-bottom:3px;}
.meta p{font-size:13px;opacity:.55;line-height:1.5;}
.arrow{font-size:22px;opacity:.5;transition:transform .25s,opacity .25s;}
.row-b:hover .arrow{transform:translateX(4px);opacity:.9;}""",
    "C": r""".wall-c{max-width:760px;margin:0 auto;display:flex;justify-content:center;gap:46px;flex-wrap:wrap;}
.bubble-c{display:flex;flex-direction:column;align-items:center;gap:16px;text-decoration:none;}
.bigcircle{width:120px;height:120px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.4);transition:transform .3s,box-shadow .3s;}
.bubble-c:hover .bigcircle{transform:translateY(-6px) scale(1.05);box-shadow:0 16px 40px rgba(0,0,0,.5);}
.bigcircle img{width:62%;height:62%;object-fit:contain;}
.cap{font-size:16px;letter-spacing:1px;opacity:.85;}""",
    "D": r"""body{background:
  radial-gradient(circle at 18% 20%, rgba(254,44,85,.28), transparent 42%),
  radial-gradient(circle at 82% 28%, rgba(0,174,236,.24), transparent 42%),
  radial-gradient(circle at 50% 92%, rgba(7,193,96,.22), transparent 46%),
  #0e0e0e;}
.card-grid-d{max-width:720px;margin:0 auto;display:grid;grid-template-columns:repeat(2,1fr);gap:24px;}
.glass-d{display:flex;flex-direction:column;align-items:flex-start;background:rgba(255,255,255,.07);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.18);border-radius:22px;padding:28px;text-decoration:none;transition:transform .25s,background .25s,border-color .25s;}
.glass-d:hover{transform:translateY(-4px);background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.32);}
.glass-d h3{font-size:20px;font-weight:500;margin:14px 0 4px;}
.glass-d p{font-size:13px;opacity:.6;margin-bottom:16px;line-height:1.6;}
.glass-d .btn{display:inline-block;font-size:13px;padding:8px 18px;border-radius:999px;background:rgba(255,255,255,.16);transition:background .25s;}
.glass-d:hover .btn{background:rgba(255,255,255,.28);}
@media(max-width:680px){.card-grid-d{grid-template-columns:1fr;}}""",
}


def icon_html(p):
    return '<div class="icon"><img src="%s" alt="%s"></div>' % (p["icon"], p["name"])


def container_html(variant):
    if variant == "A":
        cards = []
        for p in PLATFORMS:
            id_line = '<span class="id">%s</span>' % p["id"] if p["id"] else ""
            cards.append(
                '<a class="card" href="%s" target="_blank" rel="noopener">%s'
                '<h3>%s</h3><p>%s</p><span class="btn">去主页</span>%s</a>'
                % (p["href"], icon_html(p), p["name"], p["desc"], id_line))
        return '<div class="card-grid">%s</div>' % "".join(cards)
    if variant == "B":
        rows = []
        for p in PLATFORMS:
            rows.append(
                '<a class="row-b" href="%s" target="_blank" rel="noopener">'
                '<div class="icon-circle"><img src="%s" alt="%s"></div>'
                '<div class="meta"><h3>%s</h3><p>%s</p></div>'
                '<span class="arrow">&rarr;</span></a>'
                % (p["href"], p["icon"], p["name"], p["name"], p["desc"]))
        return '<div class="list-b">%s</div>' % "".join(rows)
    if variant == "C":
        bubbles = []
        for p in PLATFORMS:
            bubbles.append(
                '<a class="bubble-c" href="%s" target="_blank" rel="noopener">'
                '<div class="bigcircle"><img src="%s" alt="%s"></div>'
                '<span class="cap">%s</span></a>'
                % (p["href"], p["icon"], p["name"], p["name"]))
        return '<div class="wall-c">%s</div>' % "".join(bubbles)
    if variant == "D":
        cards = []
        for p in PLATFORMS:
            cards.append(
                '<a class="glass-d" href="%s" target="_blank" rel="noopener">%s'
                '<h3>%s</h3><p>%s</p><span class="btn">去主页</span></a>'
                % (p["href"], icon_html(p), p["name"], p["desc"]))
        return '<div class="card-grid-d">%s</div>' % "".join(cards)
    return ""


def build(variant):
    style = BASE_STYLE + "\n" + EXTRA[variant]
    body = ('<div class="wrap"><div class="page-title">名片</div>'
            '<div class="page-sub">全网同名 · 找到我</div>%s</div>') % container_html(variant)
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>名片 · 版式%s | JowJo</title>
<style>
%s</style>
</head>
<body>
%s
%s
  <div class="foot">Copyright by <a href="index.html">超认真工作室</a> · <a href="about.html">关于</a></div>
</body>
</html>""" % (variant, style, NAV, body)


if __name__ == "__main__":
    for v in ["A", "B", "C", "D"]:
        out = os.path.join(ROOT, "links-%s.html" % v.lower())
        with open(out, "w", encoding="utf-8") as f:
            f.write(build(v))
        print("生成", out)
