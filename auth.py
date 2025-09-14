# auth.py - Authentication and User Management System
import streamlit as st
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
import os
import time

# Try to import JWT, fallback to simple token if not available
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print("JWT not available, using simple token authentication")

class AuthManager:
    def __init__(self, db_path="thorium_app.db"):
        self.db_path = db_path
        self.secret_key = os.getenv("SECRET_KEY", "thorium-secret-key-2024")
        self.init_database()
    
    def init_database(self):
        """Initialize the database with users table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                preferences TEXT DEFAULT '{}'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_token TEXT UNIQUE,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                simulation_type TEXT,
                parameters TEXT,
                results TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
    
    def verify_password(self, password, stored_hash):
        """Verify password against stored hash"""
        try:
            salt, hash_value = stored_hash.split(':')
            password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return password_hash == hash_value
        except:
            return False
    
    def register_user(self, username, email, password, role="user"):
        """Register a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, role))
            
            conn.commit()
            return True, "User registered successfully!"
        except sqlite3.IntegrityError:
            return False, "Username or email already exists!"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
        finally:
            conn.close()
    
    def login_user(self, username, password):
        """Login user and create session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, password_hash, role FROM users 
            WHERE username = ? OR email = ?
        ''', (username, username))
        
        user = cursor.fetchone()
        
        if user and self.verify_password(password, user[3]):
            # Create session token
            session_token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=24)
            
            cursor.execute('''
                INSERT INTO user_sessions (user_id, session_token, expires_at)
                VALUES (?, ?, ?)
            ''', (user[0], session_token, expires_at))
            
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            ''', (user[0],))
            
            conn.commit()
            conn.close()
            
            return True, {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'role': user[4],
                'session_token': session_token
            }
        else:
            conn.close()
            return False, "Invalid username or password!"
    
    def verify_session(self, session_token):
        """Verify session token and return user info"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.username, u.email, u.role, s.expires_at
            FROM users u
            JOIN user_sessions s ON u.id = s.user_id
            WHERE s.session_token = ? AND s.expires_at > CURRENT_TIMESTAMP
        ''', (session_token,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'role': user[3]
            }
        else:
            return False, None
    
    def logout_user(self, session_token):
        """Logout user by removing session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM user_sessions WHERE session_token = ?
        ''', (session_token,))
        
        conn.commit()
        conn.close()
    
    def save_simulation(self, user_id, simulation_type, parameters, results):
        """Save simulation data for user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO simulation_history (user_id, simulation_type, parameters, results)
            VALUES (?, ?, ?, ?)
        ''', (user_id, simulation_type, str(parameters), str(results)))
        
        conn.commit()
        conn.close()
    
    def get_user_simulations(self, user_id, limit=10):
        """Get user's simulation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT simulation_type, parameters, results, created_at
            FROM simulation_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        simulations = cursor.fetchall()
        conn.close()
        
        return simulations
    
    def update_user_preferences(self, user_id, preferences):
        """Update user preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET preferences = ? WHERE id = ?
        ''', (str(preferences), user_id))
        
        conn.commit()
        conn.close()

# Initialize auth manager
auth_manager = AuthManager()

def show_login_page():
    """Display login/register page"""
    st.markdown("""
    <div class="main-header">
        <h1>🔐 Welcome to Thorium GenAI</h1>
        <p>Please login or register to access the advanced thorium energy platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add some information about the platform
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 2rem;">
        <h3 style="color: #1f77b4; margin-top: 0;">🌱 India's Thorium Energy Revolution</h3>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #2c3e50;">
            Access our comprehensive platform featuring AI-powered knowledge assistance, interactive reactor simulations, 
            policy impact analysis, and real-time energy data to explore thorium-based nuclear energy solutions.
        </p>
        <div style="display: flex; gap: 2rem; margin-top: 1.5rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: #1f77b4;">360,000</div>
                <div style="font-size: 0.9rem; color: #6c757d;">Tons of Thorium Reserves</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: #2ca02c;">70%</div>
                <div style="font-size: 0.9rem; color: #6c757d;">Less Nuclear Waste</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: #ff7f0e;">2035</div>
                <div style="font-size: 0.9rem; color: #6c757d;">Target Deployment</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        
        with st.form("login_form"):
            username = st.text_input("Username or Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", type="primary")
            
            if submit:
                if username and password:
                    success, result = auth_manager.login_user(username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_info = result
                        st.success("🎉 Login successful! Welcome to Thorium GenAI Dashboard!")
                        st.balloons()  # Add celebration animation
                        time.sleep(2)  # Brief pause to show success message
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.markdown("### Create New Account")
        
        with st.form("register_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            role = st.selectbox("Role", ["user", "researcher", "admin"])
            submit = st.form_submit_button("Register", type="primary")
            
            if submit:
                if all([username, email, password, confirm_password]):
                    if password == confirm_password:
                        success, message = auth_manager.register_user(username, email, password, role)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.error("Passwords do not match!")
                else:
                    st.error("Please fill in all fields")

def check_auth():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login_page()
        return False
    
    return True

def show_logout_button():
    """Show logout button in sidebar"""
    if st.sidebar.button("🚪 Logout"):
        if 'user_info' in st.session_state and 'session_token' in st.session_state.user_info:
            auth_manager.logout_user(st.session_state.user_info['session_token'])
        st.session_state.authenticated = False
        st.session_state.user_info = None
        st.success("👋 Logged out successfully! Thank you for using Thorium GenAI.")
        time.sleep(1)
        st.rerun()

def get_current_user():
    """Get current user information"""
    if st.session_state.authenticated and 'user_info' in st.session_state:
        return st.session_state.user_info
    return None

def require_role(required_role):
    """Decorator to require specific role"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user or user['role'] != required_role:
                st.error(f"Access denied. Required role: {required_role}")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator
