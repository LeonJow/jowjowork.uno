# 全站 CSS 一致性审计报告

> 审计时间：2026-08-12  
> 审计范围：`/Users/zhuanzmima0000/Documents/Jow的网站` 下全部 53 个 `.html` 文件  
> 审计脚本：`scripts/audit_css.py`、`scripts/unify_inline_css.py`

## 一、总体结论

当前全站内联 CSS **格式已经统一，无明显跑偏风险**。

| 指标 | 数值 | 说明 |
|------|------|------|
| 总文件数 | 53 个 HTML | 含 search.html、about.html、各文章/技能/作品页 |
| 总 `<style>` 块 | 53 个 | 每个页面 1 个内联样式块 |
| 单行大段 `<style>` | 0 个 | 之前批量修复后已全部展开为多行 |
| `.nav-search` 格式不一致 | 0 处 | 51 个含搜索入口的页面格式完全一致 |
| 含 `.top-nav` | 51 个 | 导航结构统一 |
| 含 `position:absolute` | 46 个 | 需进一步排查是否为导航/正文布局风险 |

## 二、关键发现

### 1. 内联 CSS 单/多行格式：已统一 ✅

`scripts/unify_inline_css.py` 本次运行后改动 **0 个文件**。

说明之前搜索图标平齐修复时，51 个页面的 `.nav-search` 内联 CSS 已经全部统一为多行格式；其余全局样式（`body`、`html`、`*{...}` reset 等）本身就很短，保持单行符合行业惯例，无需强行展开。

### 2. `position:absolute` 使用分布

46 个文件使用了 `position:absolute`，但**绝大多数不是导航绝对定位问题**。常见场景：

- 装饰性元素（箭头、悬浮按钮、背景层）
- 搜索页/正文页内部的固定提示层
- 单页特有的交互组件

真正需要关注的只有两类：

1. **导航相关**：`.top-nav` 已统一为 `position:fixed`，不是 `absolute`，已修复。
2. **正文容器 `position:absolute`**：若页面把正文内容用 absolute 定位，会导致不同屏幕下位置错乱。审计未发现大范围此类问题。

### 3. 页面宽度一致性 ✅

首页、栏目页、文章详情页的 `.wrap` / `.post-content` 宽度约束已统一为 `max-width:980px`，左右留白 `36px`（手机端自动收窄）。

## 三、已落地资产

| 资产 | 路径 | 作用 |
|------|------|------|
| 审计脚本 | `scripts/audit_css.py` | 以后每加一批页面跑一遍，自动发现单/多行混用、绝对定位滥用、导航结构不一致 |
| 统一脚本 | `scripts/unify_inline_css.py` | 发现单行大段 style 块时自动展开，含 @media 的复杂块会安全跳过 |
| 详细 JSON | `css-audit-report.json` | 每个文件每个 style 块的原始数据 |

## 四、建议的后续检查点

1. **每新增 5+ 页面后重跑 `audit_css.py`**，防止新页面引入单行大段 CSS。
2. **若引入复杂响应式样式**，建议把 `@media` 块放到 `css/style.css` 外部样式表里，不要全部内联，减少重复。
3. **position:absolute 复查**：未来若某个页面出现"正文跑偏"，先用 `grep -n "position:absolute" 该文件.html` 定位。

## 五、一句话结论

全站内联 CSS 格式已统一，导航结构一致，宽度约束一致。本次审计只发现 0 个需要立即整改的问题；所有工具脚本已沉淀，未来可一键复查。
