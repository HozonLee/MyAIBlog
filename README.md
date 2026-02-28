# 佑值的技术博客

沪漂程序员的技术博客，分享关于留学、语言、AI、工作和海外生活的内容。

## 🚀 快速开始

### 添加新文章

1. 在 `_posts/` 目录下创建新的 Markdown 文件，文件名格式：`YYYY-MM-DD-文章标题.md`
2. 在文件开头添加 frontmatter：

```markdown
---
title: 文章标题
date: 2026-02-28
tags: 标签1, 标签2, 标签3
---
```

3. 编写文章内容（使用 Markdown 语法）

### 部署博客

使用自动部署脚本，一键推送到两个仓库：

```bash
./deploy.sh "提交信息"
```

如果不提供提交信息，脚本会提示你输入。

部署脚本会自动完成以下步骤：
1. 生成 HTML 文件
2. 复制文件到 hozonlee.github.io 仓库
3. 推送到 MyAIBlog 仓库
4. 推送到 hozonlee.github.io 仓库

## 📝 博客地址

- 主域名：https://hozonlee.github.io/
- 备用地址：https://hozonlee.github.io/MyAIBlog/

## 🛠️ 技术栈

- 静态 HTML/CSS/JavaScript
- Markdown 内容管理
- Python 自动化脚本
- GitHub Pages 部署

## 📦 目录结构

```
blog/
├── _posts/           # Markdown 文章源文件
├── posts/            # 生成的 HTML 文章页面
├── about/            # 关于页面
├── weekly/           # 潮流周刊页面
├── tags/             # 标签页面
├── assets/           # 静态资源
│   ├── css/         # 样式文件
│   └── js/          # JavaScript 文件
├── generate_posts.py # 文章生成脚本
├── deploy.sh         # 自动部署脚本
└── index.html       # 首页
```

## ✨ 功能特性

- 📝 Markdown 写作
- 🏷️ 标签分类
- 🔍 全文搜索
- 🌓 深色/浅色模式切换
- 📡 RSS 订阅
- 💬 Giscus 评论系统
- 📊 Umami 网站统计
- 📖 文章目录
- 📜 阅读进度条
- 📋 代码复制功能

## 📄 许可证

MIT License
