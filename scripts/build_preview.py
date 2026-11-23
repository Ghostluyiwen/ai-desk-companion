#!/usr/bin/env python3
"""Build an offline, standalone preview with Python's standard library."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
fragment = (ROOT / 'src' / 'preview.html').read_text(encoding='utf-8')
fragment = fragment.replace('window.openai', 'window.previewState')
bridge = r'''<script>
(() => {
  const key = 'codex-desk-display-v1';
  let state = {};
  try { state = JSON.parse(localStorage.getItem(key) || '{}'); } catch (_) {}
  window.previewState = {
    widgetState: state,
    async setWidgetState(next) {
      this.widgetState = next;
      try { localStorage.setItem(key, JSON.stringify(next)); } catch (_) {}
    }
  };
})();
</script>'''
page = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>AI Desk Companion · 交互原型</title>
<style>body{margin:0;background:light-dark(#fff,#161a1d);font-family:system-ui,sans-serif}main{max-width:760px;margin:auto;padding:20px 0 40px}button:focus-visible,input:focus-visible{outline:2px solid #5a8dc0;outline-offset:3px}</style>
</head><body><main>'''
page += bridge + fragment + '</main></body></html>\n'
(ROOT / 'index.html').write_text(page, encoding='utf-8')
print('Built index.html')
