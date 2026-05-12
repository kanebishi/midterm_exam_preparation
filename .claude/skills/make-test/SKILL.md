---
name: make-test
description: 中学生向けの小テストHTMLを教科ごとに生成する。「英語のテスト作って」「数学のテスト作って」「理科のテスト作って」「社会のテスト作って」のように教科名 + 「テスト作って／問題作って／小テスト」というフレーズで呼ばれたときに使う。試験範囲は `subjects/<教科>.md` を参照し、10〜20問の HTML を `docs/<教科>/` に出力する。
---

# make-test — 中学生向け小テスト生成スキル

## 使うタイミング

ユーザーが以下のような発話をしたとき：
- 「英語のテスト作って」
- 「数学のテスト作って」「数学の問題作って」
- 「理科のテスト作って」「理科の小テスト」
- 「社会のテスト作って」

教科名（英語/数学/理科/社会）と「テスト・問題・小テスト」というフレーズがセットになっていれば、このスキルを起動する。

## 前提

このスキルは **現在の作業ディレクトリ (cwd) 配下に以下の構造があること**を前提とする：

```
<cwd>/
├── subjects/                       # 各教科の試験範囲メモ
│   ├── english.md
│   ├── math.md
│   ├── science.md
│   └── social-studies.md
├── docs/                           # 生成HTMLの出力先
│   ├── english/  math/  science/  social-studies/
└── works/midterm-test-generator/
    ├── templates/test.html.tmpl
    ├── maps/   world-base.svg, coords.md      # 社会の地図問題用
    └── figures/ *.svg, labels.md              # 理科の図問題用
```

構造が無い場合は、ユーザーに「`midterm_exam_preparation` リポジトリで実行してください」と伝えて中断する。

## 教科名→ファイル名のマッピング

| ユーザー発話の教科 | subjects ファイル | 出力ディレクトリ |
|---|---|---|
| 英語 | `subjects/english.md` | `docs/english/` |
| 数学 | `subjects/math.md` | `docs/math/` |
| 理科 | `subjects/science.md` | `docs/science/` |
| 社会 | `subjects/social-studies.md` | `docs/social-studies/` |

## 生成手順

### 1. 範囲データを読む
- 対応する `subjects/<教科>.md` を Read する
- 「（未記入）」が多くて出題に不十分なら、**ユーザーに「範囲情報を埋めてから再度呼んでください」と提案して中断**してよい（推測で範囲外を出すより誠実）
- 一部だけ未記入なら、記入済み部分から出題する

### 2. 問題を 10〜20問 生成する
- **形式をミックス**：穴埋め / 一問一答（短答記述） / 選択式（3〜4択） / 正誤判定 をバランスよく組み合わせる
- 範囲データ内の重要語句・公式・用語リストを **ランダム抽出**して、同じファイルから生成しても毎回違う問題セットになるようにする
- 教科の特性に合わせる：
  - **英語**: スペル / be動詞・一般動詞の使い分け / 単語の意味 / 短い英文の穴埋め
  - **数学**: 計算問題（符号付き加減乗除）／絶対値 / 大小比較 / 用語の意味
  - **理科**: 用語の意味 / 図中の名称 / 正誤判定で混同しやすい概念を突く
    - **インライン SVG 模式図を使った問題**を 3〜6問混ぜる（詳細は後述「理科の図問題の作り方」）
  - **社会**: 地名・用語の意味 / 地図上の位置 / 年号・出来事
    - **インライン SVG 地図を使った問題**を 2〜4問混ぜる（詳細は後述「社会の地図問題の作り方」）
- 各問題には必ず**答え**もセットで生成する（解説が必要なら短く添える）

### 3. HTML を組み立てる

- テンプレ `works/midterm-test-generator/templates/test.html.tmpl` を Read で読む
- 以下のプレースホルダを置換：
  - `{{TITLE}}` → 例：「英語 小テスト（2026-05-12）」
  - `{{SUBJECT}}` → 「英語」「数学」「理科」「社会」
  - `{{TOTAL}}` → 生成した問題数
  - `{{GENERATED_AT}}` → ISO形式の日付（例: 2026-05-12）
  - `{{FOOTER}}` → 「midterm_exam_preparation / make-test」
