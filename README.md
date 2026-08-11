# JowJo 网站项目

> 项目地址：https://jowjowork.uno  
> 技术栈：纯静态 HTML + 内联 CSS + 原生 JS，部署在 GitHub Pages  
> 主题风格：深色沉浸、MUJI/Apple 极简、中文优先

## 一、项目简介

这是 JowJo 个人主页兼内容站点，目前包含四大栏目：

| 栏目 | 路径 | 说明 |
|------|------|------|
| AI 经验 | `ai-sharing.html` + `ai-post-*.html` | 名人/创作者使用 AI 的经验整理 |
| SKILLS | `skills.html` + `skills-post-*.html` | 从经验里提炼的可复用技能 |
| 作品 | `works.html` + `works-post-*.html` | 个人项目与案例 |
| 名片 | `links.html` | 抖音 / B站 / 小红书 / 微信 聚合入口 |

## 二、关键约定

### 2.1 作者与头像规则

| 作者类型 | 署名 | 头像 | 说明 |
|----------|------|------|------|
| JowJo 本人写的文章 | JowJo | `media/tiger-head.png` 虎头 | 用户自写 |
| WorkBuddy/AI 整理的文章 | Jowork | `media/trex-head.jpg` 霸王龙 | 默认代笔 |
| 名人/嘉宾经验文章 | 真实姓名 | 姓氏占位符（圆形底色 + 姓） | 避免肖像权风险 |

> 谁的文章署名 JowJo 会由用户单独说明，未说明的一律按 Jowork 处理。

### 2.2 导航规则

- 顶部导航共 5 项：AI经验 / SKILLS / 作品 / 商业合作 / 关于
- 5 项等宽（`flex:1`），最大容器宽度 `1100px`，居中
- 右上角搜索图标紧跟"关于"，不再绝对定位到窗口最右边（避免宽屏刘海）
- 手机端（≤600px）5 项 + 搜索图标自适应，不遮挡"关于"

### 2.3 页面宽度规则

| 区域 | 最大宽度 | 左右留白 |
|------|----------|----------|
| 导航内部 | 1100px | 24px（手机 8px） |
| 栏目页正文 | 980px | 36px（手机 24px） |
| 文章详情页正文 | 980px | 36px（手机 24px） |
| 搜索页内容 | 980px | 36px |

### 2.4 图片与版权

- 虎头：JowJo 个人形象
- 小霸王龙头像：`media/trex-head.jpg`，来源 Wikimedia Commons，CC0 / public domain
- 名人头像：不使用真人照片，用姓氏占位符
- 内容整理自公开访谈/网络资料，页面底部需加免责声明

### 2.5 搜索功能

- 文件：`search.html` + `search-index.json`
- 支持：标题 / 摘要 / 标签 / 栏目名 / 拼音（如 `lidan` 可搜到"李诞"）
- 匹配结果会高亮显示
- 索引脚本：`scripts/build_search_index.py`，运行后自动补充拼音字段并校验链接

## 三、工作流约定

### 3.1 发布一篇新文章

1. 复制 `页面模板` 里的对应模板，重命名为 `ai-post-xxx.html` / `skills-post-xxx.html` / `works-post-xxx.html`。
2. 填写标题、正文、作者卡、免责声明。
3. 在对应栏目列表页（`ai-sharing.html` / `skills.html` / `works.html`）加入文章入口。
4. 在 `search-index.json` 里追加一条（title / desc / tags / date / cat / url），desc 建议手写，保持质量。
5. 运行索引脚本补拼音：
   ```bash
   python3 scripts/build_search_index.py
   ```
6. 运行 CSS 审计复查：
   ```bash
   python3 scripts/audit_css.py
   ```
7. 本地截图验证（桌面 + 手机两档），然后 `git add / commit / push`。

### 3.2 全站小修批量改样式

已沉淀 WorkBuddy 技能 `static-html-css-bulk-editor`，流程：
1. 先设计桌面 + 手机规则
2. 只截 2 档图验证
3. 用脚本批量应用
4. 不再手改 51 个文件

## 四、已沉淀的工具脚本

| 脚本 | 作用 |
|------|------|
| `scripts/build_search_index.py` | 给搜索索引补拼音字段、校验链接有效性 |
| `scripts/audit_css.py` | 全站内联 CSS 一致性审计 |
| `scripts/unify_inline_css.py` | 自动把单行大段 style 块展开为多行 |

## 五、暂不做/待申请项

| 项 | 状态 | 原因 |
|----|------|------|
| 微信小程序化 | 待申请 | 需要注册微信小程序主体、备案、认证资质 |
| 内容多平台自动分发 | 暂不做 | 各平台 API/格式/规则差异大，当前内容量手动分发更稳 |

## 六、一句话总结

纯静态、中文优先、内容为王。所有约定都写在这份 README 里，新加文章或小修样式前先读一遍，避免走回头路。
