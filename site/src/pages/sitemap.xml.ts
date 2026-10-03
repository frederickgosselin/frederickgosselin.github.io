// sitemap.xml with EN/FR alternates (hreflang). Built from the same data as the pages, so it never drifts.
// The standard @astrojs/sitemap i18n pairing assumes identical paths in both languages; ours differ
// (/en/about/ vs /fr/a-propos/, news slugs), so the pairs come from PAGES and the `translation` front matter.
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { PAGES } from '../i18n';

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const day = (d?: Date) => (d ? d.toISOString().slice(0, 10) : undefined);

interface Item { path: string; lastmod?: string; alt?: { lang: string; path: string }[]; }

export const GET: APIRoute = async ({ site }) => {
  const base = (site ?? new URL('https://www.fgosselin.com')).origin;
  const news = await getCollection('news');
  const pages = await getCollection('pages');
  const newest = news.map((n) => n.data.date).sort((a, b) => b.getTime() - a.getTime())[0];

  const items: Item[] = [];
  const pair = (en: string, fr: string, lastmod?: string) => {
    const alt = [{ lang: 'en', path: en }, { lang: 'fr', path: fr }];
    items.push({ path: en, lastmod, alt }, { path: fr, lastmod, alt });
  };

  pair('/en/', '/fr/', day(newest));
  pair('/en/news/', '/fr/news/', day(newest));

  for (const p of PAGES) {
    const e = pages.find((x) => x.id === `en/${p.en}`);
    const f = pages.find((x) => x.id === `fr/${p.fr}`);
    const lm = day([e?.data.modified, f?.data.modified].filter(Boolean).sort((a, b) => b!.getTime() - a!.getTime())[0] as Date | undefined);
    pair(`/en/${p.en}/`, `/fr/${p.fr}/`, lm);
  }

  for (const n of news) {
    const [lang, ...rest] = n.id.split('/');
    const path = `/${lang}/news/${rest.join('/')}/`;
    const other = lang === 'en' ? 'fr' : 'en';
    const alt = [{ lang, path }];
    if (n.data.translation) alt.push({ lang: other, path: `/${other}/news/${n.data.translation}/` });
    items.push({ path, lastmod: day(n.data.date), alt: alt.length > 1 ? alt : undefined });
  }

  const xml =
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n` +
    items
      .map(
        (i) =>
          `  <url>\n    <loc>${esc(base + i.path)}</loc>\n` +
          (i.lastmod ? `    <lastmod>${i.lastmod}</lastmod>\n` : '') +
          (i.alt ?? []).map((a) => `    <xhtml:link rel="alternate" hreflang="${a.lang}" href="${esc(base + a.path)}"/>\n`).join('') +
          `  </url>`,
      )
      .join('\n') +
    `\n</urlset>\n`;

  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
