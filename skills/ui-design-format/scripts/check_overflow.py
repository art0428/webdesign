# -*- coding: utf-8 -*-
"""溢出檢查（交付前第四項）：在手機與平板寬度下，頁面不得出現橫向捲動。

用法：
  python check_overflow.py page.html [more.html https://...] [--widths 390,768]

找出超出視窗的元素時，最常見的原因是 flex 子項沒有寫 min-width:0、表格沒轉卡片列、
或固定寬度的圖片與程式碼區塊。需要 Playwright。有溢出時結束碼為 1。
"""
import asyncio, re, sys, argparse, pathlib

JS = r"""() => {
  const vw = document.documentElement.clientWidth;
  const sw = document.documentElement.scrollWidth;
  const culprits = [];
  if (sw > vw) {
    for (const el of document.body.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      if (r.right > vw + 1 && r.width > 0) {
        const p = el.parentElement && el.parentElement.getBoundingClientRect();
        if (!p || p.right <= vw + 1) {   // 只回報最外層的溢出源頭
          let name = el.tagName.toLowerCase();
          if (typeof el.className === 'string' && el.className.trim()) name += '.' + el.className.trim().split(/\s+/).join('.');
          culprits.push({name, right: Math.round(r.right)});
        }
      }
      if (culprits.length >= 12) break;
    }
  }
  return {vw, sw, culprits};
}"""


async def run(targets, widths):
    from playwright.async_api import async_playwright
    out = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in widths:
            pg = await b.new_page(viewport={"width": w, "height": 844})
            for t in targets:
                url = t if re.match(r"https?://", t) else pathlib.Path(t).resolve().as_uri()
                await pg.goto(url, wait_until="load")
                await pg.wait_for_timeout(300)
                out.append((t, w, await pg.evaluate(JS)))
            await pg.close()
        await b.close()
    return out


def main():
    ap = argparse.ArgumentParser(description="溢出檢查")
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--widths", default="390,768")
    a = ap.parse_args()
    widths = [int(x) for x in a.widths.split(",")]
    bad = 0
    for t, w, r in asyncio.run(run(a.targets, widths)):
        ok = r["sw"] <= r["vw"]
        bad += not ok
        print(f"{t} @ {w}px：{'通過' if ok else '溢出 %dpx' % (r['sw'] - r['vw'])}")
        for c in r["culprits"]:
            print(f"    {c['name'][:60]}  右緣 {c['right']}px")
    print("通過" if not bad else f"不通過：{bad} 個頁面寬度組合有橫向溢出")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
