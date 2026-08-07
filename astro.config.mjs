// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import { syncGoogleDocCv } from './src/lib/syncCv.ts';
import { syncDevToPosts } from './src/lib/syncDevTo.ts';

// https://astro.build/config
export default defineConfig({
  site: 'https://networkandcode.github.io',
  integrations: [mdx(), syncGoogleDocCv(), syncDevToPosts()],
});
