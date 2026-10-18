---
name: "ui-design-format"
description: "通用的網頁介面設計系統（2026-10 v24 規範）。凡是要產生或修改任何網頁介面、HTML prototype、後台管理、表單頁、訂購或點餐系統、web app、landing page、互動 demo、元件庫，或使用者提到「UI」「介面」「網頁設計」「prototype」「做一個系統」「前端」時，必須先讀本 skill 再動工，即使使用者沒提到風格。內容：七套風格（S1 奶油、S2 浮雕、S3 琉璃、S4 手帳、S5 極光、S6 石墨、S7 編輯）擇一開發，S3、S5、S6 另有深色模式、S6 另有密集模式；十二組核心 ＋ SC1〜SC3 特殊色系由使用者在系統內切換（含鎖定規則）；四層色彩、十四級字級、間距標尺、圓角、元件高度、RWD 與 12 欄欄格、62 項元件清單與六項自動檢查（含元件結構尺寸、焦點環、佔位文字、拆檔無損與風格層純度）；z-index 五層；可引用的 dist/ CSS 與 theme.js（開發對接）；動態 token 與 Lucide 圖示規則；七張 Expressive 前台示範頁。"
---

# 管理者工作室 網頁介面設計系統（skill 版）

本 skill 是《網頁設計規範 v24》與其推導調研的實作摘要。規範全文依章節放在本資料夾的 `references/`，七套元件庫與 `tokens.css` 在 `assets/`、可引用的 CSS 在倉庫的 `dist/`，四項交付前檢查的腳本在 `scripts/`（索引見文末第 11 節）。**本 skill 與 `references/` 衝突時以 `references/` 為準。**

頁面上的品牌名稱一律用使用者自己的專案名稱。`assets/` 範本裡的「管理者工作室」只是範例品牌，複製標記時要換掉。術語第一次出現要白話解釋。

## 0. 三十秒摘要

一、**工程師選一套風格開發，全站只有一套風格**；風格是「殼」，只覆寫表面材質，不碰結構、色彩變數、字級。
二、**系統內建十二組核心色系 ＋ SC1〜SC3 特殊色系讓使用者切換**，切換只換第一層七個 CSS 變數；第二層灰階、第三層語意色、第四層資料視覺化色板永不隨色系變。不適用於該風格的色系要鎖住，不合法組合退回 C1 並提示，不靜默套用。
三、色彩、字級、間距、圓角一律引用 token，**不寫死數字**；字級與間距用 rem（1rem ＝ 10px），圓角框線斷點用 px；所有元件 `min-height` 不用 `height`。
四、交付前跑六項檢查：對比稽核（每個文字節點 ≥4.5）、標尺合規（字級、行距、間距、字距全在表上）、**行高配對**（字級與行距必須同代號）、390px 不橫向溢出、**元件結構尺寸**（按鈕、輸入框、膠囊的高度與規範值差 ≤1px，七套一致）、**拆檔無損與風格層純度**（dist 與示範頁逐元素相同、風格層不含結構屬性）。
五、**框線色不得拿來當文字色**。`--line` 與 `--line-2` 是給線條用的，拿來寫「不重要的字」（月曆的非本月日期、麵包屑的分隔符）對比只有 1.4，必然不及格；要淡就用 `--muted`。
六、**半透明面板上不放彩色小字**。琉璃與極光的面板是半透明的，彩色小字壓上去只剩 3.4〜4.2，改用主文字色；方向用箭頭符號加文字表達，不靠顏色。

## 1. 工作流程

1. **選風格**：依系統類型從七套選一（見第 2 節矩陣）。後台、資料密集預設 S1 奶油；要「工具感」而不是「文件感」的後台、開發者介面、資料密集儀表板選 S6 石墨；內容網站、品牌官網、長文閱讀選 S7 編輯；需求裡有深色或夜間模式，只能從 S3、S5、S6 選（第 2 節深色模式）；一屏要看大量列的後台選 S6 並提供密集模式（第 5 節）；不確定就 S1。
2. **選預設色系**：從 C1〜C12 選一組當預設（新專案預設 C1 深海藍）；SC 系列只在不鎖、不需調整的風格可當預設：SC1 為 S1、S3、S5、S6；SC2 為 S1、S3、S5、S6（高彩度，給零售、消費品、活動頁）；SC3 為 S1、S3、S5、S6（冷灰藍，給金融、資安、監控）。
3. **起手**：載入 tokens（第 5 節）＋ 該風格的表面層（第 3 節）＋ THEMES 與切換器（第 4 節）。
4. **元件**：只用第 8 節清單裡的元件與 class 語彙，狀態齊全（預設、hover、focus、disabled、錯誤、空、載入）。
5. **檢查**：第 9 節六項檢查通過才算完成。

## 2. 七套風格與選型

| 編號 | 名稱 | 材質原理 | 適合 | 不適合 |
|---|---|---|---|---|
| S1 | 奶油 CREAM | 暖白底、大圓角、1px 暖灰線、零陰影 | 任何後台、預設值 | 無短板，也沒有記憶點 |
| S2 | 浮雕 EMBOSS | 同色凸凹柔影：凸＝可按、凹＝已選／輸入區 | 操作元件多的工具型介面 | 大量小字資料表（對比先天弱）；SC1、SC2 鎖定 |
| S3 | 琉璃 GLAZE | 品牌雙色 133° 漸層背景 ＋ 毛玻璃面板 | 品牌展示、前台首頁、AI 賣點 | 資訊密集後台；iOS 對 `background-attachment:fixed` 支援差 |
| S4 | 手帳 DOODLE | 暖紙底、2px 墨色手繪歪框、硬影位移 | 餐飲、文創、電商、品牌頁 | 需快速掃描的表格（手繪框是噪音）；冷色系需調整 |
| S5 | 極光 AURORA | 雙色柔霧暈染、一角收尖的有機圓角 | 品牌故事、服務型前台、儀表板首頁 | 漸層只准三處（強調按鈕、AI 標記、hero 數字／目前狀態節點） |
| S6 | 石墨 GRAPHITE | 純無彩色近白底、1px 細線、零陰影、小圓角、N4 等寬字 | 後台、資料密集儀表板、開發者與內部工具、設定頁 | 前台品牌頁、行銷頁、需要情緒與記憶點的介面 |
| S7 | 編輯 EDITORIAL | 暖白紙、墨色、明體標題、2px 欄線分段、1px 細線、直角、零陰影 | 內容網站、品牌官網、活動頁、長文閱讀、以文章為主的內容管理後台 | 資料密集後台與儀表板（明體與留白降低密度） |

風格 × 系統類型（◎ 首選 ○ 可用 △ 有條件 ✕ 不建議；完整條件見規範 8.7）：

