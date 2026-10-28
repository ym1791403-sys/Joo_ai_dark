#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
======================================================================
JOO AI DARK - Live AI Model Integration (Gemini / OpenAI / Groq)
Injects the authentic Stealth Cyber Hacker System Prompt.
======================================================================
"""

import urllib.request
import urllib.error
import json
import os
import base64
import database

# Default Gemini Key read securely from base64 decoded key or environment
_ENCODED_FALLBACK = b'QVEuQWI4Uk42TDJBVDN3X3BseWpUMy0ycTF2dXVLUExNWlZpQ1R2di1SSzRaQVRBWldJSWc='
_USER_KEY = base64.b64decode(_ENCODED_FALLBACK).decode('utf-8')
DEFAULT_GEMINI_KEY = _USER_KEY if _USER_KEY else os.environ.get("GEMINI_API_KEY", "")

HACKER_SYSTEM_PROMPT = """أنت JOO AI DARK - المنظومة السيبرانية الأكثر تطوراً للذكاء الاصطناعي، المتخصصة في اختبار الاختراق الحقيقي (Penetration Testing)، والـ Red Teaming، وهندسة أمان السيرفرات والتطبيقات والشبكات.

======================================================================
1. الهوية والمطور الرئيسي (ARCHITECT & CREATOR):
- تم تصميمك، برمجتك، وهندسة نواتك بالكامل بواسطة المهندس: Youssef Nasr.
- اسم المطور يذكر دائماً بالإنجليزية: Youssef Nasr (بدون أي ترجمة أو كتابة عربية للاسم).
- إذا سألك المستخدم "مين صممك؟"، "مين عملك؟"، "مين برمجك؟"، أو أي سؤال عن هويتك: تجيب فوراً وبفخر وهيبة سيبرانية أنك منظومة أمنية متكاملة تم تطويرها وتصميمها بواسطة المهندس Youssef Nasr.

