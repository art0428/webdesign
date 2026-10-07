---
name: "ui-design-format"
description: "通用的網頁介面設計系統（2026-10 v10 規範）。凡是要產生或修改任何網頁介面、HTML prototype、後台管理、表單頁、訂購或點餐系統、web app、landing page、互動 demo、元件庫，或使用者提到「UI」「介面」「網頁設計」「prototype」「做一個系統」「前端」時，必須先讀本 skill 再動工，即使使用者沒提到風格。內容：六套風格（S1 奶油、S2 浮雕、S3 琉璃、S4 手帳、S5 極光、S6 石墨）擇一開發；十二組核心 ＋ SC1 特殊色系由使用者在系統內切換（含鎖定規則）；四層色彩、十三級字級、間距標尺、圓角、元件高度、RWD、62 項元件清單與四項自動檢查。"
---

# 管理者工作室 網頁介面設計系統（skill 版）

本 skill 是《網頁設計規範 v10》與其推導調研的實作摘要。規範全文依章節放在本資料夾的 `references/`，六套元件庫與 `tokens.css` 在 `assets/`，四項交付前檢查的腳本在 `scripts/`（索引見文末第 11 節）。**本 skill 與 `references/` 衝突時以 `references/` 為準。**

頁面上的品牌名稱一律用使用者自己的專案名稱。`assets/` 範本裡的「管理者工作室」只是範例品牌，複製標記時要換掉。術語第一次出現要白話解釋。

## 0. 三十秒摘要

一、**工程師選一套風格開發，全站只有一套風格**；風格是「殼」，只覆寫表面材質，不碰結構、色彩變數、字級。
二、**系統內建十二組核心色系 ＋ SC1 特殊色系讓使用者切換**，切換只換第一層七個 CSS 變數；第二層灰階、第三層語意色、第四層資料視覺化色板永不隨色系變。不適用於該風格的色系要鎖住，不合法組合退回 C1 並提示，不靜默套用。
三、色彩、字級、間距、圓角一律引用 token，**不寫死數字**；字級與間距用 rem（1rem ＝ 10px），圓角框線斷點用 px；所有元件 `min-height` 不用 `height`。
四、交付前跑四項檢查：對比稽核（每個文字節點 ≥4.5）、標尺合規（字級、行距、間距、字距全在表上）、**行高配對**（字級與行距必須同代號）、390px 不橫向溢出。
五、**框線色不得拿來當文字色**。`--line` 與 `--line-2` 是給線條用的，拿來寫「不重要的字」（月曆的非本月日期、麵包屑的分隔符）對比只有 1.4，必然不及格；要淡就用 `--muted`。
六、**半透明面板上不放彩色小字**。琉璃與極光的面板是半透明的，彩色小字壓上去只剩 3.4〜4.2，改用主文字色；方向用箭頭符號加文字表達，不靠顏色。

## 1. 工作流程

1. **選風格**：依系統類型從六套選一（見第 2 節矩陣）。後台、資料密集預設 S1 奶油；要「工具感」而不是「文件感」的後台、開發者介面、資料密集儀表板選 S6 石墨；不確定就 S1。
2. **選預設色系**：從 C1〜C12 選一組當預設（新專案預設 C1 深海藍）；SC1 只在 S1、S3、S5、S6 可當預設。
3. **起手**：載入 tokens（第 5 節）＋ 該風格的表面層（第 3 節）＋ THEMES 與切換器（第 4 節）。
4. **元件**：只用第 8 節清單裡的元件與 class 語彙，狀態齊全（預設、hover、focus、disabled、錯誤、空、載入）。
5. **檢查**：第 9 節四項檢查通過才算完成。

## 2. 六套風格與選型

| 編號 | 名稱 | 材質原理 | 適合 | 不適合 |
|---|---|---|---|---|
| S1 | 奶油 CREAM | 暖白底、大圓角、1px 暖灰線、零陰影 | 任何後台、預設值 | 無短板，也沒有記憶點 |
| S2 | 浮雕 EMBOSS | 同色凸凹柔影：凸＝可按、凹＝已選／輸入區 | 操作元件多的工具型介面 | 大量小字資料表（對比先天弱）；SC1 鎖定 |
| S3 | 琉璃 GLAZE | 品牌雙色 133° 漸層背景 ＋ 毛玻璃面板 | 品牌展示、前台首頁、AI 賣點 | 資訊密集後台；iOS 對 `background-attachment:fixed` 支援差 |
| S4 | 手帳 DOODLE | 暖紙底、2px 墨色手繪歪框、硬影位移 | 餐飲、文創、電商、品牌頁 | 需快速掃描的表格（手繪框是噪音）；冷色系需調整 |
| S5 | 極光 AURORA | 雙色柔霧暈染、一角收尖的有機圓角 | 品牌故事、服務型前台、儀表板首頁 | 漸層只准三處（強調按鈕、AI 標記、hero 數字／目前狀態節點） |
| S6 | 石墨 GRAPHITE | 純無彩色近白底、1px 細線、零陰影、小圓角、N4 等寬字 | 後台、資料密集儀表板、開發者與內部工具、設定頁 | 前台品牌頁、行銷頁、需要情緒與記憶點的介面 |

