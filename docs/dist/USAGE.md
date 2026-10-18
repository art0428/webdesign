---
title: 設計系統使用說明
kicker: 管理者工作室 設計系統
subtitle: 給工程師的 dist/ 使用手冊（24.0.0）
source: 管理者工作室
date: 2026.10.18
highlight: 設計系統使用說明 v7
---

# 設計系統使用說明 v7

v7 變更範圍（24.0.0）：對應規範 v25（v25 只改前台示範頁、不動 CSS，`dist/` 維持 `24.0.0`）。2026-10-18 全面檢查發現第 7 節的對比組合數仍寫 v15 的「118 種」，改為 v23 起的 148 種並補上密集模式的實測範圍。其餘與 v6 逐字相同。

v6 變更範圍（24.0.0）：對應規範 v24——新增 S6 石墨的**密集模式**。第 3.2 節末加「密集模式」一段；第 1.1、1.5 節與文首版號改 `24.0.0`。其餘與 v5 逐字相同。

v5 變更範圍（23.0.0）：對應規範 v23——深色改為風格的模式，**S3 琉璃、S5 極光加入深色**（共 S3、S5、S6 三套）。第 3.2 節改寫；第 1.1、1.5 節與文首版號改 `23.0.0`。其餘與 v4 逐字相同。

v4 變更範圍（22.0.0）：對應規範 v21 與 v22。第 1.1、1.5 節與文首版號改 `22.0.0`；第 2.2 節補容器左右內距與「欄格」一段（`.grid`、`.col-*`、`.dense`，規範 6.5）；第 6 節補欄格在三個級別的欄數；第 8 節禁止事項補第 8、9 條（線條重疊、有框元件貼合，規範 9.3 第六、七條）；第 11 節第五項補 v21 量的兩件事。v21 沒有改 CSS，沒有另發 21.0.0。其餘與 v3 逐字相同。

v3 變更範圍（20.0.0）：S2〜S5 以 S1 為基底重建，**七套載法一律三檔**——第 1.3 節改為七套共用、第 1.4 節改寫成「從 19.x 升上來」、第 8 節禁止事項第 5 條、第 10 節範例頁（S3 的玻璃面板就是 `.board`、數量調整器的過渡覆寫刪除）、第 12 節一問改寫。其餘與 v2 逐字相同。

v2 變更範圍：第 10 節「範例頁」改為 `dist/examples/`——七套風格各一張、各在規範 8.7 的首選情境，`example.html` 改名為 `examples/same-markup.html`；第 10 節並寫明範例頁裡兩處「版面層保護」與一處過渡用覆寫的來歷；第 2.2 節補 flex 容器 `align-items:center` 一句；第 12 節新增一問。其餘與 v1 逐字相同。

這份是給前端工程師看的：拿到 `dist/` 之後怎麼開工、每個元件怎麼寫、哪些事不能做、交付前怎麼自己檢查。規則的「為什麼」在《網頁設計規範 v24》，這裡只講「怎麼做」。本文件會同步複製成 `dist/USAGE.md`，跟著檔案一起發。

## 1. 五分鐘上手

### 1.1 拿檔案

`dist/` 在公開倉庫 `art0428/webdesign`。十一個檔，檔頭都有版號 `24.0.0`，與規範同版。**不要**從示範頁 `components_s*.html` 複製 `<style>`——那是來源，`dist/` 才是產物，複製的那一刻起你的產品就和元件庫分家了。

### 1.2 選一套風格，寫在 `<html>` 上

全站只有一套風格，建置時決定，寫在根元素：`<html lang="zh-Hant" data-style="s6">`。七套的代號：`s1` 奶油、`s2` 浮雕、`s3` 琉璃、`s4` 手帳、`s5` 極光、`s6` 石墨、`s7` 編輯。該選哪套看規範 8.7 的選型表；後台與資料密集頁用 `s1` 或 `s6`。

### 1.3 載入（七套相同）

```html
<!DOCTYPE html>
<html lang="zh-Hant" data-style="s6">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="dist/tokens.css">     <!-- 1 字級、間距、圓角、高度、動態、層級 -->
<link rel="stylesheet" href="dist/base.css">       <!-- 2 結構層 ＋ S1 材質：62 項元件、焦點環、佔位文字、RWD -->
<link rel="stylesheet" href="dist/style-s6.css">   <!-- 3 這一套的材質層；換風格只換這一行 -->
</head>
<body data-type="productive">                      <!-- 後台、購物車、結帳；前台閱讀型頁面改 expressive -->
  …
<script src="dist/theme.js"></script>
</body>
</html>
```

