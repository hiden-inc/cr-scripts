// Progressive enhancement. Without JS: plain tables (sideways scroll on phones), no TOC, no view switch.
(function () {
  var KEY = 'cr-scripts:view';
  var view = 'table';
  try { if (localStorage.getItem(KEY) === 'cards') view = 'cards'; } catch (e) {}

  function apply(v) {
    view = v;
    try { localStorage.setItem(KEY, v); } catch (e) {}
    document.querySelectorAll('.table-wrap:not(.is-fixed)').forEach(function (w) {
      w.classList.toggle('is-table', v === 'table');
      w.classList.toggle('is-cards', v === 'cards');
    });
    document.querySelectorAll('.view-switch button').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-view') === v));
    });
  }

  document.querySelectorAll('.script table').forEach(function (t) {
    var heads = Array.prototype.map.call(t.querySelectorAll('thead th'), function (th) { return th.textContent.trim(); });
    t.querySelectorAll('tbody tr').forEach(function (tr) {
      Array.prototype.forEach.call(tr.children, function (td, i) {
        td.setAttribute('data-label', heads[i] || '');
        if (i === 0) td.setAttribute('data-role', 'id');
        else if (heads[i] === '開始' || heads[i] === '終了') td.setAttribute('data-role', 'time');
      });
    });
    var fixed = document.body.getAttribute('data-kind') === 'index';
    var sw = document.createElement('div');
    sw.className = 'view-switch'; sw.setAttribute('role', 'group'); sw.setAttribute('aria-label', '表示切替');
    sw.innerHTML = '<button type="button" data-view="table">表</button><button type="button" data-view="cards">カード</button>';
    sw.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (b) apply(b.getAttribute('data-view'));
    });
    var w = document.createElement('div'); w.className = fixed ? 'table-wrap is-fixed is-cards' : 'table-wrap';
    if (!fixed) t.parentNode.insertBefore(sw, t);
    t.parentNode.insertBefore(w, t); w.appendChild(t);
  });
  apply(view);

  // TOC: h1 (parts) / h2 / h3. Placed after the meta paragraph that follows the title.
  var toc = document.querySelector('.toc');
  if (toc) {
    var ol = toc.querySelector('ol');
    document.querySelectorAll('.script h1:not(.title), .script h2, .script h3').forEach(function (h, i) {
      if (!h.id) h.id = 'h' + i;
      var li = document.createElement('li'); var a = document.createElement('a');
      a.href = '#' + h.id; a.textContent = h.textContent; li.appendChild(a);
      li.style.marginLeft = (h.tagName === 'H1' ? 0 : h.tagName === 'H2' ? 1 : 2) + 'em';
      ol.appendChild(li);
    });
    var next = toc.nextElementSibling;
    if (next && next.tagName === 'P') next.parentNode.insertBefore(toc, next.nextSibling);
  }
})();
