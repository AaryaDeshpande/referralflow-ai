import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../dist');
const port = Number(process.env.PORT || 3000);
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.pdf': 'application/pdf', '.png': 'image/png', '.svg': 'image/svg+xml', '.mp3': 'audio/mpeg' };

export async function resolveFile(urlPath) {
  let decoded;
  try { decoded = decodeURIComponent(urlPath); } catch { return null; }
  if (decoded.includes('\0') || decoded.includes('\\')) return null;
  const candidate = path.resolve(root, '.' + decoded);
  if (candidate !== root && !candidate.startsWith(root + path.sep)) return null;
  const options = decoded.endsWith('/') ? [path.join(candidate, 'index.html')] : path.extname(candidate) ? [candidate] : [candidate + '.html', path.join(candidate, 'index.html')];
  for (const file of options) {
    try { if ((await stat(file)).isFile()) return file; } catch {}
  }
  return null;
}

export function createPreviewServer() { return http.createServer(async (req, res) => {
  if (!['GET', 'HEAD'].includes(req.method)) { res.writeHead(405, { Allow: 'GET, HEAD' }); res.end(); return; }
  try {
    const file = await resolveFile(new URL(req.url, 'http://localhost').pathname);
    if (!file) { res.writeHead(404); res.end('Not found'); return; }
    const bytes = await readFile(file);
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream', 'Content-Length': bytes.length, 'Cache-Control': 'no-store' });
    res.end(req.method === 'HEAD' ? undefined : bytes);
  } catch { res.writeHead(500); res.end('Unable to read file'); }
}); }

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  createPreviewServer().listen(port, '127.0.0.1', () => console.log(`ReferralFlow local preview: http://127.0.0.1:${port}/`));
}