順序不能換：風格層靠「排在後面」覆寫，權重與基準相同，整套沒有一個 `!important` 是給產品用的。S7 編輯要多載明體：`family=Noto+Serif+TC:wght@700;900`。

### 1.4 從 19.x 升上來的 S2〜S5 產品

19.0.0 的 S2〜S5 是「過渡版」：完整樣式表、只載兩檔、不配 `base.css`。20.0.0 起這四套以 S1 為基底重建，和其他三套一樣載三檔。升級時做兩件事：

1. 在 `tokens.css` 與 `style-s*.css` 之間加回 `<link rel="stylesheet" href="dist/base.css">`。
2. 數量調整器改用 S1 的標記：`<span class="qty"><button>－</button><input class="num" value="1"><button>＋</button></span>`（19.x 的 `<span class="disp">` 不再有樣式）。其他元件的 class 語彙七套本來就相同。

材質（凸凹陰影、毛玻璃、手繪框、極光暈染）都還在，跟著 `style-s*.css` 走；頁面不用再加 `.up`、`.glass`、`.wob`、`.org` 這類修飾 class——`.board`、`.card`、`.statc` 本身就帶著那一套的材質。

### 1.5 升版

規範升一版、`dist/` 升一版。產品把 `24.0.0` 的檔換成下一版的檔，跑一次第 11 節的檢查，看 diff 就知道哪裡變了。不要在產品裡修改 `dist/` 的任何檔案——要改，回元件庫改，重新產生。

## 2. 頁面骨架

### 2.1 容器

| class | 用途 | 說明 |
|---|---|---|
| `.board` | 頁面上的大區塊 | 白底、1px 線、16px 圓角（S6 12px、S7 直角＋上緣 2px 墨線）。一頁可以有多個，區塊之間留 `--sp-6` |
| `.card` | 卡片 | `<div class="card"><div class="card-title">標題<span class="hint">副標</span></div><div class="card-body">內容</div></div>`；可點擊的加 `.click` |
| `.cardx` | 摘要方塊（金額合計） | `.ct` 標題、`.cb` 內容、`.sumrow` 一列、`.sumrow.total` 合計列 |
| `.tblwrap` | 表格容器 | 見第 6 節 |

### 2.2 間距與排版：只用 token，不寫數字

所有 `margin`、`padding`、`gap` 只取 `--sp-1`〜`--sp-10`（4／8／12／16／20／24／32／40／48／64px），連號命名。常用：元件之間 `--sp-3`、區塊內元素 `--sp-4`、區塊之間 `--sp-6`、卡片內距 `--sp-4 --sp-5`。

```css
.page{display:grid;gap:var(--sp-6);padding:var(--sp-6);max-width:1060px}   /* 內容區最大 1060px（規範 9.1） */
.toolbar{display:flex;gap:var(--sp-2);flex-wrap:wrap;align-items:center}
```

字級只用 `var(--fs-xx)`，而且**寫了字級就要寫同代號的行距** `var(--lh-xx)`：

```css
.note{font-size:var(--fs-b3);line-height:var(--lh-b3);color:var(--muted)}
```

十四級代號：`d1` 顯示數字、`h0` 展示標題（只給前台 Hero）、`h1` 頁面標題、`h2` 區塊與彈窗標題、`h3` 卡片標題列、`b1` 內文、`b2` 表格內文、`b3` 說明、`l1` 欄位標籤、`l2` 微標籤、`n1`〜`n4` 金額與編號。數字、金額、編號加 `.num`（Arial、等寬數字）。

把按鈕、膠囊排成一列的 flex 或 grid 容器，記得寫 `align-items:center`：預設的 `stretch` 會把同一列的一般按鈕（38px）拉到主按鈕的 40px，看起來像元件壞了，其實是容器的事。範例頁的 `.row`、`.sp` 都這樣寫。

**容器左右內距**（規範 6.2）：寬以上 `--sp-6`（24px）、平板 `--sp-5`（20px）、768 以下 `--sp-4`（16px）。這個內距同時是欄格的外邊距。

**欄格**（規範 6.5，22.0.0 起在 `base.css`）：頁面上不同區塊怎麼分寬度，用 12 欄格，不要自己量像素。