風格 × 色系矩陣（◎ 推薦 ○ 可用 △ 需調整 ✕ 鎖住）：

| | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | SC1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | ◎ | ◎ | ◎ | ○ | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ |
| S2 | ◎ | ◎ | ◎ | ○ | ○ | △ | △ | △ | ○ | ○ | ○ | ○ | ✕ |
| S3 | ◎ | ◎ | ◎ | ◎ | ◎ | ○ | ○ | ○ | ◎ | ◎ | ○ | ○ | ◎ |
| S4 | ○ | ○ | △ | △ | ◎ | ◎ | ◎ | ◎ | ◎ | ○ | ◎ | ◎ | △ 自動加框線 |
| S5 | ◎ | ◎ | ◎ | ◎ | ◎ | ○ | △ | △ | ○ | ◎ | ◎ | ◎ | ◎ |
| S6 | ◎ | ◎ | ◎ | ◎ | ◎ | ○ | ○ | ◎ | ◎ | ◎ | ○ | ○ | ◎ |

△ 的調整方式：S2 遇暖色改暖灰底 `#EDE8E0`；S4 遇冷色建議改選 S1；S5 遇 C7、C8 暈染只取彩色端。

**S1 與 S6 是一對**：奶油暖而軟，給文件與對外畫面；石墨冷而硬，給工程師與內部工具。兩套的辨識度靠底色拉開：S1 是暖白 `#F6F5F2`、S6 是中性灰 `#F4F4F4`，卡片都是純白。S6 是六套裡對色系最寬容的一套（沒有任何一格需調整或鎖住），因為它把品牌色壓到最少。六套 × 十三組 ＝ 78，扣掉鎖住的 S2 × SC1，可用 **77 種**。

## 3. 各風格的表面層（只覆寫材質）

S1 為基準（不掛 class），其餘五套以 `html.sty-emboss / sty-glaze / sty-doodle / sty-aurora / sty-graphite` 覆寫。所有風格共用同一份元件 HTML 與 class。

**S1 奶油**：`--page:#F6F5F2 --card:#FFFFFF --line:#E4E2DE --band:#FBFAF8 --ink:#26292E --muted:#6F6B64`。所有卡片、輸入框、按鈕 `border:1px solid var(--line)`、零陰影；容器 16px、輸入框與小卡 12px、按鈕與狀態膠囊 999px。

**S2 浮雕**：`--bg:#E6EAF0`（底即卡）`--ink:#333B49 --muted:#5F6673 --shD:rgba(163,177,198,.62) --shL:rgba(255,255,255,.95)`。凸（可按）`box-shadow:5px 5px 11px var(--shD),-5px -5px 11px var(--shL)`；凹（已選、輸入區）`inset 3px 3px 7px var(--shD),inset -3px -3px 7px var(--shL)`；不用框線；主按鈕仍實心主色配白字。CSS 變數名大小寫有別（`--shD` 不是 `--shd`）。

**S3 琉璃**：`body{background:linear-gradient(133deg,var(--acc),var(--acc2))}`；`--ink:#232936 --muted:#454C59`；亮玻璃 `rgba(255,255,255,.70)`＋`backdrop-filter:blur(24px)`＋`1px solid rgba(255,255,255,.7)`；深玻璃 `rgba(22,26,42,.66)` 配白字，只給深玻璃卡與深玻璃按鈕。鐵則：**文字不落在漸層上（一律墊玻璃）、彩色字不落在 70% 玻璃上（一律墊白）**。

**S4 手帳**：`--paper:#FAF3E4 --card:#FFFDF7 --line:#D8CDB8 --ink:#2E2A24 --muted:#6E6656`。容器 `border:2px solid var(--ink)`＋歪框 `border-radius:255px 18px 225px 18px/18px 225px 18px 255px`（交錯用 `18px 225px 18px 255px/255px 18px 225px 18px`）；按鈕硬影 `box-shadow:2.5px 2.5px 0 var(--ink)`、按下位移歸零；分隔線 2px 虛線；裝飾限紙膠帶與麥克筆畫重點；表格資料區保持乾淨。

**S5 極光**：`--page:#FCFCFD --line:#E9E9EF --ink:#22262E --muted:#686E78 --dark:#1C1F27`。背景 `body::before` 三個 `radial-gradient(color-mix(in srgb,var(--acc) 30%,transparent))` 暈染加 `blur(6px)`；面板 `rgba(255,255,255,.92)`、圓角 `26px 26px 26px 8px`（小件 `18px 18px 18px 6px`）；主按鈕墨色深丸；漸層只出現在強調按鈕 `linear-gradient(95deg,var(--acc),var(--acc2-deep))`、AI 標記、hero 數字或目前狀態節點三處。

**S6 石墨**：`--page:#F4F4F4 --card:#FFFFFF --band:#F6F6F6 --sel:#F2F2F2 --line:#E3E3E3 --line-2:#D9D9D9 --ink:#171717 --muted:#6A6A6A --dark:#3B3B3B`；圓角 `--r-lg:12px --r-sm:6px --r-pill:999px`。所有卡片、輸入框、按鈕 `1px solid var(--line)`、零陰影。三條鐵則：

