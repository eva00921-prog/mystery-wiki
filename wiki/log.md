# Wiki 操作紀錄

只能往下追加，不修改舊紀錄。

## [2026-11-17] ingest | S1 Golden Age of Detective Fiction
- 討論：discussions/S1.md
- 頁面：建立 golden-age、knox-decalogue、fair-play 骨架、overview

## [2026-11-17] ingest | S2 Van Dine 二十條規則
- 討論：discussions/S2.md
- 頁面：新增 van-dine-rules；fair-play 加入兩套規則比較；記下和密室推理的衝突，等 S5 處理

## [2026-11-17] ingest | S3 Red herring
- 討論：discussions/S3.md
- 頁面：新增 red-herring 與綜合頁 clue-design；決定不用達文西密碼的例子以免劇透

## [2026-11-17] ingest | S4 Unreliable narrator
- 討論：discussions/S4.md
- 頁面：新增 unreliable-narrator；knox-decalogue 加上規則會被打破的連結；不寫羅傑艾克洛命案的敘事者身分

## [2026-11-17] ingest | S5 The Hollow Man
- 討論：discussions/S5.md
- 頁面：新增 locked-room；處理 S2 留下的衝突，兩種觀點並列

## [2026-11-17] ingest | S6 Fell 博士密室講義整理
- 討論：discussions/S6.md
- 頁面：locked-room 加入七種分類；三大方向放在整理段落，不當成來源事實

## [2026-11-17] ingest | S7 公平推理的現代復興
- 討論：discussions/S7.md
- 頁面：新增 challenge-to-reader；fair-play 加入定義與現代做法；clue-design 加入線索索引

## [2026-11-17] lint | 第一次健康檢查
- 結果：7 個問題，見 docs/run-logs/01-lint-first-pass.txt
- 6 個是來源摘要頁的導覽行被當成事實句；1 個是 lint 程式本身的 bug：S6 標題含有 整理 兩字，整頁被誤判為整理段落而跳過檢查
- 修正：導覽行改用 > 開頭並寫進 AGENTS.md；整理段落改成標題完全等於 整理 才算
- 重跑結果：通過，見 docs/run-logs/02-lint-after-fix.txt

## [2026-11-17] query | 教學簡報大綱
- 存成 queries/slide-outline

## [2026-11-17] lint | 事實核對 v1 與 Wiki 改版
- 獨立 AI 事實核對發現 36 個問題，最嚴重的是討論中的推論被寫成有來源標記的事實，以及一處劇透，見 docs/run-logs/04-fact-check-v1.md
- 改版：概念頁一律引用到事實編號；討論中的推論只能進整理段落；lint 強制檢查事實編號
- 用新 lint 檢查舊版 Wiki，抓出 76 處只引用到來源層級的句子，見 docs/run-logs/06-new-lint-on-v1.txt

## [2026-11-17] lint | 事實核對 v2
- 沒有來源支持與扭曲原意都歸零；剩 2 處劇透與 1 處語氣，已修正，見 docs/run-logs/09-fact-check-v2.md

## [2026-11-17] slides | 生成教學簡報
- 根據 queries/slide-outline 生成 slides/index.html，共 16 張
- check_slides 第一次 4 個問題，修正後通過，見 docs/run-logs/07 與 08

## [2026-11-17] slides | 新手審查與簡報改版
- 獨立 AI 新手審查判定需要修改，見 docs/run-logs/12-review-slides-v1.md
- 簡報改版：補術語說明、例子移到對應概念後面、練習案件加上公平檢查、移除劇透
- check_slides 新增 data-wiki 必填與來源標記格式檢查，並允許例子穿插在概念之間

## [2026-11-17] slides | 新手審查 v2 與發布
- 第二次新手審查判定可以發布，修正 8 個中等問題，見 docs/run-logs/13-review-slides-v2.md
- AGENTS.md 新增簡報補充說明必須來自 Wiki 的規則
