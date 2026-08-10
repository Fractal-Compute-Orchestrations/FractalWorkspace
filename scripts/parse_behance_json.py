import urllib.request
import re
import json

url = 'https://www.behance.net/gallery/221459335/Fractal'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    
    # Behance pages often have a JSON block inside a <script> tag starting with:
    # window.initialState = ... or similar, or inside a data-initial-state attribute.
    # Let's search for "initialState" or JSON patterns in script tags.
    found_json = False
    for match in re.finditer(r'<script[^>]*>(.*?)</script>', html, re.DOTALL):
        script_content = match.group(1)
        if 'project' in script_content and 'modules' in script_content:
            # Let's search for window.initialState or similar assignment
            assignment_match = re.search(r'(?:window\.)?initialState\s*=\s*({.*?});?\s*$', script_content, re.MULTILINE)
            if assignment_match:
                json_str = assignment_match.group(1)
                data = json.loads(json_str)
                # Let's see if we can extract project modules
                project = data.get('project', {})
                modules = project.get('modules', [])
                print(f"Parsed initial state! Found {len(modules)} modules.")
                for idx, mod in enumerate(modules):
                    mod_type = mod.get('type')
                    print(f"Module {idx+1} Type: {mod_type}")
                    if mod_type == 'image':
                        sizes = mod.get('sizes', {})
                        print(f"  Sizes: {list(sizes.keys())}")
                        # print some urls
                        for size_key in ['max_3840', 'max_1920', 'disp', 'original']:
                            if size_key in sizes:
                                print(f"  {size_key}: {sizes[size_key]}")
                                break
                found_json = True
                break
                
    if not found_json:
        # Let's search for any large JSON-like script content containing project
        print("Could not find window.initialState. Let's list some script blocks containing 'project'")
        for idx, match in enumerate(re.finditer(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)):
            content = match.group(1)
            if 'project' in content and len(content) > 10000:
                print(f"Script block {idx+1} length: {len(content)}")
                # Print first 200 chars and last 200 chars
                print("Start:", content[:200])
                print("End:", content[-200:])
                
except Exception:
    import traceback
    traceback.print_exc()
