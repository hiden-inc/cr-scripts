#!/usr/bin/env python3
"""台本 md を cr-scripts に公開する（標準ライブラリのみ）。

  python3 publish.py <md> --dir hackz --author "yusaku arai" [--note "変更点"] [--kind script|plan] [--slug 2026-10-a1-gyakusetsu] [--dry-run] [--no-push]

- 新規: <dir>/<slug>.md を作り _data/scripts.yml に version 1 のブロックを足す。
- 更新（同じ slug が既にある）: 現行を <dir>/<slug>/v<N>.md に退避（旧版ページ）→ 置換 → version+1・updated・note を更新。
- push 後は GitHub Pages のビルド完了と URL の 200 を待って URL を表示する。
"""
import argparse, datetime, json, os, re, shutil, subprocess, sys, time, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "_data", "scripts.yml")
SITE = "https://hiden-inc.github.io/cr-scripts/"
REPO = "hiden-inc/cr-scripts"

def load_data():
    """scripts.yml → [(path, {k: v})] 宣言順。値は文字列（引用符は外す）。"""
    entries, cur = [], None
    if not os.path.exists(DATA):
        return entries
    for line in open(DATA, encoding="utf-8"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" ") and line.rstrip().endswith(":"):
            cur = (line.rstrip()[:-1], {}); entries.append(cur)
        elif cur and ":" in line:
            k, v = line.strip().split(":", 1)
            cur[1][k.strip()] = v.strip().strip('"')
    return entries

def dump_data(entries):
    out = ["# ページのメタ情報。キー = md のパス。新しい版ほど上に書く。",
           "# kind: script | plan / archived: true = 旧版（一覧に出ない） / note: その版の変更点"]
    for path, m in entries:
        out.append(f"{path}:")
        for k in ("kind", "archived", "author", "created", "updated", "version", "note"):
            if k in m:
                v = m[k]
                out.append(f'  {k}: "{v}"' if k in ("created", "updated") else f"  {k}: {v}")
    open(DATA, "w", encoding="utf-8").write("\n".join(out) + "\n")

def sh(*cmd, check=True):
    return subprocess.run(cmd, cwd=ROOT, check=check, capture_output=True, text=True).stdout.strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md"); ap.add_argument("--dir", required=True, help="広告主ディレクトリ（例: hackz）")
    ap.add_argument("--author", required=True); ap.add_argument("--note", default="")
    ap.add_argument("--kind", default="script", choices=["script", "plan"])
    ap.add_argument("--slug", help="省略時は md のファイル名（拡張子なし）")
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()

    body = open(a.md, encoding="utf-8").read()
    if body.startswith("---"):
        sys.exit("NG: md に front matter（先頭の ---）があります。外してください（元 md が配信されなくなる）")
    if not body.lstrip().startswith("# "):
        sys.exit("NG: md の先頭は '# 題名' にしてください（ページ題名になる）")
    slug = a.slug or re.sub(r"[^\w\-]+", "-", os.path.splitext(os.path.basename(a.md))[0]).strip("-").lower()
    rel = f"{a.dir}/{slug}.md"; target = os.path.join(ROOT, rel)
    today = datetime.date.today().isoformat()
    entries = load_data(); idx = {p: i for i, (p, _) in enumerate(entries)}
    plan = []

    if rel in idx:
        cur = entries[idx[rel]][1]; n = int(cur.get("version", "1"))
        old_rel = f"{a.dir}/{slug}/v{n}.md"
        plan.append(f"退避: {rel} → {old_rel}（旧版ページ v{n}）")
        plan.append(f"更新: {rel} を新しい内容に置換、version {n}→{n+1}、updated {today}、note '{a.note}'")
        if not a.dry_run:
            os.makedirs(os.path.dirname(os.path.join(ROOT, old_rel)), exist_ok=True)
            shutil.copyfile(target, os.path.join(ROOT, old_rel))
            old = dict(cur); old["archived"] = "true"
            entries.insert(idx[rel] + 1, (old_rel, old))
            cur.update({"version": str(n + 1), "updated": today, "note": a.note or cur.get("note", ""), "author": a.author})
    else:
        plan.append(f"新規: {rel}（version 1、created {today}、author {a.author}、kind {a.kind}）")
        if not a.dry_run:
            entries.insert(0, (rel, {"kind": a.kind, "author": a.author, "created": today, "updated": today, "version": "1", "note": a.note or "初版"}))
    url = f"{SITE}{a.dir}/{slug}/"
    print("\n".join(plan)); print("URL:", url)
    if a.dry_run:
        return
    os.makedirs(os.path.dirname(target), exist_ok=True)
    open(target, "w", encoding="utf-8").write(body if body.endswith("\n") else body + "\n")
    dump_data(entries)
    sh("git", "add", "-A")
    title = body.lstrip()[2:].split("\n", 1)[0].strip()
    sh("git", "commit", "-q", "-m", f"publish: {title}" + (f" — {a.note}" if a.note else ""))
    if a.no_push:
        print("commit のみ（--no-push）"); return
    sh("git", "push", "-q", "origin", "main"); sha = sh("git", "rev-parse", "HEAD")
    for _ in range(60):  # ビルド完了待ち（最大約8分）
        try:
            b = json.loads(sh("gh", "api", f"repos/{REPO}/pages/builds/latest"))
            if b.get("status") == "built" and b.get("commit") == sha: break
            if b.get("status") == "errored": sys.exit("NG: Pages ビルド失敗: " + str(b.get("error")))
        except subprocess.CalledProcessError: pass
        time.sleep(8)
    for _ in range(30):  # CDN 反映待ち
        try:
            if urllib.request.urlopen(f"{url}?t={time.time()}").status == 200: break
        except Exception: pass
        time.sleep(6)
    print("公開完了:", url)

if __name__ == "__main__":
    main()
