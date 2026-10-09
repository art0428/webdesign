# -*- coding: utf-8 -*-
"""行高配對檢查（交付前第三項）：字級與行距必須配成同一代號。

只看宣告值的 check_tokens.py 抓不到這一類——拿 B2 的字級配 B3 的行距，兩個值單獨看都在表上。
本腳本分兩關：
  第一關 靜態：每一條 CSS 規則裡，字級與行距是不是同一代號、有沒有寫了字級卻漏掉行距。
  第二關 動態（加 --render）：用瀏覽器把頁面畫出來，取每個文字元素實際算出來的字級與行高比對。
            只回報「源頭」——字級或行高與父層不同的元素；純繼承的子孫不重複計。

用法：
  python check_lineheight.py page.html [more.html ...] [--render] [--type productive|expressive|all]

  --render 需要 Playwright（pip install playwright && playwright install chromium）。

規範明訂的兩個例外不算違規：貨幣前綴縮小 0.68 倍、768px 以下輸入框 16px 防 iOS 放大。
有任何不合規時結束碼為 1。
"""
import asyncio, re, io, os, sys, collections, argparse, pathlib

# d1m、h0m 是 Expressive 在 768px 以下的 D1 與 H0（行距不變）
LEVELS = {
    "productive": {"d1": (30, 1.15), "h0": (26, 1.30), "h1": (21, 1.40), "h2": (17, 1.45), "h3": (14, 1.50),
                   "b1": (14, 1.80), "b2": (12.5, 1.70), "b3": (12, 1.70),
                   "l1": (12, 1.50), "l2": (11, 1.50),
                   "n1": (23, 1.20), "n2": (19, 1.25), "n3": (12.5, 1.60), "n4": (12.5, 1.60)},
    "expressive": {"d1": (44, 1.10), "d1m": (36, 1.10), "h0": (40, 1.25), "h0m": (32, 1.25), "h1": (30, 1.35), "h2": (22, 1.40), "h3": (16, 1.50),
                   "b1": (16, 1.90), "b2": (14, 1.80), "b3": (13, 1.90),
                   "l1": (12, 1.50), "l2": (11, 1.50),
                   "n1": (30, 1.15), "n2": (23, 1.20), "n3": (14, 1.60), "n4": (13, 1.60)},
}


# all：同一頁兩套都用（例如前台頁面引用了後台元件樣式）。代號沿用 Productive，Expressive 的值另掛 e 字尾供比對
LEVELS["all"] = {**LEVELS["productive"], **{k + "e": v for k, v in LEVELS["expressive"].items()}}


def build(level):
    allowed = {}
    for fs, lh in level.values():
        allowed.setdefault(fs, set()).add(lh)
    return allowed, {lh for _, lh in level.values()}


# ══════ 第一關 靜態 ══════
def rules(css):
    css = re.sub(r"/\*[\s\S]*?\*/", "", css)
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sel = m.group(1).strip().split("\n")[-1].strip()
        if sel.startswith("@") or ":root" in sel or sel.startswith("[data-type"):
            continue
        d = {}
        for part in m.group(2).split(";"):
            if ":" in part:
                p, v = part.split(":", 1)
                d[p.strip().lower()] = v.strip().replace("!important", "").strip()
        if d:
            yield sel, d


def lv_of_fs(v, level):
    m = re.search(r"var\(--fs-([a-z0-9]+)\)", v)
    if m:
        return m.group(1)
    for unit, mul in (("px", 1), ("rem", 10)):
        m = re.search(r"(-?\d*\.?\d+)%s\b" % unit, v)
        if m:
            px = float(m.group(1)) * mul
            for lv, (fs, _) in level.items():
                if abs(fs - px) < .01:
                    return lv
            return "?%gpx" % px
    if "em" in v or "%" in v:
        return "em"     # 相對值（例如貨幣前綴 .68em），交給動態關判斷
    return None


def lh_kind(v):
    m = re.search(r"var\(--lh-([a-z0-9]+)\)", v)
    if m:
        return "var", m.group(1)
    try:
        return "num", float(v)
    except ValueError:
        pass
    if "px" in v or "rem" in v:
        return "len", v
    return "other", v


def static_check(path, level, allowed, lh_table):
    s = io.open(path, encoding="utf-8").read()
    css = s if path.lower().endswith(".css") else "\n".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    items = list(rules(css))
    if not path.lower().endswith(".css"):
        for st in re.findall(r'style="([^"]*)"', s):
            d = {}
            for part in st.split(";"):
                if ":" in part:
                    p, v = part.split(":", 1)
                    d[p.strip().lower()] = v.strip()
            if d:
                items.append(("(inline)", d))
    out = collections.defaultdict(list)
    for sel, d in items:
        has_fs, has_lh = "font-size" in d, "line-height" in d
        if not (has_fs or has_lh):
            continue
        fslv = lv_of_fs(d["font-size"], level) if has_fs else None
        # 規範例外：輸入框 16px 防 iOS 放大，不論 16px 在不在該字級套裡，都不做配對檢查
        if has_fs and re.search(r"\binput\b|\btextarea\b|\bselect\b", sel) and re.search(r"\b1\.6rem\b|\b16px\b", d["font-size"]):
            continue
        if fslv and fslv.startswith("?"):
            if fslv == "?16px" and re.search(r"\binput\b|\btextarea\b|\bselect\b", sel):
                pass    # 規範例外：輸入框 16px
            else:
                out["字級不在十四級"].append((sel, d["font-size"]))
        if has_fs and not has_lh and fslv in level:
            out["有字級沒配行距"].append((sel, d["font-size"]))
        if not has_lh:
            continue
        kind, val = lh_kind(d["line-height"])
        if kind == "len":
            out["行距寫成長度（應寫倍數）"].append((sel, d["line-height"]))
        elif kind == "num":
            if round(val, 2) not in lh_table:
                out["行距不在表上"].append((sel, "%g" % val))
            elif fslv in level and round(val, 2) not in allowed[level[fslv][0]]:
                out["行距與字級不配對"].append((sel, "%s(%gpx) 配 %g，應為 %s" % (
                    fslv.upper(), level[fslv][0], val,
                    "／".join("%g" % x for x in sorted(allowed[level[fslv][0]])))))
        elif kind == "var" and fslv in level and val in level:
            if level[val][1] not in allowed[level[fslv][0]]:
                out["行距與字級不配對"].append((sel, "%s 配 lh-%s" % (fslv.upper(), val)))
    return out


