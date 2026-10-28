> 本檔是《網頁設計規範 v30》的一部分，全文見倉庫的 docs/spec.md。

## 十二、開發對接

這一章回答工程師開工第一天會問的四個問題：CSS 從哪裡引用、怎麼和框架搭、支援哪些瀏覽器、怎麼確認自己沒做歪。

### 12.1 檔案：引用，不複製

元件的樣式**不是**從示範頁 `components_s*.html` 的 `<style>` 複製出來用。公開倉庫 `art0428/webdesign` 的 `dist/` 由 `emit_css.py` 自七套元件庫產生，是唯一來源，每個檔頭都有版本號（與本規範同版）：

| 檔 | 內容 | 誰載 |
|---|---|---|
| `tokens.css` | 字級、行距、間距、圓角、高度、動態、層級 token（第四、五章） | 所有產品 |
| `base.css` | 結構層 ＋ S1 奶油的材質：62 項元件的 class、尺寸、焦點環、佔位文字、RWD、欄格 `.grid`（6.5）、密度三檔 `data-density`（5.7）。**S1 為基準** | 七套全部 |
| `style-s1.css` | 空殼（S1 材質已在 base），保持三檔載法一致 | S1 |
| `style-s6.css` | 石墨淺色 ＋ 深色（8.8），切換不換檔 | S6 |
| `style-s7.css` | 編輯的材質（明體標題、直角、欄線） | S7 |
| `style-s2.css`〜`style-s5.css` | 浮雕、琉璃、手帳、極光的材質（v20 起以 S1 為基底重建，與 S6、S7 同為薄檔）；`style-s3.css`、`style-s5.css` 另含深色（8.8，v23） | S2〜S5 |
| `theme.js` | 色系切換、鎖定規則、深淺模式、S6 深色底（`DARK_TINT`，8.8.5） | 所有產品 |

載入順序（七套相同）：

```html
<html lang="zh-Hant" data-style="s6">
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="base.css">
<link rel="stylesheet" href="style-s6.css">   <!-- 全站只換這一行 -->
<script src="theme.js"></script>
```

順序不能換：風格層靠「排在後面」覆寫，權重與基準相同，不用 `!important`。v20 起七套一律三檔；v19 的 S2〜S5 過渡版（兩檔、不配 `base.css`）已退場，從 19.x 升上來的 S2〜S5 產品要把 `base.css` 加回去，元件 HTML 照 S1 的語彙（數量調整器用 `<input>`）。

**為什麼是「一份結構 ＋ 每套一個薄材質檔」而不是七份完整檔**：七套的 CSS 有九成以上規則一字不差，七份完整檔等於同一條 `.btn` 存七份，改一次漏一處就是 v17 以前「S1 儲存格 16px、S2 20px」的翻版。結構層只有一份，風格層才改不壞結構。

**版本**：`dist/` 的版號跟本規範走（v30 ＝ `30.0.0`；沒有改 CSS 的版本不另發版號，例如 v21）。產品引用固定版號；規範升版，產品把版號改掉就跟上，diff 一目了然。

### 12.2 風格層純度（第六項檢查的一半）

`style-s*.css` 的薄檔只准出現顏色、框線、陰影、圓角、字型；**不得出現** `min-height`、`height`、`padding`、`margin`、`gap`、`font-size`、`line-height`、`z-index`、`width`、`display`、`position`。規範明訂的風格層例外（8.2 的 S7 外層區塊內距、4.1 的 S6 等寬字字距、8.2 的 S5 暈染背景 `body::before` 與 hero 暈點 `.statc.hero::after` 的定位）列在 `audit_layers.py` 的 ALLOW 表，其餘一律不通過。v20 起七個風格檔全查（v19 只查得了 S1、S6、S7）。這是 8.1「風格是殼，只覆寫材質」第一次有程式守著。

### 12.3 拆檔無損（第六項檢查的另一半）

`verify_css_split.py` 把每張示範頁的 `<style>` 全部拿掉、換成只引用 `dist/` 的三個檔，再渲染一次，逐元素比對 48 個計算屬性（顏色、框線、圓角、陰影、內距、字級、行距、層級、尺寸、`::before`／`::after`、佔位文字色）。七份元件庫（各以該套的預設密度：S6 標準、其餘寬鬆），加上 S3、S5、S6 深色的兩種入口（`data-theme="dark"` 指定、跟隨系統），加上其他密度檔（S6 的緊湊淺色與深色、S6 寬鬆，S1 的標準與緊湊，S7 標準），加上 S6 深色的中性石墨（指定、跟隨系統兩種入口；預設的跟隨色系含在 S6 深色那兩次裡，8.8.5）共 21 次比對 **0 差異**才算 `dist/` 可出貨（5.7）。這代表示範頁與 `dist/` 不可能分家：示範頁是來源，`dist/` 是產物，中間由程式保證一致。

