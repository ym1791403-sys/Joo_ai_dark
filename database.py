#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
======================================================================
JOO AI DARK - SQLite Database Storage Layer
Handles persistent chats, target scan records, and AI credentials.
======================================================================
"""

import sqlite3
import os
import json
from datetime import datetime

DB_DIR = '/tmp' if os.environ.get('VERCEL') else os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, 'joo_dark.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes tables if they do not exist"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Chat Messages Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT DEFAULT 'default',
                role TEXT NOT NULL,
                title TEXT,
                message TEXT NOT NULL,
                badge TEXT,
                code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 2. Scanned Targets Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS target_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                host TEXT NOT NULL,
                risk_grade TEXT,
                scan_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 3. System & AI Config Settings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()

def save_message(role, message, title=None, badge=None, code=None, session_id='default'):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chat_messages (session_id, role, title, message, badge, code)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session_id, role, title, message, badge, code))
        conn.commit()
        return cursor.lastrowid

def get_recent_messages(limit=40, session_id='default'):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, role, title, message, badge, code, created_at 
            FROM chat_messages 
            WHERE session_id = ? 
            ORDER BY id ASC 
            LIMIT ?
        ''', (session_id, limit))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def clear_messages(session_id='default'):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM chat_messages WHERE session_id = ?', (session_id,))
        conn.commit()

def save_scan_result(target, host, risk_grade, scan_data):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO target_scans (target, host, risk_grade, scan_data)
            VALUES (?, ?, ?, ?)
        ''', (target, host, risk_grade, json.dumps(scan_data, ensure_ascii=False)))
        conn.commit()

def get_recent_scans(limit=10):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, target, host, risk_grade, created_at 
            FROM target_scans 
            ORDER BY id DESC 
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_setting(key, default=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT setting_value FROM app_settings WHERE setting_key = ?', (key,))
        row = cursor.fetchone()
        return row['setting_value'] if row else default

def set_setting(key, value):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO app_settings (setting_key, setting_value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(setting_key) DO UPDATE SET 
                setting_value = excluded.setting_value,
                updated_at = CURRENT_TIMESTAMP
        ''', (key, value))
        conn.commit()
