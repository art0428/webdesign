# -*- coding: utf-8 -*-
"""版面稽核（交付前第七項，對應規範 6.6「手機與平板版面」）：在手機與平板寬度把頁面畫出來，
抓溢出檢查（只看整頁橫捲）抓不到的版面問題。

十一類：
  adj      有框元件貼合（< 8px），任何軸向；換行後上下兩排貼在一起也算
  line     分隔線重複或貼容器（< 12px）
  blob     膠囊變形：999px 圓角的元件被內容或換行撐高到單行高度的 1.6 倍以上
  wrap     短標籤折行：八個字以內的文字斷成兩行以上
  char     逐字斷行：三行以上、平均每行 ≤ 2.5 個字
  clip     內容被裁切：overflow hidden／clip 而內容比框寬，且不是刻意的省略號或行數限制
  out      突出容器：元件的右緣或左緣超出所在有框容器
  dangle   懸空分隔符：箭頭、斜線等分隔符在換行後落在行尾或行首
  touch    觸控目標不足（只量 < 768）：純圖示 < 44×44、文字可點元件高度 < 40、輸入框 < 44
  overlap  文字互相重疊
  page     整頁橫向溢出

用法：
  python check_layout.py page.html [more.html https://...] [--widths 360,390,768,1024] [--shots 證據圖資料夾] [--json 結果.json]

  --shots  每類問題截一張證據圖，問題元素以紅框標出（需要 Pillow）。

元件庫刻意的設計（堆疊頭像的負 margin、裝飾暈染、可兩行的次要說明等）已寫在 JS 的 EXEMPT，不算違規。
開發時才出現的控制列等區塊，加上 data-audit-skip 屬性即可排除。需要 Playwright。
有任何不合規時結束碼為 1；檔案找不到或網址載入失敗（HTTP 400 以上）時結束碼為 2。
"""
import re, os, sys, json, argparse, pathlib, collections
from playwright.sync_api import sync_playwright