- テンプレ内の `<main id="questions"> ～ </main>` の中にあるサンプル4問は**全て削除**し、生成した問題ブロックで置き換える
- 問題ブロックの構造はサンプルをそのまま踏襲する：
  - 穴埋め: `<span class="q-type">穴埋め</span>` + 本文中に `<span class="blank"></span>`
  - 一問一答: `<span class="q-type">一問一答</span>`
  - 選択式: `<span class="q-type">選択</span>` + `<ul class="choices">` で選択肢
  - 正誤判定: `<span class="q-type">正誤</span>`
  - 地図（社会のみ）: `<span class="q-type">地図</span>` + `<figure class="q-map">` 内にインライン SVG（後述）
  - 図（理科のみ）: `<span class="q-type">図</span>` + `<figure class="q-figure">` 内にインライン SVG + `<use>` 参照（後述）
- 各問題に「答えを見る」トグル（`<button class="toggle-btn">` と `<div class="answer">`）を必ず付ける

### 4. ファイルを書き出す

- 出力先: `docs/<教科>/<YYYY-MM-DD>-NNN.html`
  - NNN は同日内の連番（既存ファイルを ls で確認して採番）
  - 例: `docs/english/2026-05-12-001.html`
- Write ツールで書き出す

### 5. インデックスページを更新する

- `python3 scripts/build-index.py` を Bash で実行する
- このスクリプトは `docs/<教科>/*.html` を走査して `docs/index.html`（GitHub Pages のトップページ）を再生成する。冪等なので何度呼んでも安全
- 実行は**必ず行う**こと（忘れるとトップページに新しいテストが現れない）
- スクリプトが存在しない／エラーになる場合は、ユーザーに報告したうえで手動で `docs/index.html` を更新する案内をする

### 6. ユーザーへの提示

以下の情報を出力する：
- 生成したファイルのフルパス
- 問題数と内訳（例: 穴埋め5 / 一問一答6 / 選択3 / 正誤2 = 計16問）
- ブラウザで開くコマンド：`open <パス>`
- 印刷したい場合の案内：「ブラウザで開いて、ツールバーの『印刷 / PDF』ボタンを押すと印刷ダイアログが出ます」

## 社会の地図問題の作り方

社会（`subjects/social-studies.md`）の小テストを作るときのみ適用。他教科では使わない。

### 推奨出題数

10〜20問のうち **2〜4問** を地図問題にする。テキスト問題とのバランスをとる。

### 使う資材

- `works/midterm-test-generator/maps/world-base.svg` — ベース世界地図（viewBox `0 0 1000 500`、等距円筒図法）
- `works/midterm-test-generator/maps/coords.md` — 大陸・海洋・主要国・主要緯線経線の座標参照テーブル

### 手順

1. **ベース SVG を Read** で読み込み、`<svg>` の**中身**（`<rect>` から最後の `</g>` までの内側要素群）を取得する
2. **coords.md を Read** で読み込み、出題内容に応じた座標を取得する
3. HTML の `<body>` 冒頭付近に、地図定義用の**隠し SVG** を1つだけ配置する：

   ```html
   <svg width="0" height="0" aria-hidden="true" style="position:absolute" xmlns="http://www.w3.org/2000/svg">
     <defs>
       <g id="world-map-defn">
         <!-- world-base.svg の <svg> 内側要素をここに丸ごとコピー -->
       </g>
     </defs>
   </svg>
   ```

4. 各地図問題では、別の `<svg>` を作って `<use href="#world-map-defn"/>` で参照したうえで、マーカー要素を追加する（後述）
5. 問題ブロック構造に組み込む

**なぜ `<use>` 方式か：** 地図問題が複数あっても、ベース地図の本体は1コピーで済む。3問とも完全インラインだとHTMLが3〜4倍に膨らむ。`<use>` は同一ドキュメント内参照なので外部リソース禁止ルールには触れない。

### マーカーの3パターン

#### A. 番号マーカー（大陸・海洋・国の位置同定）

「①〜⑥の大陸名を答えよ」のような問題で使う。`<circle>` と `<text>` のペア：

```html
<circle cx="722" cy="111" r="14" class="map-marker"/>
<text x="722" y="111" class="map-num">1</text>
```

- 円の半径は `r="14"` 固定
- text は `dominant-baseline: central` で円の中央に番号が来る
- 番号は `1` から始まり、問題内で連番

#### B. 緯度経度ポイント（読み取り問題）

「点 P の緯度経度を答えよ」のような問題：

```html
<circle cx="583" cy="185" r="5" class="q-map-point"/>
<text x="583" y="175" class="q-map-label">P</text>
```

- ポイントは半径5px、青色
- ラベル文字（P, Q など）は点の少し上に配置（y を -10）

#### C. 強調ハイライト（緯線・経線の同定）

「強調されている線A・Bは何か」のような問題。既存の緯線・経線の上から赤い線を重ねる：

