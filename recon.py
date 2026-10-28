#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
======================================================================
JOO AI DARK - Public Assets & Frontend Reconnaissance Engine
Extracts publicly accessible assets:
- robots.txt & Disallowed paths
- Public <script> frontend files & bundles
- Passive detection of exposed API keys & endpoints in client-side JS
- Public security declarations (security.txt, sitemap.xml)
Strictly ethical & non-intrusive (Client-side asset inspection only)
Architect: Youssef Nasr
======================================================================
"""

import urllib.request
import urllib.error
import urllib.parse
import ssl
import re

def clean_recon_target(target_str):
    raw = (target_str or '').strip()
    if not raw.startswith('http://') and not raw.startswith('https://'):
        raw = 'https://' + raw
    try:
        parsed = urllib.parse.urlparse(raw)
        host = parsed.netloc or parsed.path
        if ':' in host:
            host = host.split(':')[0]
        base_url = f"{parsed.scheme or 'https'}://{host}"
        return host, base_url
    except Exception:
        clean = raw.replace('http://', '').replace('https://', '').split('/')[0]
        return clean, f"https://{clean}"

def fetch_url_content(url, timeout=3.0, max_bytes=100000):
    """Safely retrieves text content with strict timeout and SSL ignore"""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) JOO-AI-Dark-Recon/3.5 (Dev: Youssef Nasr)'
            }
        )
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
            raw_bytes = response.read(max_bytes)
            return raw_bytes.decode('utf-8', errors='ignore'), response.getcode()
    except Exception:
        return None, 0

def run_public_assets_recon(target_str):
    """Executes public asset discovery and client-side reconnaissance"""
    host, base_url = clean_recon_target(target_str)
    
    result = {
        "status": "success",
        "target": target_str,
        "host": host,
        "base_url": base_url,
        "robots_txt": {
            "found": False,
            "disallowed_paths": [],
            "sitemaps": [],
            "snippet": ""
        },
        "scripts": [],
        "leaked_findings": [],
        "security_txt": {"found": False, "url": f"{base_url}/.well-known/security.txt"},
        "sitemap_xml": {"found": False, "url": f"{base_url}/sitemap.xml"}
    }

    if not host or '.' not in host:
        result["status"] = "failed"
        result["error"] = "Invalid hostname provided"
        return result

    # 1. Fetch robots.txt
    robots_url = f"{base_url}/robots.txt"
    robots_body, status = fetch_url_content(robots_url, timeout=2.5, max_bytes=30000)
    if robots_body and (status == 200 or "User-agent" in robots_body or "Disallow" in robots_body):
        result["robots_txt"]["found"] = True
        result["robots_txt"]["snippet"] = robots_body[:1200]
        
        disallows = []
        sitemaps = []
        for line in robots_body.splitlines():
            line_str = line.strip()
            if line_str.lower().startswith('disallow:'):
                path = line_str.split(':', 1)[1].strip()
                if path and path not in disallows:
                    disallows.append(path)
            elif line_str.lower().startswith('sitemap:'):
                s_url = line_str.split(':', 1)[1].strip()
                if s_url and s_url not in sitemaps:
                    sitemaps.append(s_url)

        result["robots_txt"]["disallowed_paths"] = disallows[:12]
        result["robots_txt"]["sitemaps"] = sitemaps[:3]

    # 2. Fetch Landing Page HTML to discover public JS files
    html_body, _ = fetch_url_content(base_url, timeout=3.0, max_bytes=80000)
    found_scripts = []
    if html_body:
        # Regex to find <script ... src="..."
        script_matches = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html_body, re.IGNORECASE)
        for s in script_matches:
            s_clean = s.strip()
            if not s_clean:
                continue
            if s_clean.startswith('//'):
                full_script = 'https:' + s_clean
            elif s_clean.startswith('/'):
                full_script = base_url + s_clean
            elif not s_clean.startswith('http'):
                full_script = f"{base_url}/{s_clean}"
            else:
                full_script = s_clean

            if full_script not in found_scripts:
                found_scripts.append(full_script)

    result["scripts"] = found_scripts[:10]

    # 3. Passive JS scan for first-party bundle (check first 2 internal scripts)
    internal_scripts = [s for s in found_scripts if host in s or not s.startswith('http')][:2]
    findings = []
    for s_url in internal_scripts:
        js_code, js_status = fetch_url_content(s_url, timeout=2.5, max_bytes=70000)
        if not js_code:
            continue
        
        # Check Google API Key pattern
        if re.search(r'AIza[0-9A-Za-z-_]{35}', js_code):
            findings.append(f"مفتاح Google API مكشوف في ملف: {s_url.split('/')[-1]}")
        # Check AWS Key pattern
        if re.search(r'AKIA[0-9A-Z]{16}', js_code):
            findings.append(f"مفتاح AWS Access Key مكشوف في: {s_url.split('/')[-1]}")
        # Check Firebase URL
        if re.search(r'https://[a-zA-Z0-9-]+\.firebaseio\.com', js_code):
            findings.append(f"رابط Firebase Database مكشوف علناً في السكربت")
        # Check sensitive routes
        hidden_routes = re.findall(r'["\'](/(?:api/v[0-9]|admin|dashboard|portal|auth|internal)[a-zA-Z0-9_/.-]*)["\']', js_code)
        if hidden_routes:
            unique_routes = list(set(hidden_routes))[:4]
            findings.append(f"مسارات API داخلية معلنة في الكود: {', '.join(unique_routes)}")

    result["leaked_findings"] = findings

    # 4. Probe security.txt
    sec_body, sec_code = fetch_url_content(f"{base_url}/.well-known/security.txt", timeout=2.0, max_bytes=5000)
    if sec_body and (sec_code == 200 or 'Contact:' in sec_body):
        result["security_txt"]["found"] = True

    # 5. Probe sitemap.xml
    sm_body, sm_code = fetch_url_content(f"{base_url}/sitemap.xml", timeout=2.0, max_bytes=5000)
    if sm_body and (sm_code == 200 or '<?xml' in sm_body or '<urlset' in sm_body):
        result["sitemap_xml"]["found"] = True

    return result

if __name__ == '__main__':
    import sys
    test_target = sys.argv[1] if len(sys.argv) > 1 else 'https://google.com'
    print(f"[*] Auditing public assets for {test_target}...")
    recon = run_public_assets_recon(test_target)
    print(f"[+] Found {len(recon['scripts'])} public scripts.")
    print(f"[+] robots.txt found: {recon['robots_txt']['found']}")
    print(f"[+] Disallowed paths: {recon['robots_txt']['disallowed_paths']}")
