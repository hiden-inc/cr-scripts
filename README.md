# cr-scripts

CR台本の置き場。GitHub Pages で公開（ログイン不要・スマホ対応・md保存ボタン付き）。

- 台本を公開する（新規も版上げも同じ1コマンド。Notion は使わない）:

  ```bash
  python3 ~/cr-scripts/publish.py <台本.md> --dir hackz --author "yusaku arai" --note "変更点ひとこと"
  ```

  - md は Arai さんフォーマット（先頭 `# 題名`、企画／台本 概要／カット別表／絵コンテ／ナレーション／テロップ／BGM／素材）。front matter は入れない。
  - 同じ slug（ファイル名）が既にあれば版上げ: 現行を `v<N>.md` に退避（旧版ページ）→ 置換 → version+1。各ページの「版 ▾」から旧版へ飛べる。
  - `--dry-run` で何が起きるかだけ表示。公開後は URL が表示される（ビルド約1分）。
- 広告主ディレクトリの表示名は `_config.yml` の `advertisers` に1行追加する。
- 公開URL: https://hiden-inc.github.io/cr-scripts/
