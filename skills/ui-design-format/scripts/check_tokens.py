# -*- coding: utf-8 -*-
"""標尺合規檢查（交付前第二項）：掃 HTML 的 <style>、style="" 與 .css 檔裡每一個宣告，
找出不在標尺上的字級、行距、字距、間距，以及負 margin、承載文字的固定 height。

用法：
  python check_tokens.py page.html [more.html style.css ...] [--type productive|expressive|all] [-v]

  --type   字級標尺。productive（預設，後台、表單、結帳）、expressive（前台閱讀型頁面）、
           all（同一份檔案兩種都用時）。
  -v       列出每一條不合規宣告。

假設：html{font-size:62.5%}，所以 1rem = 10px；rem 會換算成 px 再比對。
引用變數的宣告（var(--fs-b1) 這類）直接視為合規，因為值由 tokens.css 決定。
有任何不合規時結束碼為 1，可以接進 CI（持續整合：每次提交自動跑檢查）。
"""
import re, io, sys, collections, argparse

# 十四級字級（D1、H0〜H3、B1〜B3、L1〜L2、N1〜N4）不重複的值；Expressive 含 768px 以下的 D1 36、H0 32
PRODUCTIVE = {"fs": {30, 26, 21, 17, 14, 12.5, 12, 11, 23, 19},
              "lh": {1.15, 1.30, 1.40, 1.45, 1.50, 1.80, 1.70, 1.20, 1.25, 1.60}}
EXPRESSIVE = {"fs": {44, 36, 40, 32, 30, 22, 16, 14, 13, 12, 11, 23},
              "lh": {1.10, 1.25, 1.35, 1.40, 1.50, 1.90, 1.80, 1.15, 1.20, 1.60}}
SP_OK = {0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64}
LS_OK = {0, -0.01, 0.02, 0.03, 0.06, 0.08, 0.15}
SP_PROPS = ("margin", "margin-top", "margin-right", "margin-bottom", "margin-left",
            "margin-inline", "margin-block", "padding", "padding-top", "padding-right",
            "padding-bottom", "padding-left", "padding-inline", "padding-block",
            "gap", "row-gap", "column-gap")
# 這些 class 名稱通常是不承載文字的裝飾或骨架（進度條、骨架屏、色塊、分隔線），固定 height 不算違規
DECOR = re.compile(r"(bar|skel|sk\b|spin|rule|divider|hr\b|dot|blob|swatch|track|thumb|line|::before|::after|svg|img|icon|avatar)", re.I)
# 規範明訂的例外：堆疊頭像、資料夾頁籤可以用負 margin
NEG_OK = re.compile(r"avstack|avatar|stack|folder|tabs?\b", re.I)
# 規範明訂的例外：768px 以下輸入框 16px 防 iOS 放大
INPUT_SEL = re.compile(r"\binput\b|\btextarea\b|\bselect\b")


def decls(css):
    """依序產出 (selector, property, value)。"""
    css = re.sub(r"/\*[\s\S]*?\*/", "", css)
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sel = m.group(1).strip().split("\n")[-1].strip()
        if sel.startswith("@") or sel.startswith(":root") or sel.startswith("[data-type"):
            continue   # token 定義本身不檢查
        for d in m.group(2).split(";"):
            if ":" not in d:
                continue
            p, v = d.split(":", 1)
            yield sel, p.strip().lower(), v.strip().replace("!important", "").strip()


def px_values(v):
    """把值裡的 px 與 rem 全部換算成 px。"""
    out = [float(x) for x in re.findall(r"(-?\d*\.?\d+)px", v)]
    out += [round(float(x) * 10, 2) for x in re.findall(r"(-?\d*\.?\d+)rem", v)]
    return out


def load(path):
    s = io.open(path, encoding="utf-8").read()
    if path.lower().endswith(".css"):
        return list(decls(s))
    css = "\n".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    items = list(decls(css))
    for st in re.findall(r'style="([^"]*)"', s):
        for d in st.split(";"):
            if ":" in d:
                p, v = d.split(":", 1)
                items.append(("(inline)", p.strip().lower(), v.strip()))
    return items


def check(path, scale):
    items = load(path)
    bad = collections.defaultdict(list)
    warn = collections.defaultdict(list)
    for sel, p, v in items:
        if "var(" in v or "calc(" in v:
            continue
        if p == "font-size":
            for n in px_values(v):
                if n in scale["fs"]:
                    continue
                if n == 16 and INPUT_SEL.search(sel):
                    continue
                bad["字級不在標尺"].append((sel, v))
        elif p == "line-height":
            if "px" in v or "rem" in v:
                bad["行距寫成長度（應寫倍數）"].append((sel, v))
            else:
                try:
                    if round(float(v), 2) not in scale["lh"]:
                        bad["行距不在表上"].append((sel, v))
                except ValueError:
                    pass
        elif p in SP_PROPS:
            for n in px_values(v):
                if n < 0:
                    if not NEG_OK.search(sel):
                        bad["負 margin"].append((sel, v))
                elif n not in SP_OK:
                    bad["間距不在標尺"].append((sel, v))
        elif p == "height":
            if px_values(v) and not DECOR.search(sel):
                warn["固定 height（若承載文字請改 min-height）"].append((sel, v))
        elif p == "letter-spacing":
            m = re.findall(r"(-?\d*\.?\d+)em", v)
            if m and round(float(m[0]), 3) not in LS_OK:
                bad["字距不在表上"].append((sel, v))
    return bad, warn, len(items)


def main():
    ap = argparse.ArgumentParser(description="標尺合規檢查")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--type", choices=["productive", "expressive", "all"], default="productive")
    ap.add_argument("-v", action="store_true", help="列出每一條不合規宣告")
    a = ap.parse_args()
    scale = {"productive": PRODUCTIVE, "expressive": EXPRESSIVE,
             "all": {k: PRODUCTIVE[k] | EXPRESSIVE[k] for k in PRODUCTIVE}}[a.type]

    total = 0
    for f in a.files:
        bad, warn, n = check(f, scale)
        cnt = sum(len(v) for v in bad.values())
        total += cnt
        summary = "  ".join(f"{c}:{len(v)}" for c, v in sorted(bad.items()))
        print(f"{f}\n  宣告 {n}，不合規 {cnt}  {summary}")
        for c, v in sorted(warn.items()):
            print(f"  提醒 {c}：{len(v)}")
        if a.v:
            for c, v in list(bad.items()) + list(warn.items()):
                print(f"  【{c}】")
                for sel, val in v[:30]:
                    print(f"    {sel[:56]:56} → {val}")
    print("通過" if total == 0 else f"不通過：共 {total} 項不合規")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