| 系統類型 | S1 | S2 | S3 | S4 | S5 | S6 | S7 | 首選 |
|---|---|---|---|---|---|---|---|---|
| 後台管理（訂單、庫存、ERP 類） | ◎ | △ | ✕ | ✕ | ○ | ◎ | △ | S1；要工具感選 S6 |
| 資料密集儀表板、報表 | ◎ | ✕ | ✕ | ✕ | ○ | ◎ | ✕ | S6 |
| 開發者工具、內部工具、系統設定 | ○ | △ | ✕ | ✕ | △ | ◎ | ✕ | S6 |
| SaaS 產品的主工作介面 | ◎ | △ | ✕ | △ | ○ | ◎ | △ | S1 |
| 少資料、多操作的工具（設定精靈、控制面板、自助機台） | ○ | ◎ | △ | ○ | ○ | ○ | ○ | S2 |
| 電商前台 | ○ | △ | ○ | ◎ | ◎ | △ | ◎ | S5；品牌偏手作選 S4、偏雜誌感選 S7 |
| 服務型前台（預約、點餐、會員中心） | ◎ | ○ | △ | ○ | ◎ | △ | ○ | S5 或 S1 |
| 品牌官網、活動頁、產品發表 | ○ | ○ | ◎ | ◎ | ◎ | △ | ◎ | S3；內容多的品牌官網選 S7 |
| 餐飲、文創、年輕客群的前台 | ○ | △ | ○ | ◎ | ○ | ✕ | ○ | S4 |
| 內容與閱讀（文章、說明中心、技術文件） | ◎ | △ | ✕ | ○ | ○ | ○ | ◎ | S7；技術文件選 S6 |

選型三條規則：一、先看系統類型（使用者一天看多久、資料多不多），再看品牌調性，最後才挑色系；**看得久、資料多的系統只考慮 S1 與 S6；以閱讀為主的前台先看 S7**，S2、S3、S4、S7 不當資料密集後台的主風格。二、一個系統只有一套風格，前後台同屬一個系統時以使用時數最長的一端決定（點餐系統照店家後台選），前後台是分開的兩個系統才可各選一套。三、字級套與風格無關：做事的頁面 Productive、看的頁面 Expressive，電商結帳仍是 Productive。不確定就選 S1。

風格 × 色系矩陣（◎ 推薦 ○ 可用 △ 需調整 ✕ 鎖住）：

| | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | SC1 | SC2 | SC3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | ◎ | ◎ | ◎ | ○ | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ | ○ | ◎ |
| S2 | ◎ | ◎ | ◎ | ○ | ○ | △ | △ | △ | ○ | ○ | ○ | ○ | ✕ | ✕ | △ 自動加框線 |
| S3 | ◎ | ◎ | ◎ | ◎ | ◎ | ○ | ○ | ○ | ◎ | ◎ | ○ | ○ | ◎ | ◎ | ○ |
| S4 | ○ | ○ | △ | △ | ◎ | ◎ | ◎ | ◎ | ◎ | ○ | ◎ | ◎ | △ 自動加框線 | △ 自動加框線 | △ |
| S5 | ◎ | ◎ | ◎ | ◎ | ◎ | ○ | △ | △ | ○ | ◎ | ◎ | ◎ | ◎ | ◎ | ○ |
| S6 | ◎ | ◎ | ◎ | ◎ | ◎ | ○ | ○ | ◎ | ◎ | ◎ | ○ | ○ | ◎ | ○ | ◎ |
| S7 | ◎ | ◎ | ◎ | ○ | ◎ | ◎ | ◎ | ◎ | ◎ | ○ | ◎ | ○ | ○ | ○ | ◎ |

△ 的調整方式：S2 遇暖色改暖灰底 `#EDE8E0`；S4 遇冷色建議改選 S1；S5 遇 C7、C8 暈染只取彩色端。

**深色模式（規範 8.8，v23）**：深色是風格的「模式」不是另一套風格——同一套風格的白天與夜間，結構、圓角、陰影形狀、框線粗細、字型、字級、間距全部不變，只換第二層灰階、第三層語意色、第四層資料色，第一層品牌色另有一組深色值；色系可用規則沿用該風格的淺色。**只有 S3 琉璃、S5 極光、S6 石墨有深色**：資料密集後台、監控、開發者工具要深色選 S6；品牌官網、活動頁要深色選 S3；前台、預約、會員中心要深色選 S5。S1、S2、S4、S7 沒有深色（暖紙色、凸凹柔影、手繪硬影、白紙黑字都是淺底上的身分），需求有夜間模式就不要選這四套。三套共用：語意色 `--err:#F28B82 --wrn:#E2B341 --ok:#74C483 --info:#7DB6EE`；`--d1` 改 `#6E97DB`；主色在 OKLab 只加明度、保留色相，加到本套最亮面板上 ≥4.6、自己淡底上 ≥4.8，**填色上一律放深色字**（`--on-acc`、`--on-acc2`、`--on-err`、`--on-ink` 都是 `#121212`），所以同一組色系在三套的深色主色不同，數值見規範 8.8 或 `dist/theme.js` 的 `DARK` 表（依風格分表）。S6：`--page:#121212 --card:#1A1A1A --band/paperc:#202020 --sel:#262626 --line:#2E2E2E --line-2:#3A3A3A --ink:#EDEDED --muted:#A3A3A3`（與 v14〜v22 相同）。S3：深玻璃升格為主材質——放資料的面板 `rgba(18,21,34,.80)`、疊在面板上的小件改白 5〜9% 薄霧、墊白處改實心面 `#232838`、背景漸層兩端各 40% 混入 `#0B0D14`，框線降為白 10〜18%，`--ink:#EDEDED --muted:#B5B8C2`；兩條鐵則照舊（文字不落在漸層上、彩色字不落在玻璃上）。S5：近黑底 `#0F1117` 上三團提亮的主副色暈染，面板 `rgba(26,29,39,.84〜.96)`、`--card:#1A1D27`、純白小件改實心面 `#1E212C`、`--line:#2C303C`、`--ink:#EDEDED --muted:#ADB1BB`、`--dark` 改 `#E4E6EC` 配深字，漸層主按鈕上的字改深色。寫法：深色規則掛在 `html[data-theme="dark"]` 底下、宣告 `color-scheme:dark`，寫在同一份元件 HTML 與同一張樣式表裡（不另做一份深色頁）；預設跟隨系統並提供淺／深／跟隨三選一、記住使用者的選擇；不用 `filter:invert()`。新寫的元件不要寫死 `#fff`，白字改引用上述四個變數。

**S1 與 S6 是一對**：奶油暖而軟，給文件與對外畫面；石墨冷而硬，給工程師與內部工具。兩套的辨識度靠底色拉開：S1 是暖白 `#F6F5F2`、S6 是中性灰 `#F4F4F4`，卡片都是純白。S6 是對色系最寬容的一套（沒有任何一格需調整或鎖住，S7 同樣如此），因為它把品牌色壓到最少。七套 × 十五組 ＝ 105，扣掉鎖住的 S2 × SC1、S2 × SC2，可用 **103 種**；S3、S5、S6 的深色模式各另 15 種，共 45 種，合計 **148 種**。

