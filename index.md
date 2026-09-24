---
title: 台本一覧
---
{% for p in site.pages %}{% if p.path != page.path and p.path contains '.md' %}{% assign dir = p.path | split: '/' | first %}
- [{{ p.title }}]({{ p.url | relative_url }}) — {{ site.advertisers[dir] | default: dir }} ／ [md]({{ p.path | relative_url }})
{% endif %}{% endfor %}
