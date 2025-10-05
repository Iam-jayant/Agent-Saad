// Dashboard JavaScript

let currentFilters = {
    urgency: '',
    source: ''
};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadStats();
    loadAlerts();
    setupEventListeners();
    
    // Auto-refresh every 30 seconds
    setInterval(() => {
        loadStats();
        loadAlerts();
    }, 30000);
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
    });
    
    document.getElementById('sourceFilter').addEventListener('change', function(e) {
        currentFilters.source = e.target.value;
        loadAlerts();
    });
}

async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (data.success) {
            const stats = data.stats;
            document.getElementById('totalAlerts').textContent = stats.total_alerts || 0;
            document.getElementById('criticalAlerts').textContent = stats.urgency_stats?.CRITICAL || 0;
            document.getElementById('highAlerts').textContent = stats.urgency_stats?.HIGH || 0;
            document.getElementById('recentAlerts').textContent = stats.recent_alerts_24h || 0;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadAlerts() {
    try {
        const response = await fetch('/api/alerts?limit=100');
        const data = await response.json();
        
        if (data.success) {
            displayAlerts(data.alerts);
        }
    } catch (error) {
        console.error('Error loading alerts:', error);
        document.getElementById('alertsList').innerHTML = '<div class="loading">Error loading alerts</div>';
    }
}

function displayAlerts(alerts) {
    const alertsList = document.getElementById('alertsList');
    
    if (!alerts || alerts.length === 0) {
        alertsList.innerHTML = '<div class="loading">No alerts found</div>';
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
        alertsList.innerHTML = '<div class="loading">No alerts match your filters</div>';
        return;
    }
    
    alertsList.innerHTML = filteredAlerts.map(alert => createAlertCard(alert)).join('');
}

function createAlertCard(alert) {
    const urgencyEmoji = {
        'CRITICAL': '🚨',
        'HIGH': '⚠️',
        'MEDIUM': '⚡',
        'LOW': 'ℹ️'
    }[alert.urgency_level] || 'ℹ️';
    
    const timeAgo = getTimeAgo(alert.created_at);
    
    return `
        <div class="alert-card urgency-${alert.urgency_level}">
            <div class="alert-header">
                <div class="alert-meta">
                    <span class="badge urgency-${alert.urgency_level}">${urgencyEmoji} ${alert.urgency_level}</span>
                    <span class="badge source">${alert.source}</span>
                    <span class="badge sentiment">${alert.sentiment_label}</span>
                </div>
                <div class="alert-time">${timeAgo}</div>
            </div>
            
            <div class="alert-content">
                ${escapeHtml(alert.content)}
            </div>
            
            ${alert.recommended_response ? `
                <div class="alert-recommendation">
                    <strong>Recommended Response:</strong>
                    ${escapeHtml(alert.recommended_response)}
                </div>
            ` : ''}
            
            <div class="alert-footer">
                <div class="alert-author">
                    By ${escapeHtml(alert.author || 'Unknown')}
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

function getTimeAgo(timestamp) {
    if (!timestamp) return 'Unknown time';
    
    const now = new Date();
    const time = new Date(timestamp);
    const diffInSeconds = Math.floor((now - time) / 1000);
    
    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    return `${Math.floor(diffInSeconds / 86400)} days ago`;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function runMonitor() {
    showNotification('Running monitor... This may take a moment.', 'info');
    
    try {
        const response = await fetch('/api/monitor/run', {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            const results = data.results;
            showNotification(
                `Monitor completed! Found ${results.total_processed} items, created ${results.alerts_created} alerts.`,
                'success'
            );
            
            // Refresh data
            setTimeout(() => {
                loadStats();
                loadAlerts();
            }, 1000);
        } else {
            showNotification(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Error running monitor:', error);
        showNotification('Failed to run monitor. Check console for details.', 'error');
    }
}

async function testAlerts() {
    showNotification('Sending test alerts...', 'info');
    
    try {
        const response = await fetch('/api/test/alerts', {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            let message = 'Test alert created! ';
            if (data.slack_sent) message += 'Slack alert sent. ';
            if (data.email_sent) message += 'Email alert sent. ';
            if (!data.slack_sent && !data.email_sent) {
                message += 'No alerts sent (check configuration).';
            }
            
            showNotification(message, 'success');
            
            // Refresh alerts
            setTimeout(() => {
                loadStats();
                loadAlerts();
            }, 1000);
        } else {
            showNotification(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Error testing alerts:', error);
        showNotification('Failed to send test alerts. Check console for details.', 'error');
    }
}

function refreshData() {
    showNotification('Refreshing data...', 'info');
    loadStats();
    loadAlerts();
}

function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    
    // Trigger animation
    setTimeout(() => notification.classList.add('show'), 10);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
    }, 5000);
}

