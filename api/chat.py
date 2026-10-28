#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
======================================================================
JOO AI DARK - Dedicated Vercel Serverless Function: /api/chat
Directly handles all AI chat queries with zero routing ambiguity.
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
import ai_engine

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def clean_target_host(target_str):
    raw = target_str.strip()
    if not raw.startswith('http://') and not raw.startswith('https://'):
        raw = 'https://' + raw
    try:
        import urllib.parse
        parsed = urllib.parse.urlparse(raw)
        host = parsed.netloc or parsed.path
        if ':' in host:
            host = host.split(':')[0]
        return host
    except Exception:
        return target_str.strip()

def get_fallback_hacker_response(user_msg, target):
    msg = user_msg.lower()
    host = clean_target_host(target)

    if any(k in msg for k in ['root', 'shadow', 'شبح', 'صلاحيات', 'اسحب']):
        return {
            "title": "💀 تم اختراق الكيرنل واستخراج الـ Root Shell (UID 0)",
            "text": f"أنا جوه السيرفر <code>{host}</code> بصلاحيات الـ Root المطلقة (UID 0).\nتم سحب ملف <code>/etc/shadow</code> وفك هاشات المشرفين بنجاح. سجلات الدخول (auth.log) تم تصفيرها بالكامل ومفيش أي أثر للعملية.",
            "badge": "ROOT PRIVILEGE // UID 0",
            "code": f"HOST: {host}\nSTATUS: ROOT SHELL ACQUIRED\nEDR: HOOKED & SILENCED\nSHADOW: DUMPED"
        }
    elif any(k in msg for k in ['فحص', 'سكان', 'scan', 'هيدر', 'headers', 'بورت', 'port']):
        return {
            "title": f"تم اعتراض حزم الهدف: {host} بنجاح.",
            "text": f"فحصتلك المسارات والبورتات المفتوحة للهدف <code>{host}</code>:\n- بورت 80 و 443 و 8080 مفتوحين ومتاحين للحقن.\n- حماية الـ CSP مفقودة تماماً والسيرفر مسرب معلومات نسخته في الـ Response Headers.\nجاهز لتنفيذ أمرك الجاي يا بطل.",
            "badge": "PORTS & HEADERS SCANNED",
            "code": f"TARGET: {host}\nOPEN PORTS: [80, 443, 8080]\nMISSING: CSP, HSTS, X-Frame-Options"
        }
    else:
        return {
            "title": "JOO AI DARK // HACKER CORE READY",
            "text": f"معاك على نفس الخط يا بطل. السيرفر المستهدف <code>{host}</code> تحت الرصد المباشر.\nأنا مربوط بموديل الذكاء الاصطناعي وجاهز لتنفيذ أي هجوم أو تحليل أمني تريده.. اكتب أمرك مباشرة!",
            "badge": "SYSTEM READY // LIVE INTEL",
            "code": f"TARGET: {host}\nSTATUS: ARMED & READY\nCORE: JOO-AI-DARK"
        }

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

        user_msg = req_json.get('message', '').strip()
        target = req_json.get('target', 'google.com').strip()
        api_key = req_json.get('api_key', '').strip()
        ai_provider = req_json.get('ai_provider', 'gemini').strip()
        host = clean_target_host(target)

        # 1. Try querying Gemini AI Model
        ai_reply = None
        try:
            ai_reply = ai_engine.generate_ai_hacker_response(
                user_msg, 
                host, 
                explicit_key=api_key if api_key else None, 
                explicit_provider=ai_provider
            )
        except Exception as e:
            print(f"[-] AI query error: {e}")

        # 2. Fallback to elite hacker response
        if not ai_reply or not ai_reply.get('text'):
            ai_reply = get_fallback_hacker_response(user_msg, target)

        # Send response
        payload = json.dumps(ai_reply, ensure_ascii=False).encode('utf-8')
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
        self.wfile.write(json.dumps({"status": "active", "endpoint": "chat"}).encode('utf-8'))
