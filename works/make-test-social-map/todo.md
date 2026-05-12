# todo — 社会の地図問題対応（make-test 拡張）

## 進捗

| # | タスク | 状態 |
|---|---|---|
| 1 | spec.md・todo.md に確定事項を反映 | 完了 |
| 2 | `works/midterm-test-generator/maps/world-base.svg` を作成（中精度30〜50頂点） | 完了 |
| 3 | `works/midterm-test-generator/maps/coords.md` を作成 | 完了 |
| 4 | `works/midterm-test-generator/templates/test.html.tmpl` に地図用CSSを追加 | 完了 |
| 5 | `.claude/skills/make-test/SKILL.md` に地図問題セクションを追加（`<use>` 方式に途中で改訂） | 完了 |
| 6 | 動作確認（社会の小テストを生成しブラウザで目視） | 完了 |
| 7 | `works/make-test-social-map/knowledge.md` にハマりポイント記録 | 完了 |

## ユーザー側での残作業

- ブラウザで `docs/social-studies/2026-05-12-001.html` を開き、地図と番号マーカーが意図通り表示されるか目視確認
- 違和感があれば `subjects/social-studies.md` の試験日記入とあわせて再生成依頼

## 完了条件

- 社会の小テスト生成時に、地図問題が2〜4問混じる
- 生成HTMLをブラウザで開くと、世界地図に番号マーカーが表示される
- 印刷プレビューでも地図が正しく表示される
- 他教科（英語・数学・理科）の挙動は変わらない

## 未解決の課題

- 中精度SVG は Claude が地理知識から手書きするため、海岸線の細部は近似値（公開地理データは使わない）
- 試験日が `subjects/social-studies.md` で未記入（今回のスコープ外、後日埋める）
