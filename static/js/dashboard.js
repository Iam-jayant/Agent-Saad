// Agent Saad Dashboard - Modern Interactive UI

let currentFilters = {
    urgency: '',
    source: ''
};

// Theme Management
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.querySelector('.theme-icon');
const themeText = document.querySelector('.theme-text');

// Initialize theme from localStorage
const currentTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', currentTheme);
updateThemeUI(currentTheme);

themeToggle.addEventListener('click', () => {
    const theme = document.documentElement.getAttribute('data-theme');
    const newTheme = theme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeUI(newTheme);
    
    // Add ripple effect
    createRipple(themeToggle);
});

function updateThemeUI(theme) {
    if (theme === 'dark') {
        themeIcon.textContent = '☀️';
        themeText.textContent = 'Light Mode';
    } else {
        themeIcon.textContent = '🌙';
        themeText.textContent = 'Dark Mode';
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadStats();
    loadAlerts();
    setupEventListeners();
    animateOnScroll();
    
    // Auto-refresh every 30 seconds
    setInterval(() => {
        loadStats();
        loadAlerts();
    }, 30000);
    
    // Add loading animation
    setTimeout(() => {
        document.querySelectorAll('.stat-card').forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    card.style.transition = 'all 0.5s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, 50);
            }, index * 100);
        });
    }, 100);
});

function setupEventListeners() {
    // Button listeners
    document.getElementById('runMonitor').addEventListener('click', runMonitor);
    document.getElementById('testAlerts').addEventListener('click', testAlerts);
    document.getElementById('refreshData').addEventListener('click', refreshData);
    
    // Filter listeners
    document.getElementById('urgencyFilter').addEventListener('change', function(e) {
        currentFilters.urgency = e.target.value;
        loadAlerts();
        animateFilterChange();
    });
    
    document.getElementById('sourceFilter').addEventListener('change', function(e) {
        currentFilters.source = e.target.value;
        loadAlerts();
        animateFilterChange();
    });
    
    // Add ripple effect to all buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            createRipple(this, e);
        });
    });
}

// Ripple Effect
function createRipple(element, event) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    
    const size = Math.max(rect.width, rect.height);
    const x = event ? event.clientX - rect.left - size / 2 : rect.width / 2 - size / 2;
    const y = event ? event.clientY - rect.top - size / 2 : rect.height / 2 - size / 2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');
    
    element.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 600);
}

// Animate filter changes
function animateFilterChange() {
    const alertsList = document.getElementById('alertsList');
    alertsList.style.opacity = '0.5';
    setTimeout(() => {
        alertsList.style.opacity = '1';
    }, 200);
}

// Scroll animations
function animateOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });
    
    document.querySelectorAll('.alert-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.5s ease';
        observer.observe(card);
    });
}

// Load Statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (data.success) {
            const stats = data.stats;
            animateNumber('totalAlerts', stats.total_alerts || 0);
            animateNumber('criticalAlerts', stats.urgency_stats?.CRITICAL || 0);
            animateNumber('highAlerts', stats.urgency_stats?.HIGH || 0);
            animateNumber('recentAlerts', stats.recent_alerts_24h || 0);
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Animate numbers
function animateNumber(elementId, target) {
    const element = document.getElementById(elementId);
    const current = parseInt(element.textContent) || 0;
    const increment = Math.ceil((target - current) / 20);
    
    if (current === target) return;
    
    let value = current;
    const timer = setInterval(() => {
        value += increment;
        if ((increment > 0 && value >= target) || (increment < 0 && value <= target)) {
            value = target;
            clearInterval(timer);
        }
        element.textContent = value;
    }, 50);
}

// Load Alerts
async function loadAlerts() {
    try {
        const response = await fetch('/api/alerts?limit=100');
        const data = await response.json();
        
        if (data.success) {
            displayAlerts(data.alerts);
        }
    } catch (error) {
        console.error('Error loading alerts:', error);
        document.getElementById('alertsList').innerHTML = `
            <div class="loading">
                <div class="loader"></div>
                <p>Error loading alerts</p>
            </div>
        `;
    }
}

// Display Alerts
function displayAlerts(alerts) {
    const alertsList = document.getElementById('alertsList');
    
    if (!alerts || alerts.length === 0) {
        alertsList.innerHTML = `
            <div class="loading">
                <p style="color: var(--text-secondary);">No alerts found. Click "Run Monitor" to start scanning.</p>
            </div>
        `;
        return;
    }
    
    // Apply filters
    let filteredAlerts = alerts;
    if (currentFilters.urgency) {
        filteredAlerts = filteredAlerts.filter(a => a.urgency_level === currentFilters.urgency);
    }
    if (currentFilters.source) {
        filteredAlerts = filteredAlerts.filter(a => a.source === currentFilters.source);
    }
    
    if (filteredAlerts.length === 0) {
        alertsList.innerHTML = `
            <div class="loading">
                <p style="color: var(--text-secondary);">No alerts match your filters</p>
            </div>
        `;
        return;
    }
    
    alertsList.innerHTML = filteredAlerts.map(alert => createAlertCard(alert)).join('');
    
    // Re-observe for animations
    setTimeout(animateOnScroll, 100);
}

