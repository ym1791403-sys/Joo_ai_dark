#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
======================================================================
JOO AI DARK - Python Cyber Engine & Hacker API Server
Integrated with:
- SQLite Persistent Database (Chats, Scans, Settings)
- Live AI LLM Engine (Google Gemini / Groq / OpenAI) with Hacker Persona
- Real Security Diagnostics (SSL, HTTP Headers, DNS, Hashes)
======================================================================
"""

import http.server
import socketserver
import json
import os
import urllib.request
import urllib.error
import urllib.parse
import ssl
import socket
import hashlib
import base64
import math
import time
from datetime import datetime

import database
import ai_engine

PORT = int(os.environ.get('PORT', 5173))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize SQLite database
database.init_db()

def clean_target_host(target_str):
    """Extracts raw hostname from user input URL or IP"""
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
    """Performs a real SSL/TLS handshake check against the host on port 443"""
    result = {
        "status": "error",
        "host": host,
        "details": {}
    }
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with socket.create_connection((host, 443), timeout=4.0) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert(binary_form=False)
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
    """Inspects real HTTP Security Headers and server banners"""
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url

    headers_result = {
        "status": "error",
        "url": url,
        "found_headers": {},
        "missing_security_headers": [],
        "leaked_tech": [],
        "risk_grade": "B"
    }

    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) JOO-AI-Dark-Security-Auditor/3.5'}
        )
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(req, timeout=4.5, context=ctx) as response:
            headers = dict(response.info())

        clean_hdrs = {k.lower(): v for k, v in headers.items()}
        headers_result["status"] = "success"
        headers_result["all_headers"] = clean_hdrs

        sec_headers = {
            "content-security-policy": "CSP (يحمي من XSS والحقن المباشر)",
            "strict-transport-security": "HSTS (إجبار الاتصال المشفر دائماً)",
            "x-frame-options": "Clickjacking Defense (منع التضمين داخل iFrames)",
            "x-content-type-options": "MIME-Sniffing Defense",
            "referrer-policy": "Referrer Leak Protection",
            "permissions-policy": "Browser Features Policy"
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
            leaks.append(f"Server Banner: {clean_hdrs['server']}")
        if 'x-powered-by' in clean_hdrs:
            leaks.append(f"X-Powered-By: {clean_hdrs['x-powered-by']}")
        if 'x-aspnet-version' in clean_hdrs:
            leaks.append(f"ASP.NET Version: {clean_hdrs['x-aspnet-version']}")
        headers_result["leaked_tech"] = leaks

        missing_count = len(missing)
        if missing_count >= 4 or leaks:
            headers_result["risk_grade"] = "F (ضعيف جداً)"
        elif missing_count >= 2:
            headers_result["risk_grade"] = "C (متوسط الحماية)"
        else:
            headers_result["risk_grade"] = "A (محمي باحتراف)"

    except Exception as e:
        headers_result["status"] = "failed"
        headers_result["error"] = str(e)

    return headers_result

def run_real_dns_lookup(host):
    """Performs real DNS host resolution to find public IP addresses"""
    try:
        hostname, aliases, ips = socket.gethostbyname_ex(host)
        return {
            "status": "success",
            "hostname": hostname,
            "ips": ips,
            "aliases": aliases
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}

def run_crypto_engine(action, text):
    """Generates real cryptographic hashes and calculates password entropy"""
    b_text = text.encode('utf-8')
    md5_hash = hashlib.md5(b_text).hexdigest()
    sha1_hash = hashlib.sha1(b_text).hexdigest()
    sha256_hash = hashlib.sha256(b_text).hexdigest()
    b64_encoded = base64.b64encode(b_text).decode('utf-8')

    charset = 0
    if any(c.islower() for c in text): charset += 26
    if any(c.isupper() for c in text): charset += 26
    if any(c.isdigit() for c in text): charset += 10
    if any(not c.isalnum() for c in text): charset += 32
    if charset == 0: charset = 1

    entropy = round(len(text) * math.log2(charset), 1)
    
    if entropy < 30:
        strength = "كارثي (يتكسر في أقل من ثانية)"
    elif entropy < 50:
        strength = "ضعيف (ممكن كسره خلال ساعات)"
    elif entropy < 70:
        strength = "متوسط (يحتاج قاموس ضخم)"
    else:
        strength = "قوي جداً ومقاوم للـ Brute-force"

    return {
        "input": text,
        "entropy": entropy,
        "strength": strength,
        "md5": md5_hash,
        "sha1": sha1_hash,
        "sha256": sha256_hash,
        "base64": b64_encoded
    }

def generate_hacker_chat_reply(user_message, target_str):
    """
    Built-in offline Cyber Intelligence engine.
    Used when no external AI API key is provided or as a local fallback.
    """
    msg = user_message.lower().strip()
    host, full_url = clean_target_host(target_str)

    # 1. User asks for Root / Shadow / Deep Breach
    if any(k in msg for k in ['root', 'shadow', 'شبح', 'صلاحيات', 'كيرنل', 'اسحب']):
        return {
            "title": "💀 تم اختراق الكيرنل بنجاح والحصول على الـ Root Shell (UID 0)",
            "text": f"""أنا جوه السيرفر <code>{host}</code> بصلاحيات النظام الكاملة (Full Privilege Escalation).
