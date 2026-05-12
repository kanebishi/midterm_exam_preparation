# 中間考査対策

中学校の中間考査に向けて、教科ごとの小テストHTMLを Claude Code で生成・蓄積するためのリポジトリ。

公開ページ： **https://kanebishi.github.io/midterm_exam_preparation/**

（GitHub Pages の Source は `main` ブランチの `/docs` ディレクトリ。`docs/index.html` がトップページ）

## ディレクトリ構成

| ディレクトリ / ファイル | 役割 |
|---|---|
| `subjects/<教科>.md` | 教科ごとの試験範囲メモ（`make-test` スキルの唯一のデータソース） |
| `docs/index.html` | 小テスト一覧のトップページ（`scripts/build-index.py` で自動生成） |
| `docs/<教科>/` | 生成された小テストHTML（`YYYY-MM-DD-<連番>.html` 形式） |
| `scripts/build-index.py` | `docs/<教科>/*.html` を走査して `docs/index.html` を再生成する冪等スクリプト |
| `.claude/skills/make-test/` | 小テスト生成用のプロジェクトスキル |
| `works/<ワーク名>/` | 進行中の作業に関する plan / spec / todo / knowledge |

対応教科：英語 / 数学 / 理科 / 社会

教科ごとの出題傾向：

| 教科 | 主な出題形式 | 図入り問題 |
|---|---|---|
| 英語 | 穴埋め / 一問一答 / 選択 / 正誤 | なし |
| 数学 | 計算 / 大小比較 / 用語 | なし |
| 理科 | 用語 / 図中の名称 / 正誤 | **植物模式図**（花の断面・葉脈・根・シダ・コケ等）を 3〜6 問 |
| 社会 | 地名・用語 / 年号 / 地図 | **世界地図**（大陸・緯度経度等）を 2〜4 問 |

図入り問題は外部画像参照なしのインライン SVG で生成されるため、`docs/<教科>/*.html` を単体で配布・印刷できる。

## 小テストの作り方

Claude Code 上で以下のように依頼すると、`make-test` スキルが起動して該当教科のHTMLを `docs/<教科>/` に出力し、続けて `scripts/build-index.py` を走らせて `docs/index.html` を更新する。

```
英語のテスト作って
数学の問題作って
理科の小テスト
社会のテスト作って
```

試験範囲は `subjects/<教科>.md` の内容に従う。範囲を変えたいときはこのファイルを編集する。スキルの詳細仕様（マーカー配置・図問題の作り方など）は `.claude/skills/make-test/SKILL.md` を参照。

## トップページの再生成（手動実行）

ファイルを手で追加・削除した後など、index を作り直したいときは：

```sh
python3 scripts/build-index.py
```

冪等なスクリプトなので何度実行しても安全。

## 関連ドキュメント

- `AGENTS.md` … Claude Code 向けの運用ルール（ワークフロー・情報永続化ルールなど）
