#!/usr/bin/env python3
"""docs/index.html を docs/<教科>/*.html から再生成する。

make-test スキルがテスト生成後に呼び出して、GitHub Pages のトップページを
最新の生成物リストに同期させる。冪等なので何度呼んでも安全。
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "index.html"

SUBJECTS: list[tuple[str, str, str]] = [
    ("english", "英語", "var(--english)"),
    ("math", "数学", "var(--math)"),
    ("science", "理科", "var(--science)"),
    ("social-studies", "社会", "var(--social)"),
]

TITLE_RE = re.compile(r"<title>([^<]*)</title>", re.IGNORECASE)


def extract_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = TITLE_RE.search(text)
    return m.group(1).strip() if m else path.name


def render_section(slug: str, label: str, color: str) -> str:
    dir_ = DOCS / slug
    files = sorted(dir_.glob("*.html")) if dir_.exists() else []
    lines = [f'<section class="subject" style="--subject-color: {color};">']
    lines.append(f"  <h2>{label}</h2>")
    if not files:
        lines.append('  <p class="empty">まだ作成されていません。</p>')
    else:
        lines.append("  <ul>")
        for f in files:
            title = html.escape(extract_title(f))
            tag = '<span class="tag">DEMO</span>' if "demo" in f.stem.lower() else ""
            href = f"{slug}/{f.name}"
            lines.append(f'    <li><a href="{href}">{title}</a>{tag}</li>')
        lines.append("  </ul>")
    lines.append("</section>")
    return "\n".join(lines)


HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>中間考査対策 — 小テスト一覧</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root {
    --accent: #2563eb;
    --accent-soft: #dbeafe;
    --text: #0f172a;
    --muted: #64748b;
    --line: #e2e8f0;
    --bg: #ffffff;
    --card: #f8fafc;
    --english: #0ea5e9;
    --math: #2563eb;
    --science: #16a34a;
    --social: #d97706;
  }
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Yu Gothic", sans-serif;
    color: var(--text);
    background: var(--bg);
    line-height: 1.7;
    max-width: 800px;
    margin: 0 auto;
    padding: 24px 20px 80px;
    font-size: 17px;
  }
  header {
    border-bottom: 2px solid var(--accent);
    padding-bottom: 16px;
    margin-bottom: 28px;
  }
  h1 { font-size: 24px; margin: 0 0 6px; }
  .lead { color: var(--muted); font-size: 14px; margin: 0; }
  .subject {
    background: var(--card);
    border: 1px solid var(--line);
    border-left: 6px solid var(--subject-color, var(--accent));
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 18px;
  }
  .subject h2 {
    font-size: 18px;
    margin: 0 0 10px;
    color: var(--subject-color, var(--accent));
  }
  .subject ul {
    margin: 0;
    padding-left: 20px;
  }
  .subject li { margin: 4px 0; }
  .subject a {
    color: var(--accent);
    text-decoration: none;
  }
  .subject a:hover { text-decoration: underline; }
  .empty { color: var(--muted); font-size: 14px; margin: 0; }
  .tag {
    display: inline-block;
    font-size: 11px;
    background: var(--accent-soft);
    color: var(--accent);
    padding: 1px 6px;
    border-radius: 4px;
    margin-left: 6px;
    vertical-align: middle;
  }
  footer {
    margin-top: 40px;
    color: var(--muted);
    font-size: 12px;
    text-align: center;
  }
</style>
</head>
<body>

<header>
  <h1>中間考査対策 — 小テスト一覧</h1>
  <p class="lead">教科ごとに生成された小テストをまとめています。</p>
</header>
"""

FOOT = """
<footer>
  midterm_exam_preparation
</footer>

</body>
</html>
"""


def build() -> str:
    sections = "\n\n".join(render_section(*s) for s in SUBJECTS)
    return HEAD + "\n" + sections + FOOT


def main() -> None:
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
