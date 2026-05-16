# 🗺️ 台灣卡店地圖（Pokémon / One Piece）

為朋友台灣行程而製嘅單檔離線地圖 app。

## 🔗 Live（傳呢條俾朋友）

**https://wical112.github.io/taiwan-card-shops/**

GitHub Pages（public repo `wical112/taiwan-card-shops`，main / root）。`git push` 後約 30 秒自動重新發佈。

## 點用 / 點交俾朋友

- 直接傳上面條 link，朋友 iPhone Safari 開 → 分享鍵「**加入主畫面**」→ 似 app icon，之後**離線都開到**。
- 或 AirDrop `index.html` 單檔俾佢（完全離線）。
- 更新資料：改檔 → `git add -A && git commit && git push` → Pages 自動 rebuild。

## 功能

- 三色分類：🔴 有寶可夢 · 🔵 有 One Piece · 🟢 兩款都有
- 地區篩選：台北・新北 / 桃園・新竹 / 台中 / 台南 / 高雄 + 店名/地址搜尋
- **📍 搵最近** — 定位後按距離排序，最近置頂
- 每間店：**Apple 地圖導航**（iPhone 優先）+ Google Maps，用真實地址導航
- 清單 + 距離 **離線可用**；地圖底圖（Leaflet/OSM）需網路，離線會自動 fallback 提示

## 資料

- 已「**提純**」為有辦官方賽事嘅店：**23 間**（台北新北 11 / 桃園新竹 3 / 台中 3 / 台南 3 / 高雄 3），純零售無賽事嘅已剔除。每間附 1-2 個 source。
- **✅ 2026 官方賽事 = 16 間**（已對寶可夢官方 2026/05–06 賽事頁核實）；**⚠️ 賽程待確認 = 7 間**（店仍營運但官方 2026 逐場排程未出）。App 內可按「✅ 只睇 2026 已確認賽事」篩選；未定位時 verified + 高信心排前。
- **One Piece 2026 係真 gap**：Bandai 官方台灣店賽只 surface 到 2024；2026 Store Tournament Vol.2 玩家報名 **2026/05/18** 才開放，故所有 OP 店標「賽程待確認」。臨行前重跑 Philips 第二輪可補回。
- 「🔵 有 One Piece」filter 含「兩款都有」店（共 6 間有 OP）。
- 地圖 pin = 約略座標（OSM Nominatim，20/23 街道級）；**導航用真實地址字串，較準**。雙子星民權店/森柒柒/紙牌屋門牌待店家確認，已標「地址待核」。
- ⚠️ 卡店常搬遷/結業，出發前務必致電 / 睇粉專確認。

## 重新整理資料

```
# 1. 改 shops_raw2.json（現行資料源；shops_raw.json 為第一輪保留）
python3 build.py            # geocode → 注入 index.html → 自動 bump sw.js VERSION
#   （python3 build.py --no-geo 可跳過 geocode 只重注入）
# 2. git add -A && git commit -m "data: refresh" && git push → Pages 自動 rebuild
```

`build.py` 已自動處理 SW VERSION bump（PWA cache invalidation）同 `DATA_UPDATED`，唔再使人手記。

## PWA / 離線

- 加入主畫面後係 standalone PWA；service worker (`sw.js`) precache app shell + 上限快取 OSM tiles → **第二次起離線都即開、行過嘅地圖都有**。
- **改任何嘢部署前必 bump `sw.js` 的 `VERSION`**（offline-first，唔 bump 用戶 cache 唔會更新）。
- 導航掣用 directions deeplink（Apple `?daddr=` / Google `dir/?api=1`）→ 一撳即由現在位置帶路。
- iOS 主畫面 icon：`icon.svg`（iOS 對 apple-touch-icon 偏好 PNG；如要最靚 icon 可日後加 180/512 PNG，現 SVG 已可用）。
- 其他：篩選狀態記憶（重開沿用）、空結果一鍵清篩選、卡片 🗺️ 跳地圖定位、重訪自動定位（已授權）、🔄 邊行邊更新（watchPosition opt-in）、Leaflet 改用 jsdelivr CDN（亞洲較穩）。

## 已知 gap

- 新北市除板橋 CardKame 外資料偏弱；新竹單一店（研究階段 directory 類網站抓唔到全名單）。
- 未經真實 iPhone 實機測試（見下）。

## 待人手確認（元芳無法代勞）

- 喺真實 iPhone Safari 打開，撳任一店「Apple 地圖導航」→ 應彈出 Apple Maps 並定位到該店。
- 「📍 搵最近」需 HTTPS 或 localhost 先攞到定位權限（`file://` 直開部分瀏覽器會擋 geolocation，但清單照用）。

資料更新：2026-05-16