## 3. 各風格的表面層（只覆寫材質）

S1 為基準，其餘六套各有一個只含材質的風格層（`dist/style-s2`〜`s7.css`，頁面以 `<html data-style="s3">` 宣告）。七套共用同一份元件 HTML 與 class（v20 起 S2〜S5 也以 S1 為基底），頁面不加 `.up`、`.glass`、`.wob`、`.org` 這類修飾 class，`.board`、`.card`、`.statc` 本身就帶著該套材質。

**S1 奶油**：`--page:#F6F5F2 --card:#FFFFFF --line:#E4E2DE --band:#FBFAF8 --ink:#26292E --muted:#6F6B64`。所有卡片、輸入框、按鈕 `border:1px solid var(--line)`、零陰影；容器 16px、輸入框與小卡 12px、按鈕與狀態膠囊 999px。

**S2 浮雕**：`--bg:#E6EAF0`（底即卡）`--ink:#333B49 --muted:#5F6673 --shD:rgba(163,177,198,.62) --shL:rgba(255,255,255,.95)`。凸（可按）`box-shadow:5px 5px 11px var(--shD),-5px -5px 11px var(--shL)`；凹（已選、輸入區）`inset 3px 3px 7px var(--shD),inset -3px -3px 7px var(--shL)`；不用框線；主按鈕仍實心主色配白字。CSS 變數名大小寫有別（`--shD` 不是 `--shd`）。

**S3 琉璃**：`body{background:linear-gradient(133deg,var(--acc),var(--acc2))}`；`--ink:#232936 --muted:#454C59`；亮玻璃 `rgba(255,255,255,.70)`＋`backdrop-filter:blur(24px)`＋`1px solid rgba(255,255,255,.7)`；深玻璃 `rgba(22,26,42,.66)` 配白字，只用在示範頁的導覽（v20 起元件不用深玻璃；統計卡 hero 是亮玻璃配主色數字）。鐵則：**文字不落在漸層上（一律墊玻璃）、彩色字不落在 70% 玻璃上（一律墊白）**。

**S4 手帳**：`--paper:#FAF3E4 --card:#FFFDF7 --line:#D8CDB8 --ink:#2E2A24 --muted:#6E6656`。容器 `border:2px solid var(--ink)`＋歪框 `border-radius:255px 18px 225px 18px/18px 225px 18px 255px`（交錯用 `18px 225px 18px 255px/255px 18px 225px 18px`）；按鈕硬影 `box-shadow:2.5px 2.5px 0 var(--ink)`、按下位移歸零；分隔線 2px 虛線；裝飾限紙膠帶與麥克筆畫重點；表格資料區保持乾淨。

**S5 極光**：`--page:#FCFCFD --line:#E9E9EF --ink:#22262E --muted:#686E78 --dark:#1C1F27`。背景 `body::before` 三個 `radial-gradient(color-mix(in srgb,var(--acc) 30%,transparent))` 暈染加 `blur(6px)`；面板 `rgba(255,255,255,.92)`、圓角 `26px 26px 26px 8px`（小件 `18px 18px 18px 6px`）；漸層只出現在強調按鈕、AI 標記、hero 數字或目前狀態節點三處；**強調按鈕就是實心主按鈕 `.btn.primary`**（`linear-gradient(95deg,var(--acc),var(--acc2-deep))`，停用時回到灰底灰字，v20）。

**S6 石墨**：`--page:#F4F4F4 --card:#FFFFFF --band:#F6F6F6 --sel:#F2F2F2 --line:#E3E3E3 --line-2:#D9D9D9 --ink:#171717 --muted:#6A6A6A --dark:#3B3B3B`；圓角 `--r-lg:12px --r-sm:6px --r-pill:999px`。所有卡片、輸入框、按鈕 `1px solid var(--line)`、零陰影。三條鐵則：

一、**側欄、頂列與頁面同色，只有卡片與輸入元件是白的**——「只有資料躺在白紙上，其餘都是同一張桌面」。做成側欄白、頁面灰就變成另一套風格。
二、**灰階是純無彩色**，每個灰的紅綠藍三值必須相等，不得帶藍調或黃調。
三、**表格區不用品牌色，只有選取列例外**——篩選膠囊選中、側欄 hover、分段控制都用中性灰 `--sel`；品牌色只留給主按鈕、連結、側欄選中項、目前頁籤、選取列。

**S7 編輯**（規範 8.2）：`--page:#FAF8F3`（暖白紙）`--card:#FFFFFF --band/paperc:#F3F0E9 --line:#E2DDD3 --ink:#1A1814 --muted:#615C54`；零陰影。外層區塊 `.board` 不加框、改上緣 `2px solid var(--ink)` 欄線，左右內距 0、上方 `--sp-6`；框只留給卡片與輸入元件（1px 細線）。兩項風格層例外（只有 S7）：**標題用明體**——H1〜H3 與元件內標題 `font-family:'Noto Serif TC','Songti TC','Source Han Serif TC','PMingLiU',serif`（Google Fonts 加載 `Noto+Serif+TC:wght@700;900`），字級行距字重照表，內文標籤按鈕仍黑體、金額仍 Arial；**直角**——`--r-lg:0 --r-sm:2px`，容器 0、按鈕輸入框選項標籤 2px、頭像圓點正圓。提示框改用 `--paperc` 底（外層區塊透明，用頁面色會消失）。

兩項風格層例外（只有 S6 適用）：按鈕與輸入框圓角 **6px**、卡片與表格容器 **12px**（狀態膠囊、篩選膠囊、屬性 tag 仍 999px）；N4 級（料號、單號、日期、IP、追蹤碼）改等寬字 `"SF Mono",Menlo,Consolas,"Liberation Mono",monospace`，**金額 N1〜N3 仍用 Arial、中文仍用 Noto Sans TC**。

## 4. 色彩四層與色系切換（十二組核心 ＋ SC1〜SC3）

**鐵則：介面上不得出現這四層以外的任何顏色。**

### 4.1 第一層 品牌雙色（使用者可切換，執行時注入七個變數）

```
--acc  --acc-soft  --acc-deep  --acc2  --acc2-soft  --acc2-deep  --acc2-text
```

