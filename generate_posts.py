#!/usr/bin/env python3
import os
import re
from datetime import datetime
from xml.sax.saxutils import escape

def parse_frontmatter(content):
    frontmatter = {}
    body = content
    
    if content.startswith('---'):
        end_index = content.find('---', 3)
        if end_index != -1:
            frontmatter_text = content[3:end_index]
            body = content[end_index + 3:].strip()
            
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')
    
    return frontmatter, body

def markdown_to_html(markdown_text):
    html = markdown_text
    
    html = re.sub(r'### (.+)', r'<h3>\1</h3>', html)
    html = re.sub(r'## (.+)', r'<h2>\1</h2>', html)
    html = re.sub(r'# (.+)', r'<h1>\1</h1>', html)
    
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    html = re.sub(r'```(\w+)?\n([\s\S]*?)```', r'<pre><code>\2</code></pre>', html)
    
    html = re.sub(r'^- (.+)', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    html = re.sub(r'(<li>.*</li>\n)+', lambda m: '<ul>' + m.group(0) + '</ul>', html)
    
    html = re.sub(r'^\d+\. (.+)', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    html = re.sub(r'^(.+)$', r'<p>\1</p>', html, flags=re.MULTILINE)
    
    html = re.sub(r'<p>(<h[1-6]>.*</h[1-6]>)?</p>', r'\1', html)
    html = re.sub(r'<p>(<ul>.*</ul>)?</p>', r'\1', html)
    html = re.sub(r'<p>(<pre>.*</pre>)?</p>', r'\1', html)
    html = re.sub(r'<p>(<li>.*</li>)?</p>', r'\1', html)
    html = re.sub(r'<p></p>', '', html)
    
    return html

def generate_html_post(frontmatter, body_html, filename, posts_json):
    title = frontmatter.get('title', '未命名文章')
    date = frontmatter.get('date', datetime.now().strftime('%Y-%m-%d'))
    tags = frontmatter.get('tags', '')
    
    # 处理标签
    tags_html = ''
    tags_list = []
    if tags:
        tag_list = tags.strip('[]').split(',')
        tags_html = '<div class="tags">'
        for tag in tag_list:
            tag = tag.strip()
            if tag:
                tags_list.append(tag)
                tags_html += f'<span class="tag">{tag}</span>'
        tags_html += '</div>'
    
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 佑值的技术博客</title>
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="alternate" type="application/rss+xml" title="佑值的技术博客 RSS" href="../feed.xml">
    <script>if(localStorage.getItem('theme')==='dark')document.documentElement.classList.add('dark-mode');</script>
</head>
<body>
    <button id="theme-toggle" class="theme-toggle" title="切换主题">🌙</button>
    
    <header>
        <h1><a href="../index.html">佑值的技术博客</a></h1>
        <p class="tagline">Be yourself and don't go with the flow.</p>
        <nav>
            <a href="../index.html">首页</a>
            <a href="../weekly/index.html">潮流周刊</a>
            <a href="../about/index.html">关于</a>
            <a href="../tags/index.html">标签</a>
            <div class="search-container">
                <input type="text" id="search-box" class="search-box" placeholder="搜索..." autocomplete="off">
                <div id="search-results" class="search-results"></div>
            </div>
        </nav>
    </header>
    <main>
        <section class="post">
            <a href="../index.html" class="back-link">← 返回首页</a>
            <div class="post-meta">
                <p>【{date}】</p>
                {tags_html}
            </div>
            <div class="post-content">
                {body_html}
            </div>
        </section>
        
        <!-- Utterances 评论系统 -->
        <section class="comments">
            <script src="https://utteranc.es/client.js"
                repo="HozonLee/MyAIBlog"
                issue-term="pathname"
                label="comment"
                theme="github-light"
                crossorigin="anonymous"
                async>
            </script>
        </section>
    </main>
    <footer>
        <div class="social-links">
            <a href="https://github.com/HozonLee">GitHub</a>
            <a href="https://twitter.com/yourusername">Twitter</a>
            <a href="https://linkedin.com/in/yourusername">LinkedIn</a>
            <a href="mailto:your.email@example.com">Email</a>
            <a href="../feed.xml" class="rss-link" title="RSS 订阅">📡 RSS</a>
        </div>
        <p>&copy; 2026 佑值的技术博客</p>
    </footer>
    
    <script id="posts-data" type="application/json">{posts_json}</script>
    <script src="../assets/js/main.js"></script>
    <!-- Umami 网站统计 -->
    <script defer src="https://cloud.umami.is/script.js" data-website-id="91404383-bdec-43de-9eb4-32d927053f11"></script>
    
    <button id="back-to-top" class="theme-toggle" style="bottom: 20px; top: auto; display: none;" title="返回顶部">↑</button>
</body>
</html>'''
    
    return html_template

def generate_rss_feed(posts):
    """生成 RSS feed"""
    site_url = "https://hozonlee.github.io/MyAIBlog"
    current_time = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    
    rss_items = ""
    for post in sorted(posts, key=lambda x: x['date'], reverse=True)[:20]:  # 最近20篇
        pub_date = datetime.strptime(post['date'], '%Y-%m-%d').strftime('%a, %d %b %Y 00:00:00 +0000')
        rss_items += f"""
    <item>
      <title>{escape(post['title'])}</title>
      <link>{site_url}/{post['url']}</link>
      <guid>{site_url}/{post['url']}</guid>
      <pubDate>{pub_date}</pubDate>
      <description>{escape(post['excerpt'])}</description>
    </item>"""
    
    rss_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>佑值的技术博客</title>
    <link>{site_url}</link>
    <description>分享留学、语言、AI、工作、海外生活的个人博客</description>
    <language>zh-CN</language>
    <lastBuildDate>{current_time}</lastBuildDate>
    <atom:link href="{site_url}/feed.xml" rel="self" type="application/rss+xml" />{rss_items}
  </channel>
</rss>"""
    
    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(rss_template)
    print("已生成：feed.xml")

def generate_tag_pages(posts):
    tags_dir = 'tags'
    if not os.path.exists(tags_dir):
        os.makedirs(tags_dir)
    
    # 收集所有标签
    all_tags = {}
    for post in posts:
        if 'tags' in post:
            for tag in post['tags']:
                if tag not in all_tags:
                    all_tags[tag] = []
                all_tags[tag].append(post)
    
    # 为每个标签生成页面
    for tag, tag_posts in all_tags.items():
        tag_posts_html = ''
        for post in sorted(tag_posts, key=lambda x: x['date'], reverse=True):
            tag_posts_html += f'''                <li>
                    <a href="../{post['url']}">
                        <h3>{post['title']}</h3>
                        <p class="date">【{post['date']}】</p>
                        <p>{post['excerpt']}</p>
                    </a>
                </li>
'''
        
        tag_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>标签：{tag} - 佑值的技术博客</title>
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="alternate" type="application/rss+xml" title="佑值的技术博客 RSS" href="../feed.xml">
    <script>if(localStorage.getItem('theme')==='dark')document.documentElement.classList.add('dark-mode');</script>
</head>
<body>
    <button id="theme-toggle" class="theme-toggle" title="切换主题">🌙</button>
    
    <header>
        <h1><a href="../index.html">佑值的技术博客</a></h1>
        <p class="tagline">Be yourself and don't go with the flow.</p>
        <nav>
            <a href="../index.html">首页</a>
            <a href="../weekly/index.html">潮流周刊</a>
            <a href="../about/index.html">关于</a>
            <a href="index.html">标签</a>
            <div class="search-container">
                <input type="text" id="search-box" class="search-box" placeholder="搜索..." autocomplete="off">
                <div id="search-results" class="search-results"></div>
            </div>
        </nav>
    </header>
    <main>
        <section class="posts">
            <h2>标签：{tag}</h2>
            <ul>
{tag_posts_html}
            </ul>
        </section>
    </main>
    <footer>
        <div class="social-links">
            <a href="https://github.com/HozonLee">GitHub</a>
            <a href="https://twitter.com/yourusername">Twitter</a>
            <a href="https://linkedin.com/in/yourusername">LinkedIn</a>
            <a href="mailto:your.email@example.com">Email</a>
            <a href="../feed.xml" class="rss-link" title="RSS 订阅">📡 RSS</a>
        </div>
        <p>&copy; 2026 佑值的技术博客</p>
    </footer>
    
    <script src="../assets/js/main.js"></script>
    <!-- Umami 网站统计 -->
    <script defer src="https://cloud.umami.is/script.js" data-website-id="91404383-bdec-43de-9eb4-32d927053f11"></script>
</body>
</html>'''
        
        tag_file = os.path.join(tags_dir, f'{tag}.html')
        with open(tag_file, 'w', encoding='utf-8') as f:
            f.write(tag_template)
        print(f"已生成：{tag_file}")
    
    # 生成标签索引页面
    tags_index_html = ''
    for tag, tag_posts in sorted(all_tags.items()):
        tags_index_html += f'''                <li>
                    <a href="{tag}.html">
                        <span>{tag}</span>
                        <span class="tag-count">({len(tag_posts)})</span>
                    </a>
                </li>
'''
    
    tags_index_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>标签 - 佑值的技术博客</title>
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="alternate" type="application/rss+xml" title="佑值的技术博客 RSS" href="../feed.xml">
    <script>if(localStorage.getItem('theme')==='dark')document.documentElement.classList.add('dark-mode');</script>
</head>
<body>
    <button id="theme-toggle" class="theme-toggle" title="切换主题">🌙</button>
    
    <header>
        <h1><a href="../index.html">佑值的技术博客</a></h1>
        <p class="tagline">Be yourself and don't go with the flow.</p>
        <nav>
            <a href="../index.html">首页</a>
            <a href="../weekly/index.html">潮流周刊</a>
            <a href="../about/index.html">关于</a>
            <a href="index.html">标签</a>
            <div class="search-container">
                <input type="text" id="search-box" class="search-box" placeholder="搜索..." autocomplete="off">
                <div id="search-results" class="search-results"></div>
            </div>
        </nav>
    </header>
    <main>
        <section class="posts">
            <h2>标签</h2>
            <ul>
{tags_index_html}
            </ul>
        </section>
    </main>
    <footer>
        <div class="social-links">
            <a href="https://github.com/HozonLee">GitHub</a>
            <a href="https://twitter.com/yourusername">Twitter</a>
            <a href="https://linkedin.com/in/yourusername">LinkedIn</a>
            <a href="mailto:your.email@example.com">Email</a>
            <a href="../feed.xml" class="rss-link" title="RSS 订阅">📡 RSS</a>
        </div>
        <p>&copy; 2026 佑值的技术博客</p>
    </footer>
    
    <script src="../assets/js/main.js"></script>
    <!-- Umami 网站统计 -->
    <script defer src="https://cloud.umami.is/script.js" data-website-id="91404383-bdec-43de-9eb4-32d927053f11"></script>
</body>
</html>'''
    
    tags_index_file = os.path.join(tags_dir, 'index.html')
    with open(tags_index_file, 'w', encoding='utf-8') as f:
        f.write(tags_index_template)
    print(f"已生成：{tags_index_file}")

def update_index_html(posts, posts_json):
    posts_html = ''
    for post in sorted(posts, key=lambda x: x['date'], reverse=True):
        posts_html += f'''                <li>
                    <a href="{post['url']}">
                        <h3>{post['title']}</h3>
                        <p class="date">【{post['date']}】</p>
                        <p>{post['excerpt']}</p>
                    </a>
                </li>
'''
    
    index_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>佑值的技术博客</title>
    <link rel="stylesheet" href="assets/css/style.css">
    <link rel="alternate" type="application/rss+xml" title="佑值的技术博客 RSS" href="feed.xml">
    <script>if(localStorage.getItem('theme')==='dark')document.documentElement.classList.add('dark-mode');</script>
</head>
<body>
    <button id="theme-toggle" class="theme-toggle" title="切换主题">🌙</button>
    
    <header>
        <h1><a href="index.html">佑值的技术博客</a></h1>
        <p class="tagline">Be yourself and don't go with the flow.</p>
        <nav>
            <a href="index.html">首页</a>
            <a href="weekly/index.html">潮流周刊</a>
            <a href="about/index.html">关于</a>
            <a href="tags/index.html">标签</a>
        </nav>
    </header>
    <main>
        <!-- 搜索框 -->
        <section class="search-container">
            <input type="text" id="search-box" class="search-box" placeholder="搜索文章..." autocomplete="off">
            <div id="search-results" class="search-results"></div>
        </section>
        
        <section class="posts">
            <ul>
{posts_html}
            </ul>
        </section>
    </main>
    <footer>
        <div class="social-links">
            <a href="https://github.com/HozonLee">GitHub</a>
            <a href="https://twitter.com/yourusername">Twitter</a>
            <a href="https://linkedin.com/in/yourusername">LinkedIn</a>
            <a href="mailto:your.email@example.com">Email</a>
            <a href="feed.xml" class="rss-link" title="RSS 订阅">📡 RSS</a>
        </div>
        <p>&copy; 2026 佑值的技术博客</p>
    </footer>
    
    <button id="back-to-top" class="theme-toggle" style="bottom: 20px; top: auto; display: none;" title="返回顶部">↑</button>
    
    <script id="posts-data" type="application/json">{posts_json}</script>
    <script src="assets/js/main.js"></script>
    <!-- Umami 网站统计 -->
    <script defer src="https://cloud.umami.is/script.js" data-website-id="91404383-bdec-43de-9eb4-32d927053f11"></script>
</body>
</html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_template)

def main():
    posts_dir = '_posts'
    output_dir = 'posts'
    
    if not os.path.exists(posts_dir):
        print(f"错误：找不到 {posts_dir} 目录")
        return
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    posts = []
    
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(posts_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, body = parse_frontmatter(content)
            body_html = markdown_to_html(body)
            
            html_filename = filename.replace('.md', '.html')
            output_path = os.path.join(output_dir, html_filename)
            
            excerpt = body.split('\n')[0] if body else ''
            excerpt = re.sub(r'<[^>]+>', '', excerpt)
            excerpt = excerpt[:150] + '...' if len(excerpt) > 150 else excerpt
            
            # 处理标签
            tags = []
            if 'tags' in frontmatter and frontmatter['tags']:
                tag_list = frontmatter['tags'].strip('[]').split(',')
                for tag in tag_list:
                    tag = tag.strip()
                    if tag:
                        tags.append(tag)
            
            posts.append({
                'title': frontmatter.get('title', '未命名文章'),
                'date': frontmatter.get('date', datetime.now().strftime('%Y-%m-%d')),
                'url': f'posts/{html_filename}',
                'excerpt': excerpt,
                'tags': tags
            })
    
    # 生成文章数据 JSON
    import json
    posts_json = json.dumps(posts, ensure_ascii=False)
    
    # 生成每篇文章的 HTML
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(posts_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, body = parse_frontmatter(content)
            body_html = markdown_to_html(body)
            
            html_filename = filename.replace('.md', '.html')
            output_path = os.path.join(output_dir, html_filename)
            
            html_content = generate_html_post(frontmatter, body_html, html_filename, posts_json)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"已生成：{output_path}")
    
    # 生成 RSS feed
    generate_rss_feed(posts)
    
    # 更新首页
    update_index_html(posts, posts_json)
    print("已更新：index.html")
    
    # 生成标签页面
    generate_tag_pages(posts)
    
    print(f"总共生成 {len(posts)} 篇文章")

if __name__ == '__main__':
    main()
