#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
======================================================================
JOO AI DARK - Dedicated Vercel Serverless Function: /api/scan
======================================================================
"""

import sys
import os
import json
import socket
import ssl
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

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

        payload = json.dumps(response_data, ensure_ascii=False).encode('utf-8')
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
        self.wfile.write(json.dumps({"status": "active", "endpoint": "scan"}).encode('utf-8'))
