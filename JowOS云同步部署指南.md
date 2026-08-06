# JowOS 云同步部署指南（Cloudflare Worker + 私有 Gist）

让 JowOS 跨设备自动同步：在 Mac 上新增/删除的任务，手机打开 `jowjowork.uno/jowos/` 也能看到。

## 原理
- JowOS 本体仍是纯静态单文件，数据默认存浏览器 `localStorage`。
- 开启「云同步」后，页面通过你的 **Cloudflare Worker** 读写一个 **GitHub 私有 Gist**（里面是 `jowos-data.json` 整份状态）。
- **GitHub token 只存在 Worker 的环境变量里，绝不进前端页面**；前端只持有一个你自己设的「同步口令」(`JOWOS_KEY`)，Worker 校验它通过才放行。
- 同步策略：打开页面自动拉取；任何改动 1.5 秒后防抖自动推送；也可手动「立即同步 / 仅拉取 / 仅推送」。冲突按「最后写入者胜」合并。

## 前置条件
- 一个 **Cloudflare 账号**（免费，workers.dev 域名免费）。
- 你已有 **GitHub 账号**（jowjowork.uno 就在用）。

---

## 步骤 1 · 建 GitHub 经典 PAT
1. 打开 https://github.com/settings/tokens
2. 点 **Generate new token (classic)**
3. Note 填 `jowos-sync`；Expiration 选 `No expiration`（或自定）
4. 勾选 **gist** 这一项（其余都不勾）
5. 生成，复制那一长串 `ghp_xxx`（只显示一次，存好）

## 步骤 2 · 建私有 Gist
1. 打开 https://gist.github.com
2. 勾选 **Secret（私有）**
3. 文件名填 `jowos-data.json`
4. 内容填 `{}`
5. 创建。URL 形如 `https://gist.github.com/<用户名>/<GIST_ID>` —— 记下其中的 **GIST_ID**（URL 最后那段）

## 步骤 3 · 建 Cloudflare Worker
1. 打开 https://dash.cloudflare.com → **Workers & Pages** → **Create** → **Create Worker**
2. 名称随便（如 `jowos-sync`），把默认代码**全删**，粘贴仓库里的 `jowos-worker.js` 内容
3. 切到 **Settings → Variables → Environment Variables**，添加 3 个（都点「Encrypt」隐藏）：
   - `GITHUB_TOKEN` = 步骤 1 的 `ghp_xxx`
   - `GIST_ID` = 步骤 2 的 GIST_ID
   - `JOWOS_KEY` = 你自己编的一长串随机串（如 `openssl rand -hex 24` 生成的），**记下来，下一步要用**
4. 点 **Deploy / Save**

## 步骤 4 · 拿 Worker 地址
部署后 Cloudflare 会给出地址，形如 `https://jowos-sync.<你的子域>.workers.dev`。复制它。

## 步骤 5 · 在 JowOS 里启用
1. 打开 `jowos/index.html`（本地或已部署的 `jowjowork.uno/jowos/`）
2. 拉到底部「同步」卡片 → 打开「启用云同步」
3. 填 **Worker 地址** 和 **同步口令**（= 步骤 3 的 `JOWOS_KEY`）
4. 点「连接测试」应显示「连接正常 ✓」；点「立即同步」
5. 换另一台设备/浏览器打开同一地址，启用同步填同样的 Worker 地址与口令 → 数据就一致了

---

## 验证跨设备
- 设备 A 加一条任务 → 约 1–2 秒内自动推送到 Gist。
- 设备 B 刷新页面（或点「立即同步」）→ 看到这条任务。

## 安全与局限
- token 只在 Worker 端，页面源码里搜不到，安全。
- **同一时刻建议主要在一台设备编辑**（个人 OS 通常如此）。若两台同时离线各改各的再上线，按「最后写入者胜」合并，被覆盖的旧数据会存到该浏览器的 `jowos.backup` 键，可手动恢复。
- 仍走 GitHub 私有 Gist，数据在你自己账号里，不上任何第三方。
- 不开启同步时，行为与之前完全一致（纯本机）。

## 文件位置
- 页面：`jowos/index.html`（已部署到站点）
- Worker 代码：`jowos-worker.js`（仓库根目录，部署时粘贴用）
