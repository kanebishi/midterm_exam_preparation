# spec — 社会の地図問題対応（make-test 拡張）

## 設計方針

### コア戦略：「ベースSVG + マーカー注入」方式

毎回ゼロからSVGを書くのではなく、リポジトリ内に**ベース世界地図SVG（1種類）**を1枚用意し、Claudeはそれを Read で読み込んでHTMLに**インライン展開**したうえで、問題ごとに番号マーカー（①〜⑨）を追加注入する。

**なぜこの方式か：**
- ゼロから書くと毎回品質がぶれる、座標もバラつく
- ベースSVGがあれば「①②③の大陸名は？」のような問題を、座標の参照テーブルから機械的に生成できる
- インライン展開すれば「HTML自己完結」の原則を維持できる（外部参照ゼロ）

## ファイル構成

```
works/midterm-test-generator/
├── templates/
│   └── test.html.tmpl                    （既存・CSS追記）
└── maps/                                 ★新規ディレクトリ
    ├── world-base.svg                    ★ベース世界地図（経緯線付き）
    └── coords.md                         ★座標参照テーブル
.claude/skills/make-test/
└── SKILL.md                              （既存・地図セクション追記）
```

### ベース地図 `world-base.svg` の仕様

- **viewBox**: `"0 0 1000 500"`（経度1°≒2.78px、緯度1°≒2.78px の等距円筒図法相当）
- **座標系**：
  - x = (経度 + 180) / 360 × 1000
  - y = (90 - 緯度) / 180 × 500
  - 例：東京（北緯35.7°, 東経139.7°） → x≈888, y≈151
- **描画内容**：
  - 六大陸の輪郭（多角形 `<path>` で粗く描画）
  - 三大洋は背景色＋ラベル位置の参考のみ
  - 経線（30°ごと）と緯線（赤道・北回帰線・南回帰線・北極圏・南極圏）を薄いグレーで描画
  - 赤道（緯度0°）と本初子午線（経度0°）はやや濃い線で強調
  - **地名や国名は描画しない**（問題で問うため）
- **スタイル**：CSS変数は使わず、SVG内で `fill` `stroke` を直接指定（テーマ非依存）

### 座標参照テーブル `coords.md`

Claudeが地図問題を作るときに参照する。形式：

```
## 大陸の中心座標（viewBox基準）
- ユーラシア大陸: x=620, y=170
- アフリカ大陸: x=540, y=290
- 北アメリカ大陸: x=250, y=180
- 南アメリカ大陸: x=320, y=340
- オーストラリア大陸: x=820, y=370
- 南極大陸: x=500, y=470

## 海洋の中心座標
- 太平洋: x=130, y=240（東半球側）
- 大西洋: x=460, y=240
- インド洋: x=680, y=330

## 主要国の中心座標
- 日本: x=890, y=170
- 中国: x=750, y=190
- ロシア: x=680, y=110
- アメリカ: x=240, y=190
- ブラジル: x=370, y=320
...
```

## SKILL.md への追記内容

新セクション「## 社会の地図問題の作り方」を追加し、以下を規定：

1. **適用範囲**：社会（`subjects/social-studies.md`）のみ。他教科では使わない
2. **推奨出題数**：地図問題は **2〜4問**（全体10〜20問の1〜3割程度）
3. **手順**：
   - a. `works/midterm-test-generator/maps/world-base.svg` を Read
   - b. `works/midterm-test-generator/maps/coords.md` を Read して座標を取得
   - c. 出題内容に応じてマーカー要素を作る（後述の3パターン）
   - d. ベースSVGの `</svg>` 直前にマーカー要素群を挿入してインライン展開
   - e. 問題ブロックの形式に組み込む
4. **問題ブロック構造**：

```html
<div class="q" data-no="N">
  <div><span class="q-no">問N</span>地図中の①〜③の大陸名を答えなさい。<span class="q-type">地図</span></div>
  <div class="q-body">
    <figure class="q-map">
      <svg viewBox="0 0 1000 500" ...>
        <!-- ベース地図の中身 -->
        <!-- ▼ マーカー注入 -->
        <circle cx="620" cy="170" r="14" class="map-marker"/>
        <text x="620" y="175" class="map-num">1</text>
        ...
      </svg>
    </figure>
  </div>
  <button class="toggle-btn" onclick="toggleAnswer(this)">答えを見る</button>
  <div class="answer"><span class="answer-label">答え:</span> ①ユーラシア ②アフリカ ③北アメリカ</div>
</div>
```

5. **マーカーの3パターン**：

| パターン | 用途 | 構造 |
|---|---|---|
| **番号マーカー** | 大陸・海洋・国の位置を①②③で問う | `<circle r="14">` + `<text>` で番号 |
| **緯度経度ポイント** | 「点Pの緯度経度は？」 | `<circle r="5">` + `<text>P</text>` |
| **強調ハイライト** | 「赤道を示す線はどれか？」 | 既存の線を色付きで上書き |

## テンプレ `test.html.tmpl` への追記

`<style>` 内に以下のCSSを追加（既存スタイルは触らない）：

```css
.q-map {
  margin: 12px 0 6px;
  text-align: center;
}
.q-map svg {
  width: 100%;
  max-width: 600px;
  height: auto;
  border: 1px solid var(--line);
  border-radius: 4px;
  background: #f8fafc;
}
.map-marker {
  fill: #ef4444;
  stroke: #fff;
  stroke-width: 2;
}
.map-num {
  fill: #fff;
  font-weight: bold;
  font-size: 14px;
  text-anchor: middle;
  dominant-baseline: middle;
  font-family: -apple-system, sans-serif;
}
.q-map-point {
  fill: #2563eb;
  stroke: #fff;
  stroke-width: 1.5;
}
@media print {
  .q-map svg { background: #fff; max-width: 100%; }
}
```

## 期待される出題例（3問）

1. **大陸の位置同定**：「地図中の①〜⑥は六大陸を示している。それぞれの名前を答えなさい。」
2. **緯度経度の読み取り**：「地図中の点Pの緯度・経度を答えなさい。」（Pを北緯30° 東経120°あたりに配置）
3. **緯線の同定**：「地図中で強調されている緯線A・Bの名前を答えなさい。」（赤道と北回帰線をハイライト）

## ユーザー確認結果（2026-05-12 確定）

1. **ベース地図の精度感** → **中精度（30〜50頂点）** で確定
   - 六大陸ごとに 30〜50 頂点で多角形描画
   - 日本・イギリス・フィリピン等の主要島国は形が認識できる程度に
2. **マーカーの色** → **提案通り**（番号=#ef4444、点=#2563eb）
3. **地図問題の数** → **提案通り**（2〜4問）
4. **国旗問題** → **テキスト問題で代替**（SVG描画はしない）
5. 既存出力の互換性については未質問だが、運用上「テキストのみが欲しい日は都度伝える」で問題ない想定

## 実装フェーズ（確認後）

1. `works/midterm-test-generator/maps/world-base.svg` を作成
2. `works/midterm-test-generator/maps/coords.md` を作成
3. `works/midterm-test-generator/templates/test.html.tmpl` にCSS追加
4. `.claude/skills/make-test/SKILL.md` に地図セクション追記
5. 動作確認：社会の小テストを1回生成し、ブラウザで地図表示を目視確認
6. `works/make-test-social-map/knowledge.md` にハマりポイントを記録