JS = r"""(W) => {
  const EXEMPT_ADJ = 'table, .seg, .qty, .p1, .p2, .p3, .p4, .tabs, .stepper, .tl, .alert, .toolbar, .transfer, .tree, .pop, .tip, .toast, .modal, .drawer, .skel, .menu, .quick, .accbar';
  const CHROME = '.sec, .use, .accbar, .head, .foot, .cap, .ds-head, .ds-foot, .sf-note, [data-audit-skip]';
  const isComp = !!document.querySelector('.sec h2') && !!document.querySelector('.tierbar');   // 本設計系統的元件庫頁
  const path = e => e.tagName.toLowerCase() + (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/).slice(0, 3).join('.') : '');
  // 元件節：元件庫用 .sec h2；其他頁用文件順序上最近的 h1〜h3
  const headOf = new Map(); let lastH = '（頁首）';
  for (const e of document.body.querySelectorAll('*')) {
    if (isComp) { if (e.matches('.sec')) lastH = (e.querySelector('h2') || e).textContent.trim(); }
    else if (/^H[1-3]$/.test(e.tagName) && e.offsetHeight) lastH = e.textContent.trim().slice(0, 30);
    headOf.set(e, lastH);
  }
  const vis = e => { if (!e.offsetWidth || !e.offsetHeight || e.closest('[hidden]')) return false; const cs = getComputedStyle(e); return cs.visibility !== 'hidden' && cs.display !== 'none'; };
  const inScope = e => isComp ? (!e.closest(CHROME) && document.querySelector('.sec') && (document.querySelector('.sec').compareDocumentPosition(e) & 4)) : !e.closest('.accbar, [data-audit-skip]');
  let uid = 0;
  const mark = e => { const host = e.closest('.board') || e.closest('section, .card, .board, header, footer, main > *') || e; if (!host.dataset.aud) host.dataset.aud = 'a' + (++uid); return host.dataset.aud; };
  const out = [];
  // 已判定為刻意設計的例外：
  //   堆疊頭像（負 margin，規範允許）、S5 統計卡與 Token 示範的暈染裝飾、S4 貼紙、Token 示範的色票標籤、
  //   次要說明文字與前台商品名（6.3 允許兩行）、黏頂／黏底列（sticky、fixed）蓋到內容、捲動容器內看不到的部分
  const EXEMPT = {adj: '.avatar, .sticker', clip: '.statc.hero, .board.org', wrap: 'small, .sub, .sf-pname, .sticker, .tok, .tok *', overlap: '.sticker'};
  const stuck = e => { for (let p = e; p && p !== document.body; p = p.parentElement) { const ps = getComputedStyle(p).position; if (ps === 'sticky' || ps === 'fixed') return true; } return false; };
  const hidden = e => { const r = e.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) { const ps = getComputedStyle(p); if (ps.overflowY !== 'visible' || ps.overflowX !== 'visible') { const q = p.getBoundingClientRect(); if (cx < q.left || cx > q.right || cy < q.top || cy > q.bottom) return true; } } return false; };
  let fid = 0;
  const add = (cat, e, detail) => { if (EXEMPT[cat] && e.matches(EXEMPT[cat])) return; if (!e.dataset.audf) e.dataset.audf = 'f' + (++fid); out.push({cat, sec: headOf.get(e) || '', path: path(e), text: (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 24), detail, aud: mark(e), audf: e.dataset.audf}); };
  const all = [...document.body.querySelectorAll('*')].filter(e => vis(e) && inScope(e));
  const cssOf = new Map(all.map(e => [e, getComputedStyle(e)]));
  const bw = cs => ['Top', 'Right', 'Bottom', 'Left'].map(s => (cs['border' + s + 'Style'] === 'none' || cs['border' + s + 'Style'] === 'hidden') ? 0 : parseFloat(cs['border' + s + 'Width']) || 0);

  // ── adj／line ──
  const boxes = [], lines = [];
  for (const e of all) {
    const cs = cssOf.get(e);
    if (cs.position === 'fixed' || cs.position === 'absolute') continue;
    if (e.closest(EXEMPT_ADJ)) continue;
    const w = bw(cs), r = e.getBoundingClientRect(), n = w.filter(x => x >= 1).length;
    if (n === 4 && r.width >= 20 && r.height >= 20) boxes.push({e, r, big: r.width >= 120 && r.height >= 40});
    else if ((n === 1 && (w[0] >= 1 || w[2] >= 1) && r.width >= 80) || e.tagName === 'HR' || e.matches('.divider, .hr')) lines.push({e, r, y: (w[0] >= 1 && w[2] < 1) ? r.top : r.bottom});
  }
  const ovX = (a, b) => Math.min(a.right, b.right) - Math.max(a.left, b.left), ovY = (a, b) => Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i], b = boxes[j];
    if (a.e.contains(b.e) || b.e.contains(a.e)) continue;
    if (a.e.matches(EXEMPT.adj) || b.e.matches(EXEMPT.adj)) continue;
    const ox = ovX(a.r, b.r), oy = ovY(a.r, b.r);
    if (ox > 0) { const g = Math.max(b.r.top - a.r.bottom, a.r.top - b.r.bottom); if (g >= 0 && g < 8) add('adj', a.e, '上下 ' + g.toFixed(1) + 'px ↔ ' + path(b.e)); }
    if (oy > 0) { const g = Math.max(b.r.left - a.r.right, a.r.left - b.r.right); if (g >= 0 && g < 8) add('adj', a.e, '左右 ' + g.toFixed(1) + 'px ↔ ' + path(b.e)); }
    if (ox > 2 && oy > 2 && !stuck(a.e) && !stuck(b.e)) add('adj', a.e, '框重疊 ↔ ' + path(b.e));
  }
  for (const l of lines) for (const bx of boxes) {
    if (!bx.big || l.e.contains(bx.e) || bx.e.contains(l.e)) continue;
    if (ovX(l.r, bx.r) <= 0.5 * Math.min(l.r.width, bx.r.width)) continue;
    const g = Math.min(Math.abs(l.y - bx.r.top), Math.abs(l.y - bx.r.bottom));
    if (g < 12) add('line', l.e, '線貼容器外緣 ' + g.toFixed(1) + 'px ↔ ' + path(bx.e));
  }

  // ── 文字行數：用 Range 量直屬文字節點的行框 ──
  const linesOf = e => {
    const tops = new Set(); let txt = '';
    for (const n of e.childNodes) if (n.nodeType === 3 && n.textContent.trim()) {
      txt += n.textContent.trim();
      const rg = document.createRange(); rg.selectNodeContents(n);
      for (const rc of rg.getClientRects()) if (rc.width > 0.5) tops.add(Math.round(rc.top));
    }
    return {n: tops.size, txt};
  };
  const leaves = [];
  for (const e of all) {
    const {n, txt} = linesOf(e);
    if (!txt) continue;
    leaves.push(e);
    const len = [...txt.replace(/\s+/g, '')].length;
    const cs = cssOf.get(e);
    if (n >= 3 && len / n <= 2.5) add('char', e, n + ' 行、' + len + ' 字');
    else if (n >= 2 && len <= 8 && cs.whiteSpace !== 'pre-line' && cs.whiteSpace !== 'pre-wrap'
             && !(cs.display === 'inline' && e.parentElement && [...e.parentElement.childNodes].some(x => x.nodeType === 3 && x.textContent.trim()))) add('wrap', e, n + ' 行、' + len + ' 字');   // 段落裡的行內文字跟著段落換行，不算
  }

  // ── blob、clip、out ──
  for (const e of all) {
    const cs = cssOf.get(e), r = e.getBoundingClientRect();
    const rad = Math.min(...['TopLeft','TopRight','BottomRight','BottomLeft'].map(k => parseFloat(cs['border' + k + 'Radius']) || 0));   // 四角都是膠囊級；S4 歪框（255／18）不算
    const painted = bw(cs).some(x => x >= 1) || (cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent') || cs.boxShadow !== 'none';
    const kids = [...e.children].filter(c => c.offsetHeight);
    const multiRow = kids.length > 1 && kids.some(c => c.getBoundingClientRect().top >= kids[0].getBoundingClientRect().bottom - 2);
    const ownLines = linesOf(e).n;
    if (painted && rad >= 100 && r.width > r.height * 1.05 && r.width >= 24 && (multiRow || ownLines > 1 || (!kids.length && ownLines === 0))) {
      const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.5;
      const single = Math.max(parseFloat(cs.minHeight) || 0, lh + parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom) + bw(cs)[0] + bw(cs)[2]);
      if (r.height > single * 1.6 && r.height > 40) add('blob', e, Math.round(r.height) + 'px，單行約 ' + Math.round(single) + 'px');
    }
    const ox = cs.overflowX;
    if ((ox === 'hidden' || ox === 'clip') && e.scrollWidth > e.clientWidth + 2 && cs.textOverflow !== 'ellipsis' && cs.webkitLineClamp === 'none'
        && !e.matches('.thumb, .media, .car, .carousel, .skel, .sk') && r.width >= 40) {
      add('clip', e, '內容 ' + e.scrollWidth + ' > 框 ' + e.clientWidth);
    }
  }
  for (const e of all) {
    const cs = cssOf.get(e);
    if (cs.position === 'absolute' || cs.position === 'fixed') continue;
    let p = e.parentElement;
    while (p && p !== document.body) { const pc = cssOf.get(p); if (pc && bw(pc).every(x => x >= 1) && pc.overflowX === 'visible') break; p = p.parentElement; }
    if (!p || p === document.body || p.closest('.pop, .tip, .menu')) continue;
    const r = e.getBoundingClientRect(), pr = p.getBoundingClientRect();
    if (r.right > pr.right + 1.5 || r.left < pr.left - 1.5) { if (!e.parentElement || !(e.parentElement.getBoundingClientRect().right > pr.right + 1.5)) add('out', e, '超出 ' + path(p) + ' ' + Math.round(Math.max(r.right - pr.right, pr.left - r.left)) + 'px'); }
  }

  // ── dangle：分隔符在行尾或行首 ──
  const SEPS = new Set(['→', '›', '/', '／', '·', '>', '|', '｜', '—', '－', '–']);
  for (const e of all) {
    const t = (e.textContent || '').trim();
    if (!(e.matches('.arr, .sep, .bsep') || (SEPS.has(t) && e.childElementCount === 0))) continue;
    const r = e.getBoundingClientRect(); if (r.width > 40) continue;
    if (getComputedStyle(e).position === 'absolute') continue;   // 輪播左右箭頭這類絕對定位的鈕不是行內分隔符
    const pcs = e.parentElement ? getComputedStyle(e.parentElement) : null;
    if (pcs && pcs.display.includes('flex') && pcs.flexDirection.startsWith('column')) continue;   // 直排本來就一項一行
    const nx = e.nextElementSibling, pv = e.previousElementSibling;
    if (nx && vis(nx) && nx.getBoundingClientRect().top >= r.bottom - 2) add('dangle', e, '「' + t + '」落在行尾，下一項換到下一行');
    else if (pv && vis(pv) && pv.getBoundingClientRect().bottom <= r.top + 2) add('dangle', e, '「' + t + '」落在行首');
  }

  // ── touch（< 768） ──
  if (W < 768) {
    for (const e of all) {
      if (!e.matches('button, a[href], select, input:not([type=checkbox]):not([type=radio]):not([type=range]):not([type=hidden]), [role=button], [role=tab], summary')) continue;
      if (e.disabled || e.closest('.alert') || e.closest('p, li > p, .prose, .art, article p')) continue;
      if (e.matches('a') && e.closest('p, .lede, .note, .foot-note, .crumb, .bc, nav.bc')) continue;
      if (e.matches('input') && e.closest('.search, .qty, .srch')) continue;   // 外框才是觸控目標，外框另量
      const r = e.getBoundingClientRect(), t = (e.textContent || '').trim();
      if (e.matches('input, select')) { if (r.height < 44 - 0.5) add('touch', e, '輸入框高 ' + Math.round(r.height) + 'px（手機應 44）'); continue; }
      const iconOnly = !/[\p{L}\p{N}]/u.test(t);   // 沒有文字或數字（符號、圖示）才算純圖示
      if (e.closest('.qty') && e.closest('.qty').getBoundingClientRect().height >= 44 - 0.5) continue;   // 數量調整器量外框（含框線 44）
      if (iconOnly && (r.width < 44 - 0.5 || r.height < 44 - 0.5)) add('touch', e, '純圖示 ' + Math.round(r.width) + '×' + Math.round(r.height));
      else if (!iconOnly && r.height < 40 - 0.5) add('touch', e, '高 ' + Math.round(r.height) + 'px');
    }
  }

  if (W < 768) for (const e of all) if (e.matches('.search, .qty')) { const h = e.getBoundingClientRect().height; if (h < 44 - 0.5) add('touch', e, path(e) + ' 外框高 ' + Math.round(h) + 'px（手機應 44）'); }
  // ── overlap：文字葉元素互相重疊 ──
  const lr = leaves.filter(e => { const cs = cssOf.get(e); return cs.position !== 'absolute' && cs.position !== 'fixed' && !(cs.display === 'inline' && e.getClientRects().length > 1); }).map(e => [e, e.getBoundingClientRect()]);
  for (let i = 0; i < lr.length; i++) for (let j = i + 1; j < lr.length; j++) {
    const [a, ra] = lr[i], [b, rb] = lr[j];
    if (a.contains(b) || b.contains(a)) continue;
    const ox = ovX(ra, rb), oy = ovY(ra, rb);
    if (ox > 3 && oy > 3 && ox * oy > 0.25 * Math.min(ra.width * ra.height, rb.width * rb.height) && !stuck(a) && !stuck(b) && !hidden(a) && !hidden(b)) add('overlap', a, '↔ ' + path(b) + '「' + (b.textContent || '').trim().slice(0, 10) + '」');
  }
  return {out, sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth};
}"""


