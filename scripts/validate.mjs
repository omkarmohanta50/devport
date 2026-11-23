import assert from 'node:assert/strict';
import { readFile, access } from 'node:fs/promises';
const html = await readFile('dist/index.html','utf8');
for (const [, target] of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
  if (target.startsWith('#')) assert(html.includes('id="'+target.slice(1)+'"'),target);
  else if (target.startsWith('/')) await access('dist'+target.split('#')[0]);
}
for (const asset of ['share.png','robots.txt']) await access('dist/'+asset);
console.log('Internal links and public assets verified.');

