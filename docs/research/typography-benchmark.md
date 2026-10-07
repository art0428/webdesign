# 字級與行距對標主流

## 一句話結論

**內文字級與行距完全站在主流上，而且中文行距的選擇有 W3C 官方規範背書；真正偏離業界的只有一件事——L1（11px）與 L2（10px）這兩級，中文圈五套主流元件庫全部沒有低於 12px 的字級。**

## 名詞

- **設計系統 design system**：一套把顏色、字級、間距等設計決策寫成共用規則與程式變數的文件，讓同一個團隊做出來的畫面長得像同一個產品。
- **token（設計代號）**：把某個數值取名字再到處引用的變數，例如 `--fs-b1` 代表內文字級，改一處全站生效。
- **type set（字級集）**：一整組成套的「字級 ＋ 行距 ＋ 字重」。
- **行距倍數**：行距 ÷ 字級。14px 的字配 22px 行距就是 1.57 倍。
- **Productive（生產型）／Expressive（表現型）**：IBM Carbon 提出的分法，前者給資料密集的後台、後者給對外閱讀的頁面。本規範採同一套分法。
- **WCAG**：W3C 的網頁無障礙指引，AA 是一般合規門檻、AAA 更嚴格。

## 比對方法

對標對象分三群共十四套，數值一律取自官方文件或官方 token 原始檔（GitHub／npm 發布包），查證日期 2026-10-06：

- **通用型**：Material Design 3、Apple HIG（iOS／macOS）、Tailwind CSS 4、Bootstrap 5
- **企業後台型**：IBM Carbon、Atlassian、Shopify Polaris、GitHub Primer、Salesforce Lightning
- **中日韓型**：Ant Design、Arco Design、TDesign、Element Plus、Semi Design；另參考日本數位廳、SmartHR、DMM

## 第一題　後台內文該用幾 px

| 系統 | 後台內文基準 | 行距 | 倍數 |
|---|---|---|---|
| IBM Carbon（productive） | 14px | 18px（緊）／20px（長段落） | 1.286／1.429 |
| Atlassian | 14px | 20px | 1.429 |
| GitHub Primer | 14px | 21px | 1.500 |
| Shopify Polaris（桌機） | 13px | 20px | 1.538 |
| Salesforce Lightning | 13px | 19.5px | 1.500 |
| Ant Design | 14px | 22px | 1.571 |
| Arco Design | 14px | 22px | 1.572 |
| TDesign | 14px | 22px | 1.571 |
| Element Plus | 14px | 25.2px（段落） | 1.800 |
| Semi Design | 14px | 20px（另備 24px 寬鬆模式） | 1.429／1.714 |
| **本規範 B1** | **14px** | **25.2px** | **1.800** |

**十套裡八套用 14px，兩套用 13px，沒有第三個答案。** 16px 在每一套裡都是「對外閱讀」那一套的值，不是後台表格與表單的預設。本規範的 14px 正中靶心。

## 第二題　中文的行距該多鬆

| 來源 | 身分 | 說法 |
|---|---|---|
| W3C clreq《中文排版需求》 | W3C 中文排版任務組 | 行距介於字級的 50%〜100%，即 **1.5〜2.0 倍**；超過字級本身不會再增加易讀性 |
| W3C JLReq《日本語組版處理的要件》 | W3C 日文排版任務組 | 行間取「二分（0.5em）以上、全角（1.0em）以下」，即 **1.5〜2.0 倍**；行長超過 35 字時應靠近 2.0 |
| WCAG 2.2 達成基準 1.4.8（AAA） | W3C | 段落內行距至少 **1.5 倍**；行長上限拉丁文 80 字、**CJK 40 字** |
| Typotheque | 荷蘭字體公司、CJK 字型開發者 | CJK 每字資訊密度較高，行距約 **1.7** 最佳；拉丁文常見自動值只有 1.2 |
| Bob Tung 董福興 | clreq 共同編輯 | 中文行高通常 **1.5〜2.0em**，可直接寫 `line-height: 1.7em` |
| justfont | 台灣字體公司 | **1.5 倍行距**被認為是理想設定 |
| Outline（開源文件工具，2026 決策） | 工程團隊 | 其他語系維持 1.5、**CJK 改 1.8**；理由是方塊字密集，1.5 讀起來擠 |
| 日本數位廳設計系統 | 日本政府官方 | 閱讀型內文 **170%**，最低 1.5 倍 |

**本規範 B1 的 1.80 落在 W3C 區間（1.5〜2.0）的中上段，與 Element Plus 的段落行距 1.8、Outline 給 CJK 的 1.8 完全相同，比日本數位廳的 1.7 略鬆。** 這一項不但合規，而且比西方後台（1.29〜1.54）更符合中文的實際需求。

要注意的是：**西方那幾套的 1.43 連 WCAG AAA 的 1.5 都沒過**，這不是中文特例，而是對所有語言都偏緊。中文圈唯一採 1.43 的 Semi Design，自己也另外做了一個 1.714 的「寬鬆行距段落」token，等於承認 1.43 只堪用於密集 UI。

