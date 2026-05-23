#!/usr/bin/env python3
"""
Run this script any time you add or remove photos from the year folders.
It rebuilds the JSON manifests AND refreshes the homepage preview photos.

Usage (from the project folder):
    python3 update-gallery.py
"""

import os, json, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
total = 0

for year in ['2023', '2024', '2025']:
    src_folder = os.path.join(BASE, f'img/Veganer Markt {year}')
    dst_folder = os.path.join(BASE, f'img/gallery/{year}')

    if not os.path.isdir(src_folder):
        print(f'  [skip] {src_folder} not found')
        continue

    files = sorted([f for f in os.listdir(src_folder) if f.lower().endswith('.jpg')])

    # 1. Rebuild full-gallery JSON (used by galerie.html)
    data = [{'file': f, 'alt': f'Veganer Markt Koblenz {year}'} for f in files]
    with open(os.path.join(BASE, f'img/gallery/all-{year}.json'), 'w') as fp:
        json.dump(data, fp, indent=2)

    # 2. Refresh homepage preview photos (g01–g12)
    for f in os.listdir(dst_folder):
        if f.lower().endswith('.jpg'):
            os.remove(os.path.join(dst_folder, f))
    chosen = files[:12]
    for i, f in enumerate(chosen, 1):
        shutil.copy2(os.path.join(src_folder, f), os.path.join(dst_folder, f'g{i:02d}.jpg'))

    total += len(files)
    print(f'  {year}: {len(files)} Fotos gesamt, {len(chosen)} Vorschaufotos aktualisiert')

print(f'\n  Gesamt: {total} Fotos. Fertig!')