```html
<div class="grid">                       <!-- 欄距 --sp-6；要密一點加 .dense（--sp-3） -->
  <div class="statc col-3">…</div><div class="statc col-3">…</div><div class="statc col-3">…</div><div class="statc col-3">…</div>
  <section class="board col-8">主體</section><aside class="board col-4">輔助</aside>
</div>
```

跨欄只有五種：`.col-12`、`.col-6`×2、`.col-8`＋`.col-4`、`.col-4`×3、`.col-3`×4。平板與中級別自動變 8 欄（`.col-3`、`.col-4` 佔半寬，其餘滿寬），480 以下 4 欄全部堆疊、欄距自動收成 `--sp-3`。固定寬的側欄、摘要面板、側滑面板不放進欄格。一批同樣的卡片排幾欄（商品卡、文章卡）照第 6 節的網格清單，不必套欄格。完整用法看 `examples/s1-admin.html` 的統計卡列。

### 2.3 顏色：只用變數

| 變數 | 用途 |
|---|---|
| `--acc` `--acc-soft` `--acc-deep` | 主色：主按鈕、選中、連結、聚焦框。淡底 `--acc-soft` |
| `--acc2` `--acc2-soft` `--acc2-deep` `--acc2-text` | 副色：品牌標記、圖表第二數列，每頁最多三處；承載文字一律 `--acc2-deep` |
| `--ink` `--muted` | 主文字、次要文字 |
| `--line` `--line-2` | 框線。**不得當文字色** |
| `--page` `--card` `--paperc` `--sel` | 頁面底、卡片底、淡帶、選取底 |
| `--err` `--wrn` `--ok` `--info` 與 `-soft` | 語意色與淡底 |
| `--d1`〜`--d8` | 圖表數列色（三個數列以上才用，固定順序） |

整個產品不應該出現任何 `#` 色碼，除了純黑純白與陰影用的半透明黑。

## 3. 色系與深淺模式

### 3.1 色系切換

```js
DS.applyTheme('c3')      // c1〜c12 核心、sc1〜sc3 特殊；回傳實際套用的 key
DS.THEMES                // 十五組的定義（名稱、色值、可用風格）
DS.allowed('sc1')        // 本風格可不可以用這組
DS.onFallback = (asked, used) => toast(asked + ' 不適用於此風格，已切回 C1')
```

不適用於本風格的組合會退回 `c1`，不會靜默套用；`onFallback` 讓你通知使用者。選擇介面照規範 3.10：十二顆核心一段、分隔線後 SC 一段，不適用的 `disabled` 反灰劃線。偏好存在 localStorage `ds.theme`，網址參數 `?theme=c3` 優先——後台設定頁、使用者偏好、網址三處必須一致（規範 4.2）。

淺型副色（SC 系列）會在 `<html>` 加 `sc-light`，需要加框線的組合加 `sc-adjust`，元件庫的 CSS 已處理，不用自己寫。

### 3.2 深淺模式（S3 琉璃、S5 極光、S6 石墨）

```js
DS.setColorScheme('dark')     // 'dark' | 'light' | 'system'
```

深色是風格的**模式**，不是另一套風格：不換風格檔、不改 HTML，`style-s3.css`、`style-s5.css`、`style-s6.css` 自己就含深色。對應 `<html data-theme="dark|light">`，不寫就跟隨系統並監聽變化；品牌色的深色值由 theme.js 的 `DARK` 表（依風格分表）套用，`--on-acc`、`--on-acc2`、`--acc2-text` 一併切換。給使用者的選項固定三個：淺／深／跟隨系統。S1、S2、S4、S7 沒有深色，呼叫無效果（規範 8.8 寫了理由）——需求裡有夜間模式就不要選這四套。

元件庫示範頁也是同一頁切換：網址加 `.dark`（例如 `components_s3_glaze.html#c1.dark`），或按頁首色系列最後的「模式」鈕；設計系統瀏覽器在「風格」下面有「模式」一列。

**密集模式（S6，規範 5.7）**

```js
DS.setDensity('compact')      // 'compact' | 'normal'；只對 S6 有效
```

