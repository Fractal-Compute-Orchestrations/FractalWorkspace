import json
import os
import re
import urllib.request

url = 'https://www.behance.net/gallery/221459335/Fractal'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    
    found = False
    for idx, match in enumerate(re.finditer(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)):
        content = match.group(1).strip()
        if 'project' in content and len(content) > 10000:
            try:
                data = json.loads(content)
                project_top = data.get('project', {})
                inner_project = project_top.get('project', {})
                modules = inner_project.get('modules', [])
                
                carousel_slides = []
                image_records = []
                
                image_idx = 1
                for m_idx, mod in enumerate(modules):
                    typename = mod.get('__typename')
                    if 'imageSizes' in mod:
                        image_sizes = mod.get('imageSizes', {})
                        all_available = image_sizes.get('allAvailable', [])
                        
                        # Find the best quality image (prefer highest width, and prefer WEBP over others if widths are equal)
                        best_url = None
                        best_width = 0
                        best_type = ''
                        
                        for item in all_available:
                            url_str = item.get('url')
                            width = item.get('width', 0)
                            img_type = item.get('type', '')
                            
                            # Let's prioritize higher width. If width is same, prefer WEBP.
                            if width > best_width:
                                best_width = width
                                best_url = url_str
                                best_type = img_type
                            elif width == best_width and img_type == 'WEBP':
                                best_url = url_str
                                best_type = img_type
                                
                        if not best_url:
                            best_url = mod.get('src')
                            
                        caption = mod.get('caption', '')
                        if not caption:
                            caption = mod.get('altText', '')
                        if not caption:
                            caption = f"Slide {image_idx}"
                            
                        # Clean caption: remove HTML tags if any
                        caption = re.sub(r'<[^>]+>', '', caption).strip()
                        
                        image_records.append({
                            'index': image_idx,
                            'url': best_url,
                            'width': best_width,
                            'type': best_type,
                            'caption': caption
                        })
                        image_idx += 1
                
                # Generate the Markdown content
                md_lines = []
                md_lines.append("# Behance Fractal Project Showcase Preview\n")
                md_lines.append("This document provides a full visual display of the design showcase slides from the Behance project: **[Fractal](https://www.behance.net/gallery/221459335/Fractal)**.\n")
                
                md_lines.append("## Interactive Carousel\n")
                md_lines.append("````carousel")
                slides = []
                for img in image_records:
                    slide_md = f"![{img['caption']}]({img['url']})\n\n**Slide {img['index']}**: {img['caption']} ({img['width']}px, {img['type']})"
                    slides.append(slide_md)
                md_lines.append(("\n<!-- slide -->\n").join(slides))
                md_lines.append("````\n")
                
                md_lines.append("## Full Visual Gallery\n")
                for img in image_records:
                    md_lines.append(f"### Slide {img['index']}: {img['caption']}")
                    md_lines.append(f"<p align=\"center\">\n  <img src=\"{img['url']}\" width=\"100%\" alt=\"Slide {img['index']} - {img['caption']}\">\n</p>")
                    md_lines.append(f"*Resolution: {img['width']}px | Format: {img['type']}*\n")
                    md_lines.append("---\n")
                
                md_content = "\n".join(md_lines)
                
                # Write to docs/behance_carousel_preview.md
                script_dir = os.path.dirname(os.path.abspath(__file__))
                workspace_dir = os.path.dirname(script_dir)
                workspace_path = os.path.join(workspace_dir, "docs", "behance_carousel_preview.md")
                with open(workspace_path, "w", encoding="utf-8") as f:
                    f.write(md_content)
                print(f"Saved carousel markdown to {workspace_path}")
                
                # Let's print the count and details
                print(f"Generated {len(image_records)} slides successfully.")
                found = True
                break
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                import traceback
                traceback.print_exc()
                
    if not found:
        print("Could not generate carousel because project JSON was not found or failed.")
        
except Exception as e:
    print(f"Error: {e}")
