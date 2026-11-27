import { realpathSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';

const proxy = { '/api': 'http://127.0.0.1:8000' };

export default defineConfig({
  root: realpathSync(fileURLToPath(new URL('.', import.meta.url))),
  server: { proxy },
  preview: { proxy },
});