```html
<line x1="0" y1="250" x2="1000" y2="250" class="map-highlight"/>
<text x="20" y="245" class="q-map-label">A</text>
```

### 問題ブロック構造（地図問題）

```html
<div class="q" data-no="N">
  <div><span class="q-no">問N</span>地図中の①〜③の大陸名を答えなさい。<span class="q-type">地図</span></div>
  <div class="q-body">
    <figure class="q-map">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" preserveAspectRatio="xMidYMid meet">
        <use href="#world-map-defn"/>
        <circle cx="722" cy="111" r="14" class="map-marker"/>
        <text x="722" y="111" class="map-num">1</text>
        <circle cx="556" cy="236" r="14" class="map-marker"/>
        <text x="556" y="236" class="map-num">2</text>
        <circle cx="222" cy="125" r="14" class="map-marker"/>
        <text x="222" y="125" class="map-num">3</text>
      </svg>
    </figure>
  </div>
  <button class="toggle-btn" onclick="toggleAnswer(this)">答えを見る</button>
  <div class="answer"><span class="answer-label">答え:</span> ①ユーラシア大陸 ②アフリカ大陸 ③北アメリカ大陸</div>
</div>
```

### 地図問題の出題テーマ例

`subjects/social-studies.md` の範囲に対応したテーマ：

- **六大陸の位置同定**：ユーラシア・アフリカ・北アメリカ・南アメリカ・オーストラリア・南極のうちランダムに3〜6個に番号を振る
- **三大洋の位置同定**：太平洋・大西洋・インド洋に番号を振る
- **緯度経度の読み取り**：coords.md「緯度経度ポイント例」から1〜2点を選んで配置し、緯度経度を答えさせる
- **主要緯線・経線の同定**：赤道・北回帰線・南回帰線・本初子午線などをハイライトして名前を答えさせる
- **主要国の位置同定**：日本・中国・アメリカ・ブラジルなど範囲メモで重視されている国に番号を振る

### 重要な制約

- **外部 SVG 参照は禁止**（`<img src="...svg">` や `<use href="...">` ともに不可）。必ず SVG の中身を HTML にインライン展開すること
- マーカー座標は `coords.md` から取得する。**勝手な座標を作らない**（精度の保証が崩れる）
- 番号マーカーが**陸地ではなく海上に乗らないように**注意する（特に小さな国・島国の場合）。配置後に座標を再確認する
- 地図問題1問あたりのマーカーは **最大6個** に抑える（多すぎると視認性が落ちる）

## 理科の図問題の作り方

理科（`subjects/science.md`）の小テストを作るときのみ適用。他教科では使わない。

### 推奨出題数

10〜20問のうち **3〜6問** を図問題にする。植物分野は図ベースの理解が中心のため、社会の地図問題（2〜4問）より多め。

### 使う資材

`works/midterm-test-generator/figures/` 配下の SVG 群と `labels.md`：

| ファイル | 内容 | 主な用途 |
|---|---|---|
| `flower-cross-section.svg` | 被子植物の花の断面 | 柱頭・花柱・子房・胚珠・やく・花糸・花弁・がくの部位名を問う |
| `pine-flower.svg` | マツの雌花・雄花とりん片拡大 | 裸子植物の特徴（胚珠がむき出し）を問う |
| `leaf-veins.svg` | 網状脈と平行脈の比較 | 双子葉類 vs 単子葉類の葉の判別 |
| `roots.svg` | 主根+側根とひげ根の比較 | 双子葉類 vs 単子葉類の根の判別 |
| `fern.svg` | シダ植物の全体と胞子のう拡大 | 胞子のうの位置・胞子で増えること |
| `moss.svg` | コケ植物の雌株・雄株 | 仮根・さく・雄器の識別 |
| `plant-classification.svg` | 植物分類の樹形図 | 階層関係を見ながら例の植物を問う |
| `labels.md` | 各図の部位座標一覧 | ラベル番号マーカーの cx/cy を取得 |

### 手順

1. **使う figure SVG を Read** で読み込む（複数同時で OK、最大4枚程度を一度に使うのは避ける）
2. **labels.md を Read** で読み込み、部位座標を取得
3. HTML の `<body>` 冒頭付近に、図定義用の**隠し SVG** を1つ配置する。使う図ごとに `<g id="...">` で登録：

   ```html
   <svg width="0" height="0" aria-hidden="true" style="position:absolute" xmlns="http://www.w3.org/2000/svg">
     <defs>
       <g id="flower-cross-section">
         <!-- flower-cross-section.svg の <svg> 内側要素をここに丸ごとコピー -->
       </g>
       <g id="leaf-veins">
         <!-- leaf-veins.svg の中身 -->
       </g>
     </defs>
   </svg>
   ```

