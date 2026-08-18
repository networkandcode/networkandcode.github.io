import type { AstroIntegration } from 'astro';
import fs from 'node:fs';
import path from 'node:path';
import https from 'node:https';

export interface HashnodeArticle {
  id: string;
  title: string;
  url: string;
  published_at: string;
  description: string;
  category?: string;
  tags?: string[];
}

export function syncHashnodePosts(): AstroIntegration {
  return {
    name: 'sync-hashnode-posts',
    hooks: {
      'astro:config:setup': async () => {
        console.log('[sync-hashnode] Syncing Hashnode article metadata...');
        try {
          const fetchRss = (url: string) => {
            return new Promise<string>((resolve, reject) => {
              const req = https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (AstroSync)' } }, (res) => {
                let data = '';
                res.on('data', (c) => (data += c));
                res.on('end', () => resolve(data));
              });
              req.on('error', reject);
            });
          };

          const rssData = await fetchRss('https://networkandcode.hashnode.dev/rss.xml');
          const dataFilePath = path.resolve(process.cwd(), 'src/data/hashnodeArticles.json');

          const items: HashnodeArticle[] = [];
          const itemRegex = /<item>([\s\S]*?)<\/item>/g;
          let match: RegExpExecArray | null;

          while ((match = itemRegex.exec(rssData)) !== null) {
            const itemContent = match[1];
            const titleMatch = itemContent.match(/<title><!\[CDATA\[(.*?)\]\]><\/title>/) || itemContent.match(/<title>(.*?)<\/title>/);
            const linkMatch = itemContent.match(/<link>(.*?)<\/link>/);
            const pubDateMatch = itemContent.match(/<pubDate>(.*?)<\/pubDate>/);
            const descMatch = itemContent.match(/<description><!\[CDATA\[([\s\S]*?)\]\]><\/description>/);
            const guidMatch = itemContent.match(/<guid[^>]*>(.*?)<\/guid>/);

            let description = '';
            if (descMatch) {
              description = descMatch[1].replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim().slice(0, 180) + '...';
            }

            if (titleMatch && linkMatch) {
              items.push({
                id: guidMatch ? guidMatch[1] : linkMatch[1],
                title: titleMatch[1],
                url: linkMatch[1],
                published_at: pubDateMatch ? new Date(pubDateMatch[1]).toISOString().slice(0, 10) : '2022-01-01',
                description,
              });
            }
          }

          if (items.length > 0) {
            fs.writeFileSync(dataFilePath, JSON.stringify(items, null, 2), 'utf-8');
            console.log(`[sync-hashnode] Synced ${items.length} Hashnode articles to src/data/hashnodeArticles.json`);
          }
        } catch (err) {
          console.error('[sync-hashnode] Hashnode sync skipped or failed (using cached json if present):', err);
        }
      },
    },
  };
}