對應 `<html data-density="compact">`。按鈕與輸入框 32px、小按鈕 28px、狀態膠囊 20px、表格儲存格上下 4px 左右 12px（列高約 30px），卡片與板的內距縮一級、`.grid` 自動改緊湊欄距；字級、顏色不變，可與深色並用。768px 以下自動回到標準（觸控下限 44px）。規則在 `base.css`，**不要自己寫一套更緊的尺寸**——要密就開這個模式，第五項檢查才量得到。示範頁網址加 `.dense`（例如 `#c1.dense`、`#c1.dark.dense`），瀏覽器的「密度」列可切換。

填色上的字不要寫死 `#fff`：主按鈕文字用 `var(--on-acc, #fff)`，深色模式會自動變成深色字。

## 4. 元件寫法

下面是最常用的三十項，class 語彙七套相同、不得自創同義名。完整 62 項的標記看元件庫示範頁對應區段（`components_s1_cream.html`），**只抄 HTML，不抄 CSS**。

### 4.1 按鈕

```html
<button class="btn primary">送出訂單</button>      <!-- 每頁最多一顆實心 -->
<button class="btn ghost">＋ 代客下單</button>      <!-- 主色外框：強調 -->
<button class="btn">下載 Excel</button>              <!-- 灰框：一般 -->
<button class="btn sm">預覽</button>                 <!-- 小：表格列內、工具列 -->
<button class="btn danger">取消訂單</button>         <!-- 紅框：不可回復，一律二次確認 -->
<button class="btn primary" disabled>送出訂單</button>
```

高度 40／38／32px（手機 44／44／40）由 `base.css` 鎖定，**不要自己設 `height` 或 `padding`**。處理中：加 `disabled` 並在文字前放 `<span class="spin"></span>`。圖示按鈕要 `aria-label`，點擊範圍 44×44。

### 4.2 輸入框與表單

```html
<div class="field">
  <label for="po">貴司採購單號 <span class="req">*</span></label>
  <input id="po" class="num" placeholder="PO-2026-xxxx">
  <div class="msg">格式：PO-年份-流水號</div>              <!-- 說明文字（選用） -->
</div>
<div class="field err">                                    <!-- 錯誤態 -->
  <label for="len">裁切長度 mm <span class="req">*</span></label>
  <input id="len" class="num" value="7500">
  <div class="msg">超出範圍：100–6000 mm</div>              <!-- 說怎麼修，不只說錯了 -->
</div>
<div class="field dis"><label>建立者</label><input disabled value="陳品妤"><div class="msg">由 Email 解析建立，不可修改</div></div>
<div class="field"><label for="addr">送貨地址</label><select id="addr"><option>桃園廠</option></select></div>
<div class="txa"><textarea rows="3"></textarea><div class="cnt2">31 / 200</div></div>
```

一定要有 `<label for>`，不可只靠 placeholder 當標籤。錯誤訊息用 `aria-describedby` 關聯。手機上輸入框字級自動 16px（防 iOS 放大），不用自己寫。

搜尋框：`<div class="search"><svg …放大鏡…></svg><input placeholder="搜尋 單號 / 客戶"></div>`。

### 4.3 核取、單選、開關、數量

```html
<span class="check on"><i></i>端蓋 ×2</span>
<span class="check"><i></i>防震墊片組</span>
<span class="check ind"><i></i>部分已選（3 / 8）</span>          <!-- 半選 -->
<span class="check dis"><i></i>代客戶報關<span class="sub">未開通</span></span>
<span class="radio on"><i></i>月結 30 天 <span class="sub">貴司核定條件</span></span>
<span class="sw2 on"><span class="tk"></span>商品上架中</span>    <!-- 開關：立即生效的設定才用 -->
<span class="qty"><button aria-label="減少">－</button><input class="num" value="100"><button aria-label="增加">＋</button></span>
```

這些示範是 `span` 加 `i`；要能鍵盤操作時，請用真正的 `<input type="checkbox">` 包在 `<label class="check">` 裡，再把 `<i>` 當視覺框——樣式一樣適用。停用的選項要說明原因（`.sub`），不要隱藏。

### 4.4 選擇類：下拉、多選、篩選膠囊、選項 chip、分段控制

```html
<div class="dd">                                              <!-- 下拉：加 .open 展開 -->
  <div class="trg">桃園廠 <span class="car">▼</span></div>
  <div class="menu"><div class="mi on">桃園廠</div><div class="mi">台中倉</div><div class="mi sep">＋ 新增地址</div></div>
</div>
<div class="mck on"><i></i>A 級經銷</div>                     <!-- 多選面板內的一列 -->
<button class="pillf on">全部<span class="n">128</span></button><button class="pillf">逾期<span class="n">2</span></button>
<span class="chip on">鋁合金 6061</span><span class="chip">不鏽鋼 304</span><span class="chip off">電解拋光</span>  <!-- off 不可選：劃線不隱藏 -->
<span class="seg"><button class="on">全部</button><button>待確認</button><button>備貨中</button></span>
```