一、**側欄、頂列與頁面同色，只有卡片與輸入元件是白的**——「只有資料躺在白紙上，其餘都是同一張桌面」。做成側欄白、頁面灰就變成另一套風格。
二、**灰階是純無彩色**，每個灰的紅綠藍三值必須相等，不得帶藍調或黃調。
三、**表格區不用品牌色，只有選取列例外**——篩選膠囊選中、側欄 hover、分段控制都用中性灰 `--sel`；品牌色只留給主按鈕、連結、側欄選中項、目前頁籤、選取列。

兩項風格層例外（只有 S6 適用）：按鈕與輸入框圓角 **6px**、卡片與表格容器 **12px**（狀態膠囊、篩選膠囊、屬性 tag 仍 999px）；N4 級（料號、單號、日期、IP、追蹤碼）改等寬字 `"SF Mono",Menlo,Consolas,"Liberation Mono",monospace`，**金額 N1〜N3 仍用 Arial、中文仍用 Noto Sans TC**。

## 4. 色彩四層與色系切換（十二組核心 ＋ SC1）

**鐵則：介面上不得出現這四層以外的任何顏色。**

### 4.1 第一層 品牌雙色（使用者可切換，執行時注入七個變數）

```
--acc  --acc-soft  --acc-deep  --acc2  --acc2-soft  --acc2-deep  --acc2-text
```

- `--acc` 主色負責所有「操作」：主按鈕、選中、連結、聚焦框、目前頁籤、進行中狀態。
- `--acc2` 副色負責「點綴」：品牌標記、圖表第二數列、趨勢箭頭；每頁最多三處。
- `--acc-deep` 十三組一律等於 `--acc`。
- **副色分兩型**：深型（十二組核心）承載文字的填色一律 `--acc2-deep` 配白字，副色當字一律 `--acc2-deep`，不承載文字的裝飾填色才用 `--acc2`；淺型（SC 系列）填色上放 `--acc2-text`（＝該風格的 `--ink`），填色元件必須有 1px 框線或置於白卡，且同一列不得與 warning 琥珀並存（並存時品牌標記改用 `--acc`）。

| 編號 | 名稱 | `--acc` | `--acc-soft` | `--acc2` | `--acc2-soft` | `--acc2-deep` | 副色型 | 可用風格 |
|---|---|---|---|---|---|---|---|---|
| C1 | 深海藍 | `#2B5FB8` | `#EDF1F9` | `#C2377B` | `#FAEEF4` | `#BA3576` | 深型 | 全部 |
| C2 | 深湖青 | `#0F5C63` | `#EBF1F2` | `#C4663A` | `#FAF2EE` | `#A15430` | 深型 | 全部 |
| C3 | 深靛 | `#2C2A72` | `#EDEDF3` | `#8C7AE6` | `#F5F4FD` | `#6A5DAF` | 深型 | 全部 |
| C4 | 電光紫 | `#6D28D9` | `#F3EDFC` | `#0F8A99` | `#EBF5F6` | `#0D7481` | 深型 | 全部 |
| C5 | 森林綠 | `#1F5E3D` | `#ECF1EF` | `#A16207` | `#F7F2EA` | `#975C07` | 深型 | 全部 |
| C6 | 胡桃棕 | `#6B4A33` | `#F2F0EE` | `#4A6B55` | `#F0F2F1` | `#4A6B55` | 深型 | 全部 |
| C7 | 焦糖磚橘 | `#A8481F` | `#F8EFEC` | `#2B2B2B` | `#EDEDED` | `#2B2B2B` | 深型 | 全部 |
| C8 | 暖墨 | `#23201E` | `#ECECEC` | `#D95F1E` | `#FCF1EC` | `#AE4C18` | 深型 | 全部 |
| C9 | 唇膏紅 | `#9F2436` | `#F7EDEF` | `#2A5C6A` | `#EEF2F3` | `#2A5C6A` | 深型 | 全部 |
| C10 | 節慶桃紅 | `#9E2C6A` | `#F7EEF3` | `#5C97CB` | `#F2F7FB` | `#336DA0` | 深型 | 全部 |
| C11 | 燒橄欖 | `#646049` | `#F3F2F0` | `#C65D52` | `#FAF2F1` | `#B2463B` | 深型 | 全部 |
| C12 | 玫瑰棕 | `#80565B` | `#F5F1F2` | `#BA797D` | `#F9F4F5` | `#9F5257` | 深型 | 全部 |
| SC1 | 深綠 × 相思黃 | `#35463D` | `#EFF0EF` | `#DACD65` | `#FCFBF3` | `#6F6519` | 淺型 | S1、S3、S5、S6；S4 需加框線；S2 鎖住 |

顏色一律 sRGB 十六進位；Pantone、RAL 等外部色號只作對照，不得寫進程式或規範。退場的舊色（石板藍 `#334155`、酒紅 `#7A2230`）新專案不得選用。專案若有既有品牌色，只替換第一層七個變數，仍須通過第 9 節對比稽核。

