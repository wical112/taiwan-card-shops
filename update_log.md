# 更新日誌 — 台灣卡店地圖

## 2026-05-18 — 搬去自訂 domain

- 新增 `CNAME` → `cards.wicalyu.com`（GitHub Pages 自訂 subdomain，DNS 經 Cloudflare）。
- `index.html` og:url / og:image 由 `wical112.github.io/taiwan-card-shops/` 改為 `https://cards.wicalyu.com/`。
- sw.js VERSION `v2` → `v3`（index.html 有改動，強制刷 PWA cache）。
- PWA 用相對路徑（`./`），搬去 subdomain root 不受影響。
- 待辦：Cloudflare 加 CNAME `cards` → `wical112.github.io`（DNS only），等 GitHub 出證書後 Enforce HTTPS。