## 第三題　最小字級

| 系統 | 最小字級 token | 用途 |
|---|---|---|
| Salesforce Lightning | 10px | 只用於開關的 ON／OFF、頭像縮寫、聊天時間戳，全站只出現 6 次 |
| Shopify Polaris | 11px（桌機） | 行動主題自動放大為 12px |
| IBM Carbon | 12px | 欄位標籤、輔助說明、法律聲明 |
| Atlassian | 12px | 次要資訊 |
| GitHub Primer | 12px | 官方註明「不符無障礙要求，只能單行用」 |
| Ant Design | 12px | — |
| Arco Design | 12px | — |
| TDesign | 12px | — |
| Element Plus | 12px | — |
| Semi Design | 12px | — |
| **本規範** | **10px（L2）、11px（L1）** | 微標籤、眉標、欄位標籤 |

**中文圈五套元件庫的最小字級 token 全部是 12px，零例外。** 西方只有兩套低於 12px，而且都有嚴格限制：Salesforce 的 10px 只給兩個字母的微標籤、更小的刻度直接指回 10px 封頂；Polaris 的 11px 一到觸控裝置就放大。

本規範已有的防護：10px 與 11px「只給單詞或極短片語的標籤，字重 700 以上並加大字距，不得寫句子」。這條限制的方向與 Salesforce 的實務一致，但**本規範把 L1 11px 用在「欄位標籤」上，這已經超出「微標籤」的範圍**——欄位標籤是表單裡每一列都要讀的功能性文字，Carbon、Atlassian、Ant 都用 12px。

另有一條歷史性風險：Chrome 在中文介面語系下長期有 12px 的最小字級下限，低於 12px 會被瀏覽器強制放大，版面計算因此失準。這個限制是否仍存在於最新版 Chrome 無法確認（官方討論串沒有結論），所以**不列為主要理由**，但它是把下限訂在 12px 的額外誘因。

## 逐項判定

### Productive 生產型（後台）

| 代號 | 本規範 | 判定 | 說明 |
|---|---|---|---|
| D1 | 30px / 1.15 | 符合主流 | 大字壓行距是通則；M3 display-large 1.12、Carbon heading-07 1.19 |
| H1 | 21px / 1.40 | 刻意不同，可辯護 | 比 M3（24px）小，但後台標題本就小：Carbon heading-03 是 20px |
| H2 | 17px / 1.45 | 符合主流 | 對應 Carbon heading-02（16px）、Atlassian heading.small（16px） |
| H3 | 13px / 1.50 | **建議調整** | 卡片標題比內文 14px 還小。Carbon 的 heading-compact-01 是 14px，與內文同級；沒有任何一套讓標題小於內文 |
| B1 | 14px / 1.80 | 符合主流 ＋ 中文最佳解 | 字級十套中八套相同；行距在 W3C 的 1.5〜2.0 區間 |
| B2 | 12.5px / 1.70 | 刻意不同，可辯護 | 非整數，業界用 13px（Polaris、Salesforce）。行距 1.70 與 Ant 的 1.571 同一帶 |
| B3 | 12px / 1.85 | 字級符合，行距偏鬆 | 12px 是業界下限，正確；但 Ant 與 TDesign 給 12px 的行距是 20px（1.67），1.85 等於 22.2px 偏鬆 |
| L1 | 11px / 1.50 | **建議調整** | 中文圈無人提供 11px；且用途是「欄位標籤」，業界一律 12px |
| L2 | 10px / 1.50 | **建議調整** | 僅 Salesforce 有 10px，且只給兩字母微標籤 |
| N1 | 23px / 1.20 | 符合主流 | 數字壓行距正確 |
| N2 | 19px / 1.25 | 符合主流 | 同上 |
| N3 | 12.5px / 1.60 | 可辯護 | 表格金額；非整數同 B2 |
| N4 | 12.5px / 1.60 | 可辯護 | 料號單號；S6 改等寬字的做法與 Carbon 的 code-01 一致 |

### Expressive 表現型（前台）

| 代號 | 本規範 | 判定 |
|---|---|---|
| B1 | 16px / 1.90 | 符合主流。16px 是 Tailwind、Bootstrap、M3 的內文基準；1.90 在 W3C 的 CJK 區間上緣，接近語雀的 2.0 |
| B2 | 14px / 1.80 | 符合主流 |
| B3 | 13px / 1.90 | 行距偏鬆，同 Productive 的 B3 |
| L1 / L2 | 12px / 11px | L2 的 11px 同樣低於中文圈下限 |
| 其餘 | — | 與主流一致 |

## 四條建議（依優先序）

**一、把最小字級下限拉到 12px。** 這是唯一一條「業界零例外、本規範例外」的偏離。具體做法有兩個方向，擇一：