### 4.2 切換器實作（三處必須一致：後台設定頁、使用者偏好、網址參數）

```js
const THEMES={
 c1:{"id":"C1","name":"深海藍","acc":"#2B5FB8","accSoft":"#EDF1F9","acc2":"#C2377B","acc2Soft":"#FAEEF4","acc2Deep":"#BA3576","accDeep":"#2B5FB8","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6"],"adjust":[],"series":"C"},
 c2:{"id":"C2","name":"深湖青","acc":"#0F5C63","accSoft":"#EBF1F2","acc2":"#C4663A","acc2Soft":"#FAF2EE","acc2Deep":"#A15430","accDeep":"#0F5C63","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6"],"adjust":[],"series":"C"},
 c3:{"id":"C3","name":"深靛","acc":"#2C2A72","accSoft":"#EDEDF3","acc2":"#8C7AE6","acc2Soft":"#F5F4FD","acc2Deep":"#6A5DAF","accDeep":"#2C2A72","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6"],"adjust":[],"series":"C"},
 c4:{"id":"C4","name":"電光紫","acc":"#6D28D9","accSoft":"#F3EDFC","acc2":"#0F8A99","acc2Soft":"#EBF5F6","acc2Deep":"#0D7481","accDeep":"#6D28D9","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6"],"adjust":[],"series":"C"},
 c5:{"id":"C5","name":"森林綠","acc":"#1F5E3D","accSoft":"#ECF1EF","acc2":"#A16207","acc2Soft":"#F7F2EA","acc2Deep":"#975C07","accDeep":"#1F5E3D","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6"],"adjust":[],"series":"C"},
 c6:{"id":"C6","name":"胡桃棕","acc":"#6B4A33","accSoft":"#F2F0EE","acc2":"#4A6B55","acc2Soft":"#F0F2F1","acc2Deep":"#4A6B55","accDeep":"#6B4A33","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6"],"adjust":[],"series":"C"},
 c7:{"id":"C7","name":"焦糖磚橘","acc":"#A8481F","accSoft":"#F8EFEC","acc2":"#2B2B2B","acc2Soft":"#EDEDED","acc2Deep":"#2B2B2B","accDeep":"#A8481F","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6"],"adjust":[],"series":"C"},
 c8:{"id":"C8","name":"暖墨","acc":"#23201E","accSoft":"#ECECEC","acc2":"#D95F1E","acc2Soft":"#FCF1EC","acc2Deep":"#AE4C18","accDeep":"#23201E","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6"],"adjust":[],"series":"C"},
 c9:{"id":"C9","name":"唇膏紅","acc":"#9F2436","accSoft":"#F7EDEF","acc2":"#2A5C6A","acc2Soft":"#EEF2F3","acc2Deep":"#2A5C6A","accDeep":"#9F2436","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6"],"adjust":[],"series":"C"},
 c10:{"id":"C10","name":"節慶桃紅","acc":"#9E2C6A","accSoft":"#F7EEF3","acc2":"#5C97CB","acc2Soft":"#F2F7FB","acc2Deep":"#336DA0","accDeep":"#9E2C6A","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6"],"adjust":[],"series":"C"},
 c11:{"id":"C11","name":"燒橄欖","acc":"#646049","accSoft":"#F3F2F0","acc2":"#C65D52","acc2Soft":"#FAF2F1","acc2Deep":"#B2463B","accDeep":"#646049","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6"],"adjust":[],"series":"C"},
 c12:{"id":"C12","name":"玫瑰棕","acc":"#80565B","accSoft":"#F5F1F2","acc2":"#BA797D","acc2Soft":"#F9F4F5","acc2Deep":"#9F5257","accDeep":"#80565B","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6"],"adjust":[],"series":"C"},
 sc1:{"id":"SC1","name":"深綠 × 相思黃","acc":"#35463D","accSoft":"#EFF0EF","acc2":"#DACD65","acc2Soft":"#FCFBF3","acc2Deep":"#6F6519","accDeep":"#35463D","acc2Type":"light","styles":["s1","s3","s5","s6"],"adjust":["s4"],"series":"SC"}
};
const STYLE='s1';                                   // 本系統選定的風格，建置時決定
function themeAllowed(k){const t=THEMES[k];return !!t&&(t.styles.includes(STYLE)||t.adjust.includes(STYLE));}
function applyTheme(k){
  let t=THEMES[k];
  if(!themeAllowed(k)){ notify(THEMES[k].id+' 不適用於此風格，已切回 C1'); k='c1'; t=THEMES.c1; }
  const r=document.documentElement.style;
  r.setProperty('--acc',t.acc);   r.setProperty('--acc-soft',t.accSoft);  r.setProperty('--acc-deep',t.accDeep);
  r.setProperty('--acc2',t.acc2); r.setProperty('--acc2-soft',t.acc2Soft); r.setProperty('--acc2-deep',t.acc2Deep);
  const ink=getComputedStyle(document.documentElement).getPropertyValue('--ink').trim();
  r.setProperty('--acc2-text', t.acc2Type==='light' ? ink : '#FFFFFF');
  document.documentElement.classList.toggle('sc-light', t.acc2Type==='light');
  document.documentElement.classList.toggle('sc-adjust', t.adjust.includes(STYLE));   // S4 × SC1：副色填色自動加 1px 墨色框線
  return k;   // 呼叫端把實際套用的 k 存回使用者偏好
}
```

