# 管理者工作室 設計系統 27.0.0 — 可引用的 CSS

由 `emit_css.py` 自七套元件庫示範頁產生，**不要手改**；改元件庫後重跑，並以 `verify_css_split.py` 確認示範頁改成引用這些檔之後每個元素的計算樣式一字不差。

## 怎麼用（七套都一樣）

```html
<html lang="zh-Hant" data-style="s6">                 <!-- 全站只選一套風格，建置時決定 -->
<link rel="stylesheet" href="tokens.css">            <!-- 1 字級、間距、圓角、高度、動態、層級 -->
<link rel="stylesheet" href="base.css">              <!-- 2 結構層 ＋ S1 材質（62 項元件、焦點環、佔位文字、RWD） -->
<link rel="stylesheet" href="style-s6.css">          <!-- 3 這一套的材質層；換風格只換這一行 -->
<script src="theme.js"></script>                     <!-- 色系切換與深淺模式 -->
```

順序不能換：風格層靠「排在後面」覆寫，權重與基準相同，不用 `!important`。

v20 起七套元件庫全部以 S1 為基底（共用同一份元件 HTML 與結構），`style-s1.css`〜`style-s7.css` 都是只有材質的薄檔，載法一律三檔。v19 的 S2〜S5「過渡版完整樣式表、不配 base.css」已退場——從 19.x 升上來的產品，S2〜S5 要把 `base.css` 加回去，數量調整器改用 S1 的 `<input>` 標記。

## 深色模式（S3 琉璃、S5 極光、S6 石墨）

深色是風格的**模式**，不是另一套風格：`style-s3.css`、`style-s5.css`、`style-s6.css` 各自內含深色。`<html data-theme="dark">` 強制深色、`data-theme="light"` 強制淺色、不寫則跟隨系統（`prefers-color-scheme`）。切換不換檔、不重載。品牌色的深色值由 `theme.js` 的 `DARK` 表（依風格分表）套用。其他四套（S1、S2、S4、S7）沒有深色，`data-theme="dark"` 對它們無效果（理由見規範 8.8）。

## 密度三檔（comfortable 寬鬆／normal 標準／compact 緊湊）

密度是第四條軸，三檔的數值全站只有一份（`base.css`），每套風格各有**預設檔**與**可選範圍**（規範 5.7 的矩陣）：S6 預設 normal，其餘六套預設 comfortable；S2、S4、S5、S7 鎖 compact。**不寫 `data-density` 就是該套的預設**（CSS 自己判斷，不靠 JS）；`<html data-density="normal">` 才回到標準，`"compact"` 緊湊。寬鬆把元件高度升到手機的觸控尺寸（44／44／40／44）、卡片與板內距 24、儲存格 16／20（列高 ≥56）、表格內文 B1、卡片與表格標題 H2；緊湊各縮一級（按鈕 32、儲存格 4／12）。**只改尺寸、不改顏色**，可與深色並用；768px 以下三檔收斂成一檔（normal）。密度是系統層的決定，頁面層只准往緊的方向覆寫一次。

## theme.js

```js
DS.applyTheme('c3')              // 切換色系 c1〜c12、sc1〜sc3；不適用於本風格的組合退回 c1，回傳實際套用的 key
DS.setColorScheme('dark')        // 'dark' | 'light' | 'system'；只對 DARK_STYLES（s3、s5、s6）有效
DS.setDensity('compact')         // 'comfortable' | 'normal' | 'compact'；不在本風格可選範圍的檔退回該套預設，回傳實際套用的檔
DS.onFallback = (asked, used) => notify(asked + ' 不適用於此風格，已切回 C1')   // 選配：退回時通知使用者
```

偏好以 localStorage 的 `ds.theme`、`ds.scheme`、`ds.density` 記住；網址參數 `?theme=c3` 優先。副色淺型（SC 系列）會自動加 `html.sc-light`，需加框線的組合加 `html.sc-adjust`。

## 瀏覽器支援

用到的新特性與最低版本：`:has()` Chrome 105／Safari 15.4／Firefox 121；`color-mix()` Chrome 111／Safari 16.2／Firefox 113；`:focus-visible` Chrome 86／Safari 15.4／Firefox 85；`aspect-ratio` Chrome 88／Safari 15／Firefox 89；`backdrop-filter` Chrome 76／Safari 9（S3 琉璃）／Firefox 103；`text-wrap:balance` Chrome 114／Safari 17.5／Firefox 121（只有前台 H0）。

**支援基線：Chrome／Edge 111+、Safari 16.4+（iOS 16.4+）、Firefox 121+。** 不支援 IE 與 Android 系統瀏覽器。再舊的瀏覽器會退化但不會壞版：`color-mix()` 失效處退回 `--acc-soft` 純色、`:has()` 只影響 SC 色系與 warning 同列的品牌標記、`text-wrap:balance` 失效只是斷行較差。

## 使用說明與範例

完整的工程師手冊在 `USAGE.md`（每個元件怎麼寫、禁止事項、交付前怎麼自己跑檢查）；`examples/` 是七張只引用本資料夾寫出來的範例頁，每一套風格一張、各在規範 8.7 的首選情境（後台、控制面板、品牌官網、點餐、預約、監控儀表板、說明中心），從 `examples/index.html` 進；新專案照情境挑一張當起點。`examples/same-markup.html` 是同一份標記換七套殼的示範，只說明「風格是殼」，不代表每套都適合那個情境。

## 檔案

| 檔 | 內容 | 大小 |
|---|---|---|
| `tokens.css` | token | 2.5 KB |
| `base.css` | 結構層 ＋ S1 材質 | 68.7 KB |
| `style-s1.css` | S1 奶油（材質在 base，空殼） | 0.3 KB |
| `style-s2.css` | S2 浮雕 | 14.9 KB |
| `style-s3.css` | S3 琉璃 淺色 ＋ 深色 | 80.0 KB |
| `style-s4.css` | S4 手帳 | 11.1 KB |
| `style-s5.css` | S5 極光 淺色 ＋ 深色 | 48.2 KB |
| `style-s6.css` | S6 石墨 淺色 ＋ 深色 | 28.4 KB |
| `style-s7.css` | S7 編輯 | 2.1 KB |
| `theme.js` | 色系、深淺模式與密度 | 17.4 KB |

## 版本

`27.0.0` 與《網頁設計規範 v27》同步；規範升版時本套檔案一起升版，產品把版號改掉就跟上。
