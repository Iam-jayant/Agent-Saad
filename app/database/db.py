import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import threading

class Database:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, db_path: str = 'agent_saad.db'):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Database, cls).__new__(cls)
                    cls._instance.db_path = db_path
                    cls._instance.init_db()
        return cls._instance
    
    def get_connection(self):
        """Get a new database connection"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                content TEXT NOT NULL,
                author TEXT,
                url TEXT,
                sentiment_score REAL,
                sentiment_label TEXT,
                urgency_level TEXT,
                recommended_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'new',
                notified BOOLEAN DEFAULT 0
            )
        ''')
        
        # Create processed_items table to avoid duplicate alerts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processed_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                item_id TEXT NOT NULL,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(source, item_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_alert(self, alert_data: Dict) -> int:
        """Add a new alert to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts (
                source, content, author, url, sentiment_score,
                sentiment_label, urgency_level, recommended_response
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            alert_data.get('source'),
            alert_data.get('content'),
            alert_data.get('author'),
            alert_data.get('url'),
            alert_data.get('sentiment_score'),
            alert_data.get('sentiment_label'),
            alert_data.get('urgency_level'),
            alert_data.get('recommended_response')
        ))
        
        alert_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return alert_id
    
    def mark_as_notified(self, alert_id: int):
        """Mark an alert as notified"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE alerts SET notified = 1 WHERE id = ?', (alert_id,))
        conn.commit()
        conn.close()
    
    def is_processed(self, source: str, item_id: str) -> bool:
        """Check if an item has already been processed"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id FROM processed_items WHERE source = ? AND item_id = ?',
            (source, item_id)
        )
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def mark_as_processed(self, source: str, item_id: str):
        """Mark an item as processed"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO processed_items (source, item_id) VALUES (?, ?)',
                (source, item_id)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # Already processed
        finally:
            conn.close()
    
    def get_recent_alerts(self, limit: int = 50) -> List[Dict]:
        """Get recent alerts"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM alerts 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_unnotified_alerts(self) -> List[Dict]:
        """Get alerts that haven't been notified yet"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM alerts 
            WHERE notified = 0 
            ORDER BY created_at DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def update_alert_status(self, alert_id: int, status: str):
        """Update alert status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE alerts SET status = ? WHERE id = ?',
            (status, alert_id)
        )
        conn.commit()
        conn.close()
    
    def get_stats(self) -> Dict:
        """Get dashboard statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total alerts
        cursor.execute('SELECT COUNT(*) as total FROM alerts')
        total = cursor.fetchone()['total']
        
        # Alerts by urgency
        cursor.execute('''
            SELECT urgency_level, COUNT(*) as count 
            FROM alerts 
            GROUP BY urgency_level
        ''')
        urgency_stats = {row['urgency_level']: row['count'] for row in cursor.fetchall()}
        
        # Recent alerts count (last 24 hours)
        cursor.execute('''
            SELECT COUNT(*) as recent 
            FROM alerts 
            WHERE datetime(created_at) > datetime('now', '-1 day')
        ''')
        recent = cursor.fetchone()['recent']
        
        conn.close()
        
        return {
            'total_alerts': total,
            'urgency_stats': urgency_stats,
            'recent_alerts_24h': recent
        }

