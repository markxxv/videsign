#!/usr/bin/env python3
"""Injects src/head.html and src/videsign.css into every page between markers.
Run after editing src/: python3 build.py"""
import re, pathlib
root = pathlib.Path(__file__).parent
css = (root/'src/videsign.css').read_text().rstrip()
head = (root/'src/head.html').read_text().rstrip()
block = '<style type="text/tailwindcss">\n' + css + '\n  </style>'
for page in sorted(root.glob('*.html')):
    s = page.read_text()
    s = re.sub(r'<!-- VIDESIGN:HEAD -->.*?<!-- /VIDESIGN:HEAD -->', lambda m: '<!-- VIDESIGN:HEAD -->\n' + head + '\n  <!-- /VIDESIGN:HEAD -->', s, flags=re.S)
    s = re.sub(r'<!-- VIDESIGN:CSS -->.*?<!-- /VIDESIGN:CSS -->', lambda m: '<!-- VIDESIGN:CSS -->\n  ' + block + '\n  <!-- /VIDESIGN:CSS -->', s, flags=re.S)
    page.write_text(s); print('built', page.name)
