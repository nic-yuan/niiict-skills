#!/usr/bin/env python3
"""
niiict Skills 索引生成器
读取 brands/ 目录下的所有 skill，自动生成 index.html
"""
import os
import json
from pathlib import Path

BRANDS_DIR = Path("brands")
OUTPUT_FILE = Path("index.html")
GITHUB_BASE = "https://nic-yuan.github.io/niiict"
CLAWHUB_BASE = "https://clawhub.ai/skills"

BRAND_META = {
    "apollo": {
        "title": "Apollo OS",
        "desc": "AI 个人操作系统 · 借鉴人体系统设计理念，构建自我感知、自我优化、自我进化的 AI 工作框架",
    },
    "inter-control": {
        "title": "Inter-Control 内控系列",
        "desc": "企业内控 Skill 系列，覆盖投诉分类、风险评分、物流预警、商品合规、月度报告、处罚裁量、风险看板7大模块",
    },
    "local": {
        "title": "Local 本地生活系列",
        "desc": "社区团购运营 Skill 系列，从选品到售后、从供应链到财务结算，覆盖社区团购全链路10大模块",
    },
    "vertical": {
        "title": "Vertical 垂直工具",
        "desc": "行业垂直工具集，解决特定场景的具体问题",
    },
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>niiict.art - Skills Portfolio</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8f9fa; color: #1a1a2e; line-height: 1.6; }}
    a {{ color: #667eea; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .hero {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 20px; text-align: center; }}
    .hero h1 {{ font-size: 2.2rem; font-weight: 700; margin-bottom: 12px; }}
    .hero p {{ font-size: 1.1rem; opacity: 0.9; }}
    .hero-badges {{ margin-top: 20px; display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }}
    .badge {{ background: rgba(255,255,255,0.2); padding: 5px 14px; border-radius: 20px; font-size: 0.85rem; }}
    .container {{ max-width: 1100px; margin: 0 auto; padding: 50px 20px; }}
    .section-title {{ font-size: 1.6rem; font-weight: 600; margin-bottom: 24px; color: #1a1a2e; display: flex; align-items: center; gap: 12px; }}
    .section-title::before {{ content: ''; width: 4px; height: 26px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 2px; }}
    .brand-intro {{ background: white; border-radius: 14px; padding: 28px; margin-bottom: 28px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }}
    .brand-intro h3 {{ font-size: 1.1rem; color: #667eea; margin-bottom: 8px; }}
    .brand-intro p {{ color: #666; font-size: 0.95rem; }}
    .modules-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }}
    .module-card {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); border: 1px solid #eee; transition: box-shadow 0.2s, transform 0.2s; }}
    .module-card:hover {{ box-shadow: 0 6px 20px rgba(0,0,0,0.12); transform: translateY(-2px); }}
    .module-card h4 {{ font-size: 0.95rem; margin-bottom: 8px; color: #1a1a2e; }}
    .module-card p {{ font-size: 0.85rem; color: #666; margin-bottom: 14px; }}
    .module-meta {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; }}
    .tag {{ background: #f0f2ff; color: #667eea; padding: 3px 10px; border-radius: 10px; font-size: 0.75rem; }}
    .tag.done {{ background: #e8f5e9; color: #43a047; }}
    .tag.planning {{ background: #fff3e0; color: #e67e00; }}
    .module-links {{ font-size: 0.8rem; color: #888; }}
    .module-links a {{ color: #667eea; font-weight: 500; }}
    .card-3 {{ background: white; border-radius: 10px; padding: 16px; box-shadow: 0 1px 8px rgba(0,0,0,0.05); border: 1px solid #eee; }}
    .card-3 h5 {{ font-size: 0.88rem; margin-bottom: 6px; color: #333; }}
    .card-3 p {{ font-size: 0.82rem; color: #666; margin-bottom: 10px; }}
    footer {{ text-align: center; padding: 40px 20px; color: #999; font-size: 0.82rem; }}
    @media (max-width: 600px) {{ .hero h1 {{ font-size: 1.6rem; }} .section-title {{ font-size: 1.3rem; }} .container {{ padding: 30px 16px; }} }}
  </style>
</head>
<body>
<section class="hero">
  <h1>niiict.art</h1>
  <p>AI Skills Portfolio · 自动同步更新</p>
  <div class="hero-badges">
    <span class="badge">🤖 AI Skills</span>
    <span class="badge">📦 模块化</span>
    <span class="badge">🚀 自动更新</span>
  </div>
</section>
<div class="container">
{content}
</div>
<footer><p>niiict.art · Powered by Apollo OS · {update_time}</p></footer>
</body>
</html>"""

BRAND_TEMPLATE = """
  <!-- {brand_title} -->
  <h2 class="section-title" style="margin-top:60px;">{brand_title}</h2>
  <div class="brand-intro">
    <h3>{brand_title}</h3>
    <p>{brand_desc}</p>
  </div>
  <div class="modules-grid">
{skills}
  </div>
"""

SKILL_CARD_DONE = """
    <div class="module-card">
      <h4>{name}</h4>
      <p>{description}</p>
      <div class="module-meta"><span class="tag done">✅ 已发布</span>{tags_html}</div>
      <div class="module-links"><a href="{clawhub_url}" target="_blank">🔗 查看技能 →</a></div>
    </div>
"""

SKILL_CARD_PLANNING = """
    <div class="module-card">
      <h4>{name}</h4>
      <p>{description}</p>
      <div class="module-meta"><span class="tag planning">🚧 开发中</span>{tags_html}</div>
    </div>
"""

def parse_skill_md(skill_path):
    """读取 SKILL.md 提取 name, description, tags, slug, published"""
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        return None
    
    with open(skill_file, encoding="utf-8") as f:
        content = f.read(3000)  # 只读前3000字符足够
    
    name = skill_path.name
    description = ""
    tags = []
    slug = name  # 默认用目录名
    published = False
    
    for line in content.split("\n"):
        if line.startswith("name:"):
            name = line.replace("name:", "").strip().strip("\"'")
        elif line.startswith("description:"):
            description = line.replace("description:", "").strip().strip("\"'>").replace(">", "")
        elif line.startswith("tags:"):
            # tags: [tag1, tag2]
            tags_str = line.replace("tags:", "").strip()
            tags = [t.strip().strip("\"'[]") for t in tags_str.split(",")]
        elif line.startswith("slug:"):
            slug = line.replace("slug:", "").strip().strip("\"'")
        elif "published" in line.lower():
            published = True
    
    return {
        "name": name,
        "description": description[:80] + "..." if len(description) > 80 else description,
        "tags": tags[:4],
        "slug": slug,
        "published": published,
    }

def build_brand_section(brand, skill_dirs):
    """构建一个品牌的HTML"""
    skills_html = ""
    
    for skill_dir in sorted(skill_dirs):
        skill_info = parse_skill_md(skill_dir)
        if not skill_info:
            continue
        
        tags_html = "".join(f'<span class="tag">{t}</span>' for t in skill_info["tags"])
        
        if skill_info["published"]:
            clawhub_url = f"{CLAWHUB_BASE}/{skill_info['slug']}"
            skills_html += SKILL_CARD_DONE.format(
                name=skill_info["name"],
                description=skill_info["description"],
                tags_html=tags_html,
                clawhub_url=clawhub_url,
            )
        else:
            skills_html += SKILL_CARD_PLANNING.format(
                name=skill_info["name"],
                description=skill_info["description"],
                tags_html=tags_html,
            )
    
    meta = BRAND_META.get(brand, {"title": brand, "desc": ""})
    return BRAND_TEMPLATE.format(
        brand_title=meta["title"],
        brand_desc=meta["desc"],
        skills=skills_html,
    )

def generate_index():
    """扫描所有brands目录，生成 index.html"""
    all_brands_html = ""
    
    for brand in ["apollo", "inter-control", "local", "vertical"]:
        brand_path = BRANDS_DIR / brand
        if not brand_path.exists():
            continue
        
        skill_dirs = [d for d in brand_path.iterdir() if d.is_dir()]
        all_brands_html += build_brand_section(brand, skill_dirs)
    
    from datetime import datetime
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    html = HTML_TEMPLATE.format(content=all_brands_html, update_time=update_time)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Generated {OUTPUT_FILE} with {len(all_brands_html)} chars")

if __name__ == "__main__":
    generate_index()