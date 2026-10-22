#!/usr/bin/env node

import { readFileSync, writeFileSync } from 'node:fs';

const [reportPath, catalogPath = 'README.md', archivePath = 'docs/archived-links.md'] = process.argv.slice(2);

if (!reportPath) {
  console.error('Usage: node scripts/archive_broken_links.mjs <lychee-report.json> [catalog] [archive]');
  process.exit(2);
}

const report = JSON.parse(readFileSync(reportPath, 'utf8'));
const originalLines = readFileSync(catalogPath, 'utf8').split('\n');
const failures = Object.values(report.error_map ?? {}).flat();
const missing = [...new Set(failures.filter(item => item.status?.code === 404).map(item => item.url))];
const archived = [];
const kept = [];

for (const line of originalLines) {
  const url = missing.find(candidate => line.includes(candidate));
  if (url) archived.push({ line: line.trim(), url });
  else kept.push(line);
}

if (!archived.length) {
  console.log('No matching HTTP 404 entries found in the catalog.');
  process.exit(0);
}

const date = new Date().toISOString().slice(0, 10);
let archive;
try {
  archive = readFileSync(archivePath, 'utf8').trimEnd();
} catch {
  archive = '# 已归档链接\n\n这里保存从主目录移出的历史条目。链接可能已经删除、迁移或不再公开；保留记录是为了后续查找新地址和避免重复调查。';
}

archive += `\n\n## ${date}：HTTP 404 基线清理\n\n`;
archive += archived.map(item => `${item.line}\n  - 原地址：${item.url}`).join('\n');
archive += '\n';

writeFileSync(catalogPath, kept.join('\n'), 'utf8');
writeFileSync(archivePath, archive, 'utf8');
console.log(`Archived ${archived.length} catalog entries.`);
