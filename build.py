#!/usr/bin/env python3
"""把 Pages CMS 的 Markdown 文章编译成可以直接打开的静态网站。"""
from __future__ import annotations
import argparse
import datetime as dt
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

import bleach
import jinja2
import mistune
import yaml

BASE = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE / 'templates'
SOURCES = BASE / 'content/posts'
CATS = ['生活随笔', '读书笔记', '小说创作', '诗词创作']
SCENES = {'生活随笔': ('clay','留'), '读书笔记': ('sand','读'), '小说创作': ('night','叙'), '诗词创作': ('sand','诗')}
ALLOWED_TAGS = set(bleach.sanitizer.ALLOWED_TAGS) | {'p','h1','h2','h3','h4','h5','h6','blockquote','hr','pre','code','img','del','s','sup','sub','br','table','thead','tbody','tr','th','td','input'}
ALLOWED_ATTRS = {'a':['href','title','rel','target'],'img':['src','alt','title','width','height','loading'],'th':['align'],'td':['align'],'input':['type','disabled','checked']}
md = mistune.create_markdown(escape=True, plugins=['strikethrough', 'table', 'task_lists', 'url'])

def parse_post(file:Path)->dict:
    raw=file.read_text(encoding='utf-8-sig')
    fm=re.match(r'\A---\s*\n(.*?)\n---\s*\n(.*)\Z',raw,re.S)
    if not fm:
        raise ValueError(f'{file.name}: 缺少 YAML 文章头部（---）。')
    data=yaml.safe_load(fm.group(1)) or {}
    if not isinstance(data,dict): raise ValueError(f'{file.name}: YAML 信息应为对象')
    if data.get('draft',False): return {}
    for key in ['title','category','date']:
        if not data.get(key): raise ValueError(f'{file.name}: 缺少 {key}')
    raw_date=data['date']
    date=raw_date.isoformat() if isinstance(raw_date,(dt.date,dt.datetime)) else str(raw_date)[:10]
    dt.date.fromisoformat(date)
    if data['category'] not in CATS: raise ValueError(f'{file.name}: 分类必须在四个预设分类内')
    slug=re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff-]+','-',file.stem).strip('-').lower()
    # 对正文 HTML 做白名单过滤，避免脚本代码进入公开网页。
    body=bleach.clean(md(fm.group(2)),tags=ALLOWED_TAGS,attributes=ALLOWED_ATTRS,strip=True,protocols={'http','https','mailto'})
    # 统一消除从 Word 粘贴产生的段首全角空格，具体缩进由阅读页 CSS 控制。
    if data['category']=='小说创作':
        body=re.sub(r'(<p>)(?:[\u0020\u3000]|&nbsp;|&#160;)+',r'\1',body)
    headings=[]
    def add_anchor(m):
        title=html.unescape(re.sub(r'<[^>]*>', '', m.group(2)))
        anchor=f'paragraph-{len(headings)+1}'
        headings.append({'id':anchor,'title':title})
        return f'<{m.group(1)} id="{anchor}">{m.group(2)}</{m.group(1)}>'
    body=re.sub(r'<(h[23])>(.*?)</h[23]>',add_anchor,body,flags=re.S|re.I)
    tags=data.get('tags','')
    if isinstance(tags,str): tags=[s.strip() for s in re.split('[，,、]',tags) if s.strip()]
    else: tags=[str(t) for t in tags if str(t).strip()]
    displayDate=date.replace('-','.')
    text=re.sub(r'<[^>]+>', '', body)
    # 正文实数统计（排除 HTML 标记和空白字符），不再展示未经验证的阅读时长。
    character_count=len(re.sub(r'\s+', '',html.unescape(text)))
    scene,glyph=SCENES[data['category']]
    series=str(data.get('series') or '').strip() if data['category']=='小说创作' else ''
    raw_chapter=data.get('chapter')
    try: chapter=int(raw_chapter) if raw_chapter not in (None,'') else None
    except (ValueError,TypeError): chapter=None
    result={
        'series':series,'chapter':chapter,
        'slug':slug,'url':f'posts/{slug}.html','title':str(data['title']),
        'date':date,'displayDate':displayDate,'category':str(data['category']),
        'excerpt':str(data.get('excerpt') or '').strip(),
        'cover':str(data.get('cover') or '').strip(),
        'featured':bool(data.get('featured',False)),
        'tags':tags,'characterCount':character_count,'scene':scene,'glyph':glyph,
        'content_raw':body,'headings':headings,
    }
    result['searchText']=' '.join([result['title'],result['excerpt'],result['category'], ' '.join(tags)]).lower()
    return result

def resource_url(path:str,root:str)->str:
    if not path: return ''
    path=path.strip()
    if path.startswith(('https://','http://','data:','mailto:','#')): return path
    return root+path.lstrip('/')

def rewrite_body_urls(body:str,root:str)->str:
    # Pages CMS 上传的图片在 Markdown 里通常是 /media/images/xxx。
    # 转换成相对路径，确保本地双击预览和 GitHub Pages 均可显示。
    def convert(m):
        if m.group(2).startswith(('/media/', 'media/','/assets/','assets/')):
            return m.group(1)+resource_url(m.group(2),root)+m.group(3)
        return m.group(0)
    return re.sub(r'((?:src|href)=")([^"]+)(")',convert,body)

