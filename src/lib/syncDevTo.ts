import type { AstroIntegration } from 'astro';
import fs from 'node:fs';
import path from 'node:path';
import https from 'node:https';

export interface DevToArticle {
  id: number;
  title: string;
  description: string;
  url: string;
  published_at: string;
  tag_list: string[];
  cover_image: string | null;
  reading_time_minutes?: number;
  positive_reactions_count?: number;
  comments_count?: number;
}

export function syncDevToPosts(): AstroIntegration {
  return {
    name: 'sync-devto-posts',
    hooks: {
      'astro:config:setup': async () => {
        console.log('[sync-devto] Syncing DEV.to article metadata...');
        try {
          const fetchJson = (url: string) => {
            return new Promise<any>((resolve, reject) => {
              const req = https.get(url, { headers: { 'User-Agent': 'AstroSync' } }, (res) => {
                let data = '';
                res.on('data', (c) => (data += c));
                res.on('end', () => {
                  try {
                    resolve(JSON.parse(data));
                  } catch (e) {
                    reject(e);
                  }
                });
              });
              req.on('error', reject);
            });
          };

          const articles = await fetchJson('https://dev.to/api/articles?username=networkandcode&per_page=100');
          const dataFilePath = path.resolve(process.cwd(), 'src/data/devtoArticles.json');

          if (Array.isArray(articles) && articles.length > 0) {
            const formatted: DevToArticle[] = articles
              .filter((art: any) => {
                const desc = (art.description || '').toLowerCase();
                const canon = (art.canonical_url || '').toLowerCase();
                // Exclude posts that first appeared on networkandcode.github.io
                return !desc.includes('networkandcode.github.io') && !canon.includes('networkandcode.github.io');
              })
              .map((art: any) => ({
                id: art.id,
                title: art.title,
                description: art.description || '',
                url: art.url,
                published_at: art.published_at,
                tag_list: art.tag_list || [],
                cover_image: art.cover_image || null,
                reading_time_minutes: art.reading_time_minutes,
                positive_reactions_count: art.positive_reactions_count,
                comments_count: art.comments_count,
              }));

            fs.writeFileSync(dataFilePath, JSON.stringify(formatted, null, 2), 'utf-8');
            console.log(`[sync-devto] Synced ${formatted.length} DEV.to articles metadata to src/data/devtoArticles.json`);
          }
        } catch (err) {
          console.error('[sync-devto] DEV.to sync skipped or failed (using cached json if present):', err);
        }
      },
    },
  };
}
