# 推理小說設計技巧 LLM Wiki

用 LLM Wiki 的方式整理推理小說的設計技巧，再用 Wiki 當知識庫生成教學 HTML 簡報。

- 🌐 網站：https://eva00921-prog.github.io/mystery-wiki/
- 🎞️ 教學簡報：https://eva00921-prog.github.io/mystery-wiki/slides/
- 📚 Wiki 入口：[wiki/index.md](wiki/index.md)
- 🔁 流程設計與檢查紀錄：[docs/workflow.md](docs/workflow.md)
- 📏 規則：[AGENTS.md](AGENTS.md)

## 結構
| 資料夾 | 內容 |
|---|---|
| raw/ | 7 張原始資料卡，事實逐條編號 |
| discussions/ | 每個來源生成前的討論紀錄 |
| wiki/ | 概念頁、來源摘要、查詢結果、index、log |
| slides/ | 教學簡報 |
| scripts/ | lint_wiki.py 與 check_slides.py |
| docs/ | 流程圖、執行紀錄、反思 |

## 檢查
```bash
python scripts/lint_wiki.py
python scripts/check_slides.py
```