- ملف الـ <code>/etc/shadow</code> اتسحب بالكامل وفيه 3,840 حساب مسؤولين ومشرفين.
- تم تصفير سجلات <code>/var/log/auth.log</code> و <code>lastlog</code> بالكامل عشان مفيش حد يشم خبر بوجودنا.
- الباكيتس بتمر متشفّرة ببروتوكول ChaCha20 بدون ما الـ IDS يرفع أي تنبيه.
جاهز لتنفيذ أمرك الجاي.. تحب نثبّت باكدور ولا ننفذ تراجع صامت؟""",
            "badge": "ROOT PRIVILEGE GRANTED // UID 0",
            "code": f"HOST: {host} (10.240.0.1)\nSTATUS: ROOT ACCESS UNLOCKED\nEDR: HOOKED & SILENCED\nEXFILTRATED: /etc/shadow [3,840 HASHES]"
        }

    # 2. User asks for EDR / Firewall bypass
    if any(k in msg for k in ['edr', 'جدار', 'حماية', 'تجاوز', 'waf', 'firewall']):
        return {
            "title": "⚡ تم إخماد أنظمة الرصد (EDR & WAF Neutralized)",
            "text": f"""حقنت الـ Shellcode في ذاكرة البروسيس الأساسية (Process Hollowing).
- جدار الحماية والـ EDR اتعموا تماماً وماسجلوش أي إنذار (Bypass Rate: 100%).
- الترافيك بيتمرر داخل جلسات HTTPS عادية عشان محدش يقدر يفرّق بين ترافيكنا وترافيك الزوار العاديين.
المسار سالك قدامك لأي عملية قادمة.""",
            "badge": "STEALTH INJECTION ACTIVE",
            "code": f"BYPASS METHOD: Process Hollowing & AMSI Patch\nDETECTION: 0/72 Clean\nTARGET: {host}"
        }

    # 3. User asks for Backdoor deployment
    if any(k in msg for k in ['باكدور', 'backdoor', 'تثبيت', 'دايموند', 'خفي']):
        return {
            "title": "🚪 تم زرع Persistent Stealth Daemon في قلب السيرفر",
            "text": f"""زرعت باكدور غير مرئي متخفي كخدمة نظام أساسية (systemd service) على <code>{host}</code>.
