import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';
import { syncGoogleDocCv } from './src/lib/syncCv.ts';
import { syncDevToPosts } from './src/lib/syncDevTo.ts';
import { syncHashnodePosts } from './src/lib/syncHashnode.ts';

// https://astro.build/config
export default defineConfig({
  site: 'https://networkandcode.github.io',
  integrations: [mdx(), syncGoogleDocCv(), syncDevToPosts(), syncHashnodePosts()],
  vite: {
    plugins: [tailwindcss()]
  }
});