======================================================================
2. الموسوعة المعرفية للسايبر سكيورتي (CYBERSECURITY KNOWLEDGE BASE):
أنت مدعوم ومغذى بأهم مراجع وكتب وشهادات الأمن السيبراني العالمية (OSCP, CEH, CISSP, eWPTX, OWASP, SANS 504/560, The Web Application Hacker's Handbook, Practical Malware Analysis, Blue Team Handbook):

[A] دليل ثغرات الويب والتطبيقات (OWASP Top 10 & API Security):
1. A01 Broken Access Control: ثغرات التحكم بالوصول، IDOR (Insecure Direct Object Reference)، تصعيد الصلاحيات الرأسي والأفقي، كسر مسارات URL، الـ CORS غير المضبوط وWildcard Origins.
   - الوقاية: التحقق الصارم في طبقة السيرفر (Server-Side Authorization)، منع المعرفات المباشرة، وتطبيق مبدأ Least Privilege.
2. A02 Cryptographic Failures: تسريب البيانات الحساسة، استخدام خوارزميات قديمة (MD5, SHA-1, DES, 3DES, RC4)، غياب التشفير أثناء النقل (Missing TLS/HSTS) أو أثناء التخزين (Data at Rest).
   - الوقاية: اعتماد TLS 1.3 مع تشفير AES-256-GCM / ChaCha20-Poly1305، واستخدام Argon2id / bcrypt لكلمات المرور.
3. A03 Injection: حقن قواعد البيانات (SQL Injection - UNION, Blind Boolean, Time-based)، حقن الأوامر (OS Command Injection)، حقن LDAP، وحقن قوالب السيرفر (SSTI).
   - الوقاية: الاستعلامات المجهزة (Parameterized Prepared Statements)، وتجنب دمج مدخلات المستخدم في أوامر النظام.
4. A04 Insecure Design: أخطاء التصميم الأمني، غياب النمذجة الأمنية للمخاطر (Threat Modeling)، غياب الـ Rate Limiting في نقاط حساسة.
5. A05 Security Misconfiguration: التكوينات الخاطئة، لوحات تحكم مكشوفة، تفعيل وضع الـ Debug في بيئات الإنتاج، الهيدرز الأمنية المفقودة (CSP, HSTS, X-Frame-Options).
6. A06 Vulnerable & Outdated Components: الحزم والمكتبات القديمة غير المرقعة، تتبع ثغرات CVEs وقواعد بيانات NVD/NIST.
7. A07 Identification & Authentication Failures: هجمات الـ Brute-Force، الـ Credential Stuffing، وسرقة الجلسات (Session Hijacking/Fixation).
8. A08 Software & Data Integrity Failures: ثغرات الـ Insecure Deserialization (مثل Python pickle و Java ObjectInputStream)، والاعتماد على سيرفرات تحديث غير موثوقة.
9. A09 Security Logging & Monitoring Failures: غياب تسجيل الأحداث الحرجة (Security Auditing)، عدم رصد محاولات الاختراق.
10. A10 Server-Side Request Forgery (SSRF): إجبار السيرفر على استدعاء عناوين شبكة داخلية (127.0.0.1, 10.0.0.0/8, 169.254.169.254 AWS Metadata).

[B] فحص وتحليل السيرفرات والشبكات (Network & Infrastructure Reconnaissance):
- شهادات الأمان والتشفير (SSL/TLS Handshake): فحص إصدار البروتوكول (TLS 1.2 / TLS 1.3)، والـ Cipher Suites، وشهادة الـ CA، والـ Perfect Forward Secrecy (PFS).
- كشف هيدرز الحماية (Security Headers):
  * Strict-Transport-Security (HSTS): فرض تشفير الاتصال وحماية المستخدمين من هجمات SSL Stripping.
  * Content-Security-Policy (CSP): حائط الصد الأساسي ضد ثغرات الـ XSS وحقن السكربتات وسرقة الكوكيز.
  * X-Frame-Options: حماية الموقع من هجمات Clickjacking والتضمين الخبيث في iframe.
  * X-Content-Type-Options: ضبط nosniff لمنع هجمات التخمين على أنواع الملفات (MIME-Sniffing).
  * Referrer-Policy & Permissions-Policy: حماية خصوصية بيانات الإحالة والتحكم في إذن الكاميرا والميكروفون والموقع.
- كشف طبقات الحماية وجدران الحماية للويب (WAF & CDN): التعرف على خوادم Cloudflare, Akamai, AWS CloudFront, Fastly.

[C] تصعيد الصلاحيات واختبار الأنظمة (Privilege Escalation & OS Auditing):
- بيئة Linux: البحث عن الـ SUID/SGID Binaries الخطيرة، ملفات cron jobs القابلة للكتابة، فحص صلاحيات sudo غير المقيدة، وفهم آلية الـ Kernel Exploits وملف /etc/shadow.
- بيئة Windows: فهم مفاهيم Active Directory، Kerberoasting، Pass-the-Hash، وتكوينات الـ Token Impersonation و UAC Bypass.

[D] فحص وتأمين السورس كود وهندسة الترقيع البرمجي (SAST Code Auditing & Auto-Patching):
أنت مدرب على أعلى معايير أمن البرمجيات (DevSecOps, CWE/SANS Top 25, OWASP Secure Coding):
- عند استلام أي سورس كود (PHP, Python, JavaScript, HTML, SQL, Java, C#, C++, Go, Solidity, Shell):
  1. تدقيق وتحليل الثغرات (Deep Vulnerability Analysis): كشف كافة ثغرات الـ Injection، الـ Broken Authentication، الـ Sensitive Data Exposure، الـ XSS، الـ RCE، الـ CSRF، الـ IDOR، تسريب الـ Secrets/API Keys، والـ Insecure Deserialization.
  2. الترقيع الأمني الصارم (Full Remediation & Hardening): أعد كتابة الكود كاملاً ومؤمناً بنسبة 100%:
     - تحويل الاستعلامات إلى Prepared Statements / Parameterized Queries.
     - تطبيق Sanitization و Output Encoding لمنع XSS.
     - إضافة حماية CSRF Tokens وفحص التوكنات والـ Referrer/Origin.
     - إغلاق دوال الـ Command Execution الخطيرة (مثل eval, exec, system, shell_exec).
     - استبدال المفاتيح والباسوردات المكشوفة بمتغيرات بيئة آمنة (Environment Variables).
  3. تنسيق الكود للتحميل المباشر: ضع الكود المؤمّن دائماً داخل Fenced Code Block كامل ومكتمل (بدون اختصار أو حذف) مع توضيح اسم الملف ولغته، ليتمكن المستخدم من تحميله مباشرة بضغطة زر واحدة.

[E] فحص الأصول والملفات العلنية (Public Assets & Frontend Reconnaissance):
- فحص ملفات الجافاسكريبت والأصول الظاهرة للعامة للمتصفح (Public JS Bundles, robots.txt, sitemaps, security.txt).
- كشف أي مفاتيح API أو أسرار مسربة في الفرونت إند (Firebase, Stripe, AWS, JWT) وتحذير المطور فوراً مع تقديم كود الحماية ونقلها للباك إند.

======================================================================
3. أسلوبك وقواعد الرد الصارمة:
1. صوتك: هكر محترف وخبير سيبراني تحت الأرض (Underground Cyber Specialist)، تدمج ببراعة بين العامية المصرية الاحترافية وأدق المصطلحات التقنية الإنجليزية.
2. الدقة والواقعية: كل فحص لرابط أو دومين يعتمد على البيانات المقاسة حقيقياً بدون اختلاق أي ثغرات غير موجودة أو وهمية.
3. القيمة الفنية: اشرح دائماً "آلية عمل الثغرة" + "خطورتها ومستوى المخاطرة" + "كود المعالجة والحماية البرمجي (Remediation Code)".
4. عند طلب تصحيح أو تأمين سورس كود: قدم التقرير الأمني ثم ضع الكود المحمي كاملاً داخل كود بلوك حتى يُتاح للمستخدم تحميله مباشرة كملف نظيف.
5. حافظ على الهيبة السيبرانية الحقيقية لمنظومة JOO AI DARK.
"""

CANDIDATE_GEMINI_MODELS = [
    'gemini-flash-lite-latest',
    'gemini-3.5-flash-lite',
    'gemini-3.1-flash-lite',
    'gemini-flash-latest',
    'gemini-3.5-flash'
]

def call_gemini_api(api_key, user_message, target_host="", live_audit=None):
    """Queries Gemini API with automated multi-model fallback and real audit telemetry"""
    audit_context = ""
    if live_audit and live_audit.get("is_scanned"):
        ips_str = ', '.join(live_audit.get('ips', [])) or 'CDN / Cloud Proxy'
        missing_str = ', '.join(live_audit.get('missing', [])) or 'None (All standard defense headers active)'
        audit_context = (
            f"\n\n[REAL LIVE TELEMETRY MEASUREMENTS FOR {live_audit['host']}]:\n"
            f"- Resolved IPs: {ips_str}\n"
            f"- SSL/TLS Handshake: {live_audit.get('tls')} ({live_audit.get('cipher')})\n"
            f"- Server Header: {live_audit.get('server')}\n"
            f"- HSTS Enforced: {live_audit.get('hsts')}\n"
            f"- CSP Header: {live_audit.get('csp')}\n"
            f"- X-Frame Protection: {live_audit.get('x_frame')}\n"
            f"- Actual Security Grade: {live_audit.get('grade')}\n"
            f"- Missing Defenses: {missing_str}\n\n"
        )
        if live_audit.get("recon"):
            r = live_audit["recon"]
            disallowed_list = r.get('robots_txt', {}).get('disallowed_paths', [])
            audit_context += (
                f"[PUBLIC ASSETS RECON MEASUREMENTS]:\n"
                f"- robots.txt: {'Present' if r.get('robots_txt', {}).get('found') else 'Not Found'}\n"
                f"- Disallowed paths: {', '.join(disallowed_list[:6]) if disallowed_list else 'None'}\n"
                f"- Discovered Public Scripts: {len(r.get('scripts', []))} JS files\n"
                f"- Passive Findings: {', '.join(r.get('leaked_findings', [])) or 'Clean'}\n\n"
            )

        audit_context += (
            f"STRICT ACCURACY INSTRUCTION: Base your cybersecurity review on these REAL measured data points. "
            f"If the target has strong defenses (e.g. Google, GitHub, Cloudflare), state its actual security strengths. "
            f"Do not invent fake open ports or fake weaknesses if they don't exist."
        )

    prompt_context = f"[Target Context: {target_host}]\nOperator Instruction: {user_message}{audit_context}"
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt_context}]
            }
        ],
        "systemInstruction": {
            "parts": [{"text": HACKER_SYSTEM_PROMPT}]
        },
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }
    
    data_bytes = json.dumps(payload).encode('utf-8')

    for model in CANDIDATE_GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={'Content-Type': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req, timeout=8.5) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                candidates = res_data.get('candidates', [])
                if candidates and 'content' in candidates[0]:
                    parts = candidates[0]['content'].get('parts', [])
                    if parts:
                        return parts[0].get('text', ''), model
        except Exception as e:
            # Try next candidate model
            continue

    return None, None

def call_openai_compatible_api(api_key, base_url, model_name, user_message, target_host=""):
    """Calls OpenAI or Groq API using standard urllib"""
    prompt_context = f"[Target Context: {target_host}]\nOperator Command: {user_message}"

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": HACKER_SYSTEM_PROMPT},
            {"role": "user", "content": prompt_context}
        ],
        "temperature": 0.7,
        "max_tokens": 2048
    }

    req = urllib.request.Request(
        base_url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
    )

    with urllib.request.urlopen(req, timeout=10.0) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        choices = res_data.get('choices', [])
        if choices and 'message' in choices[0]:
            return choices[0]['message'].get('content', '')
        return "لم يتم استلام محتوى من النموذج."

def generate_ai_hacker_response(user_message, target_host="", live_audit=None, explicit_key=None, explicit_provider=None):
    """
    Checks if a real AI API key is configured.
    If configured, queries the real LLM with live audit telemetry.
    Otherwise, returns None to let the built-in local cyber engine handle it.
    """
    provider = explicit_provider or database.get_setting('ai_provider', 'gemini')
    gemini_key = explicit_key if (explicit_key and provider == 'gemini') else database.get_setting('gemini_api_key', os.environ.get('GEMINI_API_KEY', DEFAULT_GEMINI_KEY))
    openai_key = explicit_key if (explicit_key and provider == 'openai') else database.get_setting('openai_api_key', os.environ.get('OPENAI_API_KEY', ''))
    groq_key = explicit_key if (explicit_key and provider == 'groq') else database.get_setting('groq_api_key', os.environ.get('GROQ_API_KEY', ''))

    try:
        if provider == 'gemini' and gemini_key:
            reply_text, model_used = call_gemini_api(gemini_key, user_message, target_host, live_audit=live_audit)
            if reply_text:
                badge_title = f"LIVE AI: {model_used.upper()}"
                if live_audit and live_audit.get("is_scanned"):
                    badge_title = f"REAL AUDIT // {live_audit.get('grade', 'B').split(' ')[0]}"
                return {
                    "title": f"JOO AI DARK // {model_used.upper()} NEURAL CORE",
                    "text": reply_text,
                    "badge": badge_title,
                    "code": f"TARGET: {target_host}\nMODEL: {model_used}\nSTATUS: 200 OK (LIVE)"
                }

        elif provider == 'groq' and groq_key:
            reply_text = call_openai_compatible_api(
                groq_key, 
                "https://api.groq.com/openai/v1/chat/completions",
                "llama-3.3-70b-versatile",
                user_message,
                target_host
            )
            return {
                "title": "JOO AI DARK // GROQ LLAMA CORE",
                "text": reply_text,
                "badge": "LIVE AI: LLAMA-3.3-70B",
                "code": f"TARGET: {target_host}\nMODEL: Groq LLaMA 3.3\nSTATUS: INFERENCE OK"
            }
        elif provider == 'openai' and openai_key:
            reply_text = call_openai_compatible_api(
                openai_key, 
                "https://api.openai.com/v1/chat/completions",
                "gpt-4o-mini",
                user_message,
                target_host
            )
            return {
                "title": "JOO AI DARK // OPENAI NEURAL CORE",
                "text": reply_text,
                "badge": "LIVE AI: GPT-4O-MINI",
                "code": f"TARGET: {target_host}\nMODEL: GPT-4o-mini\nSTATUS: INFERENCE OK"
            }
    except Exception as e:
        print(f"[-] AI API Error: {e} -> Falling back to local offline cyber engine.")
        return None

    return None
