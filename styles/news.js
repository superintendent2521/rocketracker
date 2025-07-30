class NewsManager {
    constructor() {
        this.apiUrl = '/api/news';  // This might need to be just '/api/news' instead
        this.newsList = document.getElementById('newsList');
        this.newsForm = document.getElementById('newsForm');
        this.contentTextarea = document.getElementById('content');
        this.previewDiv = document.getElementById('preview');
        
        this.init();
    }

    init() {
        if (this.newsList) {
            this.loadNewsPosts();
        }
        this.setupFormSubmission();
        this.setupMarkdownPreview();
    }

    setupFormSubmission() {
        this.newsForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(this.newsForm);
            const postData = {
                title: formData.get('title').trim(),
                author: formData.get('author').trim(),
                content: formData.get('content').trim()
            };

            // Basic client-side validation
            if (!postData.title || !postData.author || !postData.content) {
                this.showMessage('Please fill in all required fields', 'error');
                return;
            }

            if (postData.title.length > 100) {
                this.showMessage('Title must be 100 characters or less', 'error');
                return;
            }

            if (postData.author.length > 50) {
                this.showMessage('Author name must be 50 characters or less', 'error');
                return;
            }

            if (postData.content.length > 1000) {
                this.showMessage('Content must be 1000 characters or less', 'error');
                return;
            }

            await this.submitNewsPost(postData);
        });
    }

    setupMarkdownPreview() {
        this.contentTextarea.addEventListener('input', () => {
            const content = this.contentTextarea.value;
            const html = marked.parse(content);
            this.previewDiv.innerHTML = html;
        });
    }

     async submitNewsPost(postData) {
        const submitBtn = this.newsForm.querySelector('.submit-btn');
        const originalText = submitBtn.textContent;
        
        try {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';

            const response = await fetch(`${this.apiUrl}/post`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(postData)
            });

            const result = await response.json();

            if (response.ok) {
                this.showMessage('News post submitted successfully!', 'success');
                this.newsForm.reset();
                this.previewDiv.innerHTML = '';
                await this.loadNewsPosts();
            } else {
                // Only show server messages if they exist, skip generic "failed to submit"
                if (result.detail) {
                    this.showMessage(result.detail, 'error');
                }
            }
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    }

    async loadNewsPosts() {
        try {
            this.newsList.innerHTML = '<div class="loading">Loading news posts...</div>';
            
            const response = await fetch(this.apiUrl);
            
            if (!response.ok) {
                throw new Error('Failed to load news posts');
            }

            const posts = await response.json();
            this.renderNewsPosts(posts);
        } catch (error) {
            console.error('Error loading news posts:', error);
            this.newsList.innerHTML = `
                <div class="error">
                    Failed to load news posts. Please refresh the page.
                </div>
            `;
        }
    }

    renderNewsPosts(posts) {
        if (!posts || posts.length === 0) {
            this.newsList.innerHTML = `
                <div class="empty-state">
                    <h3>No news posts yet</h3>
                    <p>Be the first to share some news!</p>
                </div>
            `;
            return;
        }

        const postsHtml = posts.map(post => this.createPostHtml(post)).join('');
        this.newsList.innerHTML = postsHtml;
    }

    createPostHtml(post) {
        const formattedDate = new Date(post.timestamp).toLocaleString();
        const contentHtml = marked.parse(post.content);
        
        return `
            <div class="news-post">
                <div class="news-post-header">
                    <h3 class="news-post-title">${this.escapeHtml(post.title)}</h3>
                    <div class="news-post-meta">
                        <div class="news-post-author">${this.escapeHtml(post.author)}</div>
                        <div class="news-post-timestamp">${formattedDate}</div>
                    </div>
                </div>
                <div class="news-post-content">
                    ${contentHtml}
                </div>
            </div>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showMessage(message, type) {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.error, .success');
        existingMessages.forEach(msg => msg.remove());

        const messageDiv = document.createElement('div');
        messageDiv.className = type;
        messageDiv.textContent = message;
        
        this.newsForm.parentNode.insertBefore(messageDiv, this.newsForm);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.remove();
            }
        }, 5000);
    }
}

// Initialize the news manager when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new NewsManager();
});