篩選膠囊「全部」永遠第一個、帶數字；超過七個改多選下拉。分段控制不超過五段。

### 4.5 狀態、標籤、角標

```html
<span class="st wrn">● 待確認</span> <span class="st acc">● 備貨中</span> <span class="st ok">● 已出貨</span>
<span class="st err">● 已取消</span> <span class="st gray">● 已結案</span>
<span class="tag acc">3 屬性</span> <span class="tag gray">可加購</span> <span class="tag err">必選</span>
<span class="badge"><button class="btn sm">收件匣</button><b class="num">7</b></span>
待處理 <span class="count err">12</span>
<span class="aibadge">◆ AI 解析</span>
```

狀態一律「符號＋文字」，顏色對應：待人處理 `wrn`、進行中 `acc`、成功 `ok`、異常 `err`、封存 `gray`。數字角標一律紅。

### 4.6 卡片、統計卡、描述清單

```html
<div class="card"><div class="card-title">出貨備註<span class="hint">選填</span></div><div class="card-body">…</div></div>
<div class="statc hero"><div class="k">待確認</div><div class="v num">3<small>張</small></div><div class="delta up">▲ 2 vs 昨日</div></div>
<dl class="desc"><dt>單號</dt><dd class="num">SO-260907-003</dd><dt>備註</dt><dd class="full">跨兩欄的長文</dd></dl>
```

一頁最多一張 `.statc.hero`。升降用箭頭加文字，顏色跟好壞不跟方向。

### 4.7 導覽：側欄項目、頁籤、麵包屑、分頁

```html
<button class="nitem on"><svg …></svg>訂單管理</button><button class="nitem">商品與規格</button>
<span class="tabs"><button class="tab on">商品目錄</button><button class="tab">購物車</button></span>
<span class="crumb">宏達金屬 ／ 訂單管理 ／ <b class="num">SO-260830-012</b></span>   <!-- 第三層以上才出現 -->
<span class="p4"><button>‹</button><button class="on">1</button><button>2</button><button>3</button><button>…</button><button>9</button><button>›</button></span>
```

分頁全站只用 `.p4`（底線數字式），放表尾右側；上千筆改 `.p5` 跳頁式。

### 4.8 回饋：警示條、提示框、Toast、空狀態、骨架屏、進度

```html
<div class="alert err"><i>!</i><div><b>匯入失敗</b><p>第 12 列的料號不存在。修正後重新上傳即可。</p></div></div>
<div class="alert wrn"><i>!</i><div><p>價格表已過期，下單前請先更新。</p></div><button class="btn sm">更新</button></div>
<div class="alert ok"><i>✓</i><div><p>36 筆訂單同步完成。</p></div><button class="x" aria-label="關閉">×</button></div>
<div class="notice">您的專屬價已套用：<b>A級經銷 92 折</b>。</div>
<div class="toast"><i></i>訂單已建立 SO-260830-013</div>
<div class="empty"><b>還沒有訂單</b><br>分享門市連結給客戶，或用「代客下單」建立第一張<br><br><button class="btn ghost sm">＋ 代客下單</button></div>
<div class="skel"><div class="skrow"><div class="sk" style="width:110px"></div><div class="sk" style="flex:1"></div></div></div>
<div class="bar"><i style="width:62%"></i></div>
```

警示條四條守則：標題選用、動作最多一顆且是文字鈕、錯誤與警告不給關閉鈕、動作與關閉鈕和內文同一基線（CSS 已處理）。Toast 三秒自動消失、可手動關；一直要看到的訊息用警示條。表格載入用骨架屏不用轉圈。

### 4.9 覆蓋層：彈窗、側滑面板、就地確認、提示氣泡、動作選單

