import urllib.request
import re
import json

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
                    print(f"Module {m_idx+1}: type={mod.get('type')}, keys={list(mod.keys())}")
                    if 'sizes' in mod:
                        print(f"  has sizes")
                    # If type is 'media_grid', 'image', 'embed', etc.
                    # Let's inspect further
                    if 'components' in mod:
                        print(f"  has components: {len(mod['components'])}")
                        for c_idx, comp in enumerate(mod['components']):
                            print(f"    Component {c_idx+1}: type={comp.get('type')}, keys={list(comp.keys())}")
                            if 'sizes' in comp:
                                print(f"      sizes keys: {list(comp['sizes'].keys())}")
                                for k, v in comp['sizes'].items():
                                    print(f"        {k}: {v}")
                break
            except Exception as e:
                print(f"Error: {e}")
except Exception as e:
    import traceback
    traceback.print_exc()
