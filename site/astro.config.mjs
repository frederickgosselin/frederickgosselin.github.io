import { defineConfig } from 'astro/config';

// `site` is the final public URL (www.fgosselin.com via GoDaddy DNS -> GitHub Pages).
export default defineConfig({
  site: 'https://www.fgosselin.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
});
