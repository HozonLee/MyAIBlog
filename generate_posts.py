#!/usr/bin/env python3
import os
import re
from datetime import datetime

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

def generate_html_post(frontmatter, body_html, filename):
    title = frontmatter.get('title', '未命名文章')
    date = frontmatter.get('date', datetime.now().strftime('%Y-%m-%d'))
    tags = frontmatter.get('tags', '')
    
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 我的博客</title>
    <link rel="stylesheet" href="../assets/css/style.css">
    <style>
        .post-content {{
            line-height: 1.8;
        }}
        .post-content h1 {{
            font-size: 28px;
            margin-bottom: 20px;
            color: #333;
        }}
        .post-content h2 {{
            font-size: 24px;
            margin-top: 30px;
            margin-bottom: 15px;
            color: #333;
        }}
        .post-content h3 {{
            font-size: 20px;
            margin-top: 25px;
            margin-bottom: 10px;
            color: #333;
        }}
        .post-content p {{
            margin-bottom: 15px;
        }}
        .post-content ul {{
            margin-left: 20px;
            margin-bottom: 15px;
        }}
        .post-content li {{
            margin-bottom: 8px;
        }}
        .post-content pre {{
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin-bottom: 15px;
        }}
        .post-content code {{
            font-family: 'Courier New', monospace;
            background-color: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
        }}
        .post-content pre code {{
            background-color: transparent;
            padding: 0;
        }}
        .post-meta {{
            color: #999;
            margin-bottom: 20px;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #666;
            text-decoration: none;
        }}
        .back-link:hover {{
            color: #000;
        }}
    </style>
</head>
<body>
    <header>
        <h1><a href="../index.html">我的博客</a></h1>
        <nav>
            <a href="../index.html">首页</a>
            <a href="../weekly/index.html">潮流周刊</a>
            <a href="../about/index.html">关于</a>
        </nav>
    </header>
    <main>
        <section class="post">
            <a href="../index.html" class="back-link">← 返回首页</a>
            <div class="post-meta">
                <p>发布日期：{date}</p>
                <p>标签：{tags}</p>
            </div>
            <div class="post-content">
                {body_html}
            </div>
        </section>
    </main>
    <footer>
        <p>&copy; 2026 我的博客</p>
        <div class="social-links">
            <a href="https://github.com/HozonLee">GitHub</a>
            <a href="https://twitter.com/yourusername">Twitter</a>
            <a href="https://linkedin.com/in/yourusername">LinkedIn</a>
            <a href="mailto:your.email@example.com">Email</a>
        </div>
    </footer>
</body>
</html>'''
    
    return html_template

def update_index_html(posts):
    posts_html = ''
    for post in sorted(posts, key=lambda x: x['date'], reverse=True):
        posts_html += f'''                <li>
                    <a href="{post['url']}">
                        <h3>{post['title']}</h3>
                        <p class="date">{post['date']}</p>
                        <p>{post['excerpt']}</p>
                    </a>
                </li>
'''
    
    index_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的博客</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <header>
        <h1><a href="index.html">我的博客</a></h1>
        <nav>
            <a href="index.html">首页</a>
            <a href="weekly/index.html">潮流周刊</a>
            <a href="about/index.html">关于</a>
        </nav>
    </header>
    <main>
        <section class="posts">
            <h2>最新文章</h2>
            <ul>
{posts_html}
            </ul>
        </section>
    </main>
    <footer>
        <p>&copy; 2026 我的博客</p>
        <div class="social-links">
            <a href="https://github.com/HozonLee">GitHub</a>
            <a href="https://twitter.com/yourusername">Twitter</a>
            <a href="https://linkedin.com/in/yourusername">LinkedIn</a>
            <a href="mailto:your.email@example.com">Email</a>
        </div>
    </footer>
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
            
            html_content = generate_html_post(frontmatter, body_html, html_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            excerpt = body.split('\n')[0] if body else ''
            excerpt = re.sub(r'<[^>]+>', '', excerpt)
            excerpt = excerpt[:100] + '...' if len(excerpt) > 100 else excerpt
            
            posts.append({
                'title': frontmatter.get('title', '未命名文章'),
                'date': frontmatter.get('date', datetime.now().strftime('%Y-%m-%d')),
                'url': f'posts/{html_filename}',
                'excerpt': excerpt
            })
            
            print(f"已生成：{output_path}")
    
    update_index_html(posts)
    print(f"已更新：index.html")
    print(f"总共生成 {len(posts)} 篇文章")

if __name__ == '__main__':
    main()
