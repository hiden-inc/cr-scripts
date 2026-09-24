# cr-scripts

CR台本の置き場。GitHub Pages で公開（ログイン不要・スマホ対応・md保存ボタン付き）。

- 台本を追加する: `<広告主dir>/<日付-検証ID-型>.md` に Markdown を置き（front matter 不要。先頭の `# 見出し` が題名）、`_data/scripts.yml` にメタ情報（kind / author / created / updated / version / note）を1ブロック足して push。
- 版を上げる: 現行 md を `<同名ディレクトリ>/v<旧版番号>.md` にコピー（旧版ページになる）→ 現行 md を編集 → `_data/scripts.yml` に旧版ブロック（archived: true）を追加し、現行の version / updated / note を更新。旧版は各ページの「版 ▾」から開ける。
- 広告主ディレクトリの表示名は `_config.yml` の `advertisers` に1行追加する。
- 公開URL: https://hiden-inc.github.io/cr-scripts/