色系選擇介面：十二顆核心一段、分隔線後「SC 特殊」一段；每顆「主色左、副色右」雙色圓；不適用者 `disabled`、反灰 40%、劃線、`title="此風格不適用"`、鍵盤 tab 跳過；`adjust` 命中時可選並提示「副色填色自動加框線」。網址或 API 帶入不合法組合同樣退回 C1 並提示。

淺型副色的 CSS 落地（放在共用樣式）：

```css
html.sc-light .aibadge{background:var(--acc2);color:var(--acc2-text)}
html.sc-light tr:has(.st.wrn) .aibadge{background:var(--acc);color:#fff}   /* 與 warning 同列 → 改主色 */
html.sc-adjust .aibadge,html.sc-adjust .avatar.a2{border:1px solid var(--ink)}
```

### 4.3 第二層 結構灰階（各風格一組，見第 3 節）與第三層 語意色（固定）

```css
--err:#B23F2F;  --err-soft:#F7ECEA;    /* 錯誤、必填、逾期、已取消、不可回復 */
--wrn:#846200;  --wrn-soft:#F3EFE6;    /* 待處理、待確認、額度不足、需人工判斷 */
--ok:#2A722E;   --ok-soft:#EAF1EA;     /* 成功、已完成、已通過 */
--info:#1A66AA; --info-soft:#E8F0F6;   /* 中性提示、系統訊息、維護公告 */
```

狀態對應：待人處理＝warning、進行中＝主色、成功結束＝success、結案封存＝灰、異常＝error、中性提示＝info。語意色一律「符號＋文字」（例如「● 待確認」），不單靠顏色。

### 4.4 第四層 資料視覺化色板（圖表專用，固定順序，與品牌色無關）

```css
--d1:#1F4F9E; --d2:#C9781F; --d3:#00806A; --d4:#8659CC;
--d5:#5E7A12; --d6:#C7466E; --d7:#0E82A8; --d8:#B5651D;
```

這一層只負責「分辨這是第幾條資料」。**兩個數列以下**用第一層的主色與深副色；**三個以上**一律改用這八色，依 D1〜D8 固定順序取用。固定順序、與品牌色無關的意思是：使用者把色系從深海藍換成節慶桃紅，這八個顏色一個都不會動——否則同一張圖今天藍色代表 A 產品、明天變成桃紅，看圖的人會誤判。語意色不得當數列色（綠色數列會被讀成「成功」）；超過八個數列改分組或併為「其他」；永遠只有一條 Y 軸，兩個量級不同的指標畫成兩張圖。

### 4.5 著色面上的文字（對比稽核定下的規則）

一、著色面上的字只有兩種：夠亮的面配 `--ink`，夠深的面配白；不允許中等深度面配中等深度字。判斷靠計算（≥4.5），不靠目測。
二、副色承載字一律 `--acc2-deep`。
三、停用控件用灰底 `--line` 配灰字 `--muted`，不用透明度（透明度會讓白字浮在淡底上）。
四、次要文字 `--muted` 放在品牌淡底（選取列、選中項）上要改 `--ink`。
五、數字角標一律 error 紅（它表達「有事情等你」，不是品牌識別）。

## 5. 字級、行距、字距、間距、造型 token

```css
html{font-size:62.5%}                       /* 1rem = 10px，px 除以 10 即 rem */
:root,[data-type="productive"]{             /* 後台、購物車、結帳（預設） */
 --fs-d1:3.0rem;--lh-d1:1.15;--ls-d1:-0.01em; --fs-h1:2.1rem;--lh-h1:1.40;--ls-h1:0.03em;
 --fs-h2:1.7rem;--lh-h2:1.45;--ls-h2:0.06em;  --fs-h3:1.4rem;--lh-h3:1.50;--ls-h3:0.08em;
 --fs-b1:1.4rem;--lh-b1:1.80; --fs-b2:1.25rem;--lh-b2:1.70; --fs-b3:1.2rem;--lh-b3:1.70;
 --fs-l1:1.2rem;--lh-l1:1.50;--ls-l1:0.08em; --fs-l2:1.1rem;--lh-l2:1.50;--ls-l2:0.15em;
 --fs-n1:2.3rem;--lh-n1:1.20; --fs-n2:1.9rem;--lh-n2:1.25; --fs-n3:1.25rem;--lh-n3:1.60; --fs-n4:1.25rem;--lh-n4:1.60;--ls-n4:0.02em;
 --sp-1:0.4rem;--sp-2:0.8rem;--sp-3:1.2rem;--sp-4:1.6rem;--sp-5:2.0rem;--sp-6:2.4rem;--sp-7:3.2rem;--sp-8:4.0rem;--sp-9:4.8rem;--sp-10:6.4rem;
 --r-lg:16px;--r-sm:12px;--r-pill:999px;--bw:1px;--bw-on:1.5px}
[data-type="expressive"]{                   /* 前台商品頁、目錄、首頁 */
 --fs-d1:4.4rem;--lh-d1:1.10; --fs-h1:3.0rem;--lh-h1:1.35; --fs-h2:2.2rem;--lh-h2:1.40; --fs-h3:1.6rem;--lh-h3:1.50;
 --fs-b1:1.6rem;--lh-b1:1.90; --fs-b2:1.4rem;--lh-b2:1.80; --fs-b3:1.3rem;--lh-b3:1.90;
 --fs-l1:1.2rem;--lh-l1:1.50; --fs-l2:1.1rem;--lh-l2:1.50;
 --fs-n1:3.0rem;--lh-n1:1.15; --fs-n2:2.3rem;--lh-n2:1.20; --fs-n3:1.4rem;--lh-n3:1.60; --fs-n4:1.3rem;--lh-n4:1.60}
@media (max-width:767px){[data-type="expressive"]{--fs-d1:3.6rem}}
body{font-family:'Noto Sans TC',sans-serif;font-size:var(--fs-b1);line-height:var(--lh-b1)}
.num,.amt,.price{font-family:Arial,Helvetica,'Noto Sans TC',sans-serif;font-variant-numeric:tabular-nums}
```

