# 更新日誌 — 台灣卡店地圖

## 2026-05-18（後續）— Leaflet 本地化 + 安全 meta（Lucy 安全方案 T1-2/T2-2）

- **Leaflet 1.9.4 vendor 落本地** `vendor/leaflet/`（leaflet.js + leaflet.css + 5 images），移除 `cdn.jsdelivr.net` 依賴。
  - 解決 supply-chain 風險（原本 CDN 無 SRI，被污染即任意 JS on domain）。
  - 順手解「offline-safe PWA 但 map lib 靠 CDN」嘅矛盾 — 真正離線可用。
- `sw.js`：Leaflet 全套加入 `SHELL_URLS` install precache；移除已死嘅 jsdelivr SWR 分支同 `LIB` cache；`VERSION v3→v4`。
- 加 `<meta name="robots" content="noindex">` + `referrer:no-referrer`。
- 驗證：0 jsdelivr 殘留、sw.js syntax OK、leaflet.css image 路徑 relative 對齊 vendor/images。

## 2026-05-18 — 搬去自訂 domain

- 新增 `CNAME` → `cards.wicalyu.com`（GitHub Pages 自訂 subdomain，DNS 經 Cloudflare）。
- `index.html` og:url / og:image 由 `wical112.github.io/taiwan-card-shops/` 改為 `https://cards.wicalyu.com/`。
- sw.js VERSION `v2` → `v3`（index.html 有改動，強制刷 PWA cache）。
- PWA 用相對路徑（`./`），搬去 subdomain root 不受影響。
- 待辦：Cloudflare 加 CNAME `cards` → `wical112.github.io`（DNS only），等 GitHub 出證書後 Enforce HTTPS。
