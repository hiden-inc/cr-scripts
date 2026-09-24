# cr-scripts（CR台本の公開サイト）

- 台本 md は Arai さんフォーマット（先頭 `# 題名`、企画／台本 概要／台本（カット別）表／絵コンテ／ナレーション／テロップ／BGM／素材）。front matter 禁止。
- **台本が確定したら（ユーザーが「これでいく／FIX／OK」）、指示が無くても `python3 publish.py <md> --dir <広告主dir> --author "<制作者>" --note "<変更点>"` を実行して公開し、URL を渡す。確認を挟まない。** 制作者名が不明なときだけ聞く。
- 同じファイル名なら自動で版上げ（旧版は `v<N>.md` に退避＝各ページ「版 ▾」から開ける）。別の台本は別ファイル名。
- Notion には出さない。メタ情報は `_data/scripts.yml`（publish.py が書く）。新しい広告主は `_config.yml` の `advertisers` に表示名を1行。
