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
        // 更新按钮图标
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            themeToggle.textContent = '☀️';
        } else {
            themeToggle.textContent = '🌙';
        }
        
        // 切换主题
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
});