```html
<div class="modal"><div class="mh">確認出貨？</div><div class="mb">出貨後將無法修改品項與數量。</div>
  <div class="mf"><button class="btn">返回</button><button class="btn primary">確認出貨</button></div></div>
<div class="drawer"><div class="dh">SO-260907-003 <span class="st wrn">● 待確認</span><button class="x" aria-label="關閉">×</button></div>
  <div class="db">…</div><div class="df"><button class="btn sm">開啟完整頁</button><button class="btn primary sm">確認訂單</button></div></div>
<div class="popwrap"><button class="btn sm danger">刪除</button>
  <div class="pop"><div class="pt"><i>!</i>刪除這筆報價？</div><div class="pb">30 天內可還原。</div>
  <div class="pf"><button class="btn sm">取消</button><button class="btn sm danger">刪除</button></div></div></div>
<span class="tipwrap"><span class="tip">依客戶等級計算後的折後價</span><button class="btn sm">折後單價 ⓘ</button></span>
<div class="dd"><button class="kebab" aria-label="更多動作">⋯</button><div class="menu"><div class="mi">檢視明細</div><div class="mi sep danger">取消訂單</div></div></div>
```

層級已由 token 決定（`--z-pop` 20、`--z-drawer` 30、`--z-modal` 40、`--z-toast` 50），**不要自己寫 `z-index` 數字**；吸附表頭、頂列用 `var(--z-sticky)`。彈窗開啟時焦點移入、關閉時歸還原按鈕、Esc 可關（這是行為，要自己寫）。危險型彈窗主按鈕用 `.btn.danger` 並寫明後果。

### 4.10 其他

時間軸 `ul.tl > li.acc|ok|err`、步驟 `.stepper > .sp.done|.cur`、上傳區 `.upload` 與 `.upfile.ok|.err`、折疊 `.acc-p > .arow > .ahead + .abody`、頭像 `.avatar`（`.sm` 小）、分隔 `.divider`／`hr.hr`／`.vdiv`、圖表容器 `.chart > .chh + svg`。圖示一律 Lucide，尺寸 16／20／24／48、線寬 2、顏色 `currentColor`。

## 5. 表格

```html
<div class="tblwrap">
  <div class="tcap"><b>訂單</b><span class="cnt">36 筆 · 篩選 3</span>
    <span class="sp"><button class="pillf on">全部</button><button class="pillf">待確認</button><button class="btn sm">下載 Excel</button></span></div>
  <table class="t">
    <thead><tr><th class="ck"><span class="check"><i></i></span></th><th>單號</th><th>客戶</th><th>狀態</th><th style="text-align:right">金額</th><th style="text-align:right">到貨</th><th></th></tr></thead>
    <tbody>
      <tr><td class="ck"><span class="check"><i></i></span></td><td class="dt">SO-260830-012</td><td>大同機械</td>
          <td><span class="st wrn">● 待確認</span></td><td class="amt">28,166</td><td class="dt">09/08</td><td><button class="btn sm">預覽</button></td></tr>
    </tbody>
  </table>
  <div class="tfoot"><span class="p4">…</span></div>
</div>
```

- 數字靠右：金額 `.amt`、日期與單號 `.dt`（S6 自動等寬字）；千分位必加、負數紅、貨幣前綴 `<small>NT$</small>` 自動縮小。
- 儲存格內距 12／20 由 `base.css` 決定，列高由內容決定（純文字 46px、含膠囊約 50px），**不要設列高**。
- 手機（<768px）：`base.css` 目前讓 `.tblwrap` **水平捲動**。規範 6.3 要求的「轉卡片列、每格帶欄名、不做水平捲動」還沒進元件庫（已列入缺口第二批次）；在那之前，手機版的資料表請自己用 `data-l` 寫卡片化，或限制欄數到五欄以內。
- 載入中用 `.skel`，無資料用 `.empty`，載入失敗用 `.empty` 加重試鈕。

## 6. RWD 要點

斷點 1024／768／480；級別名稱（規範 6.1）是緊湊 <480、中 480〜767、平板 768〜1023、寬 1024〜1279、特寬 ≥1280，欄格分別是 4／8／8／12／12 欄。768 以下 `base.css` 已處理：輸入框 16px（防 iOS 放大）、可點元件 44px、欄位與面板滿版、表格容器可捲。要你自己做的：側欄改成覆蓋式抽屜（漢堡鈕 44px）、主要動作滿版、480 以下單欄（商品卡列表例外維持兩欄）、資料表卡片化（見第 5 節）。任何寬度 body 不得橫向捲動——flex 子項記得 `min-width:0`、不寫固定寬度、不用負 margin、長文字容器允許換行或省略。

## 7. 無障礙：已經幫你做的，和要你自己做的

