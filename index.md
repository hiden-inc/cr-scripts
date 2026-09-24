---
title: 台本一覧
---
[このサイトと台本の作り方 →](guide.md)
{% for k in site.kinds %}{%- assign rows = "" | split: "" %}{%- for p in site.pages %}{%- assign m = site.data.scripts[p.path] %}{%- if m and m.archived != true and m.kind == k[0] %}{%- assign rows = rows | push: p %}{%- endif %}{%- endfor %}{%- if rows.size > 0 %}

## {{ k[1] }}（{{ rows.size }}）
{: .sec .sec-{{ k[0] }}}

| 題名 | 広告主 | 制作者 | 作成日 | 更新日 | 版 | md |
|---|---|---|---|---|---|---|
{%- for p in rows %}{%- assign m = site.data.scripts[p.path] %}{%- assign dir = p.path | split: '/' | first %}{%- assign fam = p.path | replace: '.md', '/' %}{%- assign n = 0 %}{%- for e in site.data.scripts %}{%- if e[0] contains fam and e[1].archived %}{%- assign n = n | plus: 1 %}{%- endif %}{%- endfor %}
| [{{ p.title }}]({{ p.url | relative_url }}) | {{ site.advertisers[dir] | default: dir }} | {{ m.author }} | {{ m.created }} | {{ m.updated }} | v{{ m.version }}{% if n > 0 %} <span class="tag">旧版 {{ n }}</span>{% endif %} | [md]({{ p.path | relative_url }}) |
{%- endfor %}
{%- endif %}{% endfor %}