def target(arg):
    """網址照用；本機檔案轉成 file:// 網址，保留 # 後面的片段（例如 page.html#c3 切色系）。"""
    if re.match(r"https?://|file://", arg):
        return arg, arg
    path, _, frag = arg.partition("#")
    return pathlib.Path(path).resolve().as_uri() + ("#" + frag if frag else ""), arg


def shoot(pg, f, path):
    from PIL import Image
    pg.add_style_tag(content='[data-audf="%s"]{outline:3px solid #E5251E!important;outline-offset:1px!important}' % f["audf"])
    loc = pg.locator('[data-aud="%s"]' % f["aud"]).first
    loc.scroll_into_view_if_needed()
    tmp = path + ".tmp.png"
    bb = loc.bounding_box()
    same = pg.evaluate('([a, f]) => document.querySelector(`[data-aud="${a}"]`) === document.querySelector(`[data-audf="${f}"]`)', [f["aud"], f["audf"]])
    if same or bb["width"] < 120 or bb["height"] < 60:
        # 找不到外層區塊時截的是元素本身：往外多截 24px，紅框與相鄰元素才看得到
        sx, sy = pg.evaluate("[scrollX, scrollY]")   # bounding_box 是視窗座標，整頁截圖的 clip 要頁面座標
        x0, y0 = max(0, bb["x"] + sx - 24), max(0, bb["y"] + sy - 24)
        pg.screenshot(path=tmp, full_page=True, clip={"x": x0, "y": y0, "width": bb["x"] + sx + bb["width"] + 24 - x0,
                                                      "height": bb["y"] + sy + bb["height"] + 24 - y0})
    else:
        loc.screenshot(path=tmp)
    im = Image.open(tmp)
    el = pg.locator('[data-audf="%s"]' % f["audf"]).first.bounding_box()
    hb = loc.bounding_box()
    top = 0
    if el and hb and im.height > 1400:   # 長的區塊以問題元素為中心截 700px（CSS）
        cy = (el["y"] - hb["y"] + el["height"] / 2) * 2
        top = int(max(0, min(im.height - 1400, cy - 700)))
    im.crop((0, top, im.width, min(im.height, top + 1400))).save(path)
    os.remove(tmp)
    pg.evaluate('document.querySelectorAll("style").forEach(s=>{if(s.textContent.includes("data-audf"))s.remove()})')


