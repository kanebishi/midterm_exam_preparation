# spec — 理科の図問題対応（make-test 拡張）

## 設計方針

### コア戦略：「再利用可能な図 SVG 群 + ラベル番号注入」方式

社会の地図問題と同じく、`works/midterm-test-generator/figures/` に**単元別の植物模式図 SVG** を置き、隠し `<defs>` に `<g id="...">` で登録 → 各問題で `<use href="#...">` 参照する。問題ごとには番号マーカーや引き出し線を上乗せして出題する。

**なぜこの方式か：**
- 社会の `world-base.svg` + `coords.md` 方式と対称性が取れるため、SKILL.md が読みやすい
- 同じ図を「部位名を問う」「比較問題」「正誤判定」と複数パターンで使い回せる
- 外部画像参照なしで HTML 自己完結の原則を維持できる

## ファイル構成

```
works/midterm-test-generator/
├── templates/
│   └── test.html.tmpl              （既存・CSS追記）
├── maps/                           （既存・社会用、触らない）
│   ├── world-base.svg
│   └── coords.md
└── figures/                        ★新規ディレクトリ
    ├── flower-cross-section.svg    被子植物の花の縦断面（がく/花弁/おしべ/めしべ/胚珠）
    ├── pine-flower.svg             マツの雌花・雄花とりん片
    ├── leaf-veins.svg              葉脈比較（網状脈 vs 平行脈）
    ├── roots.svg                   根のつくり比較（主根+側根 vs ひげ根）
    ├── fern.svg                    シダ植物（葉・茎・根・胞子のう）
    ├── moss.svg                    コケ植物（雌株・雄株・仮根）
    ├── plant-classification.svg    植物分類の樹形図
    └── labels.md                   各図のラベル候補位置一覧
.claude/skills/make-test/
└── SKILL.md                        （既存・理科セクション追記）
```

## 必要な図 7 種類

### 1. flower-cross-section.svg（花のつくり断面図）

- **viewBox**: `0 0 400 400`
- **描画内容**：
  - がく（緑、花の根元）
  - 花弁（淡いピンク、左右2枚で断面表現）
  - おしべ × 2（やく + 花糸、断面の左右）
  - めしべ（中央、柱頭 → 花柱 → 子房 → 胚珠）
  - 胚珠は子房の中に小さな円で2〜3個
- **問題例**：①〜⑥のラベル番号を打って「①は何か」を問う

### 2. pine-flower.svg（マツの花）

- **viewBox**: `0 0 500 400`
- **描画内容**：
  - 左右に **雌花**（紫がかった赤、上方の枝先・りん片構造）と **雄花**（黄色、下方の枝先・花粉のう）
  - 雌花は **胚珠がりん片の上にむき出し**で配置（裸子植物の特徴）
  - 中央に拡大した「りん片1枚」の断面（胚珠が見える）
- **問題例**：雌花と雄花を識別、胚珠がむき出しなことを問う

### 3. leaf-veins.svg（葉脈比較）

- **viewBox**: `0 0 500 300`
- **描画内容**：
  - 左：**網状脈**（双子葉類、広葉、主脈から細かい網目状の側脈）
  - 右：**平行脈**（単子葉類、細長い葉、平行に走る線）
- **問題例**：「双子葉類はどちらの葉脈か」「網状脈の葉の例を1つ答えよ」

### 4. roots.svg（根のつくり比較）

- **viewBox**: `0 0 500 300`
- **描画内容**：
  - 左：**主根+側根**（双子葉類型、太い主根 + 細い側根が放射状）
  - 右：**ひげ根**（単子葉類型、同じ太さの根が束状）
- **問題例**：「双子葉類の根はどちらか」「単子葉類の例を答えよ」

### 5. fern.svg（シダ植物）

- **viewBox**: `0 0 400 400`
- **描画内容**：
  - 羽状複葉（左右対称の葉、上方）
  - 茎（地下茎、地表近く）
  - 根（下方、ひげ状）
  - 葉裏の**胞子のう**（拡大マーカー or 別表示で粒状に描画）
- **問題例**：「胞子のうはどこか」「シダ植物の特徴を答えよ」

### 6. moss.svg（コケ植物）

- **viewBox**: `0 0 500 350`
- **描画内容**：
  - 左：**雌株**（さく＋柄、地表に仮根）
  - 右：**雄株**（雄器を上端に持つ、仮根）
  - 下方に **仮根**（地表下、ヒゲ状）
- **問題例**：雌株・雄株の識別、仮根の役割

### 7. plant-classification.svg（植物分類の樹形図）

- **viewBox**: `0 0 700 500`
- **描画内容**：
  - 最上段「植物」
  - 第2段「種子植物 / 種子をつくらない植物」
  - 第3段「被子植物 / 裸子植物 ／ シダ植物 / コケ植物」
  - 第4段（被子植物の下）「双子葉類 / 単子葉類」
  - 第5段（双子葉類の下）「合弁花類 / 離弁花類」
- 各ノードに**空欄ラベル**（ラベルを伏せて「①は何類か」と問う運用に対応）

## 共通スタイル方針

- **線画ベース** + 必要に応じて薄い塗り（教科書テイスト）
- 色は最小限：緑（葉・がく）、ピンク（花弁）、黄色（やく・雄花）、紫赤（雌花）、薄茶（根・茎）、黒（輪郭線）
- 印刷時のかすれを避けるため、輪郭は `stroke-width="1.5"` 以上
- **テキストラベルは図の中に焼き込まない**（問題で問うため空白のまま、ラベル番号は問題ごとに上乗せ）

## labels.md の構造

各 SVG ごとに、引き出し線の起点・終点候補をテーブル化：

