# knowledge.md — 中間考査対策テスト生成スキル ナレッジ集

## 教科書情報の調査ナレッジ

### 開隆堂 Sunshine English Course 1（令和7年度版）

**確定情報源（URL）**

- 公式紹介ページ：https://krdkrk.jp/english/
- 内容解説資料 PDF（20ページ、A3）：https://krdkrk.jp/kwp_2025/wp-content/uploads/2024/04/r7jh_english_naiyo.pdf
- 年間指導計画 PDF：https://www.kairyudo.co.jp/contents/04_shiryo/nenkei/chu/data/siryo_nenkei_1.pdf
- 年間指導計画作成資料 トップ：https://www.kairyudo.co.jp/contents/04_shiryo/nenkei/chu/index.htm

**確定したページ対応**

- **Get Ready 2 = p.10〜11**（内容解説資料 p.24-25 のサンプル画像で確認）
- Get Ready 2 はすごろく形式の小学校復習（14マス）

**年間指導計画から判明している構造（4月〜6月）**

| 時期 | 単元 | 配当時数 | 言語材料 |
|------|------|---------|---------|
| 4月 | Get Ready 1〜6 | 6 | 1〜4: 小学校で学んだ表現 (like / can / want to / When, Where疑問文) / 5: アルファベットの文字と音、つづり字と発音 / 6: 英語の語順 |
| 5月 | PROGRAM 1 友だちを作ろう | 5 | be動詞（肯定・否定・疑問）、whereの疑問文 |
| 5月 | Step 1 発表上手になろう | 1 | 発表をする際のポイント |
| 5月 | PROGRAM 2 1-Bの生徒たち | 5 | 一般動詞（肯定・否定・疑問）、複数形、whenの疑問文 |
| 6月 | アクションコーナー | 1 | 命令文 |
| 6月 | PROGRAM 3 タレントショーを開こう | 5 | can（肯定・否定・疑問）、whatの疑問文 |

**推定したページ対応（各 Get Ready が見開き2ページと仮定）**

- Get Ready 1: p.8-9
- Get Ready 2: p.10-11（確定）
- Get Ready 3: p.12-13（推定）
- Get Ready 4: p.14-15（推定）
- Get Ready 5: p.16-17（推定）
- Get Ready 6: p.18-19（推定）

**PROGRAM 1 以降の主要文法学習順**

- PROGRAM 1: be動詞 (am/are) + where疑問文 — 単元名「新しい友だちとの出会い」
- PROGRAM 2: 一般動詞 + 複数形 + when疑問文 — 単元名「みんなの趣味は？」
- PROGRAM 3: can + what疑問文 — 単元名「できることを教えて！」
- PROGRAM 5: 三人称単数現在形

## 教科書版違いの罠

- **令和3年度版（R3）と令和7年度版（R7）でページ構成が大きく異なる**
  - R3: Get Ready (p.10-11 のみ) → PROGRAM 0 (p.14-19: 自己紹介・アルファベット・つづり字) → PROGRAM 1
  - R7: Get Ready 1〜6 に統合・拡張（PROGRAM 0 は廃止）
- R3 のページ番号を R7 にそのまま適用してはいけない
- 検索結果に PDF が出てきたら、必ず**作成日付**で R3 / R7 を判別する（年間指導計画は更新日が「2024年6月28日」なら R7）

## PDF 取得時のハマりポイント

- WebFetch でバイナリPDFを取得すると `maxContentLength` を超えてエラーになることがある（11MBの内容解説資料は超過）
- 代替手段：`curl -o /tmp/foo.pdf <URL>` でローカルに落として、Read ツールに `pages` 引数を渡すと PDF を画像として読める
- 大きな PDF は `pages: "1-5"` のように小分けに読む
