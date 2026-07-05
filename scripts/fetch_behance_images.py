import urllib.request
import re
import json

url = 'https://www.behance.net/gallery/221459335/Fractal'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    
    # Find all image URLs
    images = re.findall(r'https://[^"\s]*\.(?:jpg|jpeg|png|gif|webp)[^"\s]*', html)
    unique = list(set(images))
    print(f'Found {len(unique)} total images:')
    for i, img in enumerate(unique[:50]):
        print(f'{i+1}. {img}')
except Exception as e:
    print(f'Error: {e}')