# ══════ 第二關 動態 ══════
JS = r"""()=>{
  const SKIP=new Set(['SCRIPT','STYLE','SVG','PATH','G','RECT','CIRCLE','LINE','POLYLINE','TEXT','TSPAN','DEFS','USE','TITLE','OPTION','NOSCRIPT']);
  const out=[];
  const walk=(el)=>{
    if(SKIP.has(el.tagName.toUpperCase())) return;
    let own=false;
    for(const n of el.childNodes) if(n.nodeType===3 && n.nodeValue.trim()){ own=true; break; }
    if(own && el.getClientRects().length){
      const cs=getComputedStyle(el);
      const fs=parseFloat(cs.fontSize);
      const lh=cs.lineHeight==='normal'?null:parseFloat(cs.lineHeight);
      const pa=el.parentElement;
      let root=true;
      if(pa){
        const ps=getComputedStyle(pa), pfs=parseFloat(ps.fontSize);
        const plh=ps.lineHeight==='normal'?null:parseFloat(ps.lineHeight);
        if(Math.abs(pfs-fs)<0.01 && ((plh===null&&lh===null)||(plh!==null&&lh!==null&&Math.abs(plh-lh)<0.01))) root=false;
      }
      if(root){
        let path=el.tagName.toLowerCase();
        if(el.className && typeof el.className==='string' && el.className.trim()) path+='.'+el.className.trim().split(/\s+/).join('.');
        out.push({path, text:el.textContent.trim().slice(0,24), fs:+fs.toFixed(2), ratio:lh===null?null:+(lh/fs).toFixed(3)});
      }
    }
    for(const c of el.children) walk(c);
  };
  walk(document.body);
  return out;
}"""


async def render_all(paths):
    from playwright.async_api import async_playwright
    res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1280, "height": 900})
        for path in paths:
            url = path if re.match(r"https?://", path) else pathlib.Path(path).resolve().as_uri()
            await pg.goto(url, wait_until="load")
            await pg.wait_for_timeout(500)
            res[path] = await pg.evaluate(JS)
        await b.close()
    return res


def classify(nodes, allowed):
    bad = collections.defaultdict(list)
    for nd in nodes:
        fs, ratio = nd["fs"], nd["ratio"]
        key = next((px for px in allowed if abs(px - fs) < .01), None)
        if key is None:
            # 貨幣前綴 0.68 倍：任何標尺字級乘以 0.68
            if any(abs(px * .68 - fs) < .1 for px in allowed):
                continue
            if abs(fs - 16) < .01:
                continue    # 輸入框 16px 例外
            bad["字級不在十四級"].append(nd)
        elif ratio is None:
            bad["行高 normal（沒指定，body 記得寫 line-height:var(--lh-b1)）"].append(nd)
        elif not any(abs(ratio - a) < .02 for a in allowed[key]):
            bad["行高與字級不配對"].append(nd)
    return bad


def main():
    ap = argparse.ArgumentParser(description="行高配對檢查")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--render", action="store_true", help="加跑第二關（需要 Playwright）")
    ap.add_argument("--type", choices=["productive", "expressive", "all"], default="productive")
    a = ap.parse_args()
    level = LEVELS[a.type]
    allowed, lh_table = build(level)

    total = 0
    print("== 第一關 靜態：CSS 規則裡的字級與行距配對 ==")
    for f in a.files:
        if re.match(r"https?://", f):
            continue
        out = static_check(f, level, allowed, lh_table)
        n = sum(len(v) for v in out.values())
        total += n
        print(f"{f}：不合規 {n}")
        for c, v in sorted(out.items()):
            print(f"  【{c}】")
            for sel, val in v[:30]:
                print(f"    {sel[:48]:48} {val}")

    if a.render:
        print("\n== 第二關 動態：渲染後每個源頭文字元素的實際字級與行高 ==")
        res = asyncio.run(render_all(a.files))
        for f, nodes in res.items():
            bad = classify(nodes, allowed)
            n = sum(len(v) for v in bad.values())
            total += n
            print(f"{f}：源頭元素 {len(nodes)}，不合規 {n}")
            for c, v in sorted(bad.items()):
                print(f"  【{c}】")
                for nd in v[:30]:
                    want = allowed.get(nd["fs"])
                    w = "／".join("%g" % x for x in sorted(want)) if want else "—"
                    print(f"    {nd['path'][:30]:30} 「{nd['text']}」 字級 {nd['fs']} 行高 {nd['ratio']} 應為 {w}")
    print("\n通過" if total == 0 else f"\n不通過：共 {total} 項不合規")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