def build(dest:Path)->None:
    site=yaml.safe_load((BASE/'data/site.yml').read_text(encoding='utf-8'))
    posts=[parse_post(f) for f in sorted(SOURCES.glob('*.md'))]
    posts=[p for p in posts if p]
    posts.sort(key=lambda p:(p['date'],p['slug']),reverse=True)
    featured=next((p for p in posts if p['featured']),posts[0] if posts else None)
    novel_groups={}
    for post in posts:
        if post['category']=='小说创作' and post['series']:
            novel_groups.setdefault(post['series'],[]).append(post)
    for chapters in novel_groups.values():
        chapters.sort(key=lambda p:(p['chapter'] if p['chapter'] is not None else 999999,p['date'],p['slug']))
    novels=[{'title':title,'chapters':chapters,'count':len(chapters),'latest':max(p['date'] for p in chapters)} for title,chapters in novel_groups.items()]
    novels.sort(key=lambda w:w['latest'],reverse=True)
    shorts=[p for p in posts if p['category']=='小说创作' and not p['series']]
    poems=[p for p in posts if p['category']=='诗词创作']
    stats={'articles':len(posts),'novel_chapters':sum(1 for p in posts if p['category']=='小说创作'),'novel_works':len(novels)}
    novel_nav={}
    for work in novels:
        chapters=work['chapters']
        for i,p in enumerate(chapters):
            novel_nav[p['slug']]={'previous':chapters[i-1] if i else None,'next':chapters[i+1] if i+1<len(chapters) else None}

    env=jinja2.Environment(loader=jinja2.FileSystemLoader(str(TEMPLATE_DIR)),autoescape=True,trim_blocks=True,lstrip_blocks=True)
    dest.mkdir(parents=True,exist_ok=True)
    for name in ['styles.css','app.js','favicon.svg']:
        shutil.copy2(BASE/name,dest/name)
    shutil.copytree(BASE/'assets',dest/'assets',dirs_exist_ok=True)
    shutil.copytree(BASE/'media',dest/'media',dirs_exist_ok=True)
    site_url=str(site.get('siteUrl','')).strip().rstrip('/')
    now=dt.date.today().year
    def render(name,page,title,description,root='',post=None,additional=None):
        def cvt(p):
            clone=dict(p)
            clone['cover_for_page']=resource_url(p['cover'],root)
            clone['content']=rewrite_body_urls(p['content_raw'],root)
            return clone
        all_posts=[cvt(p) for p in posts]
        feat=next((p for p in all_posts if p['featured']),all_posts[0] if all_posts else None)
        canonical=None
        if site_url:
            current=post['url'] if post else ('index.html' if page=='home' else page+'.html')
            canonical=site_url+'/'+current
        og_image=site_url+'/assets/avatar.webp' if site_url else None
        context={'site':site,'page':page,'title':title,'description':description,'root':root,'year':now,
                 'posts':all_posts,'categories':CATS,'featured':feat,
                 'novels':novels,'shorts':shorts,'poems':poems,'stats':stats,
                 'post':cvt(post) if post else None,'canonical':canonical,'og_image':og_image}
        if additional:context.update(additional)
        target=dest/name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(env.get_template(('index' if page=='home' else page)+'.html').render(**context),encoding='utf-8')
    render('index.html','index' if False else 'home',f"{site['name']} · {site['author']} 的个人博客",str(site.get('intro','')))
    render('archive.html','archive',f"所有文章 · {site['name']}",f"{site['author']} 的文字归档")
    render('about.html','about',f"关于作者 · {site['name']}",str(site['bio']))
    render('novels.html','novels',f"小说目录 · {site['name']}",'在这里，故事按章节慢慢展开。')
    render('poetry.html','poetry',f"诗词创作 · {site['name']}",'写诗、填词，也写那些未曾说尽的话。')
    for i,post in enumerate(posts):
        other=posts[(i+1)%len(posts)] if len(posts)>1 else None
        render(post['url'],'article',f"{post['title']} · {site['name']}",post['excerpt'],root='../',post=post,additional={'next_post':other,'novel_nav':novel_nav.get(post['slug'])})
    (dest/'.nojekyll').write_text('',encoding='utf-8')
    if site_url:
        from xml.sax.saxutils import escape
        items=''.join(f'<item><title>{escape(p["title"])}</title><link>{escape(site_url+"/"+p["url"])}</link><guid>{escape(site_url+"/"+p["url"])}</guid><description>{escape(p["excerpt"])}</description></item>' for p in posts)
        rss=f'<?xml version="1.0" encoding="utf-8"?><rss version="2.0"><channel><title>{escape(site["name"])}</title><link>{escape(site_url)}</link><description>{escape(site.get("intro",""))}</description>{items}</channel></rss>'
        (dest/'feed.xml').write_text(rss,encoding='utf-8')
        (dest/'sitemap.xml').write_text('<?xml version="1.0" encoding="utf-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{escape(site_url+"/"+url)}</loc></url>' for url in ['index.html','about.html','archive.html','novels.html','poetry.html']+[p['url'] for p in posts])+'</urlset>',encoding='utf-8')
    print(f'✅ 构建完成：{len(posts)} 篇公开文章，{sum(1 for _ in SOURCES.glob("*.md"))-len(posts)} 篇草稿 → {dest}')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='dist')
    args=parser.parse_args()
    out=Path(args.output)
    if not out.is_absolute(): out=BASE/out
    build(out)