// Create Alert Card
function createAlertCard(alert) {
    const urgencyEmoji = {
        'CRITICAL': '🚨',
        'HIGH': '⚠️',
        'MEDIUM': '⚡',
        'LOW': 'ℹ️'
    }[alert.urgency_level] || 'ℹ️';
    
    const timeAgo = getTimeAgo(alert.created_at);
    const sentimentEmoji = alert.sentiment_label === 'NEGATIVE' ? '😠' : '😊';
    
    return `
        <div class="alert-card urgency-${alert.urgency_level}">
            <div class="alert-header">
                <div class="alert-meta">
                    <span class="badge urgency-${alert.urgency_level}">
                        ${urgencyEmoji} ${alert.urgency_level}
                    </span>
                    <span class="badge source">📍 ${alert.source}</span>
                    <span class="badge sentiment">
                        ${sentimentEmoji} ${alert.sentiment_label} 
                        <span style="opacity: 0.8;">(${(alert.sentiment_score || 0).toFixed(2)})</span>
                    </span>
                </div>
                <div class="alert-time">⏱️ ${timeAgo}</div>
            </div>
            
            <div class="alert-content">
                ${escapeHtml(alert.content)}
            </div>
            
            ${alert.recommended_response ? `
                <div class="alert-recommendation">
                    <strong>💡 Recommended Response:</strong>
                    ${escapeHtml(alert.recommended_response)}
                </div>
            ` : ''}
            
            <div class="alert-footer">
                <div class="alert-author">
                    👤 ${escapeHtml(alert.author || 'Unknown')}
                </div>
                ${alert.url ? `
                    <a href="${escapeHtml(alert.url)}" target="_blank" class="alert-link">
                        View Post →
                    </a>
                ` : ''}
            </div>
        </div>
    `;
}

// Time ago helper
function getTimeAgo(timestamp) {
    if (!timestamp) return 'Unknown time';
    
    const now = new Date();
    const time = new Date(timestamp);
    const diffInSeconds = Math.floor((now - time) / 1000);
    
    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`;
    return time.toLocaleDateString();
}

// Escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Run Monitor
async function runMonitor() {
    const btn = document.getElementById('runMonitor');
    btn.disabled = true;
    btn.innerHTML = '<span class="btn-icon">⏳</span><span>Running...</span>';
    
    showToast('Running monitor... Scanning social media for mentions.', 'info');
    
    try {
        const response = await fetch('/api/monitor/run', {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            const results = data.results;
            showToast(
                `✅ Monitor completed! Found ${results.total_processed} items, created ${results.alerts_created} new alerts.`,
                'success'
            );
            
            // Refresh data with animation
            setTimeout(() => {
                loadStats();
                loadAlerts();
            }, 1000);
        } else {
            showToast(`❌ Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Error running monitor:', error);
        showToast('❌ Failed to run monitor. Check console for details.', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span class="btn-icon">▶️</span><span>Run Monitor</span>';
    }
}

// Test Alerts
async function testAlerts() {
    const btn = document.getElementById('testAlerts');
    btn.disabled = true;
    btn.innerHTML = '<span class="btn-icon">⏳</span><span>Testing...</span>';
    
    showToast('🧪 Sending test alerts to Slack and Email...', 'info');
    
    try {
        const response = await fetch('/api/test/alerts', {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            let message = '✅ Test alert created! ';
            if (data.slack_sent) message += '📱 Slack ✓ ';
            if (data.email_sent) message += '📧 Email ✓ ';
            if (!data.slack_sent && !data.email_sent) {
                message += '⚠️ No notifications sent (check configuration).';
            }
            
            showToast(message, 'success');
            
            // Refresh alerts
            setTimeout(() => {
                loadStats();
                loadAlerts();
            }, 1000);
        } else {
            showToast(`❌ Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Error testing alerts:', error);
        showToast('❌ Failed to send test alerts. Check console for details.', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span class="btn-icon">🧪</span><span>Test Alerts</span>';
    }
}

// Refresh Data
function refreshData() {
    const btn = document.getElementById('refreshData');
    btn.style.transform = 'rotate(360deg)';
    
    showToast('🔄 Refreshing data...', 'info');
    loadStats();
    loadAlerts();
    
    setTimeout(() => {
        btn.style.transform = 'rotate(0deg)';
    }, 600);
}

// Toast Notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 5000);
}

// Add CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .btn {
        position: relative;
        overflow: hidden;
    }
`;
document.head.appendChild(style);
