# database.py - Database utilities and data management
import sqlite3
import json
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class DatabaseManager:
    def __init__(self, db_path="thorium_app.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize all database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                preference_key TEXT,
                preference_value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Energy data cache
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS energy_data_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_type TEXT,
                data_source TEXT,
                data_content TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                UNIQUE(data_type, data_source)
            )
        ''')
        
        # Export history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS export_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                export_type TEXT,
                file_name TEXT,
                file_path TEXT,
                export_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # App analytics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action_type TEXT,
                page_name TEXT,
                session_id TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_user_preference(self, user_id, key, value):
        """Save user preference"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_preferences (user_id, preference_key, preference_value, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, key, str(value)))
        
        conn.commit()
        conn.close()
    
    def get_user_preferences(self, user_id):
        """Get all user preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT preference_key, preference_value FROM user_preferences
            WHERE user_id = ?
        ''', (user_id,))
        
        preferences = dict(cursor.fetchall())
        conn.close()
        
        return preferences
    
    def cache_energy_data(self, data_type, data_source, data_content, ttl_hours=1):
        """Cache energy data with TTL"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        expires_at = datetime.now() + timedelta(hours=ttl_hours)
        
        cursor.execute('''
            INSERT OR REPLACE INTO energy_data_cache 
            (data_type, data_source, data_content, last_updated, expires_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)
        ''', (data_type, data_source, json.dumps(data_content), expires_at))
        
        conn.commit()
        conn.close()
    
    def get_cached_energy_data(self, data_type, data_source):
        """Get cached energy data if not expired"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT data_content FROM energy_data_cache
            WHERE data_type = ? AND data_source = ? AND expires_at > CURRENT_TIMESTAMP
        ''', (data_type, data_source))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return json.loads(result[0])
        return None
    
    def log_export(self, user_id, export_type, file_name, file_path, export_data):
        """Log export activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO export_history 
            (user_id, export_type, file_name, file_path, export_data)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, export_type, file_name, file_path, str(export_data)))
        
        conn.commit()
        conn.close()
    
    def get_export_history(self, user_id, limit=10):
        """Get user's export history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT export_type, file_name, created_at
            FROM export_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        history = cursor.fetchall()
        conn.close()
        
        return history
    
    def log_analytics(self, user_id, action_type, page_name, session_id, metadata=None):
        """Log user analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO app_analytics 
            (user_id, action_type, page_name, session_id, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, action_type, page_name, session_id, str(metadata) if metadata else None))
        
        conn.commit()
        conn.close()
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get simulation count
        cursor.execute('SELECT COUNT(*) FROM simulation_history WHERE user_id = ?', (user_id,))
        simulation_count = cursor.fetchone()[0]
        
        # Get export count
        cursor.execute('SELECT COUNT(*) FROM export_history WHERE user_id = ?', (user_id,))
        export_count = cursor.fetchone()[0]
        
        # Get last login
        cursor.execute('SELECT last_login FROM users WHERE id = ?', (user_id,))
        last_login = cursor.fetchone()[0]
        
        # Get most used simulation type
        cursor.execute('''
            SELECT simulation_type, COUNT(*) as count
            FROM simulation_history
            WHERE user_id = ?
            GROUP BY simulation_type
            ORDER BY count DESC
            LIMIT 1
        ''', (user_id,))
        
        favorite_simulation = cursor.fetchone()
        
        conn.close()
        
        return {
            'simulation_count': simulation_count,
            'export_count': export_count,
            'last_login': last_login,
            'favorite_simulation': favorite_simulation[0] if favorite_simulation else 'None'
        }

# Initialize database manager
db_manager = DatabaseManager()

def get_user_stats_display(user_id):
    """Get formatted user stats for display"""
    stats = db_manager.get_user_stats(user_id)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Simulations Run", stats['simulation_count'])
    
    with col2:
        st.metric("Files Exported", stats['export_count'])
    
    with col3:
        st.metric("Last Login", stats['last_login'][:10] if stats['last_login'] else 'Never')
    
    with col4:
        st.metric("Favorite Tool", stats['favorite_simulation'])
