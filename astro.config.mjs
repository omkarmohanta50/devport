import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
const site = process.env.SITE_URL || 'https://shreeman-omkar.pages.dev';
export default defineConfig({ site, integrations: site ? [sitemap()] : [] });