| 代號 | 用途 | 字重 | 字型 |
|---|---|---|---|
| D1 | 顯示數字（統計大數） | 700 | Arial |
| H1 / H2 / H3 | 頁面標題 / 區塊標題、彈窗與面板標題 / 卡片標題列、行內小標題 | 900 | 黑體 |
| B1 / B2 / B3 | 內文 / 表格內密集內文 / 說明輔助 | 400 | 黑體 |
| L1 / L2 | 欄位標籤 / 微標籤眉標 | 700 | 黑體 |
| N1 / N2 / N3 / N4 | 合計金額 / 小計 / 表格金額 / 料號單號日期 | 700 700 700 400 | Arial |

硬規則：字級只能是這十三級，寫 `var(--fs-xx)` 就要同時寫 `var(--lh-xx)`；12px 是承載句子的最小字級（Expressive 13px）；11px 是整套標尺的絕對下限，只給 L2 微標籤（一到四個字的單詞或極短片語），字重 700 以上並加大字距，不得寫句子；**欄位標籤一律 12px（L1），不得用 11px**；**不得出現 10px 以下的字**；**標題不得小於它所領導的內文**（H3 與 B1 同為 14px，靠字重 900 與字距區分）；**H2 與 H3 依用途分**：彈窗（`.modal .mh`）、側滑面板（`.drawer .dh`）、獨立自成一件事的大卡片用 H2，卡片標題列（`.card-title`）、表格標題（`.tcap`）、圖表卡標題、表單分組小標題用 H3，覺得卡片標題太小就改用 H2、不得新增中間值（見規範 4.2）；中文不用斜體；行距不採用 M3 或 Tailwind 的 1.43（中文會糊）；行動裝置不縮字級只改版型；金額千分位必加、貨幣前綴縮小 0.68 倍轉灰、表格中靠右、負數轉 error 紅。

**行距一定要跟字級配成同一代號**，不可以拿 B2 的字級去配 B3 的行距。每個值單獨看都在表上，所以肉眼與只看宣告值的檢查都抓不出來。沒有自己指定行距的元素會往上繼承，所以 `body` 一定要寫 `line-height:var(--lh-b1)`——漏掉的話整份文件的預設行距會退回瀏覽器的 `normal`（約 1.2 倍）。兩個例外是規範自己要求的、不算違規：貨幣前綴縮小 0.68 倍、768px 以下輸入框 16px 防 iOS 放大。見規範 4.2。

間距：所有 margin、padding、gap 只取 `--sp-1`〜`--sp-10`（4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48 / 64px），負 margin 不用（堆疊頭像、資料夾頁籤例外）。卡片內距 16 / 20、儲存格 12 / 20、標籤到元件 8、元件之間 12、區塊之間 24。

圓角四級固定、維持 px：18px 焦點框與大面板、16px 卡片與表格容器、12px 輸入框小卡選單、999px 所有按鈕與狀態膠囊；框線 1px、選中 1.5px。陰影由各風格定義（奶油、極光、石墨零陰影，浮雕雙向柔影，琉璃面板投影，手帳硬影）。

**風格層例外只有 S6 石墨**：按鈕與輸入框 6px、卡片與表格容器 12px；N4 級改等寬字。其餘五套一律照上表。

元件高度一律 `min-height`（rem）：主按鈕 4.0（手機 4.4）、一般按鈕 3.8（4.4）、小按鈕 3.2（4.0）、輸入框 4.0（4.4，字 16px 防 iOS 放大）、狀態膠囊 2.4、表格列 4.4、側欄項目 3.8；相鄰可點元件至少留 8px。正圓元件（頭像、圓點、播放鈕）加 `aspect-ratio:1/1` 以免在 flex 列被拉成橢圓。

## 6. RWD

