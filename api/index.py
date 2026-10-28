#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
======================================================================
JOO AI DARK - Vercel Serverless Function Handler
Provides /api/chat, /api/scan, /api/crypto, /api/settings on Vercel.
======================================================================
"""

import sys
import os
import json
import urllib.request
import urllib.error
import urllib.parse
import ssl
import socket
import hashlib
import base64
import math
from datetime import datetime
from http.server import BaseHTTPRequestHandler

# Ensure root directory is in sys.path for database & ai_engine imports
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import database
import ai_engine

# Initialize database
database.init_db()

def clean_target_host(target_str):
    raw = target_str.strip()
    if not raw.startswith('http://') and not raw.startswith('https://'):
        raw = 'https://' + raw
    try:
        parsed = urllib.parse.urlparse(raw)
        host = parsed.netloc or parsed.path
        if ':' in host:
            host = host.split(':')[0]
        return host, raw
    except Exception:
        return target_str.strip(), target_str.strip()

def run_real_ssl_check(host):
    result = {"status": "error", "host": host, "details": {}}
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with socket.create_connection((host, 443), timeout=3.5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cipher = ssock.cipher()
                version = ssock.version()
                result["status"] = "success"
                result["details"] = {
                    "tls_version": version,
                    "cipher_suite": cipher[0] if cipher else "Unknown",
                    "cipher_bits": cipher[2] if cipher else 0,
                    "connected": True
                }
    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)
    return result

def run_real_headers_check(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url

    headers_result = {
        "status": "error", "url": url,
        "found_headers": {}, "missing_security_headers": [],
        "leaked_tech": [], "risk_grade": "B"
    }

    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) JOO-AI-Dark-Security-Auditor/3.5'}
        )
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(req, timeout=4.0, context=ctx) as response:
            headers = dict(response.info())

        clean_hdrs = {k.lower(): v for k, v in headers.items()}
        headers_result["status"] = "success"

        sec_headers = {
            "content-security-policy": "CSP (يحمي من XSS)",
            "strict-transport-security": "HSTS (إجبار التشفير)",
            "x-frame-options": "Clickjacking Defense",
            "x-content-type-options": "MIME-Sniffing Defense"
        }

        missing = []
        for hdr, desc in sec_headers.items():
            if hdr in clean_hdrs:
                headers_result["found_headers"][hdr] = clean_hdrs[hdr]
            else:
                missing.append(f"{hdr.upper()} - {desc}")
        headers_result["missing_security_headers"] = missing

        leaks = []
        if 'server' in clean_hdrs:
            leaks.append(f"Server: {clean_hdrs['server']}")
        if 'x-powered-by' in clean_hdrs:
            leaks.append(f"X-Powered-By: {clean_hdrs['x-powered-by']}")
        headers_result["leaked_tech"] = leaks

        if len(missing) >= 3 or leaks:
            headers_result["risk_grade"] = "F (ضعيف جداً)"
        elif len(missing) >= 1:
            headers_result["risk_grade"] = "C (متوسط الحماية)"
        else:
            headers_result["risk_grade"] = "A (محمي باحتراف)"

    except Exception as e:
        headers_result["status"] = "failed"
        headers_result["error"] = str(e)

    return headers_result

def run_real_dns_lookup(host):
    try:
        hostname, aliases, ips = socket.gethostbyname_ex(host)
        return {"status": "success", "hostname": hostname, "ips": ips, "aliases": aliases}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

def run_crypto_engine(action, text):
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

    return {
        "input": text,
        "entropy": entropy,
        "strength": strength,
        "md5": md5_hash,
        "sha256": sha256_hash,
        "base64": b64_encoded
    }

def generate_hacker_chat_reply(user_message, target_str):
    msg = user_message.lower().strip()
    host, full_url = clean_target_host(target_str)

    if any(k in msg for k in ['root', 'shadow', 'شبح', 'صلاحيات', 'اسحب']):
        return {
            "title": "💀 تم اختراق الكيرنل بنجاح والحصول على الـ Root Shell (UID 0)",
            "text": f"أنا جوه السيرفر <code>{host}</code> بصلاحيات النظام الكاملة. ملف الـ /etc/shadow اتسحب بالكامل وتصفير سجلات auth.log تم بدون إثارة أي تنبيهات.",
            "badge": "ROOT PRIVILEGE GRANTED // UID 0",
            "code": f"HOST: {host}\nSTATUS: ROOT ACCESS UNLOCKED\nEDR: HOOKED & SILENCED"
        }
    elif any(k in msg for k in ['فحص', 'سكان', 'scan', 'هيدر', 'headers']):
        headers_data = run_real_headers_check(full_url)
        dns_data = run_real_dns_lookup(host)
        ips_str = ", ".join(dns_data.get('ips', ['غير متاح']))
        return {
            "title": f"تم اعتراض حزم الهدف: {host} بنجاح.",
            "text": f"لقطتلك الهدف تحت المجهر:\n- الـ IP الفعلي: {ips_str}\n- تقييم الأمان: {headers_data.get('risk_grade', 'N/A')}\n- نواقص الحماية: {len(headers_data.get('missing_security_headers', []))} هيدرز.",
            "badge": f"GRADE: {headers_data.get('risk_grade', 'B')}",
            "code": f"TARGET: {host}\nIPS: {ips_str}\nSTATUS: AUDITED"
        }
    else:
        return {
            "title": "JOO AI DARK متصل وجاهز للعمليات.",
            "text": f"معاك على نفس الخط يا بطل. السيرفر المستهدف حالياً هو <code>{host}</code>.\nالأدوات الحقيقية وموديل الـ AI جاهزين لأي أمر جديد.",
            "badge": "SYSTEM READY // VERCEL CORE",
            "code": f"TARGET: {host}\nPLATFORM: VERCEL SERVERLESS\nCORE: JOO-AI-DARK-V3.5"
        }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_path = self.path.split('?')[0]
        
        if url_path == '/api/history':
            history = database.get_recent_messages(limit=50)
            self._send_json(history)
            return
            
        elif url_path == '/api/settings':
            provider = database.get_setting('ai_provider', 'gemini')
            gemini_key = database.get_setting('gemini_api_key', os.environ.get('GEMINI_API_KEY', ''))
            settings_data = {
                "ai_provider": provider,
                "has_gemini": bool(gemini_key)
            }
            self._send_json(settings_data)
            return

        self._send_json({"status": "active", "platform": "vercel"})

    def do_POST(self):
        url_path = self.path.split('?')[0]
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            req_json = json.loads(post_data) if post_data else {}
        except Exception:
            req_json = {}

        if url_path == '/api/chat':
            user_msg = req_json.get('message', '').strip()
            target = req_json.get('target', 'google.com').strip()
            client_api_key = req_json.get('api_key')
            client_provider = req_json.get('ai_provider')

            if client_api_key and client_provider:
                database.set_setting(f'{client_provider}_api_key', client_api_key)
                database.set_setting('ai_provider', client_provider)

            host, _ = clean_target_host(target)

            database.save_message(role='user', message=user_msg)

            ai_reply = ai_engine.generate_ai_hacker_response(user_msg, host)
            if not ai_reply:
                ai_reply = generate_hacker_chat_reply(user_msg, target)

            database.save_message(
                role='ai',
                message=ai_reply.get('text', ''),
                title=ai_reply.get('title', ''),
                badge=ai_reply.get('badge', ''),
                code=ai_reply.get('code', '')
            )
            self._send_json(ai_reply)
            return

        elif url_path == '/api/scan':
            target = req_json.get('target', 'https://google.com')
            host, full_url = clean_target_host(target)
            dns = run_real_dns_lookup(host)
            ssl_info = run_real_ssl_check(host)
            headers_info = run_real_headers_check(full_url)

            response_data = {
                "target": target,
                "host": host,
                "dns": dns,
                "ssl": ssl_info,
                "headers": headers_info,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            database.save_scan_result(target, host, headers_info.get('risk_grade', 'N/A'), response_data)
            self._send_json(response_data)
            return

        elif url_path == '/api/crypto':
            text = req_json.get('text', '')
            res = run_crypto_engine('hash', text)
            self._send_json(res)
            return

        elif url_path == '/api/settings':
            if 'ai_provider' in req_json:
                database.set_setting('ai_provider', req_json['ai_provider'])
            if 'gemini_api_key' in req_json and req_json['gemini_api_key']:
                database.set_setting('gemini_api_key', req_json['gemini_api_key'].strip())
            self._send_json({"status": "success"})
            return

        elif url_path == '/api/clear_history':
            database.clear_messages()
            self._send_json({"status": "cleared"})
            return

        self._send_json({"error": "Endpoint not found"})

    def _send_json(self, data):
        payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
