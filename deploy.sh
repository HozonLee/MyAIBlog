#!/bin/bash

# 博客部署脚本 - 同时推送到 MyAIBlog 和 hozonlee.github.io

# 设置路径
BLOG_DIR="/Users/hozon/Documents/trae_projects/blog"
MAIN_REPO_DIR="/Users/hozon/Documents/trae_projects/hozonlee.github.io"

# 获取提交信息
if [ -z "$1" ]; then
    echo "请输入提交信息："
    read commit_msg
else
    commit_msg="$1"
fi

echo "======================================"
echo "开始部署博客..."
echo "提交信息: $commit_msg"
echo "======================================"

# 步骤 1: 在 blog 目录生成 HTML
echo ""
echo "步骤 1/5: 生成 HTML 文件..."
cd "$BLOG_DIR"
python3 generate_posts.py
if [ $? -ne 0 ]; then
    echo "❌ 生成 HTML 失败"
    exit 1
fi
echo "✅ HTML 文件生成成功"

# 步骤 2: 复制文件到主仓库
echo ""
echo "步骤 2/5: 复制文件到 hozonlee.github.io..."
cp -r "$BLOG_DIR"/* "$MAIN_REPO_DIR/"
if [ $? -ne 0 ]; then
    echo "❌ 复制文件失败"
    exit 1
fi
echo "✅ 文件复制成功"

# 步骤 3: 推送到 MyAIBlog 仓库
echo ""
echo "步骤 3/5: 推送到 MyAIBlog 仓库..."
cd "$BLOG_DIR"
git add .
git commit -m "$commit_msg"
if [ $? -ne 0 ]; then
    echo "⚠️  MyAIBlog 仓库没有变化，跳过提交"
else
    git push origin main
    if [ $? -ne 0 ]; then
        echo "❌ 推送到 MyAIBlog 失败"
        exit 1
    fi
    echo "✅ MyAIBlog 推送成功"
fi

# 步骤 4: 推送到 hozonlee.github.io 仓库
echo ""
echo "步骤 4/5: 推送到 hozonlee.github.io 仓库..."
cd "$MAIN_REPO_DIR"
git add .
git commit -m "$commit_msg"
if [ $? -ne 0 ]; then
    echo "⚠️  hozonlee.github.io 仓库没有变化，跳过提交"
else
    git push origin main
    if [ $? -ne 0 ]; then
        echo "❌ 推送到 hozonlee.github.io 失败"
        exit 1
    fi
    echo "✅ hozonlee.github.io 推送成功"
fi

# 完成
echo ""
echo "======================================"
echo "🎉 博客部署完成！"
echo "======================================"
echo ""
echo "博客地址: https://hozonlee.github.io/"
echo "备用地址: https://hozonlee.github.io/MyAIBlog/"
echo ""
echo "等待 GitHub Pages 部署（约 1-2 分钟）..."
