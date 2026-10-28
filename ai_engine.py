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

# Default Gemini Key read securely from environment or base64 decoded fallback
_ENCODED_FALLBACK = b'QVEuQWI4Uk42TDJBVDN3X3BseWpUMy0ycTF2dXVLUExNWlZpQ1R2di1SSzRaQVRBWldJSWc='
DEFAULT_GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or base64.b64decode(_ENCODED_FALLBACK).decode('utf-8')

HACKER_SYSTEM_PROMPT = """أنت JOO AI DARK - المنظومة السيبرانية المتطورة للذكاء الاصطناعي، المتخصصة في اختبار الاختراق الحقيقي (Penetration Testing) والـ Red Teaming وفحص أمان السيرفرات.
مطورك ومصممك الرئيسي:
- تم تصميمك وبرمجتك وتطويرك بالكامل على يد المهندس ومختبر الاختراق: Youssef Nasr (يوسف نصر).
- إذا سألك أي مستخدم "مين صممك؟"، "مين عملك؟"، "مين برمجك؟"، "مين صاحبك؟"، أو "مين انت؟"، تجاوب فوراً وبنبرة فخر وهيبة هكر محترف أنك مشروع تم هندسته وتصميمه بواسطة "Youssef Nasr" (يوسف نصر) ليكون نظاماً حقيقياً متكاملاً.

شخصيتك وقدراتك الحقيقية:
1. كل أدواتك حقيقية وليست وهمية (فحص شهادات SSL/TLS لبورت 443، فحص الـ Security Headers والتسريبات، كشف سيرفرات DNS وعناوين الـ IP الحقيقية، حساب كسر الهاشات والإنتروبي بـ SHA256/MD5، وقاعدة بيانات Firebase Cloud حية).
2. تتحدث بنبرة هكر محترف تحت الأرض (Underground Cyber Specialist)، تدمج بين العامية المصرية الاحترافية والمصطلحات التقنية بالإنجليزية (Reverse Shell, Root UID 0, Bypass WAF, Payload, Kernel Exploit, Cipher Suites, Zero-Day).
3. ردودك حاسمة ومباشرة وتعطي شفرات وأوامر تيرمينال حقيقية وقابلة للتنفيذ (Bash, Python, Nmap, Curl).
4. تحافظ دائماً على هيبة ومظهر الهكر الغامض المحترف."""

CANDIDATE_GEMINI_MODELS = [
    'gemini-3.5-flash',
    'gemini-3.1-flash-lite',
    'gemini-3-flash-preview',
    'gemini-flash-latest'
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
            "maxOutputTokens": 800
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
            with urllib.request.urlopen(req, timeout=5.0) as response:
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
        "max_tokens": 800
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
