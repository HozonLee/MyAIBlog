# 我的博客

这是一个基于GitHub Pages的个人博客，用于分享留学、语言学习、AI技术、工作和海外生活方面的内容。

## 项目结构

```
blog/
├── _posts/         # 博客文章（Markdown格式）
├── weekly/         # 潮流周刊
│   └── index.html  # 周刊列表页面
├── about/          # 关于页面
│   └── index.html  # 关于页面内容
├── assets/         # 静态资源
│   ├── css/        # CSS样式文件
│   └── images/     # 图片文件
├── index.html      # 首页
├── .gitignore      # Git忽略文件
└── README.md       # 项目说明
```

## 如何使用

### 1. 克隆仓库

```bash
git clone <your-repository-url>
cd blog
```

### 2. 添加内容

- **博客文章**：在 `_posts` 目录中创建 Markdown 文件，文件名格式为 `YYYY-MM-DD-title.md`
- **周刊内容**：在 `weekly` 目录中创建新的页面或更新 `index.html`
- **图片**：将图片放在 `assets/images` 目录中

### 3. 部署到GitHub Pages

1. 确保你的仓库名为 `<username>.github.io`
2. 将代码推送到 GitHub 仓库的 `main` 分支
3. 在 GitHub 仓库的设置中，找到 "Pages" 选项
4. 选择 "main" 分支作为构建源，点击 "Save"
5. 等待几分钟，你的博客就会在 `https://<username>.github.io` 上可用

## 自定义

- **修改样式**：编辑 `assets/css/style.css` 文件
- **修改页面内容**：编辑对应的 HTML 文件
- **添加新页面**：在根目录或子目录中创建新的 HTML 文件

## 特点

- 简洁的设计风格
- 响应式布局，适配不同设备
- 支持 Markdown 写作
- 易于部署和维护
- 完全托管在 GitHub 上，免费使用
