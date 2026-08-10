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
                
                print(f"Total modules found: {len(modules)}")
                image_idx = 1
                for m_idx, mod in enumerate(modules):
                    typename = mod.get('__typename')
                    if 'imageSizes' in mod or 'src' in mod:
                        # This looks like an image module
                        src = mod.get('src')
                        img_sizes = mod.get('imageSizes', [])
                        caption = mod.get('caption', '')
                        alt = mod.get('altText', '')
                        print(f"\nImage {image_idx} (Module {m_idx+1}): typename={typename}")
                        print(f"  src: {src}")
                        print(f"  alt: {alt}")
                        print(f"  caption: {caption}")
                        print("  sizes:")
                        for size_obj in img_sizes:
                            print(f"    {size_obj.get('size')}: {size_obj.get('url')}")
                        image_idx += 1
                    else:
                        print(f"\nNon-image Module {m_idx+1}: typename={typename}")
                        if 'text' in mod:
                            print(f"  text: {mod.get('text')[:100]}...")
                break
            except Exception as e:
                print(f"Error parsing JSON: {e}")
except Exception:
    import traceback
    traceback.print_exc()
