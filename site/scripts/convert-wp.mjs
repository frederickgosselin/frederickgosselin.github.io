// One-time migration: WordPress REST snapshot + Polylang map -> Markdown content collections.
// Run from site/: node scripts/convert-wp.mjs
import fs from 'node:fs';
import path from 'node:path';
import TurndownService from 'turndown';
import { gfm } from 'turndown-plugin-gfm';

const ROOT = path.resolve(import.meta.dirname, '..', '..');
const SITE = path.resolve(import.meta.dirname, '..');
const wp = JSON.parse(fs.readFileSync(path.join(ROOT, 'migration', 'wp_content_by_lang.json'), 'utf8'));
const map = JSON.parse(fs.readFileSync(path.join(ROOT, 'migration', 'polylang_map.json'), 'utf8'));
const BACKUP_UPLOADS = path.join(ROOT, 'backup', 'wp-content', 'uploads');

const tagName = Object.fromEntries(wp.tags.map((t) => [t.id, t.name]));
const catName = Object.fromEntries(wp.categories.map((c) => [c.id, c.name]));

// "en" and "fr" lists in the snapshot are identical (the lang filter was ignored): use one and split by the DB map.
const allPosts = wp.en.posts;
const allPages = wp.en.pages;

const td = new TurndownService({ headingStyle: 'atx', bulletListMarker: '-', codeBlockStyle: 'fenced', emDelimiter: '*' });
td.use(gfm);
td.keep(['iframe', 'sub', 'sup']);
td.addRule('wpcaption', {
  filter: (n) => n.nodeName === 'FIGURE' || (n.nodeName === 'DIV' && /wp-caption/.test(n.getAttribute('class') || '')),
  replacement: (content) => `\n\n${content.trim()}\n\n`,
});

const usedUploads = new Set();
const missingUploads = new Set();

function localizeUploads(html) {
  // i0.wp.com/<host>/wp-content/uploads/... and absolute site URLs -> /uploads/...
  return html.replace(
    /(?:https?:)?\/\/(?:i\d\.wp\.com\/)?[^\s"'<>()]*?\/wp-content\/uploads\/([^\s"'<>()?]+?)(?:\?[^\s"'<>()]*)?(?=["'<>\s)])/g,
    (_, rel) => {
      const clean = decodeURIComponent(rel);
      // drop WordPress thumbnail suffix (-300x200) when the original exists
      const orig = clean.replace(/-\d+x\d+(\.[a-z0-9]+)$/i, '$1');
      const pick = fs.existsSync(path.join(BACKUP_UPLOADS, orig)) ? orig : clean;
      if (fs.existsSync(path.join(BACKUP_UPLOADS, pick))) usedUploads.add(pick);
      else missingUploads.add(pick);
      return '/uploads/' + pick.split('/').map(encodeURIComponent).join('/');
    },
  );
}

function slugify(s) {
  return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/&[a-z]+;/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 70);
}
const decode = (s) => s.replace(/&#8217;|&rsquo;/g, '’').replace(/&#8220;|&#8221;/g, '"').replace(/&amp;/g, '&').replace(/&#038;/g, '&').replace(/&nbsp;/g, ' ').replace(/&#8211;/g, '–').replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n));
const q = (s) => JSON.stringify(s);

function toMd(html) {
  let md = td.turndown(localizeUploads(html));
  md = md.replace(/ /g, ' ').replace(/\n{3,}/g, '\n\n').trim();
  return md + '\n';
}

// translation partner id per item
const partner = {};
for (const g of map.pairs) {
  if (g.en && g.fr) { partner[g.en] = g.fr; partner[g.fr] = g.en; }
}

function write(file, front, body) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `---\n${front}---\n\n${body}`, 'utf8');
}

const slugById = {};
const out = { posts: 0, pages: 0 };

// ---- posts -> news
for (const p of allPosts) {
  const lang = map.post_lang[String(p.id)];
  if (!lang) throw new Error('no language for post ' + p.id);
  const title = decode(p.title.rendered);
  const date = p.date.slice(0, 10);
  const slug = `${date}-${slugify(title) || p.id}`;
  slugById[p.id] = slug;
  p._lang = lang; p._slug = slug;
}
for (const p of allPosts) {
  const tags = (p.tags || []).map((t) => tagName[t]).filter(Boolean);
  const cats = (p.categories || []).map((c) => catName[c]).filter(Boolean).filter((c) => c !== 'Uncategorized' && c !== 'Non classé');
  const tr = partner[p.id] ? slugById[partner[p.id]] : null;
  let front = `title: ${q(decode(p.title.rendered))}\ndate: ${p.date.slice(0, 10)}\nwpId: ${p.id}\n`;
  if (tags.length) front += `tags: ${JSON.stringify(tags)}\n`;
  if (cats.length) front += `categories: ${JSON.stringify(cats)}\n`;
  if (tr) front += `translation: ${q(tr)}\n`;
  write(path.join(SITE, 'src', 'content', 'news', p._lang, p._slug + '.md'), front, toMd(p.content.rendered));
  out.posts++;
}

// ---- pages
const pageSlug = { 143: 'about', 187: 'a-propos', 232: 'research-opportunities', 239: 'opportunites-de-recherche', 121: 'teaching', 18: 'enseignement', 127: 'videos', 124: 'videos', 134: 'publications', 132: 'publications' };
for (const p of allPages) {
  const lang = map.post_lang[String(p.id)];
  const slug = pageSlug[p.id];
  if (!lang || !slug) throw new Error('page not mapped ' + p.id);
  const front = `title: ${q(decode(p.title.rendered))}\nwpId: ${p.id}\nmodified: ${p.modified.slice(0, 10)}\norder: ${p.menu_order ?? 0}\n`;
  write(path.join(SITE, 'src', 'content', 'pages', lang, slug + '.md'), front, toMd(p.content.rendered));
  out.pages++;
}

// ---- copy referenced uploads
let copied = 0, bytes = 0;
for (const rel of usedUploads) {
  const src = path.join(BACKUP_UPLOADS, rel);
  const dst = path.join(SITE, 'public', 'uploads', rel);
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  fs.copyFileSync(src, dst);
  copied++; bytes += fs.statSync(src).size;
}
console.log(out, 'uploads copied:', copied, (bytes / 1e6).toFixed(1) + ' MB');
console.log('missing uploads:', [...missingUploads]);