斷點 1024 / 768 / 480（px，描述裝置）。768 以下：側欄改覆蓋式抽屜加遮罩、漢堡鈕 44px；表格轉卡片列（每格 `data-l` 帶欄名，不做水平捲動）；輸入框 16px；商品規格頁計價面板改底部固定條；主要動作滿版。480 以下單欄。任何寬度 body 不得橫向捲動（flex 子項記得 `min-width:0`）。

## 7. 版型與文案（摘要）

後台：側欄式框架（側欄 226px、頂列麵包屑與通知鈴、內容區最大 1060px）。前台：頂部分頁式。每頁最多一顆實心主按鈕；危險動作二次確認且寫明後果；空狀態是邀請不是報告（給出口）；錯誤訊息說怎麼修；語氣是專業同事，不用驚嘆號與語尾助詞。詳見規範第九、十一章。

## 8. 元件清單（62 項：核心 45 必備、選用 17 依系統勾選）

**核心（每個專案都要，六套風格皆已實作）**
基礎：設計 Token、字級層級、分隔線。動作：按鈕、動作鈕 ⋯、分段控制。表單：輸入框、搜尋框、核取與單選、篩選膠囊、開關、上傳、多行輸入、下拉選單、多選＋搜尋、日期與時間選擇器、自動完成、數字步進器、選項 chip。資料呈現：表格、表格進階（排序、欄位切換、批次選取）、卡片、統計卡、描述清單、狀態標籤、屬性 tag、折疊面板、頭像、數字角標。導覽：側欄項目、頁籤、麵包屑、分頁器（P4 底線數字式）、側滑面板。回饋：彈窗、就地確認、提示氣泡、Toast、警示條（四語意色）、提示框、空狀態、骨架屏、通知鈴、進度條、搜尋無結果。

**選用（依系統類型）**
工具列、滑桿、級聯選擇、穿梭框、摘要方塊、來源標記（原 AI 標記）、百分比膠囊、量表、樹狀、時間軸、圖表（兩個數列以下用主色與深副色，三個以上改用第四層八色）、媒體與輪播、動態列表、步驟精靈、唯讀步驟、分割面板、結果頁。

**警示條與提示框（v7 定案、v8 補對齊守則，六套一致）**：警示條 `.alert` 不用左側 4px 色條，改 `border:1px solid color-mix(in srgb,currentColor 32%,transparent)` 一圈細框，框線顏色自動跟著語意色走；標題與內文同一行（`b` 與 `p` 都 `display:inline`），圖示保留，背景仍是該語意的 `-soft` 淡底。四條使用守則：**標題是選用的**（一句話講得完就不要標題）、**動作最多一顆**且做成帶底線的文字連結而非按鈕（`.alert .btn.sm` 去底去框去陰影）、**錯誤與警告不給關閉鈕**（使用者關掉就看不到問題了，只有 info 與 ok 可關）、**文字動作與關閉鈕要跟內文站在同一條基線上**（和內文共用同一個行框：同字級、同行距、`align-self:flex-start`，不要再給它 `min-height`——按鈕那個 32px 會把整列撐高，差將近 6px）。提示框 `.notice` 去掉左側主色條與彩色底，S1 與 S6 直接用頁面灰底無框、S2 用凹面無框、S3 是 1px 玻璃框、S4 是 2px 虛線框、S5 是淡線框加淡底——它只是「順便一提」，不該比旁邊的內容搶眼。

六套**共用同一份元件 HTML**：S1 奶油是基準，其餘五套只掛 `html.sty-*` 覆寫材質；六套的 62 個節標題逐字相同，少任何一項都會在設計系統瀏覽器的元件索引顯示 ✕。共用 class 語彙（六套一致，不得自創同義名）：`.btn .btn.primary .btn.sm .btn.danger`、`.field label input .req .msg`、`.st.acc/.wrn/.ok/.err/.gray`、`.tag.acc/.err/.gray`、`.aibadge`、`.chip`、`.pillf`、`.seg`、`.qty`、`.check`、`.radio`、`.sw2`、`.card .card-title`、`.tblwrap .tcap table.t .amt .dt .p4`、`.statc .k .v .delta`、`.desc`、`.avatar`、`.badge`、`.count`、`.tabs .tab`、`.nitem`、`.drawer`、`.modal .mh .mb .mf`、`.pop`、`.tip`、`.toast`、`.alert.err/.wrn/.ok/.info`、`.notice`、`.empty`、`.skel`、`.bell`、`.bar`、`.stepper`、`.tl`、`.feed`、`.divider .hr .vdiv`。完整標記與樣式直接抄 `assets/components/` 裡所選風格檔案的對應區段（每項元件一節，節標題六套逐字相同，可用 grep 找）。

## 9. 交付前四項自動檢查（腳本在本 skill 的 `scripts/`）

四項都通過才算完成。腳本對任何 HTML 檔或網址都能跑，有不合規時結束碼為 1，可以直接接進 CI（持續整合：每次提交自動跑檢查）。第一、四項與第三項的 `--render` 需要先裝依賴：`pip install -r scripts/requirements.txt && playwright install chromium`（Playwright 是自動操控瀏覽器的工具）。

