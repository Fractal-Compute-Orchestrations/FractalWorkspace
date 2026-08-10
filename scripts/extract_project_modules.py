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
                print("Successfully loaded script block as JSON!")
                
                # Let's inspect the keys
                print("Top-level keys:", list(data.keys()))
                
                # Behance JSON structure might have project details inside. Let's recursively search for "project"
                # or just search for modules directly.
                def find_key(obj, target_key):
                    if isinstance(obj, dict):
                        if target_key in obj:
                            return obj[target_key]
                        for v in obj.values():
                            res = find_key(v, target_key)
                            if res is not None:
                                return res
                    elif isinstance(obj, list):
                        for item in obj:
                            res = find_key(item, target_key)
                            if res is not None:
                                return res
                    return None

                # Let's look for 'project' or 'modules'
                project_data = data.get('project')
                if not project_data:
                    # Search recursively
                    project_data = find_key(data, 'project')
                
                if project_data:
                    print("Found project data!")
                    if isinstance(project_data, dict):
                        print("Project keys:", list(project_data.keys()))
                        modules = project_data.get('modules', [])
                        print(f"Found {len(modules)} modules in project.")
                        
                        image_modules = []
                        for m_idx, mod in enumerate(modules):
                            if mod.get('type') == 'image':
                                sizes = mod.get('sizes', {})
                                # Check what sizes we have
                                image_modules.append({
                                    'id': mod.get('id'),
                                    'sizes': sizes,
                                    'caption': mod.get('caption_plain', '')
                                })
                        
                        print(f"Found {len(image_modules)} image modules:")
                        for m_idx, img_mod in enumerate(image_modules):
                            print(f"\nImage {m_idx + 1}: ID={img_mod['id']}, Caption='{img_mod['caption']}'")
                            for sz in ['max_3840', 'max_1200', 'disp', 'original']:
                                if sz in img_mod['sizes']:
                                    print(f"  {sz}: {img_mod['sizes'][sz]}")
                                    
                break
            except Exception as e:
                print(f"Failed to parse script block {idx+1} as JSON: {e}")
                
except Exception:
    import traceback
    traceback.print_exc()
