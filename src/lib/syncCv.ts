import type { AstroIntegration } from 'astro';
import fs from 'node:fs';
import path from 'node:path';
import https from 'node:https';

const GOOGLE_DOC_URL = 'https://docs.google.com/document/d/e/2PACX-1vRB5hdZs7dKLFRZonRdw9I_l5JfhQLJ4jMGtwLcaNmM_kEs3f1t_up7WdjieEWC08Q9jVdpfBeoB4K7/pub';

export function syncGoogleDocCv(): AstroIntegration {
  return {
    name: 'sync-google-doc-cv',
    hooks: {
      'astro:config:setup': async () => {
        console.log('[sync-cv] Fetching latest CV from Google Doc...');
        try {
          const html = await new Promise<string>((resolve, reject) => {
            https.get(GOOGLE_DOC_URL, (res) => {
              let data = '';
              res.on('data', (chunk) => (data += chunk));
              res.on('end', () => resolve(data));
            }).on('error', reject);
          });

          // Clean HTML: Keep structure but clean Google wrapper styles
          let docHtml = '';
          const contentsMatch = html.match(/<div class="[^"]*doc-content[^"]*">([\s\S]*?)<\/div>\s*<\/body>/i) 
                             || html.match(/<div id="contents">([\s\S]*?)<\/div>\s*<\/body>/i);

          if (contentsMatch) {
            docHtml = contentsMatch[1];
          } else {
            const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
            docHtml = bodyMatch ? bodyMatch[1] : html;
          }

          // Clean out unwanted script tags, style attributes, and banner headers from Google Doc export
          docHtml = docHtml
            .replace(/<script[\s\S]*?<\/script>/gi, '')
            .replace(/<div id="banners">[\s\S]*?<\/div>\s*<\/div>/gi, '')
            .replace(/<style[\s\S]*?<\/style>/gi, '')
            .replace(/style="[^"]*"/gi, '')
            .replace(/class="[^"]*"/gi, '');

          const cvDataPath = path.resolve(process.cwd(), 'src/data/cv.json');
          fs.mkdirSync(path.dirname(cvDataPath), { recursive: true });
          fs.writeFileSync(
            cvDataPath, 
            JSON.stringify({ 
              url: GOOGLE_DOC_URL, 
              updatedAt: new Date().toISOString(), 
              cleanHtml: docHtml 
            }, null, 2)
          );
          console.log('[sync-cv] Successfully synced HTML CV data to src/data/cv.json');
        } catch (err) {
          console.error('[sync-cv] Failed to fetch Google Doc CV:', err);
        }
      },
    },
  };
}