| 檢查 | 指令 | 標準 |
|---|---|---|
| 一、對比稽核 | `python scripts/audit_contrast.py page.html --themes all` | 把頁面畫出來，對每個文字節點取周邊像素當底色；一般字 ≥4.5、大字 ≥3.0；停用控件豁免。頁面若支援色系切換，每個可用色系都要 0 不及格（`--themes` 走網址 hash，例如 `page.html#c3`） |
| 二、標尺合規 | `python scripts/check_tokens.py page.html` | 字級不在十三級、行距字距不在表上、間距不在標尺、負 margin，任何一項出現即不通過；固定 `height` 列為提醒，承載文字的要改 `min-height` |
| 三、行高配對 | `python scripts/check_lineheight.py page.html --render` | 靜態掃每條 CSS 規則的字級與行距是否同代號、有沒有寫了字級卻漏掉行距；`--render` 再渲染頁面，比對每個文字元素實際算出來的字級與行高。`check_tokens.py` 只看宣告值，抓不到這一類 |
| 四、溢出檢查 | `python scripts/check_overflow.py page.html` | 390px、768px 寬度下不得橫向捲動，並列出撐破版面的元素 |

前台閱讀型頁面（`data-type="expressive"`）的二、三項加 `--type expressive`。開發時才出現的控制列等區塊，加上 `data-audit-skip` 屬性即可排除在對比稽核外。

批次改動後，所選風格的每個頁面都要截圖對照，不抽樣。若無法執行腳本（例如沒有 Python 環境），至少逐條人工核對：所有字級與行距都引用 `var(--fs-xx)` ＋ 同代號 `var(--lh-xx)`、間距只用 `--sp-*`、沒有寫死的色碼。

## 10. 起手式

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="tokens.css">          <!-- 從本 skill 的 assets/tokens.css 複製到專案 -->
<style>
:root{ /* 第一層由 applyTheme() 注入；第二層依所選風格；第三、四層固定 */
  --acc:#2B5FB8;--acc-soft:#EDF1F9;--acc-deep:#2B5FB8;--acc2:#C2377B;--acc2-soft:#FAEEF4;--acc2-deep:#BA3576;--acc2-text:#FFFFFF;
  --ink:#26292E;--muted:#6F6B64;--line:#E4E2DE;--band:#FBFAF8;--page:#F6F5F2;--card:#FFFFFF;
  --err:#B23F2F;--err-soft:#F7ECEA;--wrn:#846200;--wrn-soft:#F3EFE6;--ok:#2A722E;--ok-soft:#EAF1EA;--info:#1A66AA;--info-soft:#E8F0F6;
  --d1:#1F4F9E;--d2:#C9781F;--d3:#00806A;--d4:#8659CC;--d5:#5E7A12;--d6:#C7466E;--d7:#0E82A8;--d8:#B5651D}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--ink)}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r-lg)}
.btn{min-height:3.8rem;padding:0.9rem 2.0rem;border-radius:var(--r-pill);border:1px solid var(--line);background:#fff;font-size:var(--fs-b2);line-height:var(--lh-b2);font-weight:700}
.btn.primary{min-height:4.0rem;padding:1.0rem 2.4rem;background:var(--acc);border-color:var(--acc);color:#fff}
.btn:disabled{background:var(--line);color:var(--muted);border-color:transparent;opacity:1}
</style>
<body data-type="productive">   <!-- 前台閱讀型頁面改 expressive -->
```

任何元件的 CSS 不得寫死色碼與字級，一律引用變數；唯一例外是純黑純白與陰影用的半透明黑。

## 11. 參考檔索引（需要細節時才讀，不必一次全讀）

| 要查的事 | 讀這個檔 |
|---|---|
| 名詞對照表、文件目的、五條設計總則 | `references/overview.md` |
| 第三章 色彩四層、十二組核心 ＋ SC1 色碼、副色深型與淺型、著色面上的文字 | `references/color.md` |
| 第四章 字型、十三級字級、行距配對、金額與數字格式 | `references/typography.md` |
| 第五章 間距標尺、圓角、框線、元件高度 | `references/spacing-radius.md` |
| 第六章 斷點、側欄抽屜、表格轉卡片列 | `references/rwd.md` |
| 第七章 元件規範（含警示條與提示框守則） | `references/components.md` |
| 第八章 六套風格的表面層、風格 × 色系矩陣 | `references/styles.md` |
| 第九章 後台與前台版型 | `references/layout.md` |
| 第十章 對比、焦點、鍵盤操作 | `references/accessibility.md` |
| 第十一章 介面文案（按鈕、錯誤訊息、空狀態的寫法） | `references/copywriting.md` |
| 附錄 已退場的歷年色系 | `references/legacy-colors.md` |
| 某個元件的完整 HTML 與 CSS | `assets/components/<風格>.html`，搜尋該元件的節標題 |
| 六套共用的數值一覽（字級、間距、圓角、色彩、斷點） | `assets/foundations.html` |
| 字級、間距、造型 token | `assets/tokens.css` |
