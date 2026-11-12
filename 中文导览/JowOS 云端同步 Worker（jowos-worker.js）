// JowOS Cloud Sync Worker
// 部署到 Cloudflare Workers（免费额度足够个人用）。
// 环境变量（Secrets，绝不可写进前端）：
//   GITHUB_TOKEN = GitHub 经典 PAT，仅需 gist 权限
//   GIST_ID      = 你的私有 Gist ID（URL 里 https://gist.github.com/<用户名>/<GIST_ID> 那段）
//   JOWOS_KEY    = 你自己设的一长串随机口令，前端「同步口令」填同一个
// 前端通过 Header `x-jowos-key` 携带口令；不匹配一律 401。
// GET  -> 读取 Gist 里的 jowos-data.json 原文返回
// POST -> 用 PATCH 覆盖写入 Gist（整个状态快照）

const FILE = 'jowos-data.json';

export default {
  async fetch(request, env) {
    const CORS = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
      'Access-Control-Allow-Headers': 'content-type,x-jowos-key',
    };
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }

    const key = request.headers.get('x-jowos-key');
    if (!key || key !== env.JOWOS_KEY) {
      return new Response('unauthorized', { status: 401, headers: CORS });
    }

    const api = `https://api.github.com/gists/${env.GIST_ID}`;
    const headers = {
      Authorization: `token ${env.GITHUB_TOKEN}`,
      'User-Agent': 'jowos-sync',
      Accept: 'application/vnd.github+json',
    };

    try {
      if (request.method === 'GET') {
        const r = await fetch(api, { headers });
        if (!r.ok) return new Response('gist read failed: ' + r.status, { status: 502, headers: CORS });
        const j = await r.json();
        const content = j.files && j.files[FILE] ? j.files[FILE].content : '{}';
        return new Response(content, {
          status: 200,
          headers: { ...CORS, 'Content-Type': 'application/json' },
        });
      }

      if (request.method === 'POST') {
        const body = await request.text();
        try { JSON.parse(body); } catch (e) {
          return new Response('invalid json', { status: 400, headers: CORS });
        }
        const r = await fetch(api, {
          method: 'PATCH',
          headers: { ...headers, 'Content-Type': 'application/json' },
          body: JSON.stringify({ files: { [FILE]: { content: body } } }),
        });
        if (!r.ok) return new Response('gist write failed: ' + r.status, { status: 502, headers: CORS });
        return new Response('{"ok":true}', {
          status: 200,
          headers: { ...CORS, 'Content-Type': 'application/json' },
        });
      }

      return new Response('method not allowed', { status: 405, headers: CORS });
    } catch (e) {
      return new Response('error: ' + e.message, { status: 500, headers: CORS });
    }
  },
};
