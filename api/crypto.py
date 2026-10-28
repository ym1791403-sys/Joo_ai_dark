#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
======================================================================
JOO AI DARK - Dedicated Vercel Serverless Function: /api/crypto
======================================================================
"""

import json
import hashlib
import base64
import math
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            req_json = json.loads(post_data) if post_data else {}
        except Exception:
            req_json = {}

        text = req_json.get('text', '')
        b_text = text.encode('utf-8')
        md5_hash = hashlib.md5(b_text).hexdigest()
        sha256_hash = hashlib.sha256(b_text).hexdigest()
        b64_encoded = base64.b64encode(b_text).decode('utf-8')

        charset = 0
        if any(c.islower() for c in text): charset += 26
        if any(c.isupper() for c in text): charset += 26
        if any(c.isdigit() for c in text): charset += 10
        if any(not c.isalnum() for c in text): charset += 32
        if charset == 0: charset = 1

        entropy = round(len(text) * math.log2(charset), 1)
        strength = "قوي جداً ومقاوم للـ Brute-force" if entropy >= 60 else "ضعيف (ممكن كسره)"

        res = {
            "input": text,
            "entropy": entropy,
            "strength": strength,
            "md5": md5_hash,
            "sha256": sha256_hash,
            "base64": b64_encoded
        }

        payload = json.dumps(res, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "active", "endpoint": "crypto"}).encode('utf-8'))
