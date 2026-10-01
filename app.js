const projects = [{
  name: 'CampusTrack',
  image: 'assets/campustrack.png',
  category: 'Full-stack application',
  description: 'A focused internship tracker with accounts, a saved application board, deadlines, and CSV export.',
  tags: ['PYTHON', 'FASTAPI', 'SQLALCHEMY', 'JAVASCRIPT'],
  features: ['Username/password accounts with salted password hashes and expiring server sessions.', 'Owner-scoped database queries and CSRF-protected record changes.', 'Search, stage filtering, deadline counts, edit/delete flows, and CSV export.', 'SQLite for local development; PostgreSQL configuration for deployment.'],
  learning: 'The next learning goal is to trace one request from the browser through authentication to a database query.'
}, {
  name: 'NoteLens',
  image: 'assets/notelens.png',
  category: 'Applied machine learning',
  description: 'A study-note search engine that compares keyword retrieval with a learned latent representation, and cites each passage.',
  tags: ['PYTHON', 'SCIKIT-LEARN', 'TF-IDF', 'LSA'],
  features: ['Upload original text, Markdown, or a small text-based PDF.', 'TF-IDF baseline, truncated SVD representation, and hybrid ranking.', 'Source filenames, pages, passage numbers, and transparent similarity scores.', 'A reproducible small retrieval benchmark and explicit out-of-vocabulary handling.'],
  learning: 'The next learning goal is to explain why a retrieval score is not the same thing as factual confidence.'
}, {
  name: 'RepoCheck',
  image: 'assets/repocheck.png',
  category: 'Developer tool + API',
  description: 'A read-only repository checker that flags missing essentials and risky patterns, with redacted reports and practical fixes.',
  tags: ['PYTHON', 'FASTAPI', 'CLI', 'SECURITY'],
  features: ['Shared scanner rules power the command-line interface and HTTP API.', 'Bounded ZIP inspection without extracting or executing files.', 'Rule identifiers, severity filters, line locations, and JSON export.', 'Matched source values are excluded from reports; findings require human review.'],
  learning: 'The next learning goal is to explain false positives and how bounded input processing reduces risk.'
}, {
  name: 'This portfolio',
  image: 'assets/portfolio.png',
  category: 'Responsive web design',
  description: 'A lightweight home for the projects: semantic HTML, responsive CSS, keyboard-accessible details, and honest project status.',
  tags: ['HTML', 'CSS', 'JAVASCRIPT', 'ACCESSIBILITY'],
  features: ['Semantic landmarks, keyboard navigation, accessible dialog controls, and responsive layouts.', 'Original CSS illustration and self-hosted project screenshots.', 'No tracking scripts, external font dependencies, or framework build step.', 'Project links are enabled only once the corresponding URLs are verified.'],
  learning: 'The next learning goal is to explain the browser rendering process and how layout changes at different widths.'
}];
// Publication URLs remain null until confirmed live. Never invent demo links.
const published = {
  campustrack: null,
  notelens: null,
  repocheck: null,
  portfolio: null
};

function el(tag, attrs = {}, ...children) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k.startsWith('on')) n.addEventListener(k.slice(2), v);
    else n.setAttribute(k, v);
  }
  children.flat().forEach(c => n.append(c instanceof Node ? c : document.createTextNode(String(c))));
  return n;
}

function details(p) {
  const box = document.querySelector('#project-details');
  box.replaceChildren(el('div', {
    class: 'eyebrow'
  }, p.category.toUpperCase()), el('h2', {}, p.name), el('p', {}, p.description), el('ul', {}, ...p.features.map(f => el('li', {}, f))), el('p', {}, p.learning));
  document.querySelector('#project-dialog').showModal();
}
document.querySelector('#projects').replaceChildren(...projects.map((p, i) => el('article', {
  class: 'project'
}, el('div', {
  class: 'project-image'
}, el('img', {
  src: p.image,
  alt: p.name + ' application screenshot',
  loading: 'lazy',
  width: '1280',
  height: '860'
})), el('div', {
  class: 'project-meta'
}, el('h3', {}, p.name), el('span', {
  class: 'project-number'
}, '0' + (i + 1) + ' / ' + p.category)), el('p', {}, p.description), el('div', {
  class: 'tags'
}, ...p.tags.map(t => el('span', {
  class: 'tag'
}, t))), el('div', {
  class: 'project-links'
}, el('button', {
  onclick: () => details(p)
}, 'Explore the project ↗'), el('a', { class: 'text-link', href: 'https://github.com/me-vishnurnair/' + Object.keys(published)[i] }, 'View code ↗'), published[Object.keys(published)[i]] ? el('a', {
  class: 'text-link',
  href: published[Object.keys(published)[i]]
}, 'Live demo ↗') : el('span', {
  class: 'pending'
}, 'Public demo awaiting publication')))));
document.querySelector('#close-dialog').onclick = () => document.querySelector('#project-dialog').close();
