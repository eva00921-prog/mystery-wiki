"""LLM Wiki 健康檢查，對應 AGENTS.md 第 4 節 Lint。

用法：python scripts/lint_wiki.py
通過印出 ✅，否則列出所有問題並以 1 結束。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
TYPES = {"concept", "source", "query", "overview"}
SKIP = {"index.md", "log.md"}

errors = []
raw_ids = {p.name.split("-")[0] for p in RAW.glob("S*.md")}
raw_facts = set()
for p in RAW.glob("S*.md"):
    raw_facts |= set(re.findall(r"^- (S\d+-F\d+)", p.read_text(encoding="utf-8"), re.M))

pages = {p.stem: p for p in WIKI.rglob("*.md") if p.name not in SKIP}
linked_to = {name: 0 for name in pages}


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        return None, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


for name, path in pages.items():
    rel = path.relative_to(ROOT)
    meta, body = parse(path)
    if meta is None:
        errors.append(f"{rel}：缺少 frontmatter")
        continue
    for key in ["title", "type", "sources", "updated"]:
        if key not in meta:
            errors.append(f"{rel}：frontmatter 缺少 {key}")
    if meta.get("type") not in TYPES:
        errors.append(f"{rel}：type 必須是 {sorted(TYPES)}")

    declared = set(re.findall(r"S\d+", meta.get("sources", "")))
    cited = set()
    in_summary = False
    for i, line in enumerate(body.splitlines(), 1):
        s = line.strip()
        if s.startswith("#"):
            in_summary = re.sub(r"^#+\s*", "", s).strip() == "整理"
            continue
        if not s or in_summary or s.startswith(">"):
            continue  # > 開頭是導覽或說明，不是事實句
        # 只有連結的導覽行不算事實句
        if re.fullmatch(r"(相關頁面：)?\s*(\[\[[^\]]+\]\][、，\s]*)+", s):
            pass
        else:
            marks = re.findall(r"\[(S\d+)(-F\d+)?\]", s)
            if not marks:
                errors.append(f"{rel}:{i}：事實句缺少來源標記 → {s[:40]}")
            elif meta.get("type") in ("concept", "overview") and any(not f for _, f in marks):
                errors.append(f"{rel}:{i}：概念頁必須引用到事實編號，例如 [S2-F3]，不能只寫 [S2] → {s[:40]}")
            cited |= {sid for sid, _ in marks}
        for fact in re.findall(r"\b(S\d+-F\d+)\b", s):
            if fact not in raw_facts:
                errors.append(f"{rel}:{i}：引用了不存在的事實編號 {fact}")
        for link in re.findall(r"\[\[([^\]]+)\]\]", s):
            if link not in pages:
                errors.append(f"{rel}:{i}：連結 [[{link}]] 指向不存在的頁面")
            elif link != name:
                linked_to[link] += 1

    for sid in cited - raw_ids:
        errors.append(f"{rel}：引用的來源 {sid} 在 raw/ 中不存在")
    if cited != declared:
        errors.append(f"{rel}：frontmatter sources {sorted(declared)} 和內文引用 {sorted(cited)} 不一致")

# index 與頁面一致
index = (WIKI / "index.md").read_text(encoding="utf-8")
listed = set(re.findall(r"\[\[([^\]]+)\]\]", index))
for name in pages:
    if name not in listed:
        errors.append(f"index.md：沒有列出 {name}")
    else:
        linked_to[name] += 1
for name in listed - set(pages):
    errors.append(f"index.md：列出了不存在的頁面 {name}")

# 孤兒概念頁：除了 index 以外沒有任何頁面連到它
for name, path in pages.items():
    meta, _ = parse(path)
    if meta and meta.get("type") == "concept" and linked_to[name] <= 1:
        errors.append(f"{path.relative_to(ROOT)}：孤兒頁面，沒有其他頁面連到它")

# log 格式
log = (WIKI / "log.md").read_text(encoding="utf-8")
for line in log.splitlines():
    if line.startswith("## ") and not re.match(r"## \[\d{4}-\d{2}-\d{2}\] (ingest|query|lint|slides) \| ", line):
        errors.append(f"log.md：格式錯誤 → {line}")
ingested = set(re.findall(r"ingest \| (S\d+)", log))
for sid in raw_ids - ingested:
    errors.append(f"log.md：{sid} 有原始資料卡但沒有 ingest 紀錄")
for sid in raw_ids:
    if not (ROOT / "discussions" / f"{sid}.md").exists():
        errors.append(f"discussions/{sid}.md：缺少討論紀錄，違反先討論後生成")

if errors:
    print(f"❌ lint 發現 {len(errors)} 個問題")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print(f"✅ lint 通過：{len(pages)} 個頁面，{len(raw_ids)} 個來源，全部都有來源標記與正確連結")