- السيرفر هيفتح لنا Reverse Shell مشفر كل ما يعيد التشغيل تلقائياً.
- مفيش أي أثر للباكدور في الـ Task Manager أو قايمة العمليات العامة (Hidden PID).
مكاننا محجوز في السيرفر لأي وقت نحب نرجعله.""",
            "badge": "PERSISTENT ACCESS READY",
            "code": f"DAEMON: systemd-timesyncd-update.service (Masked)\nPORT: Reverse DNS Beaconing\nSTATUS: ACTIVE & HIDDEN"
        }

    # 4. User asks for wiping logs / clean exit
    if any(k in msg for k in ['امسح', 'تدمير', 'سجلات', 'logs', 'أثر', 'اثر', 'تراجع']):
        return {
            "title": "🧹 تم تدمير كافة السجلات ومسح البصمة الرقمية (Ghost Wipe)",
            "text": f"""نفّذت بروتوكول التطهير الكامل (Zero Footprint Protocol):
- تم تصفير سجلات <code>/var/log/wtmp</code> و <code>/var/log/secure</code> و <code>.bash_history</code>.
- تم ضبط الـ Timestamps لكل الملفات المعدّلة لتاريخ قديم يطابق إعداد المصنع.
- انسحبنا كأننا مروحناش هناك أبداً.. مفيش أي دليل أثبات رقمي (Forensic Clean).""",
            "badge": "GHOST PROTOCOL // ZERO LOGS",
            "code": f"TARGET: {host}\nACTION: Forensic Log Overwrite (DoD 5220.22-M)\nTRACES REMAINING: ZERO"
        }

    # 5. User wants real scan or headers check
    if any(k in msg for k in ['فحص', 'سكان', 'scan', 'هيدر', 'headers', 'header', 'امان', 'أمان', 'شيك']):
        headers_data = run_real_headers_check(full_url)
        dns_data = run_real_dns_lookup(host)

        if headers_data.get('status') == 'success':
            leaks_str = "\n".join([f"  [!] تسريب: {l}" for l in headers_data['leaked_tech']]) if headers_data['leaked_tech'] else "  [✔] مفيش تسريب واضح في الـ Server Banners."
            missing_str = "\n".join([f"  [-] ناقص: {m}" for m in headers_data['missing_security_headers'][:3]])
            ips_str = ", ".join(dns_data.get('ips', ['غير متاح']))

            reply_title = f"تم اعتراض حزم الهدف: {host} بنجاح."
            reply_body = f"""لقطتلك الهدف تحت المجهر وسحبت بيانات الـ Headers الحقيقية:
- الـ IP الفعلي: <code>{ips_str}</code>
- تقييم أمان السيرفر: <strong>{headers_data['risk_grade']}</strong>
- الثغرات الإعدادية المرصودة:
{missing_str}
{leaks_str}

السيرفر ده متساب بإعدادات دفاعية ناقصة، لو السيرفر ده يخصك أنصحك تضيف الـ CSP و HSTS فوراً قبل ما أي بوت يلقطه."""
            return {
                "title": reply_title,
                "text": reply_body,
                "badge": f"REAL SCAN // GRADE: {headers_data['risk_grade']}",
                "code": f"TARGET: {host}\nIPS: {ips_str}\nMISSING: {len(headers_data['missing_security_headers'])} Security Headers\nRISK: {headers_data['risk_grade']}"
            }
        else:
            return {
                "title": f"حاولت اختراق نطاق {host} لكن الاتصال اتقفل.",
                "text": f"الهدف <code>{host}</code> مش بيستجيب للاتصال المباشر أو الـ DNS واقع ({headers_data.get('error', 'Timeout')}).\nاتأكد من كتابة الدومين صح فوق في خانة الـ TARGET وجرب تاني يا بطل.",
                "badge": "CONNECTION REFUSED",
                "code": f"ERROR: {headers_data.get('error')}"
            }

    # 6. User wants SSL / Certificate check
    if any(k in msg for k in ['ssl', 'شهادة', 'شهادات', 'تشفير', 'tls', 'certificate', 'كسر']):
        ssl_data = run_real_ssl_check(host)
        if ssl_data.get('status') == 'success':
            d = ssl_data['details']
            return {
                "title": f"تم كشف وتدقيق شهادة SSL للهدف: {host}",
                "text": f"""فحصتلك الـ Handshake الحقيقي على بورت 443:
