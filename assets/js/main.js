// 立即应用保存的主题（避免闪烁）- 在 head 中已执行，这里作为备用
(function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark-mode');
    }
})();

// DOM 加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 主题切换功能
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    
    if (themeToggle) {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            themeToggle.textContent = '☀️';
        } else {
            themeToggle.textContent = '🌙';
        }
        
        themeToggle.addEventListener('click', function() {
            html.classList.toggle('dark-mode');
            
            if (html.classList.contains('dark-mode')) {
                localStorage.setItem('theme', 'dark');
                themeToggle.textContent = '☀️';
            } else {
                localStorage.setItem('theme', 'light');
                themeToggle.textContent = '🌙';
            }
        });
    }
    
    // 搜索功能
    const searchBox = document.getElementById('search-box');
    const searchResults = document.getElementById('search-results');
    
    if (searchBox) {
        let postsData = [];
        
        const postsDataElement = document.getElementById('posts-data');
        if (postsDataElement) {
            try {
                postsData = JSON.parse(postsDataElement.textContent);
            } catch (e) {
                console.error('解析文章数据失败:', e);
            }
        }
        
        searchBox.addEventListener('input', function() {
            const query = this.value.trim().toLowerCase();
            
            if (query.length === 0) {
                searchResults.innerHTML = '';
                return;
            }
            
            const results = postsData.filter(post => {
                return post.title.toLowerCase().includes(query) ||
                       post.excerpt.toLowerCase().includes(query) ||
                       (post.tags && post.tags.some(tag => tag.toLowerCase().includes(query)));
            });
            
            displayResults(results, query);
        });
        
        function displayResults(results, query) {
            if (results.length === 0) {
                searchResults.innerHTML = '<p style="text-align: center; color: #999;">没有找到相关文章</p>';
                return;
            }
            
            let html = '';
            results.forEach(post => {
                const highlightedTitle = highlightText(post.title, query);
                const highlightedExcerpt = highlightText(post.excerpt, query);
                
                html += `
                    <div class="search-result-item">
                        <a href="${post.url}">
                            <h4>${highlightedTitle}</h4>
                            <p>${highlightedExcerpt}</p>
                            <p class="date">【${post.date}】</p>
                        </a>
                    </div>
                `;
            });
            
            searchResults.innerHTML = html;
        }
        
        function highlightText(text, query) {
            if (!query) return text;
            const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
            return text.replace(regex, '<mark style="background-color: #ffeb3b; padding: 0 2px;">$1</mark>');
        }
        
        function escapeRegex(string) {
            return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        }
    }
    
    // 返回顶部功能
    const backToTop = document.getElementById('back-to-top');
    
    if (backToTop) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTop.style.display = 'block';
            } else {
                backToTop.style.display = 'none';
            }
        });
        
        backToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // 生成文章目录（TOC）
    generateTOC();
    
    // 代码高亮和复制功能
    enhanceCodeBlocks();
    
    // 阅读进度条
    initReadingProgress();
});

// 生成文章目录
function generateTOC() {
    const postContent = document.querySelector('.post-content');
    if (!postContent) return;
    
    const headings = postContent.querySelectorAll('h2, h3');
    if (headings.length < 2) return; // 如果标题太少，不生成目录
    
    // 为每个标题添加锚点
    headings.forEach((heading, index) => {
        const id = 'heading-' + index;
        heading.id = id;
    });
    
    // 生成目录 HTML
    let tocHTML = '<div class="toc"><h3>📑 目录</h3><ul>';
    
    headings.forEach((heading, index) => {
        const level = heading.tagName.toLowerCase();
        const text = heading.textContent;
        const id = 'heading-' + index;
        
        tocHTML += `<li class="toc-${level}"><a href="#${id}">${text}</a></li>`;
    });
    
    tocHTML += '</ul></div>';
    
    // 插入到文章开头
    postContent.insertAdjacentHTML('afterbegin', tocHTML);
}

// 代码高亮和复制功能
function enhanceCodeBlocks() {
    const codeBlocks = document.querySelectorAll('.post-content pre code');
    
    codeBlocks.forEach((codeBlock, index) => {
        const pre = codeBlock.parentElement;
        const code = codeBlock.textContent;
        
        // 检测语言
        const lang = detectLanguage(code);
        
        // 高亮代码
        const highlightedCode = highlightCode(code, lang);
        codeBlock.innerHTML = highlightedCode;
        
        // 包装代码块
        const wrapper = document.createElement('div');
        wrapper.className = 'code-block';
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);
        
        // 添加代码头部
        const header = document.createElement('div');
        header.className = 'code-header';
        header.innerHTML = `
            <span class="code-lang">${lang || 'code'}</span>
            <button class="copy-btn" data-index="${index}">复制</button>
        `;
        wrapper.insertBefore(header, pre);
        
        // 绑定复制事件
        const copyBtn = header.querySelector('.copy-btn');
        copyBtn.addEventListener('click', function() {
            navigator.clipboard.writeText(code).then(() => {
                copyBtn.textContent = '已复制!';
                copyBtn.classList.add('copied');
                
                setTimeout(() => {
                    copyBtn.textContent = '复制';
                    copyBtn.classList.remove('copied');
                }, 2000);
            }).catch(err => {
                console.error('复制失败:', err);
            });
        });
    });
}

// 检测代码语言
function detectLanguage(code) {
    // 简单的语言检测
    if (code.includes('def ') || code.includes('import ') && code.includes(':')) {
        return 'python';
    }
    if (code.includes('function') || code.includes('const ') || code.includes('let ')) {
        return 'javascript';
    }
    if (code.includes('<') && code.includes('>')) {
        return 'html';
    }
    if (code.includes('{') && code.includes('}') && code.includes(':')) {
        return 'json';
    }
    if (code.includes('$') || code.includes('npm') || code.includes('git')) {
        return 'bash';
    }
    return '';
}

// 简单的代码高亮
function highlightCode(code, lang) {
    // 转义 HTML
    let highlighted = code
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    
    // 高亮注释
    highlighted = highlighted.replace(/(\/\/.*$|#.*$)/gm, '<span class="code-comment">$1</span>');
    
    // 高亮字符串
    highlighted = highlighted.replace(/(".*?"|'.*?'|`.*?`)/g, '<span class="code-string">$1</span>');
    
    // 高亮关键字
    const keywords = ['function', 'const', 'let', 'var', 'if', 'else', 'for', 'while', 'return', 'class', 'import', 'from', 'def', 'print', 'True', 'False', 'None'];
    const keywordRegex = new RegExp(`\\b(${keywords.join('|')})\\b`, 'g');
    highlighted = highlighted.replace(keywordRegex, '<span class="code-keyword">$1</span>');
    
    // 高亮函数调用
    highlighted = highlighted.replace(/(\w+)(?=\()/g, '<span class="code-function">$1</span>');
    
    // 高亮数字
    highlighted = highlighted.replace(/\b(\d+)\b/g, '<span class="code-number">$1</span>');
    
    return highlighted;
}

// 阅读进度条
function initReadingProgress() {
    // 创建进度条元素
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    progressBar.id = 'reading-progress';
    document.body.appendChild(progressBar);
    
    // 获取文章区域
    const article = document.querySelector('.post-content') || document.querySelector('main');
    if (!article) return;
    
    // 监听滚动
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset;
        const docHeight = article.offsetHeight;
        const winHeight = window.innerHeight;
        
        // 计算阅读进度
        let progress = (scrollTop / (docHeight - winHeight)) * 100;
        progress = Math.min(100, Math.max(0, progress));
        
        progressBar.style.width = progress + '%';
    });
}
