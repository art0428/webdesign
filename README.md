# 管理者工作室 網頁設計系統 · ui-design-format

一套可以直接裝進 Claude 的網頁介面設計系統（以 Agent Skill 形式提供：裝好之後，Claude 做網頁時會自動照這套規範）。
七套風格（S3、S5、S6 另有深色模式；依風格可切寬鬆、標準、緊湊三檔密度）、十二組核心色系加三組特殊色系、十四級字級、間距與動態標尺、12 欄欄格、62 項元件、可直接引用的 CSS（`dist/`）、前台示範頁，外加五支交付前的自動檢查腳本。手機與平板版面有專門的規則與檢查。

**A Claude Agent Skill for building web UIs: 7 visual styles (3 with dark mode) × 15 color themes, a 14-level type scale, spacing tokens, 62 components, and 5 automated pre-delivery checks (contrast, token compliance, line-height pairing, overflow, mobile/tablet layout). Docs are in Traditional Chinese.**

**線上預覽** → <https://art0428.github.io/webdesign/>
左側切換風格、模式（S3、S5、S6 可切淺色／深色）、密度（寬鬆／標準／緊湊，依風格開放）與色系，右側即時換裝；「前台示範」檢視是每套風格各做一個它最適合的網站（S1 會員中心、S2 自助機台、S3 產品發表、S4 咖啡館官網、S5 選物電商、S6 開發者產品官網、S7 線上雜誌），頁頂寫明適合與不適合的用途，「通用規範」檢視放各風格共用的字級、間距、圓角、色彩與斷點。

---

## 安裝

### Claude Code（建議）

在 Claude Code 裡輸入：

```
/plugin marketplace add art0428/webdesign
/plugin install ui-design-format@webdesign
```

第一行把這個倉庫登記成外掛來源，第二行安裝。之後有更新時，用 `/plugin` 選單更新即可。

### 手動安裝（Claude Code）

```bash
git clone https://github.com/art0428/webdesign.git
cp -r webdesign/skills/ui-design-format ~/.claude/skills/
```

放在 `~/.claude/skills/` 是所有專案都生效；只想給單一專案用，就複製到該專案的 `.claude/skills/`。

### claude.ai 網頁版

下載 [`dist/ui-design-format.zip`](dist/ui-design-format.zip)，在 claude.ai 的 Skills 設定頁上傳。

---

## 怎麼用

裝好之後不需要特別呼叫。只要請 Claude 做網頁介面，它就會先讀這套規範，例如：

- 「做一個訂位系統的後台，用 S6 石墨、C2 深湖青」
- 「幫我做一個咖啡店的品牌首頁」（沒指定風格時，Claude 會依系統類型從七套中挑選並說明理由）
- 「檢查這個頁面有沒有符合設計規範」（會跑下面的五項檢查）

## 七套風格

全站只選一套。風格是「殼」，只覆寫表面材質，不碰結構、色彩變數和字級，所以七套共用同一份元件 HTML。

| 編號 | 名稱 | 材質 | 適合 |
|---|---|---|---|
| S1 | 奶油 CREAM | 暖白底、大圓角、1px 暖灰線、零陰影 | 任何後台，預設值 |
| S2 | 浮雕 EMBOSS | 同色凸凹柔影 | 操作元件多的工具型介面 |
| S3 | 琉璃 GLAZE | 雙色漸層背景 ＋ 毛玻璃面板；另有深色模式 | 品牌展示、前台首頁 |
| S4 | 手帳 DOODLE | 暖紙底、手繪歪框、硬影 | 餐飲、文創、電商 |
| S5 | 極光 AURORA | 雙色柔霧暈染、有機圓角；另有深色模式 | 品牌故事、服務型前台 |
| S6 | 石墨 GRAPHITE | 純灰階、1px 細線、小圓角；另有深色模式，預設標準密度 | 資料密集後台、開發者工具 |
| S7 | 編輯 EDITORIAL | 暖白紙、明體標題、欄線分段、直角 | 內容網站、品牌官網、長文閱讀 |

