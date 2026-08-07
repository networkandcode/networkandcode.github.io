import type { AstroIntegration } from 'astro';
import fs from 'node:fs';
import path from 'node:path';
import https from 'node:https';

export function syncDevToPosts(): AstroIntegration {
  return {
    name: 'sync-devto-posts',
    hooks: {
      'astro:config:setup': async () => {
        console.log('[sync-devto] Checking for DEV.to posts updates...');
        try {
          const fetchJson = (url: string) => {
            return new Promise<any>((resolve, reject) => {
              const req = https.get(url, { headers: { 'User-Agent': 'AstroSync' } }, (res) => {
                let data = '';
                res.on('data', (c) => (data += c));
                res.on('end', () => resolve(JSON.parse(data)));
              });
              req.on('error', reject);
            });
          };

          const articles = await fetchJson('https://dev.to/api/articles?username=networkandcode&per_page=100');
          const postsDir = path.resolve(process.cwd(), '_posts');

          for (const art of articles) {
            const dateStr = art.published_at.slice(0, 10);
            const subfolder = path.join(postsDir, dateStr);
            fs.mkdirSync(subfolder, { recursive: true });

            const slug = art.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
            const filepath = path.join(subfolder, `${dateStr}-${slug}.md`);

            if (!fs.existsSync(filepath)) {
              console.log(`[sync-devto] Fetching body for new post: ${art.title}`);
              const detail = await fetchJson(`https://dev.to/api/articles/${art.id}`);
              let bodyMd = detail.body_markdown || '';

              if (bodyMd.startsWith('---')) {
                const parts = bodyMd.split('---');
                if (parts.length >= 3) {
                  bodyMd = parts.slice(2).join('---');
                }
              }

              const cover = art.cover_image ? `cover_image: "${art.cover_image}"\n` : '';
              const tags = art.tag_list?.length ? `tags: "${art.tag_list.join(', ')}"\ncategories: "${art.tag_list.join(', ')}"\n` : '';
              const frontmatter = `---\ncanonical_url: "${art.url}"\ndate: "${dateStr}"\ntitle: "${art.title.replace(/"/g, '\\"')}"\n${cover}${tags}---\n\n**This post first appeared on [dev.to](${art.url})**\n\n`;

              fs.writeFileSync(filepath, frontmatter + bodyMd.trim() + '\n', 'utf-8');
            }
          }
          console.log('[sync-devto] All DEV.to posts synced.');
        } catch (err) {
          console.error('[sync-devto] DEV.to sync check skipped or failed:', err);
        }
      },
    },
  };
}