- `--acc` 主色負責所有「操作」：主按鈕、選中、連結、聚焦框、目前頁籤、進行中狀態。
- `--acc2` 副色負責「點綴」：品牌標記、圖表第二數列、趨勢箭頭；每頁最多三處。
- `--acc-deep` 十五組一律等於 `--acc`。
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
| SC2 | 鈷藍 × 亮橘 | `#2449E8` | `#EEF1FD` | `#FF7A1A` | `#FFF3EA` | `#B0490A` | 淺型 | S1、S3、S5、S6；S4 需加框線；S2 鎖住（高彩度，前台與活動頁） |
| SC3 | 石板藍 × 冰川青 | `#3D4C5E` | `#EFF1F3` | `#5FB4C9` | `#F0F8FA` | `#296778` | 淺型 | S1、S3、S4、S5、S6；S2 需加框線（冷灰藍，工具型） |

顏色一律 sRGB 十六進位；Pantone、RAL 等外部色號只作對照，不得寫進程式或規範。退場的舊色（石板藍 `#334155`、酒紅 `#7A2230`）新專案不得選用。專案若有既有品牌色，只替換第一層七個變數，仍須通過第 9 節對比稽核。

### 4.2 切換器實作（三處必須一致：後台設定頁、使用者偏好、網址參數）

```js
const THEMES={
 c1:{"id":"C1","name":"深海藍","acc":"#2B5FB8","accSoft":"#EDF1F9","acc2":"#C2377B","acc2Soft":"#FAEEF4","acc2Deep":"#BA3576","accDeep":"#2B5FB8","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c2:{"id":"C2","name":"深湖青","acc":"#0F5C63","accSoft":"#EBF1F2","acc2":"#C4663A","acc2Soft":"#FAF2EE","acc2Deep":"#A15430","accDeep":"#0F5C63","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c3:{"id":"C3","name":"深靛","acc":"#2C2A72","accSoft":"#EDEDF3","acc2":"#8C7AE6","acc2Soft":"#F5F4FD","acc2Deep":"#6A5DAF","accDeep":"#2C2A72","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c4:{"id":"C4","name":"電光紫","acc":"#6D28D9","accSoft":"#F3EDFC","acc2":"#0F8A99","acc2Soft":"#EBF5F6","acc2Deep":"#0D7481","accDeep":"#6D28D9","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c5:{"id":"C5","name":"森林綠","acc":"#1F5E3D","accSoft":"#ECF1EF","acc2":"#A16207","acc2Soft":"#F7F2EA","acc2Deep":"#975C07","accDeep":"#1F5E3D","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c6:{"id":"C6","name":"胡桃棕","acc":"#6B4A33","accSoft":"#F2F0EE","acc2":"#4A6B55","acc2Soft":"#F0F2F1","acc2Deep":"#4A6B55","accDeep":"#6B4A33","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c7:{"id":"C7","name":"焦糖磚橘","acc":"#A8481F","accSoft":"#F8EFEC","acc2":"#2B2B2B","acc2Soft":"#EDEDED","acc2Deep":"#2B2B2B","accDeep":"#A8481F","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c8:{"id":"C8","name":"暖墨","acc":"#23201E","accSoft":"#ECECEC","acc2":"#D95F1E","acc2Soft":"#FCF1EC","acc2Deep":"#AE4C18","accDeep":"#23201E","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c9:{"id":"C9","name":"唇膏紅","acc":"#9F2436","accSoft":"#F7EDEF","acc2":"#2A5C6A","acc2Soft":"#EEF2F3","acc2Deep":"#2A5C6A","accDeep":"#9F2436","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c10:{"id":"C10","name":"節慶桃紅","acc":"#9E2C6A","accSoft":"#F7EEF3","acc2":"#5C97CB","acc2Soft":"#F2F7FB","acc2Deep":"#336DA0","accDeep":"#9E2C6A","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c11:{"id":"C11","name":"燒橄欖","acc":"#646049","accSoft":"#F3F2F0","acc2":"#C65D52","acc2Soft":"#FAF2F1","acc2Deep":"#B2463B","accDeep":"#646049","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c12:{"id":"C12","name":"玫瑰棕","acc":"#80565B","accSoft":"#F5F1F2","acc2":"#BA797D","acc2Soft":"#F9F4F5","acc2Deep":"#9F5257","accDeep":"#80565B","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 sc1:{"id":"SC1","name":"深綠 × 相思黃","acc":"#35463D","accSoft":"#EFF0EF","acc2":"#DACD65","acc2Soft":"#FCFBF3","acc2Deep":"#6F6519","accDeep":"#35463D","acc2Type":"light","styles":["s1","s3","s5","s6","s7"],"adjust":["s4"],"series":"SC"},
 sc2:{"id":"SC2","name":"鈷藍 × 亮橘","acc":"#2449E8","accSoft":"#EEF1FD","acc2":"#FF7A1A","acc2Soft":"#FFF3EA","acc2Deep":"#B0490A","acc2Type":"light","styles":["s1","s3","s5","s6","s7"],"adjust":["s4"],"series":"SC","accDeep":"#2449E8"},
 sc3:{"id":"SC3","name":"石板藍 × 冰川青","acc":"#3D4C5E","accSoft":"#EFF1F3","acc2":"#5FB4C9","acc2Soft":"#F0F8FA","acc2Deep":"#296778","acc2Type":"light","styles":["s1","s3","s4","s5","s6","s7"],"adjust":["s2"],"series":"SC","accDeep":"#3D4C5E"}
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
  document.documentElement.classList.toggle('sc-adjust', t.adjust.includes(STYLE));   // S4 × SC1、S4 × SC2、S2 × SC3：副色填色自動加 1px 墨色框線
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
 --fs-d1:3.0rem;--lh-d1:1.15;--ls-d1:-0.01em; --fs-h0:2.6rem;--lh-h0:1.30;--ls-h0:0.02em; --fs-h1:2.1rem;--lh-h1:1.40;--ls-h1:0.03em;
 --fs-h2:1.7rem;--lh-h2:1.45;--ls-h2:0.06em;  --fs-h3:1.4rem;--lh-h3:1.50;--ls-h3:0.08em;
 --fs-b1:1.4rem;--lh-b1:1.80; --fs-b2:1.25rem;--lh-b2:1.70; --fs-b3:1.2rem;--lh-b3:1.70;
 --fs-l1:1.2rem;--lh-l1:1.50;--ls-l1:0.08em; --fs-l2:1.1rem;--lh-l2:1.50;--ls-l2:0.15em;
 --fs-n1:2.3rem;--lh-n1:1.20; --fs-n2:1.9rem;--lh-n2:1.25; --fs-n3:1.25rem;--lh-n3:1.60; --fs-n4:1.25rem;--lh-n4:1.60;--ls-n4:0.02em;
 --sp-1:0.4rem;--sp-2:0.8rem;--sp-3:1.2rem;--sp-4:1.6rem;--sp-5:2.0rem;--sp-6:2.4rem;--sp-7:3.2rem;--sp-8:4.0rem;--sp-9:4.8rem;--sp-10:6.4rem;
 --r-lg:16px;--r-sm:12px;--r-pill:999px;--bw:1px;--bw-on:1.5px}
[data-type="expressive"]{                   /* 前台商品頁、目錄、首頁 */
 --fs-d1:4.4rem;--lh-d1:1.10; --fs-h0:4.0rem;--lh-h0:1.25; --fs-h1:3.0rem;--lh-h1:1.35; --fs-h2:2.2rem;--lh-h2:1.40; --fs-h3:1.6rem;--lh-h3:1.50;
 --fs-b1:1.6rem;--lh-b1:1.90; --fs-b2:1.4rem;--lh-b2:1.80; --fs-b3:1.3rem;--lh-b3:1.90;
 --fs-l1:1.2rem;--lh-l1:1.50; --fs-l2:1.1rem;--lh-l2:1.50;
 --fs-n1:3.0rem;--lh-n1:1.15; --fs-n2:2.3rem;--lh-n2:1.20; --fs-n3:1.4rem;--lh-n3:1.60; --fs-n4:1.3rem;--lh-n4:1.60}
@media (max-width:767px){[data-type="expressive"]{--fs-d1:3.6rem;--fs-h0:3.2rem}}
:root{--dur-1:120ms;--dur-2:200ms;--dur-3:320ms;--ease-out:cubic-bezier(.2,0,0,1);--ease-in:cubic-bezier(.4,0,1,1)}
@media (prefers-reduced-motion:reduce){:root{--dur-1:0ms;--dur-2:0ms;--dur-3:0ms}}
body{font-family:'Noto Sans TC',sans-serif;font-size:var(--fs-b1);line-height:var(--lh-b1)}
.num,.amt,.price{font-family:Arial,Helvetica,'Noto Sans TC',sans-serif;font-variant-numeric:tabular-nums}
```

