> 本檔是《網頁設計規範 v23》的一部分，全文見倉庫的 docs/spec.md。

## 十、無障礙規範

### 10.1 對比度

- 一般文字對背景 **至少 4.5:1**（WCAG AA 標準）。
- 大字（18px 以上且字重 700 以上）至少 3:1。
- 本規範第三章的所有色碼都已實測驗證，直接使用即符合標準。新增顏色前必須實測。
- **框線色不得拿來當文字色。** `--line` 與 `--line-2` 是給線條用的；拿來寫「不重要的字」（月曆的非本月日期、麵包屑的分隔符）對比只有 1.4，必然不及格。要淡就用 `--muted`。
- **半透明面板上不放彩色小字。** 琉璃與極光的面板是半透明的，副色或語意色的小字壓上去只剩 3.4〜4.2；改用主文字色，方向與好壞用符號加文字表達，不靠顏色。
- **佔位文字（placeholder）一律 `::placeholder{color:var(--muted);opacity:1}`。** 瀏覽器預設的 `#757575` 在白底 4.61 勉強過，但 S2 的輸入框是底色 `#E6EAF0`（3.82）、S6 深色的卡片 `#1A1A1A`（3.78）、S1 頁面底 `#F6F5F2`（4.23）都不及格；而佔位文字不是文字節點，v17 以前的對比稽核量不到它。v18 起 `audit_contrast.py` 把每個有佔位文字的輸入框當一個節點量。

### 10.2 不可只靠顏色

總則四的具體做法：狀態標籤用「● 待確認」，不是只有一個黃點；錯誤欄位用「紅框＋下方文字說明」，不是只把框變紅；圖表的每個數列除顏色外要有圖例或直接標註。

### 10.3 鍵盤操作

- 所有可互動元件必須能用 Tab 鍵到達，順序與視覺順序一致。
- **Focus 狀態必須可見，而且七套同一種寫法**：

```css
/* 鍵盤到達才顯示（:focus-visible），滑鼠點擊不顯示；一律 2px 主色，外推 2px */
.btn:focus-visible,.chip:focus-visible,.pillf:focus-visible,.tabs .tab:focus-visible,.nitem:focus-visible,
.seg button:focus-visible,a:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
/* 輸入框、下拉選單、多行輸入：外推 0，環貼著框線 */
input:focus-visible,select:focus-visible,textarea:focus-visible{outline:2px solid var(--acc);outline-offset:0}
```

  不可用 `outline:none` 移除而不補上替代樣式——換框線色不算替代樣式（1.5px 的框線在玻璃與浮雕底上看不出來）。v17 以前七套只有色系切換鈕照做，按鈕、chip、頁籤、側欄項目全是瀏覽器預設的 1px 黑框，輸入框 S1、S6、S7 寫 `outline:none` 再換框線色、S2 寫 outline，鍵盤使用者在七套裡看到三種焦點。**驗收**：`audit_sizes.py` 把每類可互動元件的第一個實例聚焦，計算值必須是 `2px solid` 且顏色等於 `--acc`。
- 彈窗開啟時焦點移入彈窗、關閉時歸還原按鈕；Esc 可關閉。
- 下拉選單支援方向鍵選擇、Enter 確認、Esc 關閉。

### 10.4 表單

- 每個輸入框都要有 `<label>` 並用 `for` 正確關聯，不可只靠 placeholder 當標籤（placeholder 在輸入後會消失，使用者會忘記這欄是什麼）。
- 必填用「文字標籤＋紅色星號」雙重標示，並在 `aria-required` 標記。
- 錯誤訊息放在該欄位下方、用 `aria-describedby` 關聯，讓螢幕閱讀器唸得到。

### 10.5 動態效果

- 轉場的時長、緩動與可動屬性見 5.5：一律引用 `--dur-*` 與 `--ease-*`，元件內不超過 320ms，不做會觸發重新排版的屬性。
- 尊重系統的「減少動態」設定。轉場時長已由 5.5 的 token 歸零；迴圈動畫（骨架屏、轉圈）另外用下面這段停掉：

```css
@media (prefers-reduced-motion: reduce){
  *{ animation-duration:.01ms !important; transition-duration:.01ms !important; }
}
```

---