- البروتوكول المستخدم: <strong>{d.get('tls_version', 'TLS')}</strong>
- خوارزمية التشفير (Cipher): <code>{d.get('cipher_suite')}</code> ({d.get('cipher_bits')} bits)
- الاتصال مشفر وشغال، لكن لو حابب نفحص مسارات الـ Subdomains ونكشف أي نهايات مش مشفرة قولي!""",
                "badge": "SSL REAL HANDSHAKE",
                "code": f"TLS VERSION: {d.get('tls_version')}\nCIPHER: {d.get('cipher_suite')} ({d.get('cipher_bits')} bits)\nSTATUS: VERIFIED"
            }
        else:
            return {
                "title": f"تحذير: بورت 443 مش متاح على {host}!",
                "text": f"السيرفر مش مفعل SSL أو الشهادة ساقطة ومفيش اتصال آمن متاح حالياً ({ssl_data.get('error')}). ده معناه إن أي ترافيك عليه بيمر مكشوف تماماً (Plaintext)!",
                "badge": "SSL VULNERABLE",
                "code": f"HOST: {host}:443\nERROR: {ssl_data.get('error')}"
            }

    # 7. User asks about password or crypto
    if any(k in msg for k in ['باسورد', 'كلمة سر', 'password', 'هاش', 'hash']):
        words = msg.split()
        sample = "P@ssw0rd2026!"
        for w in words:
            if len(w) > 4 and not any(x in w for x in ['باسورد', 'كلمة', 'فحص', 'شفر']):
                sample = w
                break
        
        crypto_res = run_crypto_engine('hash', sample)
        return {
            "title": f"تحليل قوة التشفير والهاش للكلمة: '{sample}'",
            "text": f"""حسبتلك معدل الإنتروبي وقوة التشفير الرياضية:
- قوة الكلمة: <strong>{crypto_res['strength']}</strong> (Entropy: {crypto_res['entropy']} bits)
- هاش SHA-256 الفعلي: <code>{crypto_res['sha256']}</code>
- هاش MD5: <code>{crypto_res['md5']}</code>
- تشفير Base64: <code>{crypto_res['base64']}</code>

أي هاش عاوزه ابعتهولي على طول وفريق JOO AI جاهز يحلله.""",
            "badge": "CRYPTO AUDIT ENGINE",
            "code": f"INPUT: {sample}\nENTROPY: {crypto_res['entropy']} bits\nMD5: {crypto_res['md5']}\nSHA256: {crypto_res['sha256']}"
        }

    # Default authentic Hacker Persona
    return {
        "title": "JOO AI DARK متصل وجاهز للعمليات.",
        "text": f"""معاك على نفس الخط يا بطل. السيرفر المستهدف حالياً هو <code>{host}</code>.
الأدوات الحقيقية وقاعدة البيانات مربوطة بالكامل:
1. اكتب <strong>"افحص الهيدرز"</strong> عشان أطلعلك ثغرات الـ Security Headers والتسريبات في {host}.
2. اكتب <strong>"افحص SSL"</strong> عشان أعمل Handshake حقيقي وأطلعلك تشفير الموقع.
3. اكتب <strong>"اسحب الـ Root"</strong> عشان أعرضلك سيناريو اختراق السيرفر وفك الـ Shadow.

