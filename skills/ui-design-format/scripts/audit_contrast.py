# -*- coding: utf-8 -*-
"""對比稽核（交付前第一項）：把頁面畫出來，掃每一個文字節點的對比。

背景色不靠猜 CSS，而是從渲染後的截圖取樣（文字框周邊像素的眾數），
所以漸層、毛玻璃、半透明疊層都算得準。門檻依 WCAG（網頁無障礙國際標準）：
一般字 ≥ 4.5，大字（24px 以上，或 18.66px 以上且粗體）≥ 3.0。停用中的控件豁免。

用法：
  python audit_contrast.py page.html [more.html https://... ] [--themes c1,c2,sc1] [--width 1280] [-v]

  --themes  頁面支援用網址 hash 切換色系時（例如 page.html#c3），逐一稽核這些色系。
            填 all 代表十二組核心 ＋ SC1〜SC3。不填就只稽核頁面目前的樣子。
  --width   視窗寬度，預設 1280。

需要 Playwright 與 Pillow：
  pip install -r requirements.txt && playwright install chromium
有任何不及格時結束碼為 1。想讓某塊區域不受稽核（例如只在開發時出現的控制列），
在該元素加上 data-audit-skip 屬性。
"""
import asyncio, io, re, sys, collections, argparse, pathlib

ALL_THEMES = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "sc1", "sc2", "sc3"]