| 代號 | 用途 | 字重 | 字型 |
|---|---|---|---|
| D1 | 顯示數字（統計大數） | 700 | Arial |
| H0 | 展示標題（只給前台 Hero 與活動主標，一頁最多一個） | 900 | 黑體 |
| H1 / H2 / H3 | 頁面標題 / 區塊標題、彈窗與面板標題 / 卡片標題列、行內小標題 | 900 | 黑體 |
| B1 / B2 / B3 | 內文 / 表格內密集內文 / 說明輔助 | 400 | 黑體 |
| L1 / L2 | 欄位標籤 / 微標籤眉標 | 700 | 黑體 |
| N1 / N2 / N3 / N4 | 合計金額 / 小計 / 表格金額 / 料號單號日期 | 700 700 700 400 | Arial |

硬規則：字級只能是這十四級；**H0 只給前台 Hero 與活動主標、一頁最多一個、後台不用，一行以十四字為上限、最多兩行，必須加 `text-wrap:balance`**（40px 中文標題容易在最後一行只剩一兩個字），768 以下降為 32px；D1 仍只給數字；寫 `var(--fs-xx)` 就要同時寫 `var(--lh-xx)`；12px 是承載句子的最小字級（Expressive 13px）；11px 是整套標尺的絕對下限，只給 L2 微標籤（一到四個字的單詞或極短片語），字重 700 以上並加大字距，不得寫句子；**欄位標籤一律 12px（L1），不得用 11px**；**不得出現 10px 以下的字**；**標題不得小於它所領導的內文**（H3 與 B1 同為 14px，靠字重 900 與字距區分）；**H2 與 H3 依用途分**：彈窗（`.modal .mh`）、側滑面板（`.drawer .dh`）、獨立自成一件事的大卡片用 H2，卡片標題列（`.card-title`）、表格標題（`.tcap`）、圖表卡標題、表單分組小標題用 H3，覺得卡片標題太小就改用 H2、不得新增中間值（見規範 4.2）；中文不用斜體；行距不採用 M3 或 Tailwind 的 1.43（中文會糊）；行動裝置不縮字級只改版型；金額千分位必加、貨幣前綴縮小 0.68 倍轉灰、表格中靠右、負數轉 error 紅。

**行距一定要跟字級配成同一代號**，不可以拿 B2 的字級去配 B3 的行距。每個值單獨看都在表上，所以肉眼與只看宣告值的檢查都抓不出來。沒有自己指定行距的元素會往上繼承，所以 `body` 一定要寫 `line-height:var(--lh-b1)`——漏掉的話整份文件的預設行距會退回瀏覽器的 `normal`（約 1.2 倍）。兩個例外是規範自己要求的、不算違規：貨幣前綴縮小 0.68 倍、768px 以下輸入框 16px 防 iOS 放大。見規範 4.2。

間距：所有 margin、padding、gap 只取 `--sp-1`〜`--sp-10`（4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48 / 64px），負 margin 不用（堆疊頭像、資料夾頁籤例外）。卡片內距 16 / 20、儲存格與表頭與表格標題列 12 / 20（勾選欄 `.ck` 右內距 0 例外）、欄位標籤到輸入框 8（`.field label{margin-bottom:var(--sp-2)}`）、說明文字到輸入框 4、元件之間 12、區塊之間 24。token 連號命名，`--sp-7` 是 32px、`--sp-8` 是 40px（規範 v18 前的 space-8＝32 寫法已廢）。

**焦點環（規範 10.3，v18）**：鍵盤到達的每個可互動元件 `:focus-visible{outline:2px solid var(--acc);outline-offset:2px}`，輸入框、下拉、多行輸入 `outline-offset:0`；不得 `outline:none` 而不補，換框線色不算替代。滑鼠點擊不顯示（`:focus-visible` 自然如此）。

**佔位文字（規範 10.1，v18）**：`::placeholder{color:var(--muted);opacity:1}`。瀏覽器預設的 `#757575` 在 S2 底、S6 深色、S1 頁面底都不到 4.5。

**層級（規範 5.6，v18）**：只有五層 `--z-sticky:10`（吸附表頭、頂列、底部固定條）、`--z-pop:20`（下拉、就地確認、自動完成）、`--z-drawer:30`、`--z-modal:40`、`--z-toast:50`（Toast、提示氣泡）。不得出現表外的 `z-index`；元件內局部堆疊用 `z-index:1` 加 `isolation:isolate`。

圓角四級固定、維持 px：18px 焦點框與大面板、16px 卡片與表格容器、12px 輸入框小卡選單、999px 所有按鈕與狀態膠囊；框線 1px、選中 1.5px。陰影由各風格定義（奶油、極光、石墨零陰影，浮雕雙向柔影，琉璃面板投影，手帳硬影）。

**風格層例外只有 S6 石墨與 S7 編輯**：S6 按鈕與輸入框 6px、卡片與表格容器 12px、N4 級改等寬字；S7 容器 0、按鈕與輸入元件 2px、標題用明體。其餘五套一律照上表。

**元件高度是結構層，七套共用（規範 5.4，v17）**：高度做成 token、`min-height` 鎖定、**垂直內距歸零、flex 置中**，框線粗細與陰影有無都不會改變高度；**風格層不得出現 `min-height` 與 `padding`**。

