// 主题切换功能
(function() {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    
    // 从 localStorage 读取主题设置
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
        themeToggle.textContent = '☀️';
    } else {
        themeToggle.textContent = '🌙';
    }
    
    // 切换主题
    themeToggle.addEventListener('click', function() {
        body.classList.toggle('dark-mode');
        
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
            themeToggle.textContent = '☀️';
        } else {
            localStorage.setItem('theme', 'light');
            themeToggle.textContent = '🌙';
        }
    });
})();

// 搜索功能
(function() {
    const searchBox = document.getElementById('search-box');
    const searchResults = document.getElementById('search-results');
    
    if (!searchBox) return;
    
    // 文章数据（会在生成时注入）
    let postsData = [];
    
    // 从页面获取文章数据
    const postsDataElement = document.getElementById('posts-data');
    if (postsDataElement) {
        try {
            postsData = JSON.parse(postsDataElement.textContent);
        } catch (e) {
            console.error('解析文章数据失败:', e);
        }
    }
    
    // 搜索功能
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
            // 高亮匹配的关键词
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
})();

// 返回顶部功能
(function() {
    const backToTop = document.getElementById('back-to-top');
    
    if (!backToTop) return;
    
    // 显示/隐藏返回顶部按钮
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTop.style.display = 'block';
        } else {
            backToTop.style.display = 'none';
        }
    });
    
    // 点击返回顶部
    backToTop.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
})();