def lum(rgb):
    def f(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def ratio(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + .05) / (min(x, y) + .05)


def dist(a, b):
    return sum((p - q) ** 2 for p, q in zip(a, b)) ** .5


def mode(pixels):
    q = collections.Counter((p[0] // 6, p[1] // 6, p[2] // 6) for p in pixels)
    (r, g, b), _ = q.most_common(1)[0]
    return (min(255, r * 6 + 3), min(255, g * 6 + 3), min(255, b * 6 + 3))


COLLECT_JS = r"""
(() => {
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  let n;
  while ((n = walker.nextNode())) {
    const t = n.textContent.trim();
    if (!t) continue;
    const el = n.parentElement;
    if (!el) continue;
    if (el.closest('[data-audit-skip], .accbar, script, style, noscript')) continue;
    if (el.closest('[disabled], :disabled, [aria-disabled="true"]')) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
    const r = document.createRange(); r.selectNodeContents(n);
    const b = r.getBoundingClientRect();
    if (b.width < 4 || b.height < 4) continue;
    const eb = el.getBoundingClientRect();
    const m = cs.color.match(/\d+(\.\d+)?/g).map(Number);
    if (m.length >= 4 && m[3] === 0) continue;
    out.push({
      text: t.slice(0, 28),
      x: b.left + scrollX, y: b.top + scrollY, w: b.width, h: b.height,
      ex: eb.left + scrollX, ey: eb.top + scrollY, ew: eb.width, eh: eb.height,
      color: m.slice(0, 3), fs: parseFloat(cs.fontSize), fw: parseInt(cs.fontWeight) || 400,
      rot: cs.transform !== 'none',
      cls: (typeof el.className === 'string' && el.className.trim()) ? el.tagName.toLowerCase() + '.' + el.className.trim().split(/\s+/)[0] : el.tagName.toLowerCase()
    });
  }
  return out;
})()
"""


def pad_estimate(img, nd):
    """優先取「元素框內、文字框外」的內距帶——那才是字形正後方的底色。"""
    px = img.load()
    ex0, ey0, ex1, ey1 = int(nd["ex"]), int(nd["ey"]), int(nd["ex"] + nd["ew"]), int(nd["ey"] + nd["eh"])
    tx0, ty0, tx1, ty1 = int(nd["x"]) - 1, int(nd["y"]) - 1, int(nd["x"] + nd["w"]) + 1, int(nd["y"] + nd["h"]) + 1
    if (ex1 - ex0) * (ey1 - ey0) > 40000:
        return None     # 大容器不算內距帶
    ins = 5 if ey1 - ey0 >= 40 else 3 if ey1 - ey0 >= 24 else 2 if ey1 - ey0 >= 20 else 1
    band = []
    for j in range(max(ey0 + ins, ty0 - 6), min(ey1 - ins, ty1 + 7)):
        for i in range(max(ex0 + ins, tx0 - 6), min(ex1 - ins, tx1 + 7)):
            if tx0 <= i <= tx1 and ty0 <= j <= ty1:
                continue
            if 0 <= i < img.width and 0 <= j < img.height:
                band.append(px[i, j][:3])
    if len(band) < 12:
        return None
    est = mode(band)
    return None if dist(est, tuple(nd["color"])) < 30 else est


def ring_estimate(img, nd):
    """文字框外側環帶的像素眾數。"""
    px = img.load()
    x0, y0, x1, y1 = int(nd["x"]), int(nd["y"]), int(nd["x"] + nd["w"]), int(nd["y"] + nd["h"])
    ring = []
    for off in ((1, 2) if nd["h"] < 26 else (3, 4, 5)):
        for i in range(x0 - off, x1 + off + 1):
            for j in (y0 - off, y1 + off):
                if 0 <= i < img.width and 0 <= j < img.height:
                    ring.append(px[i, j][:3])
        for j in range(y0 - off, y1 + off + 1):
            for i in (x0 - off, x1 + off):
                if 0 <= i < img.width and 0 <= j < img.height:
                    ring.append(px[i, j][:3])
    return mode(ring) if ring else None


def rotated_estimate(img, nd):
    """旋轉元素的文字框不準，改取中心附近、排除文字色後的眾數。"""
    px = img.load()
    cx, cy = int(nd["x"] + nd["w"] / 2), int(nd["y"] + nd["h"] / 2)
    pts = [px[i, j][:3] for i in range(cx - 6, cx + 7) for j in range(cy - 6, cy + 7)
           if 0 <= i < img.width and 0 <= j < img.height]
    pts = [p for p in pts if dist(p, tuple(nd["color"])) > 40]
    return mode(pts) if pts else None


async def audit(targets, themes, width):
    from playwright.async_api import async_playwright
    from PIL import Image
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": width, "height": 900}, device_scale_factor=1)
        pg = await ctx.new_page()
        for t in targets:
            base = t if re.match(r"https?://", t) else pathlib.Path(t).resolve().as_uri()
            for th in (themes or [None]):
                url = base + (f"#{th}" if th else "")
                await pg.goto(url, wait_until="load")
                # 固定背景在整頁截圖時會錯位，稽核時改成跟著捲動
                await pg.add_style_tag(content="body{background-attachment:scroll !important}")
                await pg.wait_for_timeout(300)
                nodes = await pg.evaluate(COLLECT_JS)
                img = Image.open(io.BytesIO(await pg.screenshot(full_page=True))).convert("RGB")
                fails = []
                for nd in nodes:
                    bg = rotated_estimate(img, nd) if nd["rot"] else (pad_estimate(img, nd) or ring_estimate(img, nd))
                    if bg is None:
                        continue
                    r = ratio(tuple(nd["color"]), bg)
                    large = nd["fs"] >= 24 or (nd["fs"] >= 18.66 and nd["fw"] >= 700)
                    need = 3.0 if large else 4.5
                    if r < need:
                        fails.append({**nd, "bg": bg, "ratio": round(r, 2), "need": need})
                results.append((url, len(nodes), fails))
        await browser.close()
    return results


def main():
    ap = argparse.ArgumentParser(description="對比稽核")
    ap.add_argument("targets", nargs="+", help="HTML 檔案路徑或網址")
    ap.add_argument("--themes", default="", help="逐一稽核的色系 hash，逗號分隔；all ＝ 十五組")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("-v", action="store_true", help="列出每個不及格節點")
    a = ap.parse_args()
    themes = ALL_THEMES if a.themes == "all" else [x for x in a.themes.split(",") if x]

    results = asyncio.run(audit(a.targets, themes, a.width))
    total_nodes = total_fails = 0
    for url, n, fails in results:
        total_nodes += n
        total_fails += len(fails)
        print(f"{url}\n  文字節點 {n}，不及格 {len(fails)}")
        if a.v or len(fails) <= 10:
            for f in fails:
                hexc = "#%02X%02X%02X" % tuple(f["color"])
                hexb = "#%02X%02X%02X" % tuple(f["bg"])
                print(f"    {f['ratio']:>5} < {f['need']}  {f['cls'][:24]:24} 字 {hexc} 底 {hexb} 「{f['text']}」")
    print(f"\n合計 {total_nodes} 個文字節點，{total_fails} 個不及格")
    print("通過" if total_fails == 0 else "不通過")
    sys.exit(1 if total_fails else 0)


if __name__ == "__main__":
    main()
