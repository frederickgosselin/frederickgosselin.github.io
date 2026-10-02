export const LANGS = ['en', 'fr'] as const;
export type Lang = (typeof LANGS)[number];

// Page slugs per language, in menu order. Each row is one page and its translation.
export const PAGES: { en: string; fr: string }[] = [
  { en: 'about', fr: 'a-propos' },
  { en: 'research-opportunities', fr: 'opportunites-de-recherche' },
  { en: 'teaching', fr: 'enseignement' },
  { en: 'videos', fr: 'videos' },
  { en: 'publications', fr: 'publications' },
];

export const T = {
  en: {
    siteName: 'Frédérick P. Gosselin',
    role: 'Full Professor, Department of Mechanical Engineering, Polytechnique Montréal',
    news: 'News',
    allNews: 'All news',
    latest: 'Latest news',
    menu: { about: 'About', 'research-opportunities': 'Research opportunities', teaching: 'Teaching', videos: 'Videos', publications: 'Publications' } as Record<string, string>,
    otherLang: 'Français',
    lab: 'Laboratory for Multiscale Mechanics (LM2)',
    skip: 'Skip to content',
    tags: 'Tags',
  },
  fr: {
    siteName: 'Frédérick P. Gosselin',
    role: 'Professeur titulaire, Département de génie mécanique, Polytechnique Montréal',
    news: 'Nouvelles',
    allNews: 'Toutes les nouvelles',
    latest: 'Dernières nouvelles',
    menu: { 'a-propos': 'À propos', 'opportunites-de-recherche': 'Opportunités de recherche', enseignement: 'Enseignement', videos: 'Vidéos', publications: 'Publications' } as Record<string, string>,
    otherLang: 'English',
    lab: 'Laboratoire de mécanique multiéchelles (LM2)',
    skip: 'Aller au contenu',
    tags: 'Mots-clés',
  },
} as const;

/** Dates are stored as UTC midnight; format in UTC so they never slip a day. */
export const fmtDate = (lang: Lang, d: Date) =>
  new Intl.DateTimeFormat(lang === 'fr' ? 'fr-CA' : 'en-CA', { dateStyle: 'long', timeZone: 'UTC' }).format(d);

export const other =(l: Lang): Lang => (l === 'en' ? 'fr' : 'en');
export const pageUrl = (l: Lang, slug: string) => `/${l}/${slug}/`;
/** Translate a page slug from language `from` to the other language. */
export const pageTranslation = (from: Lang, slug: string) => {
  const row = PAGES.find((p) => p[from] === slug);
  return row ? row[other(from)] : undefined;
};
