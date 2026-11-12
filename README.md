# JowJoWork

个人站 · https://jowjowork.uno

纯静态（HTML + CSS + JS），无构建步骤、无后端、无数据库。
往 `main` 分支推送后，GitHub Actions 会自动把根目录发布到 `gh-pages`，约 1 分钟生效。

## 文件

| 文件 | 内容 |
|---|---|
| `index.html` | 首页（一句话自我介绍） |
| `hobbies.html` | 半桶水 · 17 项，每项含怎么入门 / 条件 / 花费 / 先学什么 |
| `places.html` | 一些店 · 按城市分 |
| `thoughts.html` | 一些思考 · 4 个主题 |
| `post.html` | 文章详情模板，复制改名复用 |
| `social.html` | 自媒体 · 8 个平台 |
| `about.html` | 关于 · 参数表 |
| `assets/style.css` | 全站配色与字体，顶部变量可改 |
| `assets/site.js` | 滚动进场、进度条、导航高亮 |

## 不能删的文件

- `CNAME` — 内容是 `jowjowork.uno`，删了自定义域名失效
- `.nojekyll` — 删了 GitHub 可能走 Jekyll 处理导致白屏
- `.github/workflows/deploy.yml` — 自动部署，删了推送后不会发布

## 改内容

改本地文件 → 提交 → 推送。不用碰命令行也行，GitHub Desktop 拖一下就好。

## 旧版

2026 年 11 月改版前的完整旧站（含 30 余篇 AI 文章、media 素材、搜索系统）：
- 本地备份：`发散区_思考/JowJoWork_V1_旧站备份_2026-11-12/`
- Git 标签：`backup-before-redesign-2026-11-12`
