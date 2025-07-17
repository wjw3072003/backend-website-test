#!/usr/bin/env python3
import re

def load_mapping():
    mapping = {}
    with open('js_css_mapping.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if ' -> ' in line:
                url, local = line.strip().split(' -> ')
                mapping[url] = local
    return mapping

def replace_html(html_path, mapping, out_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    for url, local in mapping.items():
        html = html.replace(url, local)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'已替换并保存到{out_path}')

def main():
    mapping = load_mapping()
    replace_html('aimuspal_homepage_clean.html', mapping, 'aimuspal_homepage_full.html')

if __name__ == '__main__':
    main() 