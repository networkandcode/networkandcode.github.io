export interface PostData {
  id: string;
  title: string;
  dateStr: string;
  category: string;
  body: string;
  rawUrl: string;
}

export function parsePostFilename(filename: string) {
  // Extract date if present (YYYY-MM-DD)
  const match = filename.match(/^(\d{4}-\d{2}-\d{2})-(.+)$/);
  if (match) {
    return {
      dateStr: match[1],
      slug: match[2].replace(/\.(md|markdown|html)$/, '')
    };
  }
  return {
    dateStr: '2022-01-01',
    slug: filename.replace(/\.(md|markdown|html)$/, '')
  };
}