色系由使用者在系統內切換：十二組核心 C1〜C12 加三組特殊色系 SC1〜SC3。七套 × 十五組共 105 種，扣掉鎖住的 S2 × SC1、S2 × SC2，共 103 種可用組合；S3、S5、S6 的深色模式各另有 15 種，合計 148 種。深色是同一套風格的夜間版本，只換顏色、不換結構，需要夜間模式的專案從這三套選。密度是另一條軸，分寬鬆、標準、緊湊三檔，只改元件高度與內距、不改顏色：寬鬆是桌機直接採用手機的觸控尺寸，緊湊給一屏要看大量列的後台。每套風格決定預設哪一檔、能選哪幾檔——S6 預設標準，其餘六套預設寬鬆；S2、S4、S5、S7 的材質在小元件上會壞，不開放緊湊。

## 開發時引用 CSS

`dist/` 是可以直接引用的樣式檔，每個檔頭都有版號，與規範同版。載三個檔加一支切換色系的腳本，全站只換風格那一行：

```html
<html lang="zh-Hant" data-style="s1">
<link rel="stylesheet" href="dist/tokens.css">
<link rel="stylesheet" href="dist/base.css">
<link rel="stylesheet" href="dist/style-s1.css">
<script src="dist/theme.js"></script>
```

工程師手冊是 [`dist/USAGE.md`](dist/USAGE.md)（每個元件怎麼寫、欄格怎麼用、禁止事項）。七套風格各有一張只引用 `dist/` 寫成的範例頁：[線上看](https://art0428.github.io/webdesign/dist/examples/)。

## 五項交付前檢查

腳本放在 `skills/ui-design-format/scripts/`，對任何 HTML 檔或網址都能跑。不合規時結束碼為 1，可以直接接進 CI（持續整合：每次提交時自動跑的檢查）。

```bash
pip install -r skills/ui-design-format/scripts/requirements.txt
playwright install chromium
```

| 檢查 | 指令 | 抓什麼 |
|---|---|---|
| 對比稽核 | `python audit_contrast.py page.html --themes all` | 從畫面截圖取樣底色，任何文字對比低於 WCAG（網頁無障礙國際標準）門檻 4.5（大字 3.0） |
| 標尺合規 | `python check_tokens.py page.html` | 不在標尺上的字級、行距、字距、間距 |
| 行高配對 | `python check_lineheight.py page.html --render` | 字級與行距沒有配成同一代號（例如 B2 的字配 B3 的行距） |
| 溢出檢查 | `python check_overflow.py page.html` | 390px、768px 寬度下的橫向捲動，並列出撐破版面的元素 |
| 版面稽核 | `python check_layout.py page.html --shots shots/` | 360、390、768、1024 四種寬度下的元件貼合、按鈕與膠囊折行、逐字斷行、裁切、突出容器、手機觸控目標不足（圖示與輸入框 44px、文字鈕 40px）、文字重疊，並截證據圖 |

## 倉庫結構

```
skills/ui-design-format/      ← 這一整個資料夾就是 skill，複製走就能用
├── SKILL.md                  Claude 每次都會讀的核心規則（風格、色彩、字級、元件、檢查）
├── references/               規範全文依章節拆開，需要細節時才讀
├── assets/                   tokens.css、各風格元件庫、前台示範頁、通用規範頁（當範本複製）
└── scripts/                  五項交付前檢查
dist/                         可引用的 CSS（tokens、base、style-s1〜s7、theme.js）、USAGE.md、examples/
dist/ui-design-format.zip     給 claude.ai 上傳用的打包檔
docs/                         線上預覽（GitHub Pages）、規範全文 spec.md、調研 research/
```

規範全文：[docs/spec.md](docs/spec.md)（v27）。每個數值背後的推導與業界對標：[docs/research/](docs/research/README.md)。

## 授權

[MIT](LICENSE)：可以自由使用、修改、商用，保留版權聲明即可。