```markdown
## flower-cross-section.svg

| 番号候補 | x   | y   | 部位名 | 備考 |
|---------|-----|-----|--------|------|
| 柱頭    | 200 | 80  | 柱頭   | めしべの先端 |
| 花柱    | 200 | 130 | 花柱   | めしべの中間 |
| 子房    | 200 | 200 | 子房   | めしべの根元、膨らみ |
| 胚珠    | 200 | 220 | 胚珠   | 子房の中 |
| やく    | 150 | 150 | やく   | おしべ先端 |
| 花糸    | 140 | 220 | 花糸   | おしべの柄 |
| 花弁    | 260 | 140 | 花弁   | 花びら |
| がく    | 280 | 280 | がく   | 花の付け根、緑 |
```

Claude は問題作成時に「部位 N 個を選んで番号 ①②③ を割り当て、座標から `<circle>` + `<text>` を生成する」運用にする。

## SKILL.md への追記内容

新セクション「## 理科の図問題の作り方」を追加し、以下を規定：

1. **適用範囲**：理科（`subjects/science.md`）のみ。他教科では使わない
2. **推奨出題数**：図問題は **3〜6問**（全体10〜20問の3〜4割程度。社会の地図問題2〜4問より多め＝植物分野は図ベースの理解が中心のため）
3. **手順**：
   - a. 必要な figure SVG を Read（複数同時で OK、最大4枚程度）
   - b. `figures/labels.md` を Read してラベル位置を取得
   - c. HTML の `<body>` 冒頭に隠し `<svg width="0" height="0">` の `<defs>` を1つ置き、使う図を `<g id="...">` で全部登録
   - d. 各問題では `<svg viewBox="..."><use href="#..."/>` でその図を参照し、ラベル番号やハイライトを上乗せ
4. **問題ブロック構造**（部位名を問うパターン）：

```html
<div class="q" data-no="N">
  <div><span class="q-no">問N</span>図の①〜④の名称を答えなさい。<span class="q-type">図</span></div>
  <div class="q-body">
    <figure class="q-figure">
      <svg viewBox="0 0 400 400" preserveAspectRatio="xMidYMid meet">
        <use href="#flower-cross-section"/>
        <circle cx="200" cy="80" r="14" class="fig-marker"/>
        <text x="200" y="80" class="fig-num">1</text>
        <circle cx="200" cy="200" r="14" class="fig-marker"/>
        <text x="200" y="200" class="fig-num">2</text>
        <circle cx="150" cy="150" r="14" class="fig-marker"/>
        <text x="150" y="150" class="fig-num">3</text>
        <circle cx="280" cy="280" r="14" class="fig-marker"/>
        <text x="280" y="280" class="fig-num">4</text>
      </svg>
    </figure>
  </div>
  <button class="toggle-btn" onclick="toggleAnswer(this)">答えを見る</button>
  <div class="answer"><span class="answer-label">答え:</span> ①柱頭 ②子房 ③やく ④がく</div>
</div>
```

5. **マーカーの3パターン**（社会と対称）：

| パターン | 用途 | 構造 |
|---|---|---|
| **番号マーカー** | 部位名を①②③で問う | `<circle r="14">` + `<text>` で番号 |
| **比較選択ハイライト** | 「網状脈はどちらか」 | 2つの図を並べ、片側に枠 or 矢印 |
| **領域強調** | 「胞子のうの位置はどこか」 | 該当部位を半透明色で塗りつぶし or 矢印 |

## テンプレ `test.html.tmpl` への追記

`<style>` 内に以下のCSSを追加（既存スタイル・社会用 `.q-map` 系は触らない）：

```css
.q-figure {
  margin: 12px 0 6px;
  text-align: center;
}
.q-figure svg {
  width: 100%;
  max-width: 480px;
  height: auto;
  border: 1px solid var(--line);
  border-radius: 4px;
  background: #fafafa;
}
.fig-marker {
  fill: #ef4444;
  stroke: #fff;
  stroke-width: 2;
}
.fig-num {
  fill: #fff;
  font-weight: bold;
  font-size: 14px;
  text-anchor: middle;
  dominant-baseline: middle;
  font-family: -apple-system, sans-serif;
}
.fig-highlight {
  fill: rgba(239, 68, 68, 0.25);
  stroke: #ef4444;
  stroke-width: 2;
}
@media print {
  .q-figure svg { background: #fff; max-width: 100%; }
}
```

## 期待される出題例（4問）

1. **花のつくり**：「図の①〜④の名称を答えなさい」（柱頭・子房・やく・がく など）
2. **マツの花**：「図のAは雌花・雄花のどちらか。理由とともに答えよ」
3. **葉脈と分類**：「葉脈が網状脈の植物は、双子葉類・単子葉類のどちらか」
4. **シダ植物**：「図の Y で示した部分を何というか。またそこで作られるものを答えよ」

## ユーザー確認結果（2026-05-13 確定）

1. **図 7 種類のリスト** → **7 種類すべて作る**で確定
2. **図のスタイル** → **教科書テイスト（線画 + 控えめな塗り）** で確定
3. **図問題の出題比率** → **3〜6 問**で確定
4. **subjects/science.md の「重要用語・概念」セクション** → **空のまま進める**で確定（後日必要なら追記）

## 実装フェーズ（確認後）

1. `works/midterm-test-generator/figures/` ディレクトリを作成
2. 7 種類の SVG を作成
3. `works/midterm-test-generator/figures/labels.md` を作成
4. `works/midterm-test-generator/templates/test.html.tmpl` に CSS 追加
5. `.claude/skills/make-test/SKILL.md` に「理科の図問題の作り方」セクション追加
6. 動作確認：理科の小テストを 1 回生成し、ブラウザで図表示を目視確認
7. `works/make-test-science-figures/knowledge.md` にハマりポイントを記録