def main():
    ap = argparse.ArgumentParser(description="版面稽核")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--widths", default="360,390,768,1024")
    ap.add_argument("--shots", help="證據圖資料夾")
    ap.add_argument("--json", help="結果寫成 JSON")
    a = ap.parse_args()
    widths = [int(x) for x in a.widths.split(",")]
    missing = [x for x in a.files if not re.match(r"https?://|file://", x) and not os.path.exists(x.partition("#")[0])]
    if missing:
        print("找不到檔案：" + "、".join(missing), file=sys.stderr)
        sys.exit(2)
    if a.shots:
        try:
            import PIL  # noqa: F401
        except ImportError:
            sys.exit("--shots 需要 Pillow：pip install Pillow")
        os.makedirs(a.shots, exist_ok=True)

    res, shot_keys = [], set()
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for W in widths:
            ctx = br.new_context(viewport={"width": W, "height": 900}, device_scale_factor=2)
            for arg in a.files:
                url, name = target(arg)
                pg = ctx.new_page()
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                resp = pg.goto(url, wait_until="load")
                if resp is not None and resp.status >= 400:
                    print("載入失敗：%s（HTTP %d）" % (name, resp.status))
                    sys.exit(2)
                pg.wait_for_timeout(700)
                pg.add_style_tag(content="*,*::before,*::after{animation:none!important;transition:none!important} .accbar{display:none!important}")
                r = pg.evaluate(JS, W)
                if r["sw"] > r["cw"]:
                    res.append({"page": name, "w": W, "cat": "page", "sec": "", "path": "html", "text": "", "detail": "scrollWidth %d > %d" % (r["sw"], r["cw"])})
                for f in r["out"]:
                    f.update(page=name, w=W)
                    sk = (name, f["sec"], f["cat"], W >= 768)
                    if a.shots and sk not in shot_keys:
                        shot_keys.add(sk)
                        fn = "%s_%s_%d_%d.png" % (re.sub(r"[^\w.-]+", "_", pathlib.Path(name.split("#")[0]).stem), f["cat"], W, len(shot_keys))
                        try:
                            shoot(pg, f, os.path.join(a.shots, fn))
                            f["shot"] = fn
                        except Exception as ex:
                            f["shot_err"] = str(ex)[:80]
                    res.append(f)
                if errs:
                    res.append({"page": name, "w": W, "cat": "jserr", "sec": "", "path": "", "text": "", "detail": errs[0][:120]})
                pg.close()
            ctx.close()
        br.close()

    if a.json:
        for f in res:
            f.pop("aud", None); f.pop("audf", None)
        json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("== 版面稽核：%d 個頁面 × %s ==" % (len(a.files), "／".join(map(str, widths))))
    seen = set()
    for f in res:
        k = (f["cat"], f["page"], f["sec"], f["path"])
        if k in seen:
            continue
        seen.add(k)
        print("  %-7s %-28s %4d  %-16s %-26s %s" % (f["cat"], f["page"][-28:], f["w"], f["sec"][:16], f["path"][:26], f["detail"][:60]))
    c = collections.Counter(f["cat"] for f in res)
    print("\n通過" if not res else "\n不通過：共 %d 項不合規  %s" % (len(res), "  ".join("%s:%d" % kv for kv in sorted(c.items()))))
    sys.exit(1 if res else 0)


if __name__ == "__main__":
    main()
