# 管理者工作室 網頁設計系統 · ui-design-format

一套可以直接裝進 Claude 的網頁介面設計系統（以 Agent Skill 形式提供：裝好之後，Claude 做網頁時會自動照這套規範）。
六套風格、十二組核心色系加一組特殊色系、十三級字級、間距標尺、62 項元件，外加四支交付前的自動檢查腳本。

**A Claude Agent Skill for building web UIs: 6 visual styles × 13 color themes, a 13-level type scale, spacing tokens, 62 components, and 4 automated pre-delivery checks (contrast, token compliance, line-height pairing, overflow). Docs are in Traditional Chinese.**

**線上預覽** → <https://art0428.github.io/webdesign/>
左側切換風格與色系，右側即時換裝；「通用規範」檢視放六套共用的字級、間距、圓角、色彩與斷點。

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
- 「幫我做一個咖啡店的品牌首頁」（沒指定風格時，Claude 會依頁面類型從六套中挑選並說明理由）
- 「檢查這個頁面有沒有符合設計規範」（會跑下面的四項檢查）

## 六套風格

全站只選一套。風格是「殼」，只覆寫表面材質，不碰結構、色彩變數和字級，所以六套共用同一份元件 HTML。

| 編號 | 名稱 | 材質 | 適合 |
|---|---|---|---|
| S1 | 奶油 CREAM | 暖白底、大圓角、1px 暖灰線、零陰影 | 任何後台，預設值 |
| S2 | 浮雕 EMBOSS | 同色凸凹柔影 | 操作元件多的工具型介面 |
| S3 | 琉璃 GLAZE | 雙色漸層背景 ＋ 毛玻璃面板 | 品牌展示、前台首頁 |
| S4 | 手帳 DOODLE | 暖紙底、手繪歪框、硬影 | 餐飲、文創、電商 |
| S5 | 極光 AURORA | 雙色柔霧暈染、有機圓角 | 品牌故事、服務型前台 |
| S6 | 石墨 GRAPHITE | 純灰階、1px 細線、小圓角 | 資料密集後台、開發者工具 |

色系由使用者在系統內切換：十二組核心 C1〜C12 加一組特殊色系 SC1。六套 × 十三組共 78 種，扣掉鎖住的 S2 × SC1，共 77 種可用組合。

## 四項交付前檢查

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

## 倉庫結構

```
skills/ui-design-format/      ← 這一整個資料夾就是 skill，複製走就能用
├── SKILL.md                  Claude 每次都會讀的核心規則（風格、色彩、字級、元件、檢查）
├── references/               規範全文依章節拆開，需要細節時才讀
├── assets/                   tokens.css、六套元件庫 HTML、通用規範頁（當範本複製）
└── scripts/                  四項交付前檢查
docs/                         線上預覽（GitHub Pages）、規範全文 spec.md、調研 research/
dist/ui-design-format.zip     給 claude.ai 上傳用的打包檔
```

規範全文：[docs/spec.md](docs/spec.md)（v10）。每個數值背後的推導與業界對標：[docs/research/](docs/research/README.md)。

## 授權

[MIT](LICENSE)：可以自由使用、修改、商用，保留版權聲明即可。
