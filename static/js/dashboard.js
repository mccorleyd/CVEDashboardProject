(() => {
  // --- Mobile menu toggle -------------------------------------------------
  const menu = document.querySelector('#menu');
  const links = document.querySelector('#links');

  if (menu && links) {
    menu.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      menu.setAttribute('aria-expanded', String(open));
    });
  }

  // --- CVE explorer filtering ---------------------------------------------
  // The server embeds the normalised CVE list as JSON inside a <script>
  // tag with type="application/json". Reading it here means the browser
  // never has to make a second request for data it already received.
  const source = document.querySelector('#cve-data');
  if (!source) return;

  const cves = JSON.parse(source.textContent);
  const results = document.querySelector('#cve-results');
  const count = document.querySelector('#result-count');

  // Always render CVE descriptions as plain text, never as HTML. An API
  // description is untrusted external data; textContent guarantees the
  // browser cannot interpret it as markup.
  const safeText = (value) => document.createTextNode(value ?? 'Not supplied');

  function render() {
    const search = document.querySelector('#search').value.toLowerCase();
    const severity = document.querySelector('#severity').value;
    const minimum = Number(document.querySelector('#min-score').value || 0);
    const kev = document.querySelector('#kev-only').checked;
    const sort = document.querySelector('#sort').value;

    let matches = cves.filter((c) =>
      `${c.id} ${c.description}`.toLowerCase().includes(search)
      && (!severity || c.severity === severity)
      && (c.score ?? -1) >= minimum
      && (!kev || c.known_exploited)
    );

    matches.sort((a, b) =>
      sort === 'score'
        ? (b.score ?? -1) - (a.score ?? -1)
        : String(b.published).localeCompare(String(a.published))
    );

    results.replaceChildren();
    count.textContent = `${matches.length} vulnerability result(s).`;

    if (!matches.length) {
      results.textContent = 'No results match these filters. Try Clear filters.';
      return;
    }

    matches.forEach((c) => {
      const article = document.createElement('article');
      const h = document.createElement('h2');
      const a = document.createElement('a');
      const p = document.createElement('p');
      const meta = document.createElement('p');

      article.className = 'cve';
      a.href = `/cves/${encodeURIComponent(c.id)}`;
      a.textContent = c.id;
      h.append(a);
      p.append(safeText(c.description));
      meta.textContent = `${c.severity} · CVSS: ${c.score ?? 'Not scored'}${c.known_exploited ? ' · Known Exploited' : ''}`;

      article.append(h, p, meta);
      results.append(article);
    });
  }

  document.querySelector('#filters').addEventListener('input', render);
  document.querySelector('#filters').addEventListener('reset', () => setTimeout(render));
  render();
})();