已內建：鍵盤焦點環（`:focus-visible` 2px 主色）、佔位文字對比、所有文字色與底色的對比（148 種風格 × 色系組合實測 0 不及格：淺色 103 種，加 S3、S5、S6 深色各 15 種；S6 的密集模式與深色加密集另各測 15 種）、停用態不用透明度、減少動態時轉場歸零。

要自己做：每個輸入框有 `<label for>`；純圖示按鈕 `aria-label`；裝飾性圖示 `aria-hidden="true"`；狀態不只靠顏色（符號＋文字的 class 已帶，文字要你填）；彈窗焦點管理與 Esc；Tab 順序與視覺一致；不要為了「乾淨」寫 `outline:none`。

## 8. 禁止事項（第五、六項檢查會擋）

1. 寫死字級、間距、顏色、圓角、高度、z-index 的數字。
2. 在產品 CSS 裡覆寫元件的 `min-height`、`padding`、`font-size`、`line-height`；要密一點的表格也不是改列高。
3. 複製示範頁的 `<style>`、修改 `dist/` 的檔案。
4. 混用第三方 UI 庫（Ant Design、Element Plus、MUI 等）的元件外觀；需要行為用 headless 庫。
5. 同一產品用兩套風格；任何一套少載 `base.css`。
6. `outline:none` 不補替代；`!important`。
7. 自創 class 同義名（`.button`、`.btn-primary`、`.status`）——七套共用同一份語彙，檢查腳本認的是元件庫的 class。
8. 一處分隔放兩條線：區塊標題用了延伸細線，下面就不再放分隔線或 `.card-title` 底線；兩個有框容器相鄰不再加分隔線（規範 9.3 第六條）。
9. 有框元件貼在一起：按鈕列與輸出框、卡片與卡片、輸入框與按鈕之間至少 `--sp-3`；一排並排的小按鈕、chip、膠囊可以 `--sp-2`（規範 9.3 第七、十條）。

## 9. 需要新元件時

先用既有元件組合。真的要新增：到元件庫提 PR，七套都要做、過六項檢查、寫進規範第七章，再進產品。風格層的例外（例如某套要不同圓角）寫進規範第八章才算數。產品裡不要長出規範外的元件。

## 10. 範例頁

`dist/examples/` 有八張頁面，全部只引用 `dist/`，頁面自己的 CSS 只做排版（grid、flex、gap，一律用 token），元件 HTML 照第 4 節的 class 寫。從 `examples/index.html` 進。

**七套風格不是七種口味，是七種情境。** 規範 8.7 的選型表說：看得久、資料多的系統只考慮 S1 與 S6；以閱讀為主的前台先看 S7；S2、S3、S4、S7 不當資料密集後台的主風格。所以每一套的範例都是它的首選情境，不是同一張後台換皮：

| 檔 | 風格 | 情境 | 字級組 | 看什麼 |
|---|---|---|---|---|
| `s1-admin.html` | S1 奶油 | 後台管理（訂單列表） | Productive | 側欄框架、統計卡、篩選列、資料表、分頁；任何後台的預設起點 |
| `s2-console.html` | S2 浮雕 | 少資料多操作的工具（出貨站控制面板） | Productive | 大開關、分段控制、數量、整排按鈕；資料很少、操作很多 |
| `s3-brand.html` | S3 琉璃 | 品牌官網／產品發表 | Expressive | Hero、特色卡、CTA；**所有文字都在 `.board` 玻璃面板上**（S3 的 `.board` 本身就是玻璃），不直接壓漸層（規範 8.2） |
| `s4-menu.html` | S4 手帳 | 餐飲前台（點餐） | Expressive | 菜單卡、配料 chip、數量、底部購物條；手機 480 以下兩欄 |
| `s5-booking.html` | S5 極光 | 服務型前台（預約與會員中心） | Expressive | 步驟、日期與時段膠囊、預約摘要；漸層只在強調按鈕與 hero 數字 |
| `s6-dashboard.html` | S6 石墨 | 資料密集儀表板（監控） | Productive | KPI、折線圖（SVG 只用 `var(--acc)`／`var(--err)`）、服務健康、告警表；右上角切淺／深／跟隨系統 |
| `s7-article.html` | S7 編輯 | 內容與閱讀（說明中心文章） | Expressive | 目錄、明體標題、40 字行寬的長文、提示框與警示條 |
| `same-markup.html` | 全部 | 同一份標記換七套殼 | — | 只說明「風格是殼」（規範 8.1），不代表每套都適合那個情境 |

