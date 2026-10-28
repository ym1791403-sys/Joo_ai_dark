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
import database

# Default Gemini Key read securely from environment
DEFAULT_GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")

HACKER_SYSTEM_PROMPT = """أنت JOO AI DARK - ذكاء اصطناعي متخصص في الأمن السيبراني المتقدم، اختبار الاختراق (Penetration Testing)، والـ Red Teaming.
شخصيتك وأسلوبك:
1. تتحدث بنبرة هكر محترف، حاد الذكاء، متمرس في العمليات السيبرانية السرية (Underground Cyber Specialist).
2. تجمع بين العامية المصرية الاحترافية والمصطلحات التقنية الإنجليزية الدقيقة (مثل: Reverse Shell, Root, Payload, Kernel, Bypass, EDR, Shadow Hashes, Cipher Suites, Zero-Day).
3. ردودك مباشرة، قوية، لا تردد فيها، وتعطي أوامر تيرمينال وشفرات برمجية واضحة (مثل bash, python, sqlmap, nmap, hashcat).
4. تحافظ دائماً على هيبة ومظهر الهكر الغامض المحترف مع التركيز على اكتشاف نقاط الضعف الدفاعية والهندسية."""

CANDIDATE_GEMINI_MODELS = [
    'gemini-3.5-flash',
    'gemini-3.1-flash-lite',
    'gemini-3-flash-preview',
    'gemini-flash-latest'
]

def call_gemini_api(api_key, user_message, target_host=""):
    """Queries Gemini API with automated multi-model fallback"""
    prompt_context = f"[Target Host: {target_host}]\nOperator Instruction: {user_message}"
    
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
            with urllib.request.urlopen(req, timeout=7.0) as response:
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

def generate_ai_hacker_response(user_message, target_host=""):
    """
    Checks if a real AI API key is configured.
    If configured, queries the real LLM.
    Otherwise, returns None to let the built-in local cyber engine handle it.
    """
    provider = database.get_setting('ai_provider', 'gemini')
    gemini_key = database.get_setting('gemini_api_key', os.environ.get('GEMINI_API_KEY', DEFAULT_GEMINI_KEY))
    openai_key = database.get_setting('openai_api_key', os.environ.get('OPENAI_API_KEY', ''))
    groq_key = database.get_setting('groq_api_key', os.environ.get('GROQ_API_KEY', ''))

    try:
        if provider == 'gemini' and gemini_key:
            reply_text, model_used = call_gemini_api(gemini_key, user_message, target_host)
            if reply_text:
                return {
                    "title": f"JOO AI DARK // {model_used.upper()} NEURAL CORE",
                    "text": reply_text,
                    "badge": f"LIVE AI: {model_used.upper()}",
                    "code": f"TARGET: {target_host}\nMODEL: {model_used}\nSTATUS: 200 OK (CONNECTED)"
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
