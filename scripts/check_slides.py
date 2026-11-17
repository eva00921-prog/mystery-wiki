"""教學簡報檢查，對應 AGENTS.md 第 6 節。

用法：python scripts/check_slides.py
檢查每張投影片是否能追溯到 Wiki、教學結構是否完整、文字量是否適合新手。
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLIDES = ROOT / "slides" / "index.html"
WIKI = ROOT / "wiki"
ORDER = ["goal", "why", "concept", "example", "quiz", "summary", "refs"]
MAX_CHARS = 230          # 一張投影片的字數上限，超過新手讀不完
C_LEVEL = {"S6", "S7"}   # AGENTS.md 第 5 節：只有 C 級來源時要保守用語
HEDGES = ("一般認為", "有一種整理", "有一種說法", "例如", "有作家")


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides, self.cur, self.depth, self.block = [], None, 0, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section" and "slide" in a.get("class", ""):
            self.cur = {"role": a.get("data-role", ""), "wiki": a.get("data-wiki", ""),
                        "text": "", "blocks": [], "title": ""}
            self.depth = 1
            return
        if self.cur is None:
            return
        if tag == "section":
            self.depth += 1
        if tag in ("li", "p", "h2", "h3", "td"):
            self.block = tag
            self.cur["blocks"].append("")

    def handle_endtag(self, tag):
        if self.cur is None:
            return
        if tag == "section":
            self.depth -= 1
            if self.depth == 0:
                self.slides.append(self.cur)
                self.cur = None

    def handle_data(self, data):
        if self.cur is None:
            return
        self.cur["text"] += data
        if self.cur["blocks"]:
            self.cur["blocks"][-1] += data


def page_sources(name):
    path = next(WIKI.rglob(f"{name}.md"), None)
    if not path:
        return None
    m = re.search(r"^sources: \[(.*?)\]", path.read_text(encoding="utf-8"), re.M)
    return set(re.findall(r"S\d+", m.group(1))) if m else set()


p = Parser()
p.feed(SLIDES.read_text(encoding="utf-8"))
errors, roles = [], []

for n, s in enumerate(p.slides, 1):
    tag = f"第 {n} 張"
    role = s["role"]
    roles.append(role)
    if role not in ORDER:
        errors.append(f"{tag}：data-role {role!r} 不在教學結構 {ORDER} 裡")
    names = [w.strip() for w in s["wiki"].split(",") if w.strip()]
    if not names:
        errors.append(f"{tag}：缺少 data-wiki，每張投影片都要標出根據的 Wiki 頁面")
    allowed = set()
    for w in names:
        src = page_sources(w)
        if src is None:
            errors.append(f"{tag}：data-wiki 指向不存在的 Wiki 頁面 {w}")
        else:
            allowed |= src
    cited = set(re.findall(r"\[(S\d+)\]", s["text"]))
    if role in ("concept", "example", "why") and not names:
        errors.append(f"{tag}：{role} 投影片必須用 data-wiki 標出根據的 Wiki 頁面")
    if role in ("concept", "example") and not cited:
        errors.append(f"{tag}：內容投影片沒有任何來源標記")
    for sid in cited - allowed:
        errors.append(f"{tag}：引用了 {sid}，但它不在所標的 Wiki 頁面 {names} 的來源裡，無法追溯")
    for b in s["blocks"]:
        tags = set(re.findall(r"\[(S\d+)\]", b))
        if tags and tags <= C_LEVEL and not any(h in b for h in HEDGES):
            errors.append(f"{tag}：只有 C 級來源 {sorted(tags)} 支持，卻沒有用保守語氣 → {b.strip()[:30]}")
    length = len(re.sub(r"\s+|\[S\d+\]", "", s["text"]))
    if length > MAX_CHARS and role != "refs":  # 參考資料頁是清單，不限字數
        errors.append(f"{tag}：字數 {length} 超過 {MAX_CHARS}，對新手太擠，請拆成兩張")
    if role == "quiz" and "答案" not in s["text"]:
        errors.append(f"{tag}：小測驗沒有提供答案")

# 來源標記格式：一律寫成 [S1]
html = SLIDES.read_text(encoding="utf-8")
for bad in re.findall(r'<span class="src">(?!\[S\d+\])([^<]*)</span>', html):
    errors.append(f"來源標記格式錯誤：{bad!r}，應寫成 [S1] 這種格式")

# 教學結構順序：例子可以穿插在概念之間，緊跟著它示範的概念
phase = ["concept" if r == "example" else r for r in roles]
seen = [r for i, r in enumerate(phase) if i == 0 or r != phase[i - 1]]
for r in ORDER:
    if r not in roles:
        errors.append(f"教學結構缺少 {r} 投影片")
idx = [ORDER.index(r) for r in seen if r in ORDER]
if idx != sorted(idx) or len(seen) != len(set(seen)):
    errors.append(f"教學結構順序錯誤：目前是 {seen}，應該依照 {ORDER}")

if errors:
    print(f"❌ 簡報檢查發現 {len(errors)} 個問題")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print(f"✅ 簡報檢查通過：{len(p.slides)} 張投影片，每張都能追溯到 Wiki，教學結構完整")