```css
:root{--h-btn-primary:4.0rem;--h-btn:3.8rem;--h-btn-sm:3.2rem;--h-input:4.0rem;--h-qty:3.4rem;--h-pill:2.4rem;--h-nav:3.8rem;--h-tag:2.0rem}
@media (max-width:767px){:root{--h-btn-primary:4.4rem;--h-btn:4.4rem;--h-btn-sm:4.0rem;--h-input:4.4rem;--h-qty:4.4rem}}
.btn{min-height:var(--h-btn);padding:0 var(--sp-5);display:inline-flex;align-items:center;justify-content:center}
```

| 元件 | 高度 | 水平內距 |
|---|---|---|
| 主按鈕 `.btn.primary` | 4.0rem（手機 4.4） | `--sp-6` |
| 一般按鈕 `.btn`、危險鈕 `.btn.danger`、選項 chip `.chip` | 3.8rem（4.4） | 按鈕 `--sp-5`、chip `--sp-4` |
| 小按鈕 `.btn.sm`、篩選膠囊 `.pillf` | 3.2rem（4.0） | 小按鈕 `--sp-3`、膠囊 `--sp-4` |
| 輸入框、下拉選單 | 4.0rem（4.4，字 16px 防 iOS 放大） | `--sp-3` |
| 數量調整器 `.qty` | 3.4rem（4.4），加減鈕 3.2rem 寬 | — |
| 狀態膠囊 `.st` | 2.4rem（不放大） | `--sp-3` |
| 屬性 tag `.tag` | 2.0rem | `--sp-2` |
| 側欄項目 `.nitem` | 3.8rem | `--sp-4` |
| 表格列 | **不另設**，由儲存格內距 `--sp-3` 與內容決定：純文字 ≈46px、含狀態膠囊約 50px | 儲存格 `--sp-5` |

**密集模式（規範 5.7，v24，目前只開放 S6 石墨）**：密集和深色一樣是同一套風格的「模式」，不是另一套風格。`<html data-density="compact">`（或 `DS.setDensity('compact')`）把高度 token 各縮一級：主按鈕、一般按鈕、輸入框、側欄項目 32px，小按鈕、篩選膠囊、數量調整器 28px，狀態膠囊 20px，屬性 tag 18px；表格儲存格與表頭內距上下 4（`--sp-1`）左右 12（`--sp-3`），純文字列高約 30px；表格標題列 8／12、板 16、卡片標題列與內容和統計卡 8／12、描述清單 4／12；欄格自動改緊湊欄距 `--sp-3`。**只改尺寸，字級、行距、顏色、圓角、框線粗細都不變**，可與深色並用（`data-theme="dark" data-density="compact"`）。用在一屏要看大量列、用滑鼠操作的後台（訂單與庫存清單、監控與日誌、對帳、權限表）；預設一律標準、不跟隨系統，使用者的選擇記在 `localStorage` 的 `ds.density`。768px 以下不生效（44px 觸控下限優先，CSS 本身包在 `@media (min-width:768px)` 裡）。規則在 `base.css`、七套共用，開放與否由 `theme.js` 的 `DENSE_STYLES` 決定；S1 的留白、S2〜S5 與 S7 的材質在 28〜32px 的元件上會擠，先不開放。風格層不得出現密集規則。

為什麼這樣寫：v16 以前這張表只是數字沒落到 CSS，七套實測同一顆按鈕有三到四種高度（S1 39、S2 45、S4 41px）。警示條內的 `.btn.sm` 依 7.3 豁免（`min-height:0`）。相鄰可點元件至少留 8px。正圓元件（頭像、圓點、播放鈕）加 `aspect-ratio:1/1` 以免在 flex 列被拉成橢圓。

**動態（規範 5.5）**：轉場時長只用 `--dur-1` 120ms（顏色、框線、陰影、按下：滑過與聚焦）、`--dur-2` 200ms（元件內位移與展開：開關滑塊、折疊、下拉、提示氣泡）、`--dur-3` 320ms（彈窗、側滑面板、Toast），進場與狀態變化用 `--ease-out`、退場用 `--ease-in` 且短一級；不寫死秒數、不寫 `transition:all`；只轉場顏色、背景、框線色、陰影、`opacity`、`transform`，不轉場 `width`、`height`、`top`、`left`、`margin`、`padding`（移動用 `translate`）。骨架屏與轉圈等迴圈動畫不受此限。

## 6. RWD

斷點 1024 / 768 / 480（px，描述裝置）。768 以下：側欄改覆蓋式抽屜加遮罩、漢堡鈕 44px；表格轉卡片列（每格 `data-l` 帶欄名，不做水平捲動）；輸入框 16px；商品規格頁計價面板改底部固定條；主要動作滿版。480 以下單欄，**例外是商品卡列表維持兩欄**（卡片與欄間距收為 `--sp-3`、名稱最多兩行 `-webkit-line-clamp:2`、評價只留星等、加入購物車改右下角 44px 圖示鈕並以 `aria-label` 寫明商品名稱；見規範 6.3）。任何寬度 body 不得橫向捲動（flex 子項記得 `min-width:0`）。

**級別與欄格（規範 6.1、6.5，v22）**：五個級別緊湊 <480、中 480〜767、平板 768〜1023、寬 1024〜1279、特寬 ≥1280。頁面上不同區塊怎麼分寬度一律用 `base.css` 的 12 欄格：`<div class="grid">` 裡放 `.col-12`、`.col-6`×2、`.col-8`＋`.col-4`、`.col-4`×3、`.col-3`×4 五種跨欄，不開其他分法；平板與中自動 8 欄、緊湊 4 欄全部堆疊。欄距標準 `--sp-6`、緊湊 `--sp-3`（加 `.dense`；480 以下自動）。固定寬的側欄 226px、摘要面板 340px、側滑面板不佔欄格（混合格）。同一種卡片排幾欄照上面的網格清單，不必套欄格。容器左右內距寬以上 `--sp-6`、平板 `--sp-5`、768 以下 `--sp-4`（規範 6.2；舊條文的 26px 已改正）。

## 7. 版型與文案（摘要）

後台：側欄式框架（側欄 226px、頂列麵包屑與通知鈴、內容區最大 1060px）。前台：頂部分頁式。每頁最多一顆實心主按鈕；危險動作二次確認且寫明後果；空狀態是邀請不是報告（給出口）；錯誤訊息說怎麼修；語氣是專業同事，不用驚嘆號與語尾助詞。詳見規範第九、十一章。

