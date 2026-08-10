import re
import urllib.request

url = 'https://www.behance.net/gallery/221459335/Fractal'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    
    # Let's find all occurrences of images that have the project ID '221459335'
    # We want to identify the exact order they appear in the HTML.
    # To do this, let's find all image tags or links that match.
    # A typical pattern is mir-s3-cdn-cf.behance.net/project_modules/<size>/<img_id>221459335.<hash>.<ext>
    matches = re.findall(r'https://mir-s3-cdn-cf\.behance\.net/project_modules/[a-zA-Z0-9_]+/([a-f0-9]+221459335\.[a-f0-9]+\.(?:png|jpg|jpeg|webp))', html)
    
    # Let's see the ordered matches and resolve them to unique image IDs, preserving order
    seen = set()
    ordered_files = []
    for match in matches:
        # match is like: c6ca87221459335.67d47de252ed6.png
        img_id = match.split('.')[0]
        if img_id not in seen:
            seen.add(img_id)
            ordered_files.append(match)
            
    print(f"Found {len(ordered_files)} ordered image IDs:")
    for idx, f in enumerate(ordered_files):
        print(f"{idx+1}: {f}")
        
except Exception as e:
    print(f"Error: {e}")