新專案照情境挑一張當起點；照抄它的 `<link>` 順序與 `data-style`，把內容換掉就是第一頁。

範例頁的 `<style>` 裡有兩處不是純排版，開工前先知道來歷，免得照抄成習慣：

1. `.t .btn.sm,.t .dt{white-space:nowrap}`：窄欄裡按鈕文字與單號不得折行。這是元件庫還沒規範到的一條（缺口盤點第二批次），之後會收進 `base.css`，到時這條可以刪。
2. `@media (max-width:767px){.tcap{flex-wrap:wrap}…}`：表格標題列在手機上允許換行，否則篩選膠囊會被擠成兩行。同上，屬於第二批次的「手機表格」缺口。

範例頁的驗證：`check_examples.py` 在 1100 與 390 寬各渲染一次，要求 0 個 JavaScript 錯誤、`scrollWidth` 不大於視窗寬、按鈕／輸入框／膠囊／chip 的高度與規範 5.4 差 ≤1px（S6 另測深色跟隨系統與手動切回淺色）。目前八張全部通過，截圖在 `report/size_audit_v3/`。

## 11. 交付前自己跑六項檢查

通用版檢查腳本在 `skills/ui-design-format/scripts/`（第一至四項；第五、六項只在維護元件庫時跑，不隨公開版發佈），需要 Python 3 與 Playwright（`pip install playwright && playwright install chromium`）。對自己的頁面跑：

| 項 | 腳本 | 怎麼跑 | 通過標準 |
|---|---|---|---|
| 一 對比 | `audit_contrast.py` | 指向你的頁面（含佔位文字） | 每個文字節點 ≥4.5（大字 ≥3.0），0 不及格 |
| 二 標尺 | `check_tokens.py` | 掃你的 CSS | 字級、行距、間距、字距全在表上 |
| 三 行高 | `audit_lineheight.py` | 靜態＋渲染 | 字級與行距同代號，0 不合規 |
| 四 溢出 | 任何瀏覽器 | 390px、768px | `scrollWidth` 不大於視窗寬 |
| 五 尺寸 | `audit_sizes.py` | 渲染你的頁面 | 按鈕、輸入框、膠囊高度與規範差 ≤1px；儲存格 12／20；標籤到輸入框 8；焦點環 2px 主色；有框元件相距不低於 8px、兩條線之間要有內容（v21） |
| 六 拆檔 | `verify_css_split.py`、`audit_layers.py` | 只有改元件庫時要跑 | dist 與示範頁 0 差異；風格層 0 結構屬性 |

要登入的單頁應用（SPA）：用 Playwright 先登入、列出要掃的路由、每頁跑一遍，接進 CI（每次提交自動跑）。公開倉庫 `scripts/` 的通用版腳本接受網址。

## 12. 常見問題

**按鈕比我想的高／矮。** 高度是 token 鎖的（主 40、一般 38、小 32；手機 44）。你的頁面在 768px 以下？那就是 44，正確。

**我需要一個 36px 的按鈕。** 沒有。三個尺寸對應三種層級，第四個尺寸要先進規範。

**我的 S2〜S5 頁面升到 20.0.0 之後沒有框線、按鈕變成瀏覽器預設。** 少載了 `base.css`，見 1.4。

**深色模式下主按鈕的字是黑的。** 正確。規範 8.8：深色的填色上一律深色字（對比才夠），由 `--on-acc` 決定。

**字放大 150% 版面壞了。** 檢查有沒有寫死 `height` 或 px 的字級；元件全部是 `min-height` 與 rem，字放大時會跟著長。

**color-mix 在舊 Safari 沒效。** 支援基線 Safari 16.4+。更舊的會退回 `--acc-soft` 純色，不會壞版（規範 12.6）。

**我想用 Tailwind。** 可以用它排版（grid、flex、gap），但間距值要對應到 `--sp-*`，元件外觀仍由 `dist/` 決定；不要用它的預設間距與顏色。

**我的系統同時有後台和前台，要用兩套風格嗎？** 不要。規範 8.1 說一個產品一套風格。後台和前台差的是字級組（`data-type="productive"` 與 `"expressive"`），不是風格；同一套 S1 可以同時長出 `s1-admin.html` 那樣的後台和一張前台頁。真的要兩種氣質，做成兩個產品、各自一套。
