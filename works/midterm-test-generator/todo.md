# todo.md — 中間考査対策テスト生成スキル

最終更新: 2026-05-12

## 現在地

**Phase 1 完了。Phase 2 待ち（試験範囲情報の入力待ち）。**

## Phase 1: 雛形作成 [完了]

- [x] `works/midterm-test-generator/plan.md` 作成
- [x] `works/midterm-test-generator/spec.md` 作成
- [x] `subjects/english.md` 作成（空テンプレ）
- [x] `subjects/math.md` 作成（空テンプレ）
- [x] `subjects/science.md` 作成（空テンプレ）
- [x] `subjects/social-studies.md` 作成（空テンプレ）
- [x] `works/midterm-test-generator/templates/test.html.tmpl` 作成
- [x] `.claude/skills/make-test/SKILL.md` 作成（プロジェクトスコープ）
- [x] `docs/<教科>/` 出力先ディレクトリ作成

## Phase 2: 範囲情報入力 → 試運転 [次にここ]

- [x] `subjects/english.md` に教科書情報・範囲・重要単語/文法を記入（Sunshine 1 令和7年度版 / p.12-15 / 試験日2026-05-18 / 推定範囲: Get Ready 3-4）
  - [ ] ユーザーが実物教科書で p.12-15 の単元名・内容を最終確認
- [ ] `subjects/math.md` に同上を記入
- [ ] `subjects/science.md` に同上を記入（理科を実施する場合）
- [ ] `subjects/social-studies.md` に同上を記入（社会を実施する場合）
- [ ] 1教科で `/make-test` 相当（「〇〇のテスト作って」）を実行して動作確認
- [ ] 生成HTMLをブラウザで開いて UX を確認（トグル動作、印刷プレビュー）
- [ ] 必要なら `test.html.tmpl` を調整（フォントサイズ、配色、余白など）

## Phase 3: GitHub Pages 公開 [Phase 2 完了後]

- [ ] `git init`
- [ ] `.gitignore` の見直し（`docs/` は公開対象なのでコミット対象）
- [ ] GitHub リポジトリ作成（`gh repo create`）
- [ ] 初回 push
- [ ] GitHub Pages を `docs/` ルートで有効化
- [ ] `docs/index.html` の教科一覧トップを作成（生成済みテストへのリンク集）

## 未解決の質問・課題

- (none)

## 補足

- スキルは `.claude/skills/make-test/` に置いてあるので、このリポジトリ内でのみ有効。他リポジトリで使いたくなったらコピー or ユーザースコープへ移動
- 問題のバラつきは Claude のランダム性に依存。同じ範囲データから何度でも違うテストが出る前提