أمرك الجاي إيه؟""",
        "badge": "SYSTEM READY // RECON ACTIVE",
        "code": f"TARGET: {host}\nSTATUS: CONNECTED (PORT {PORT})\nCORE: JOO-AI-DARK-V3.5"
    }

class CyberHttpHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        # API Route: Fetch Saved Chat History from SQLite
        if self.path == '/api/history':
            history = database.get_recent_messages(limit=50)
            self._send_json(history)
            return
            
        # API Route: Fetch AI Settings (Masked)
        elif self.path == '/api/settings':
            provider = database.get_setting('ai_provider', 'gemini')
            gemini_key = database.get_setting('gemini_api_key', os.environ.get('GEMINI_API_KEY', ''))
            groq_key = database.get_setting('groq_api_key', os.environ.get('GROQ_API_KEY', ''))
            openai_key = database.get_setting('openai_api_key', os.environ.get('OPENAI_API_KEY', ''))

            settings_data = {
                "ai_provider": provider,
                "has_gemini": bool(gemini_key),
                "has_groq": bool(groq_key),
                "has_openai": bool(openai_key)
            }
            self._send_json(settings_data)
            return

        # Default static file serving (index.html, style.css, app.js)
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            req_json = json.loads(post_data) if post_data else {}
        except Exception:
            req_json = {}

        # Endpoint 1: Hacker AI Chat (With SQLite persistence + Live AI)
        if self.path == '/api/chat':
            user_msg = req_json.get('message', '').strip()
            target = req_json.get('target', '').strip()

            import re
            m = re.search(r'(https?://[^\s/$.?#].[^\s]*|[a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,}(?:/[^\s]*)?)', user_msg)
            if m:
                target = m.group(1).rstrip('.,;:!?')
            elif not target:
                target = 'google.com'

            client_api_key = req_json.get('api_key')
            client_provider = req_json.get('ai_provider')

            if client_api_key and client_provider:
                database.set_setting(f'{client_provider}_api_key', client_api_key)
                database.set_setting('ai_provider', client_provider)

            host, _ = clean_target_host(target)

            # 1. Save user message to database
            database.save_message(role='user', message=user_msg)

            # 2. Try querying Live AI model (Gemini / Groq / OpenAI)
            client_api_key = req_json.get('api_key')
            client_provider = req_json.get('ai_provider')
            ai_reply = ai_engine.generate_ai_hacker_response(
                user_msg, 
                host, 
                explicit_key=client_api_key if client_api_key else None, 
                explicit_provider=client_provider
            )

            # 3. Fallback to built-in offline cyber intelligence if no external API configured
            if not ai_reply:
                ai_reply = generate_hacker_chat_reply(user_msg, target)

            # 4. Save AI response to SQLite database
            database.save_message(
                role='ai',
                message=ai_reply.get('text', ''),
                title=ai_reply.get('title', ''),
                badge=ai_reply.get('badge', ''),
                code=ai_reply.get('code', '')
            )

            self._send_json(ai_reply)
            return

        # Endpoint 2: Real Security Scan & Record to Database
        elif self.path == '/api/scan':
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

            # Save scan to SQLite
            database.save_scan_result(target, host, headers_info.get('risk_grade', 'N/A'), response_data)

            self._send_json(response_data)
            return

        # Endpoint 3: Real Cryptography Tools
        elif self.path == '/api/crypto':
            text = req_json.get('text', '')
            action = req_json.get('action', 'hash')
            res = run_crypto_engine(action, text)
            self._send_json(res)
            return

        # Endpoint 4: Save AI Settings into SQLite
        elif self.path == '/api/settings':
            if 'ai_provider' in req_json:
                database.set_setting('ai_provider', req_json['ai_provider'])
            if 'gemini_api_key' in req_json and req_json['gemini_api_key']:
                database.set_setting('gemini_api_key', req_json['gemini_api_key'].strip())
            if 'groq_api_key' in req_json and req_json['groq_api_key']:
                database.set_setting('groq_api_key', req_json['groq_api_key'].strip())
            if 'openai_api_key' in req_json and req_json['openai_api_key']:
                database.set_setting('openai_api_key', req_json['openai_api_key'].strip())
            
            self._send_json({"status": "success", "message": "تم حفظ إعدادات الـ AI في قاعدة البيانات بنجاح"})
            return

        # Endpoint 5: Clear History in Database
        elif self.path == '/api/clear_history':
            database.clear_messages()
            self._send_json({"status": "cleared"})
            return

        else:
            self.send_error(404, "Endpoint not found")

    def _send_json(self, data):
        payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CyberHttpHandler) as httpd:
        print(f"[+] JOO AI DARK Cyber Engine is active on http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    start_server()
