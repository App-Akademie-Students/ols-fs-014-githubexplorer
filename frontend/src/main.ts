import './styles.css';

interface ProjectFileScan {
  files: { path: string; content: string }[];
  incomplete: boolean;
}

interface DocumentationAnalysis {
  summary: string;
  topics: string[];
  evidence_paths: string[];
}

interface RepositoryTree {
  entries: { path: string; type: 'blob' | 'tree' | 'commit' }[];
  truncated: boolean;
}

interface RepositoryPreviewResponse {
  url: string;
  owner: string;
  repo: string;
  description: string | null;
  languages: Record<string, number>;
  readme: string | null;
  project_files: ProjectFileScan;
  documentation: DocumentationAnalysis | null;
  repository_tree?: RepositoryTree | null;
}

interface TreeNode {
  folder: boolean;
  children: Map<string, TreeNode>;
}

const form = document.querySelector<HTMLFormElement>('form')!;
const input = document.querySelector<HTMLInputElement>('#url')!;
const button = form.querySelector<HTMLButtonElement>('button')!;
const status = document.querySelector<HTMLElement>('#status')!;
const error = document.querySelector<HTMLElement>('#error')!;
const result = document.querySelector<HTMLElement>('#result')!;
const formatter = new Intl.NumberFormat('de-DE');
let loading = false;

function element<K extends keyof HTMLElementTagNameMap>(tag: K, text?: string) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  return node;
}

function section(title: string) {
  const node = element('section');
  node.append(element('h2', title));
  return node;
}

function list(items: string[], className = '') {
  const node = element('ul');
  node.className = className;
  for (const item of items) node.append(element('li', item));
  return node;
}

function renderTree(children: Map<string, TreeNode>): HTMLUListElement {
  const items = element('ul');
  for (const [name, node] of [...children].sort(([a, x], [b, y]) =>
    Number(y.folder) - Number(x.folder) || a.localeCompare(b, 'de')
  )) {
    const item = element('li');
    if (node.folder) {
      const details = element('details');
      details.append(element('summary', name + '/'));
      if (node.children.size) details.append(renderTree(node.children));
      item.append(details);
    } else {
      item.append(element('span', name));
    }
    items.append(item);
  }
  return items;
}

function render(preview: RepositoryPreviewResponse) {
  const overview = section(preview.repo);
  const metadata = element('dl');
  for (const [label, value] of [
    ['Owner', preview.owner],
    ['Beschreibung', preview.description || 'Keine Beschreibung verfügbar'],
  ]) {
    metadata.append(element('dt', label), element('dd', value));
  }
  const link = element('a', 'Auf GitHub öffnen');
  const url = new URL(preview.url);
  if (url.origin === 'https://github.com') link.href = url.href;
  overview.append(metadata, link, element('h3', 'Sprachen'));
  const languages = Object.entries(preview.languages)
    .sort(([, a], [, b]) => b - a)
    .map(([name, bytes]) => `${name} · ${formatter.format(bytes)} Bytes`);
  overview.append(languages.length ? list(languages, 'tags') : element('p', 'Keine Sprachdaten verfügbar'));

  const analysis = section('Dokumentationsanalyse');
  const documentation = preview.documentation;
  if (documentation) {
    analysis.append(element('p', documentation.summary), element('h3', 'Themen'));
    analysis.append(documentation.topics.length ? list(documentation.topics, 'tags') : element('p', 'Keine Themen verfügbar'));
    analysis.append(element('h3', 'Belegpfade'));
    analysis.append(documentation.evidence_paths.length ? list(documentation.evidence_paths, 'paths') : element('p', 'Keine Belegpfade verfügbar'));
  } else {
    analysis.append(element('p', 'Keine Analyse verfügbar'));
  }

  const tree = section('Dateibaum');
  tree.className = 'tree';
  if (preview.repository_tree) {
    const children = new Map<string, TreeNode>();
    if (preview.repository_tree.truncated) {
      const note = element('p', 'GitHub hat nur einen Teilbaum geliefert.');
      note.className = 'notice';
      tree.append(note);
    }
    for (const entry of preview.repository_tree.entries) {
      const parts = entry.path.split('/');
      let siblings = children;
      for (const [index, name] of parts.entries()) {
        const folder = index < parts.length - 1 || entry.type === 'tree';
        const node = siblings.get(name) ?? { folder, children: new Map<string, TreeNode>() };
        node.folder ||= folder;
        siblings.set(name, node);
        siblings = node.children;
      }
    }
    tree.append(children.size ? renderTree(children) : element('p', 'Das Repository enthält keine Einträge.'));
  } else {
    tree.append(element('p', 'Dateibaum nicht verfügbar'));
  }

  result.replaceChildren(overview, analysis, tree);
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (loading) return;

  loading = true;
  button.disabled = true;
  input.readOnly = true;
  result.setAttribute('aria-busy', 'true');
  result.replaceChildren();
  error.hidden = true;
  status.textContent = 'Repository wird analysiert …';

  try {
    const response = await fetch('/api/repositories/preview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: input.value.trim() }),
    });

    if (!response.ok) {
      const body = await response.json().catch(() => null);
      error.textContent = typeof body?.detail === 'string'
        ? body.detail
        : `Die Analyse ist fehlgeschlagen (HTTP ${response.status}).`;
      error.hidden = false;
      return;
    }

    const preview: RepositoryPreviewResponse = await response.json();
    render(preview);
    status.textContent = 'Analyse abgeschlossen.';
  } catch {
    error.textContent = 'Die Vorschau konnte nicht geladen werden. Prüfe, ob das Backend läuft, und versuche es erneut.';
    error.hidden = false;
  } finally {
    loading = false;
    button.disabled = false;
    input.readOnly = false;
    result.setAttribute('aria-busy', 'false');
    if (!error.hidden) status.textContent = '';
  }
});