**線條與框線的兩條結構規則（規範 9.3 第六、七條，v21）**——每個元件單看都對、放在一起卻線條打架，是 AI 產頁面最常見的錯：
一、**一處分隔只用一條線。** 區塊標題用了延伸細線，下方就不再放分隔線或卡片標題列的底線；`.card-title` 已有底線，標題就不再用延伸細線；兩個有框線的容器相鄰時不再加分隔線。判斷法：兩條線之間只有空白、沒有任何文字或元件，其中一條就是多餘的。
二、**有框線的元件相鄰時最小間距 `--sp-3`（12px）。** 按鈕列與輸出框、卡片與卡片、輸入框與按鈕邊緣到邊緣至少 12px；並排的小按鈕、chip、膠囊可用 `--sp-2`；低於 8px 視為貼合。刻意共用框線的組件不在此限：分段控制、數量調整器、分頁器、頁籤、表格內部，以及下拉選單與觸發元件之間的 `--sp-1`。

**間距三原則（規範 9.3 第八至十條，v22）**：內部間距 ≤ 外部間距（卡片內距 16／20，卡片之間至少 `--sp-6`）；區塊之間一律大於區塊內部（區塊內 `--sp-3`〜`--sp-4`、區塊之間 `--sp-6` 以上、頁面大區段 `--sp-7`〜`--sp-8`）；`--sp-1`、`--sp-2` 只用在元件內部與同一組並排小元件之間，獨立元件或組與組之間最小 `--sp-3`（就是上面第二條）。

## 8. 元件清單（62 項：核心 45 必備、選用 17 依系統勾選）

**核心（每個專案都要，七套風格皆已實作）**
基礎：設計 Token、字級層級、分隔線。動作：按鈕、動作鈕 ⋯、分段控制。表單：輸入框、搜尋框、核取與單選、篩選膠囊、開關、上傳、多行輸入、下拉選單、多選＋搜尋、日期與時間選擇器、自動完成、數字步進器、選項 chip。資料呈現：表格、表格進階（排序、欄位切換、批次選取）、卡片、統計卡、描述清單、狀態標籤、屬性 tag、折疊面板、頭像、數字角標。導覽：側欄項目、頁籤、麵包屑、分頁器（P4 底線數字式）、側滑面板。回饋：彈窗、就地確認、提示氣泡、Toast、警示條（四語意色）、提示框、空狀態、骨架屏、通知鈴、進度條、搜尋無結果。

**選用（依系統類型）**
工具列、滑桿、級聯選擇、穿梭框、摘要方塊、來源標記（原 AI 標記）、百分比膠囊、量表、樹狀、時間軸、圖表（兩個數列以下用主色與深副色，三個以上改用第四層八色）、媒體與輪播、動態列表、步驟精靈、唯讀步驟、分割面板、結果頁。

**警示條與提示框（v7 定案、v8 補對齊守則，七套一致）**：警示條 `.alert` 不用左側 4px 色條，改 `border:1px solid color-mix(in srgb,currentColor 32%,transparent)` 一圈細框，框線顏色自動跟著語意色走；標題與內文同一行（`b` 與 `p` 都 `display:inline`），圖示保留，背景仍是該語意的 `-soft` 淡底。四條使用守則：**標題是選用的**（一句話講得完就不要標題）、**動作最多一顆**且做成帶底線的文字連結而非按鈕（`.alert .btn.sm` 去底去框去陰影）、**錯誤與警告不給關閉鈕**（使用者關掉就看不到問題了，只有 info 與 ok 可關）、**文字動作與關閉鈕要跟內文站在同一條基線上**（和內文共用同一個行框：同字級、同行距、`align-self:flex-start`，不要再給它 `min-height`——按鈕那個 32px 會把整列撐高，差將近 6px）。提示框 `.notice` 去掉左側主色條與彩色底，S1 與 S6 直接用頁面灰底無框、S2 用凹面無框、S3 是 1px 玻璃框、S4 是 2px 虛線框、S5 是淡線框加淡底——它只是「順便一提」，不該比旁邊的內容搶眼。

七套**共用同一份元件 HTML**：S1 奶油是基準，其餘六套只覆寫材質（S2〜S5 由 `build_from_s1.py` 以 S1 ＋ `material/<套>.css` 產生，v20；S6、S7 由各自的產生器以 S1 為基底重建；S3、S5、S6 的深色規則由 `build_dark.py` 插進同一份元件庫，v23）；七套的 62 個節標題逐字相同，少任何一項都會在設計系統瀏覽器的元件索引顯示 ✕。共用 class 語彙（七套一致，不得自創同義名）：`.btn .btn.primary .btn.sm .btn.danger`、`.field label input .req .msg`、`.st.acc/.wrn/.ok/.err/.gray`、`.tag.acc/.err/.gray`、`.aibadge`、`.chip`、`.pillf`、`.seg`、`.qty`、`.check`、`.radio`、`.sw2`、`.card .card-title`、`.tblwrap .tcap table.t .amt .dt .p4`、`.statc .k .v .delta`、`.desc`、`.avatar`、`.badge`、`.count`、`.tabs .tab`、`.nitem`、`.drawer`、`.modal .mh .mb .mf`、`.pop`、`.tip`、`.toast`、`.alert.err/.wrn/.ok/.info`、`.notice`、`.empty`、`.skel`、`.bell`、`.bar`、`.stepper`、`.tl`、`.feed`、`.divider .hr .vdiv`。完整標記與樣式直接抄 `assets/components/` 裡所選風格檔案的對應區段（每項元件一節，節標題六套逐字相同，可用 grep 找）。

**圖示（規範 7.4）**：全站只用 Lucide（開源、ISC 授權），版本寫死不用 latest，線條畫法不混實心；尺寸只有 16（配 B2、B3、L1）、20（配 B1、H3、按鈕）、24（頂列圖示鈕、H2）、48（空狀態與插圖），線寬一律 2；顏色 `currentColor`，只有「本身就是操作」才用主色，語意色只給狀態圖示；圖示與文字間距 16px 配 4px、20px 以上配 8px；純圖示按鈕要 `aria-label` 且點擊範圍 44×44，裝飾性圖示加 `aria-hidden="true"`；七套風格共用同一組圖示。

**前台長什麼樣**：`assets/storefront/*.html` 七張選物店首頁（掛 Expressive，只用元件庫 class；S3、S5、S6 同一頁可切深色），設計系統瀏覽器的「前台示範」檢視可切換風格、模式與色系。做前台時照它的結構起手。

## 9. 交付前四項自動檢查（腳本在本 skill 的 `scripts/`）

四項都通過才算完成。（第 0 節提到的第五、六項——元件結構尺寸與拆檔無損——只在維護元件庫本身時跑，腳本不隨公開版發佈；照 `dist/` 引用 CSS、不覆寫元件尺寸的產品，這兩項自然成立。）腳本對任何 HTML 檔或網址都能跑，有不合規時結束碼為 1，可以直接接進 CI（持續整合：每次提交自動跑檢查）。第一、四項與第三項的 `--render` 需要先裝依賴：`pip install -r scripts/requirements.txt && playwright install chromium`（Playwright 是自動操控瀏覽器的工具）。