4. 各図問題では、別の `<svg>` を作って `<use href="#<id>"/>` で参照したうえで、マーカー要素を追加する
5. 問題ブロック構造に組み込む（後述）

**なぜ `<use>` 方式か：** 図問題が複数あっても、図本体は1コピーで済む。社会の地図問題と同じ仕組み。

### マーカーの3パターン

#### A. 番号マーカー（部位名を問う）

「①〜④の部位名を答えよ」のような問題で使う。`<circle>` と `<text>` のペア：

```html
<circle cx="200" cy="110" r="14" class="fig-marker"/>
<text x="200" y="110" class="fig-num">1</text>
```

- 円の半径は `r="14"` 固定
- text は `dominant-baseline: central` で円の中央に番号が来る
- 番号は `1` から始まり、問題内で連番

#### B. アルファベットラベル（比較選択）

「葉脈Aは網状脈・平行脈のどちらか」のような問題。図には既に A, B のラベルがあるが、追加で説明矢印を打つときに使う：

```html
<text x="145" y="280" class="fig-label">A</text>
```

#### C. 領域ハイライト（部位の位置を強調）

「胞子のうの位置を示せ」のような問題。該当部位の周囲に半透明の枠：

```html
<rect x="190" y="170" width="40" height="30" rx="6" class="fig-highlight"/>
```

### 問題ブロック構造（図問題）

```html
<div class="q" data-no="N">
  <div><span class="q-no">問N</span>図の①〜④の名称を答えなさい。<span class="q-type">図</span></div>
  <div class="q-body">
    <figure class="q-figure">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" preserveAspectRatio="xMidYMid meet">
        <use href="#flower-cross-section"/>
        <circle cx="200" cy="110" r="14" class="fig-marker"/>
        <text x="200" y="110" class="fig-num">1</text>
        <circle cx="200" cy="255" r="14" class="fig-marker"/>
        <text x="200" y="255" class="fig-num">2</text>
        <circle cx="155" cy="150" r="14" class="fig-marker"/>
        <text x="155" y="150" class="fig-num">3</text>
        <circle cx="165" cy="318" r="14" class="fig-marker"/>
        <text x="165" y="318" class="fig-num">4</text>
      </svg>
    </figure>
  </div>
  <button class="toggle-btn" onclick="toggleAnswer(this)">答えを見る</button>
  <div class="answer"><span class="answer-label">答え:</span> ①柱頭 ②子房 ③やく ④がく</div>
</div>
```

### 図問題の出題テーマ例

`subjects/science.md` の試験範囲に対応したテーマ：

- **花のつくり**：被子植物の花の断面（`flower-cross-section`）の各部位を①〜⑥で問う
- **マツの花**：（`pine-flower`）雌花・雄花の識別、胚珠がむき出しなことの確認
- **葉脈と分類**：（`leaf-veins`）A・B どちらが双子葉類か、その理由
- **根のつくりと分類**：（`roots`）A・B どちらがひげ根か、対応する植物例
- **シダ植物**：（`fern`）胞子のうの位置、胞子で増えること、葉・茎・根の有無
- **コケ植物**：（`moss`）雌株・雄株の識別、仮根の役割
- **植物の分類**：（`plant-classification`）「裸子植物の例」「合弁花類の例」など階層をたどる問題

### 重要な制約

- **外部 SVG 参照は禁止**（社会の地図問題と同じ）。必ず `<defs>` 内に `<g id="...">` で丸ごとインライン展開
- マーカー座標は `labels.md` から取得する。**勝手な座標を作らない**（部位を覆い隠す事故を防ぐ）
- 1問あたりのマーカーは **最大6個**（社会の地図問題と同じ上限）
- **テキストラベルを SVG 内に焼き付けない**：問題で部位名を問うため、図内に「柱頭」「子房」等と書いてしまうと答えが見えてしまう（既に各 SVG はラベルなしで作られているので、注入する `<text>` も番号のみにする）
- **比較図（葉脈・根）の左右ラベル A・B は焼き付け済み**：そのまま使う

## 重要な注意事項

- **HTML は単体で完結**させること。外部CSS/JSを読み込まない（GitHub Pages 配信時も追加設定不要にするため）
- 出題内容に**範囲外の知識を混ぜない**。`subjects/*.md` に書かれていない単語・公式・年号は使わない
- 答えに**自信がない問題は出さない**。中学1年生が解いて「正解なのに×をつけられた」が起きるのは最悪
- 教科ごとの言語：英語の問題は英文＋日本語の指示文、その他は日本語
