import json
import re
import urllib.request

url = 'https://www.behance.net/gallery/221459335/Fractal'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    
    for idx, match in enumerate(re.finditer(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)):
        content = match.group(1).strip()
        if 'project' in content and len(content) > 10000:
            try:
                data = json.loads(content)
                project_top = data.get('project', {})
                inner_project = project_top.get('project', {})
                print("Inner project keys:", list(inner_project.keys()))
                
                modules = inner_project.get('modules', [])
                print(f"Found {len(modules)} modules in inner project.")
                
                image_modules = []
                for m_idx, mod in enumerate(modules):
                    if mod.get('type') == 'image':
                        sizes = mod.get('sizes', {})
                        image_modules.append({
                            'id': mod.get('id'),
                            'sizes': sizes,
                            'caption': mod.get('caption_plain', '')
                        })
                
                print(f"Found {len(image_modules)} image modules.")
                for m_idx, img_mod in enumerate(image_modules):
                    print(f"\nImage {m_idx + 1}: ID={img_mod['id']}, Caption='{img_mod['caption']}'")
                    for sz in ['max_3840', 'max_1200', 'disp', 'original']:
                        if sz in img_mod['sizes']:
                            print(f"  {sz}: {img_mod['sizes'][sz]}")
                break
            except Exception as e:
                print(f"Error parsing JSON: {e}")
except Exception:
    import traceback
    traceback.print_exc()