| 檢查 | 指令 | 標準 |
|---|---|---|
| 一、對比稽核 | `python scripts/audit_contrast.py page.html --themes all` | 把頁面畫出來，對每個文字節點取周邊像素當底色；一般字 ≥4.5、大字 ≥3.0；停用控件豁免。頁面若支援色系切換，每個可用色系都要 0 不及格（`--themes` 走網址 hash，例如 `page.html#c3`） |
| 二、標尺合規 | `python scripts/check_tokens.py page.html` | 字級不在十四級、行距字距不在表上、間距不在標尺、負 margin，任何一項出現即不通過；固定 `height` 列為提醒，承載文字的要改 `min-height` |
| 三、行高配對 | `python scripts/check_lineheight.py page.html --render` | 靜態掃每條 CSS 規則的字級與行距是否同代號、有沒有寫了字級卻漏掉行距；`--render` 再渲染頁面，比對每個文字元素實際算出來的字級與行高。`check_tokens.py` 只看宣告值，抓不到這一類 |
| 四、溢出檢查 | `python scripts/check_overflow.py page.html` | 390px、768px 寬度下不得橫向捲動，並列出撐破版面的元素 |

前台閱讀型頁面（`data-type="expressive"`）的二、三項加 `--type expressive`；同一頁兩套都用（例如前台頁面引用了元件庫的後台樣式）改用 `--type all`。開發時才出現的控制列等區塊，加上 `data-audit-skip` 屬性即可排除在對比稽核外。

批次改動後，所選風格的每個頁面都要截圖對照，不抽樣。若無法執行腳本（例如沒有 Python 環境），至少逐條人工核對：所有字級與行距都引用 `var(--fs-xx)` ＋ 同代號 `var(--lh-xx)`、間距只用 `--sp-*`、沒有寫死的色碼。

## 10. 起手式：引用 dist/，不要複製示範頁的 CSS（規範第十二章）

元件樣式的唯一來源是公開倉庫根目錄的 `dist/`（由 `emit_css.py` 自七套元件庫產生，檔頭有版號，與規範同版）。工程師手冊 `dist/USAGE.md`（＝《設計系統使用說明 v4》）、範例頁 `dist/examples/`（七套風格各一張、各在 8.7 的首選情境：S1 後台、S2 控制面板、S3 品牌官網、S4 點餐、S5 預約、S6 監控儀表板、S7 說明中心；`same-markup.html` 是同一份標記換七套殼，只說明「風格是殼」）。幫人起新頁面時，照情境挑一張範例當起點，不要七套都拿訂單後台換皮。**不要**從 `components_s*.html` 複製 `<style>`——複製那一刻起產品與元件庫就分家。

七套載法相同（三檔 ＋ theme.js，順序不能換；v20 起 S2〜S5 也以 S1 為基底，七套共用同一份元件 HTML）：

```html
<html lang="zh-Hant" data-style="s1">              <!-- 全站只選一套風格，建置時決定 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="dist/tokens.css">     <!-- 字級、間距、圓角、高度、動態、層級 -->
<link rel="stylesheet" href="dist/base.css">       <!-- 結構層 ＋ S1 材質：62 項元件、焦點環、佔位文字、RWD -->
<link rel="stylesheet" href="dist/style-s1.css">   <!-- 這一套的材質層；換風格只換這一行（s1〜s7） -->
<body data-type="productive">                      <!-- 前台閱讀型頁面改 expressive -->
  …元件 HTML 照第 8 節的 class 語彙寫…
<script src="dist/theme.js"></script>              <!-- DS.applyTheme('c1')、DS.setColorScheme('dark'|'light'|'system')、DS.setDensity('compact'|'normal') -->
```

v19 的 S2〜S5 過渡版（兩檔、不載 base.css）已退場。頁面不加 `.up`、`.glass`、`.wob`、`.org` 之類的修飾 class——`.board`、`.card`、`.statc` 本身就帶著該套材質；數量調整器一律用 `<input>`。S5 的漸層強調按鈕就是 `.btn.primary`。

深色（只有 S3、S5、S6）：`<html data-theme="dark">` 強制深、`light` 強制淺、不寫跟隨系統；這三套的風格檔同時含 `html[data-theme="dark"]` 與 `@media (prefers-color-scheme:dark)` 兩段，切換不換檔、不重載，品牌色深色值由 theme.js 的 DARK 表（依風格分表）套用。產品可用任何框架，但元件 HTML 照元件庫 class、樣式只來自 dist；**不混第三方 UI 庫的元件外觀**，需要行為就用 headless 庫。瀏覽器基線 Chrome／Edge 111+、Safari 16.4+（iOS 16.4+）、Firefox 121+。

任何元件的 CSS 不得寫死色碼與字級，一律引用變數；唯一例外是純黑純白與陰影用的半透明黑。

## 11. 參考檔索引（需要細節時才讀，不必一次全讀）

| 要查的事 | 讀這個檔 |
|---|---|
| 名詞對照表、文件目的、五條設計總則 | `references/overview.md` |
| 第三章 色彩四層、十二組核心與 SC 特殊色系色碼、副色深型與淺型、著色面上的文字 | `references/color.md` |
| 第四章 字型、十四級字級、行距配對、金額與數字格式 | `references/typography.md` |
| 第五章 間距標尺、圓角、框線、元件高度、動態（時長與緩動）、層級、密集模式 | `references/spacing-radius.md` |
| 第六章 斷點與級別、容器寬度與內距、12 欄欄格系統、側欄抽屜、表格轉卡片列 | `references/rwd.md` |
| 第七章 元件規範（含警示條與提示框守則、Lucide 圖示規範） | `references/components.md` |
| 第八章 各風格定義、風格 × 色系矩陣、風格 × 系統類型選型、深色模式（S3、S5、S6） | `references/styles.md` |
| 第九章 後台與前台版型、頁面結構、線條與間距原則 | `references/layout.md` |
| 第十章 對比、焦點、鍵盤操作 | `references/accessibility.md` |
| 第十一章 介面文案（按鈕、錯誤訊息、空狀態的寫法） | `references/copywriting.md` |
| 第十二章 開發對接：引用 dist/ 的 CSS、theme.js、瀏覽器支援基線 | `references/dev-handoff.md` |
| 附錄 已退場的歷年色系 | `references/legacy-colors.md` |
| 某個元件的完整 HTML 與 CSS | `assets/components/<風格>.html`，搜尋該元件的節標題 |
| 前台頁面的結構範例（選物店首頁，Expressive 字級） | `assets/storefront/<風格>.html` |
| 各風格共用的數值一覽（字級、間距、圓角、色彩、斷點） | `assets/foundations.html` |
| 字級、間距、造型 token | `assets/tokens.css` |