- 保守做法：L1 從 11px 改 12px、L2 從 10px 改 11px，並把 L2 的用途限制寫死為「只給一到四個字的微標籤，不得用於欄位標籤」。
- 徹底做法：L1 與 L2 合併為單一的 12px 標籤級，用字重與字距區分眉標與欄位標籤。十三級變十二級。

徹底做法與中文圈五套元件庫完全一致，但會動到十三級的架構與既有元件，影響面較大。

**二、H3 不應小於 B1。** 卡片標題 13px 配內文 14px，在視覺層級上是倒置的。建議 H3 改 14px，靠字重 900 與字距 0.08em 與內文區隔——這正是 Carbon 的 `heading-compact-01`（14px / 600 semibold）與 `body-compact-01`（14px / 400 regular）的做法。

**三、B3 的行距從 1.85 收到 1.60 或 1.70。** 12px 的說明文字配 22.2px 行距偏鬆，業界同字級普遍是 20px。這一條影響小，可與其他改動一起做。

**四、考慮為 B1 增設「緊湊」行距。** Carbon 給同一個 14px 兩個行距：元件內的短文字用 18px（1.286）、長段落用 20px（1.429）。本規範目前是用「換字級」（表格內改用 B2 12.5px）來解決密度問題，Carbon 是「同字級換行距」。Carbon 的做法讓表格內文與一般內文一樣大、只是行距緊，可讀性較好。這是架構層級的選項，不是缺陷，列為備查。

## 附錄　關於 `html{font-size:62.5%}`

本規範用 62.5% 讓 1rem ＝ 10px。這個寫法在業界有爭議，查證後的事實是：

- **它不會破壞使用者自訂的瀏覽器預設字級。** 62.5% 是百分比而非固定 px，使用者把預設字級調到 24px 時，根字級變成 15px，所有 rem 值等比跟著放大。「這個 hack 會讓放大失效」的說法在技術上不成立。
- **真正的風險是混用第三方元件庫。** Tailwind、Bootstrap、Ant Design 的尺寸都以 1rem ＝ 16px 為前提，混進來會整體縮成 62.5%。
- **本專案自建六套元件庫、不混用第三方 UI 庫，所以可以繼續用。** 但建議在規範裡補一句：若日後引入第三方 UI 庫，必須把根字級改回 100% 並重算整份標尺。

## 出處

- Material Design 3 type scale tokens：https://m3.material.io/styles/typography/type-scale-tokens
- Apple Human Interface Guidelines, Typography：https://developer.apple.com/design/human-interface-guidelines/typography
- Tailwind CSS font-size：https://tailwindcss.com/docs/font-size
- Bootstrap variables：https://github.com/twbs/bootstrap/blob/v5.3.8/scss/_variables.scss
- IBM Carbon type sets：https://carbondesignsystem.com/elements/typography/type-sets/
- IBM Carbon type tokens：https://github.com/carbon-design-system/carbon/blob/main/packages/type/scss/_styles.scss
- Atlassian typography：https://atlassian.design/foundations/typography
- Shopify Polaris text tokens：https://github.com/Shopify/polaris/blob/main/polaris-tokens/src/themes/base/text.ts
- GitHub Primer typography：https://primer.style/foundations/primitives/typography
- Salesforce Lightning Design System：https://www.npmjs.com/package/@salesforce-ux/design-system
- Ant Design 字體規範：https://ant.design/docs/spec/font-cn
- Ant Design 行高公式原始碼：https://github.com/ant-design/ant-design/blob/master/components/theme/themes/shared/genFontSizes.ts
- Arco Design theme：https://arco.design/react/docs/token
- TDesign font tokens：https://github.com/Tencent/tdesign-common/blob/develop/style/web/theme/_font.less
- Element Plus reset（`p{line-height:1.8}`）：https://github.com/element-plus/element-plus/blob/dev/packages/theme-chalk/src/reset.scss
- Semi Design typography variables：https://github.com/DouyinFE/semi-design/blob/main/packages/semi-foundation/typography/variables.scss
- W3C clreq 中文排版需求：https://w3c.github.io/clreq/
- W3C JLReq 日本語組版處理的要件：https://www.w3.org/TR/jlreq/
- WCAG 2.2 Understanding 1.4.8 Visual Presentation：https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html
- Typotheque, Typesetting CJK text：https://www.typotheque.com/articles/typesetting-cjk-text
- Bob Tung, Best Practice in Chinese Layout：https://bobtung.medium.com/best-practice-in-chinese-layout-f933aff1728f
- justfont 排版觀念：https://blog.justfont.com/2013/05/popular-typography-2/
- Outline PR 13822（CJK 行距調整）：https://github.com/outline/outline/pull/13822
- 日本數位廳設計系統 typography：https://design.digital.go.jp/dads/foundations/typography/
- SmartHR Design System 行送り：https://smarthr.design/products/design-tokens/leading/
- FED Mentor, 62.5% html font-size hack：https://fedmentor.dev/posts/rem-html-font-size-hack/
- Martin Haehnel, Font sizing using the rem unit：https://blog.martin-haehnel.de/2025/06/21/css-font-sizing-using-the-rem-unit/