### 12.4 theme.js

```js
DS.applyTheme('c3')          // 切換色系 c1〜c12、sc1〜sc3；不適用於本風格的組合退回 c1，回傳實際套用的 key
DS.setColorScheme('dark')    // 'dark' | 'light' | 'system'；只對 S3、S5、S6 有效，跟隨系統時監聽 prefers-color-scheme
DS.setDarkTint('neutral')    // 'follow'（預設）| 'neutral'；S6 深色底跟隨色系或中性石墨（8.8.5），其他風格無效果；DS.darkTint() 回目前生效的值
DS.labelTables()             // 依表頭替表格每格補 data-l（手機卡片列的欄名，6.3）；載入時自動跑一次，動態新增列後再呼叫
DS.setDensity('compact')     // 'comfortable' | 'normal' | 'compact'；不在本風格可選範圍的檔退回該套預設，回傳實際套用的檔（5.7 的矩陣 DS.DENSITY）
DS.onFallback = (asked, used) => notify(asked + ' 不適用於此風格，已切回 C1')
```

風格由 `<html data-style="s6">` 宣告，建置時決定、全站一套（8.1）。偏好以 localStorage 的 `ds.theme`、`ds.scheme`、`ds.darkTint`、`ds.density` 記住，網址參數 `?theme=c3`、`?tint=neutral` 優先（4.2 要求三處一致）。深色模式的品牌色由 `DARK` 表套用（8.8；v23 起依風格分表：`DARK.s3`、`DARK.s5`、`DARK.s6`），`--on-acc`、`--on-acc2`、`--acc2-text` 一併切換；S6 深色的跟隨色系由 `DARK_TINT` 注入六個面、四個語意淡底與品牌色（8.8.5）。

### 12.5 對接路線：純 CSS，不混第三方 UI 庫的外觀

產品以任何框架（React、Vue、Svelte、原生）開發都可以，但**元件的 HTML 照元件庫的 class 語彙寫，樣式只來自 `dist/`**；框架負責資料綁定與狀態，不負責長相。不得在同一產品混用 Ant Design、Element Plus、MUI 等第三方 UI 庫的元件外觀——它們的尺寸、圓角、焦點環、間距都不是本規範的，混進來第五、六項檢查一定不過。需要第三方的行為（日期選擇、虛擬捲動、拖曳）時，用無樣式（headless）的函式庫，外觀仍由 `dist/` 決定。

選這條路線的理由：七套風格切換天然支援、檢查腳本直接適用、沒有兩套 token 要對照。代價是複雜元件（級聯選擇、穿梭框、日期範圍）的行為要自己寫或找 headless 庫。

### 12.6 瀏覽器支援基線與降級

元件庫用到的新特性與最低版本：

| 特性 | 用在 | Chrome／Edge | Safari | Firefox |
|---|---|---|---|---|
| `:focus-visible` | 10.3 焦點環 | 86 | 15.4 | 85 |
| `:has()` | SC 色系與 warning 同列的品牌標記（3.4） | 105 | 15.4 | 121 |
| `color-mix()` | 警示條框線、S5 暈染 | 111 | 16.2 | 113 |
| `aspect-ratio` | 正圓元件、商品縮圖 | 88 | 15 | 89 |
| `backdrop-filter` | S3 琉璃面板 | 76 | 9（`-webkit-`） | 103 |
| `text-wrap:balance` | 前台 H0（4.2） | 114 | 17.5 | 121 |

**支援基線：Chrome／Edge 111+、Safari 16.4+（iOS 16.4+）、Firefox 121+。不支援 IE 與 Android 系統瀏覽器。** 這條線以內所有特性都原生可用。再舊的瀏覽器會退化但不會壞版：`color-mix()` 失效處退回 `--acc-soft` 純色；`:has()` 失效只影響 SC 色系與 warning 並存那一格的品牌標記顏色；`text-wrap:balance` 失效只是斷行較差；`backdrop-filter` 失效時 S3 面板退回 92% 不透明白。驗收：支援基線的最低版本各開一次元件庫示範頁，五項加第六項檢查全部通過。

---
