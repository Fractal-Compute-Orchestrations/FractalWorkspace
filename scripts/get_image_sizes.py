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
                modules = inner_project.get('modules', [])
                
                print(f"Total modules: {len(modules)}")
                for m_idx, mod in enumerate(modules):
                    typename = mod.get('__typename')
                    if 'imageSizes' in mod:
                        print(f"\nModule {m_idx+1} (typename={typename}):")
                        image_sizes = mod.get('imageSizes')
                        print(f"  imageSizes type: {type(image_sizes)}")
                        print(f"  imageSizes content: {image_sizes}")
                        if isinstance(image_sizes, list):
                            for item in image_sizes:
                                print(f"    item type: {type(item)}, content: {item}")
                        elif isinstance(image_sizes, dict):
                            for k, v in image_sizes.items():
                                print(f"    {k}: {type(v)}, content: {v}")
                break
            except Exception as e:
                print(f"Error parsing JSON: {e}")
except Exception:
    import traceback
    traceback.print_exc()
