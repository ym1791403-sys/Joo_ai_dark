#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
======================================================================
JOO AI DARK - Dedicated Vercel Serverless Function: /api/settings
======================================================================
"""

import sys
import os
import json
from http.server import BaseHTTPRequestHandler

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import database

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        provider = database.get_setting('ai_provider', 'gemini')
        gemini_key = database.get_setting('gemini_api_key', os.environ.get('GEMINI_API_KEY', ''))
        settings_data = {
            "ai_provider": provider,
            "has_gemini": bool(gemini_key or os.environ.get("GEMINI_API_KEY"))
        }
        payload = json.dumps(settings_data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            req_json = json.loads(post_data) if post_data else {}
        except Exception:
            req_json = {}

        if 'ai_provider' in req_json:
            database.set_setting('ai_provider', req_json['ai_provider'])
        if 'gemini_api_key' in req_json and req_json['gemini_api_key']:
            database.set_setting('gemini_api_key', req_json['gemini_api_key'].strip())

        payload = json.dumps({"status": "success"}).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(payload)
