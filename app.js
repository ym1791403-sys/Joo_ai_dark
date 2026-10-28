/* ===================================================================
   JOO AI DARK - Interactive Cyber AI Engine & Real Security Tools
   Persona: Underground Cyber Security Hacker AI
   =================================================================== */

// Web Audio API Sound Synthesizer
class CyberSoundEngine {
    constructor() {
        this.enabled = true;
        this.ctx = null;
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                this.ctx = new AudioContext();
            }
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    playBeep(freq = 880, duration = 0.08, type = 'sine') {
        if (!this.enabled) return;
        try {
            this.init();
            if (!this.ctx) return;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
            gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start();
            osc.stop(this.ctx.currentTime + duration);
        } catch (e) {
            // Audio fallback
        }
    }

    playSuccess() {
        if (!this.enabled) return;
        this.playBeep(520, 0.08, 'triangle');
        setTimeout(() => this.playBeep(880, 0.12, 'sine'), 80);
    }

    playAlert() {
        if (!this.enabled) return;
        this.playBeep(440, 0.06, 'sawtooth');
        setTimeout(() => this.playBeep(330, 0.1, 'sawtooth'), 60);
    }

    playClick() {
        if (!this.enabled) return;
        this.playBeep(1200, 0.02, 'sine');
    }
}

const soundEngine = new CyberSoundEngine();

// DOM Elements
const chatHistory = document.getElementById('chatHistory');
const chatContainer = document.getElementById('chatContainer');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const typingIndicator = document.getElementById('typingIndicator');
const typingText = document.getElementById('typingText');
const terminalDrawer = document.getElementById('terminalDrawer');
const terminalToggleBtn = document.getElementById('terminalToggleBtn');
const closeTerminalBtn = document.getElementById('closeTerminalBtn');
const clearTerminalBtn = document.getElementById('clearTerminalBtn');
const terminalBody = document.getElementById('terminalBody');
const terminalInput = document.getElementById('terminalInput');
const soundToggleBtn = document.getElementById('soundToggleBtn');
const sidebar = document.getElementById('sidebar');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const closeSidebarBtn = document.getElementById('closeSidebarBtn');
const clearChatBtn = document.getElementById('clearChatBtn');
const toastNotification = document.getElementById('toastNotification');
const toastMsg = document.getElementById('toastMsg');
const targetInput = document.getElementById('targetInput');
const startRealScanBtn = document.getElementById('startRealScanBtn');
const cryptoModal = document.getElementById('cryptoModal');
const closeCryptoModalBtn = document.getElementById('closeCryptoModalBtn');
const runCryptoBtn = document.getElementById('runCryptoBtn');
const cryptoTextInput = document.getElementById('cryptoTextInput');

let isProcessing = false;

// Audio toggle
soundToggleBtn.addEventListener('click', () => {
    soundEngine.enabled = !soundEngine.enabled;
    soundToggleBtn.classList.toggle('active', soundEngine.enabled);
    soundToggleBtn.innerHTML = soundEngine.enabled ? 
        '<i class="fa-solid fa-volume-high"></i>' : 
        '<i class="fa-solid fa-volume-xmark"></i>';
    showToast(soundEngine.enabled ? "المؤثرات الصوتية: مفعّلة" : "المؤثرات الصوتية: مكتومة");
});

// Sidebar Mobile Toggle
mobileMenuBtn.addEventListener('click', () => sidebar.classList.add('open'));
closeSidebarBtn.addEventListener('click', () => sidebar.classList.remove('open'));

// Terminal Toggle
terminalToggleBtn.addEventListener('click', () => {
    soundEngine.playClick();
    terminalDrawer.classList.toggle('open');
    if (terminalDrawer.classList.contains('open')) {
        terminalInput.focus();
    }
});

closeTerminalBtn.addEventListener('click', () => terminalDrawer.classList.remove('open'));
clearTerminalBtn.addEventListener('click', () => {
    terminalBody.innerHTML = '<div class="term-line info">[+] Terminal buffer cleared. Ready for hacker commands...</div>';
});

// Append lines to Terminal
function appendTerminalLine(text, type = 'info') {
    const line = document.createElement('div');
    line.className = `term-line ${type}`;
    line.textContent = text;
    terminalBody.appendChild(line);
    terminalBody.scrollTop = terminalBody.scrollHeight;
}

// Terminal commands runner
terminalInput.addEventListener('keydown', async (e) => {
    if (e.key === 'Enter') {
        const cmd = terminalInput.value.trim();
        if (!cmd) return;
        soundEngine.playBeep(900, 0.05);
        appendTerminalLine(`joo@dark-ai:~$ ${cmd}`, 'highlight');
        terminalInput.value = '';
        await executeTerminalCommand(cmd);
    }
});

async function executeTerminalCommand(cmd) {
    const parts = cmd.split(' ');
    const mainCmd = parts[0].toLowerCase();
    const arg = parts.slice(1).join(' ').trim();

    if (mainCmd === 'help') {
        appendTerminalLine('Available Hacker Commands:', 'warn');
        appendTerminalLine('  scan <domain>     : Run live real scan (DNS, SSL, Headers)', 'info');
        appendTerminalLine('  ssl <domain>      : Real SSL/TLS handshake & cipher check', 'info');
        appendTerminalLine('  headers <domain>  : Real HTTP Security headers auditor', 'info');
        appendTerminalLine('  hash <string>     : Calculate real MD5 & SHA-256 hashes', 'info');
        appendTerminalLine('  dump              : Simulate database tables extraction', 'info');
        appendTerminalLine('  clear             : Clear the terminal screen', 'info');
    } else if (mainCmd === 'clear') {
        terminalBody.innerHTML = '';
    } else if (mainCmd === 'scan') {
        const target = arg || targetInput.value;
        appendTerminalLine(`[*] Sending live probe to target: ${target}...`, 'info');
        try {
            const res = await fetch('/api/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target })
            });
            const data = await res.json();
            appendTerminalLine(`[✔] Host resolved: ${data.host}`, 'success');
            if (data.dns && data.dns.ips) {
                appendTerminalLine(`[+] IP Addresses: ${data.dns.ips.join(', ')}`, 'success');
            }
            if (data.headers) {
                appendTerminalLine(`[!] Risk Grade: ${data.headers.risk_grade}`, data.headers.risk_grade.includes('F') ? 'danger' : 'warn');
                appendTerminalLine(`[!] Missing Headers: ${data.headers.missing_security_headers ? data.headers.missing_security_headers.length : 0}`, 'warn');
            }
            if (data.ssl && data.ssl.details) {
                appendTerminalLine(`[+] SSL Cipher: ${data.ssl.details.cipher_suite}`, 'info');
            }
        } catch (err) {
            appendTerminalLine(`[-] Failed to connect: ${err.message}`, 'danger');
        }
    } else if (mainCmd === 'hash') {
        const text = arg || 'admin';
        appendTerminalLine(`[*] Generating real cryptographic hashes for "${text}"...`, 'info');
        try {
            const res = await fetch('/api/crypto', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, action: 'hash' })
            });
            const data = await res.json();
            appendTerminalLine(`[MD5]    ${data.md5}`, 'success');
            appendTerminalLine(`[SHA256] ${data.sha256}`, 'highlight');
            appendTerminalLine(`[Base64] ${data.base64}`, 'info');
        } catch (e) {
            appendTerminalLine(`[-] Error: ${e.message}`, 'danger');
        }
    } else if (mainCmd === 'dump') {
        handleQuickAction('dump_db');
    } else {
        appendTerminalLine(`Command '${mainCmd}' sent to JOO AI Neural Engine...`, 'info');
        sendMessage(cmd);
    }
}

// Show Toast
function showToast(msg) {
    toastMsg.textContent = msg;
    toastNotification.classList.add('show');
    setTimeout(() => toastNotification.classList.remove('show'), 2800);
}

// Clear Chat
clearChatBtn.addEventListener('click', async () => {
    if (confirm('تفريغ سجل المحادثة وقاعدة البيانات بالكامل؟')) {
        localStorage.removeItem('joo_chat_history');
        try {
            await fetch('/api/clear_history', { method: 'POST' });
        } catch (e) {}
        chatHistory.innerHTML = `
            <div class="system-message-banner">
                <i class="fa-solid fa-skull text-danger"></i>
                <span>تم تفريغ المحادثة وإعادة تهيئة قاعدة بيانات <strong>JOO AI DARK</strong>.</span>
            </div>
        `;
        showToast('تم مسح المحادثة وقاعدة البيانات');
    }
});

// Auto-expand textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Submit Chat Form
chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = messageInput.value.trim();
    if (!text || isProcessing) return;
    sendMessage(text);
    messageInput.value = '';
    messageInput.style.height = 'auto';
});

messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// Quick prompt pill
function sendPrompt(text) {
    if (isProcessing) return;
    sendMessage(text);
}

// Real Scan Button Click
startRealScanBtn.addEventListener('click', () => {
    const target = targetInput.value.trim();
    if (!target) {
        showToast('برجاء كتابة رابط الهدف أولاً');
        return;
    }
    soundEngine.playAlert();
    sendMessage(`اعمل فحص حقيقي شامل وسريع للهدف: ${target}`);
});

// Send User Message & Handle Hacker AI Response
async function sendMessage(userText) {
    isProcessing = true;
    soundEngine.playClick();

    // Render User Message
    const userRow = document.createElement('div');
    userRow.className = 'message-row user-row';
    const timeNow = getCurrentTime();
    userRow.innerHTML = `
        <div class="message-content-wrapper">
            <div class="message-bubble user-bubble">
                <p>${escapeHTML(userText)}</p>
            </div>
            <div class="message-meta">
                <span>${timeNow}</span>
                <i class="fa-solid fa-check-double text-cyan"></i>
            </div>
        </div>
        <div class="avatar-box user-avatar">
            <i class="fa-solid fa-user"></i>
        </div>
    `;
    chatHistory.appendChild(userRow);
    scrollToBottom();

    // Show Typing Indicator
    typingIndicator.classList.remove('hidden');
    typingText.textContent = `JOO AI DARK يخترق الحزم ويحلل أمرك: "${userText.slice(0, 30)}..."`;
    scrollToBottom();

    appendTerminalLine(`[*] Intercepted: "${userText}"`, 'info');

        // Helper to persist message locally for Vercel Serverless
        appendLocalHistory({ role: 'user', message: userText, created_at: timeNow });

        const localApiKey = localStorage.getItem('joo_api_key') || '';
        const localProvider = localStorage.getItem('joo_ai_provider') || 'gemini';

        // Call Real Backend API with Hacker Persona
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: userText,
                target: targetInput.value.trim() || 'google.com',
                api_key: localApiKey,
                ai_provider: localProvider
            })
        });

        const data = await response.json();
        
        setTimeout(() => {
            typingIndicator.classList.add('hidden');
            renderHackerAIResponse(data);
            isProcessing = false;
            soundEngine.playSuccess();
            scrollToBottom();
        }, 800);

    } catch (err) {
        // Fallback offline handler
        setTimeout(() => {
            typingIndicator.classList.add('hidden');
            renderHackerAIResponse({
                title: "تم استلام أمرك من قبل JOO AI DARK",
                text: `أنا معاك يا بطل. متصل محلياً وجاهز لتنفيذ أي فحص على السيرفر المستهدف: ${targetInput.value}.`,
                badge: "OFFLINE / LOCAL CORE",
                code: `TARGET: ${targetInput.value}\nSTATUS: READY`
            });
            isProcessing = false;
            soundEngine.playSuccess();
            scrollToBottom();
        }, 800);
    }
}

// Render Hacker AI Response Card
function renderHackerAIResponse(resData, saveLocally = true) {
    if (saveLocally) {
        appendLocalHistory({
            role: 'ai',
            message: resData.text,
            title: resData.title,
            badge: resData.badge,
            code: resData.code,
            created_at: getCurrentTime()
        });
    }
    const timeNow = getCurrentTime();
    const aiRow = document.createElement('div');
    aiRow.className = 'message-row ai-row';

    const formattedText = (resData.text || '').replace(/\n/g, '<br>');

    aiRow.innerHTML = `
        <div class="avatar-box ai-avatar">
            <i class="fa-solid fa-skull text-danger"></i>
            <span class="ai-glow-ring"></span>
        </div>
        <div class="message-content-wrapper">
            <div class="message-bubble ai-bubble">
                <div class="ai-header-status">
                    <span class="ai-label"><i class="fa-solid fa-terminal text-cyan"></i> JOO AI DARK // HACKER INTEL</span>
                    <span class="scan-time-badge"><i class="fa-solid fa-shield"></i> ${resData.badge || 'LIVE VERIFIED'}</span>
                </div>
                <div class="ai-main-text">
                    <h3 class="result-title text-success">
                        <i class="fa-solid fa-circle-exclamation text-warning"></i>
                        ${escapeHTML(resData.title || 'تم اكتمال العملية بنجاح')}
                    </h3>
                    <div class="result-question" style="font-size: 0.98rem; line-height: 1.7;">
                        ${formattedText}
                    </div>
                </div>

                ${resData.code ? `
                <div class="vuln-details-card">
                    <div class="vuln-header">
                        <span class="vuln-tag high">LIVE SYSTEM LOG</span>
                        <span class="vuln-param">Target: <code>${escapeHTML(targetInput.value)}</code></span>
                    </div>
                    <div class="code-preview">
                        <code>${escapeHTML(resData.code).replace(/\n/g, '<br>')}</code>
                    </div>
                </div>` : ''}

                <div class="action-buttons-group">
                    <button class="action-btn primary" onclick="sendPrompt('افحص الهيدرز الحقيقية وشوف الثغرات')">
                        <i class="fa-solid fa-shield-virus"></i> فحص الهيدرز الحقيقي
                    </button>
                    <button class="action-btn secondary" onclick="sendPrompt('افحص تشفير الـ SSL وبورت 443')">
                        <i class="fa-solid fa-lock"></i> كشف شهادة الـ SSL
                    </button>
                    <button class="action-btn outline" onclick="openCryptoModal()">
                        <i class="fa-solid fa-key"></i> أداة الهاشات والباسوردات
                    </button>
                </div>
            </div>
            <div class="message-meta">
                <span>${timeNow}</span>
                <span class="ai-model-tag">JOO-HACKER-ENGINE-V3.5</span>
            </div>
        </div>
    `;

    chatHistory.appendChild(aiRow);
    appendTerminalLine(`[✔] JOO AI DARK: ${resData.title}`, 'success');
}

// Quick action buttons dispatcher
window.handleQuickAction = function(actionType) {
    if (actionType === 'dump_db') {
        sendMessage('اسحبلي كل داتا الموقع دلوقتي واكشف الجداول');
    } else if (actionType === 'deep_scan') {
        sendMessage('كمل فحص باقي المسارات والـ Endpoints المخفية');
    } else if (actionType === 'exploit_payload') {
        sendMessage('وريني كود البايلود كامل وطريقة تنفيذه في المتصفح');
    }
};

// Copy code action
window.copyCode = function(button) {
    soundEngine.playClick();
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fa-solid fa-check"></i> تم النسخ!';
    showToast('تم النسخ إلى الحافظة');
    setTimeout(() => button.innerHTML = originalText, 2000);
};

// Copy Result Text
window.copyResultText = function(elementId) {
    soundEngine.playClick();
    const text = document.getElementById(elementId).textContent;
    navigator.clipboard.writeText(text);
    showToast('تم نسخ القيمة للحافظة بنجاح');
};

// Crypto Modal Handlers
function openCryptoModal() {
    soundEngine.playClick();
    cryptoModal.classList.add('open');
    runCryptoCalculation();
}

closeCryptoModalBtn.addEventListener('click', () => {
    cryptoModal.classList.remove('open');
});

runCryptoBtn.addEventListener('click', () => {
    runCryptoCalculation();
});

async function runCryptoCalculation() {
    const text = cryptoTextInput.value.trim() || 'Admin2026!';
    soundEngine.playClick();
    try {
        const res = await fetch('/api/crypto', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, action: 'hash' })
        });
        const data = await res.json();
        document.getElementById('entropyVal').textContent = `${data.entropy} bits - ${data.strength}`;
        document.getElementById('sha256Val').textContent = data.sha256;
        document.getElementById('md5Val').textContent = data.md5;
        document.getElementById('b64Val').textContent = data.base64;
        showToast('تم حساب الهاشات وقوة الباسورد بنجاح');
    } catch (e) {
        showToast('خطأ في الاتصال بمحرك التشفير');
    }
}

// Sidebar tools buttons click handlers
document.querySelectorAll('.tool-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        soundEngine.playClick();
        document.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const action = btn.dataset.action;

        if (action === 'headers') {
            sendMessage(`افحص الـ Security Headers والتسريبات في السيرفر: ${targetInput.value}`);
        } else if (action === 'ssl') {
            sendMessage(`افحص شهادة الـ SSL والتشفير لبورت 443 على: ${targetInput.value}`);
        } else if (action === 'dns') {
            sendMessage(`اكشف الـ IP الفعلي وسيرفرات الـ DNS لنطاق: ${targetInput.value}`);
        } else if (action === 'crypto') {
            openCryptoModal();
        } else if (action === 'entropy') {
            openCryptoModal();
        } else if (action === 'dump') {
            sendMessage('اسحبلي محاكاة جداول المشرفين والبيانات');
        }
    });
});

// Utility functions
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function getCurrentTime() {
    const now = new Date();
    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const isPM = hours >= 12;
    hours = hours % 12 || 12;
    return `${hours}:${minutes} ${isPM ? 'م' : 'ص'}`;
}

function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}

// AI Model Configuration Modal Elements
const aiConfigBtn = document.getElementById('aiConfigBtn');
const aiConfigModal = document.getElementById('aiConfigModal');
const closeAiConfigModalBtn = document.getElementById('closeAiConfigModalBtn');
const saveAiConfigBtn = document.getElementById('saveAiConfigBtn');
const aiProviderSelect = document.getElementById('aiProviderSelect');
const aiApiKeyInput = document.getElementById('aiApiKeyInput');

aiConfigBtn.addEventListener('click', async () => {
    soundEngine.playClick();
    aiConfigModal.classList.add('open');
    try {
        const res = await fetch('/api/settings');
        const data = await res.json();
        if (data.ai_provider) {
            aiProviderSelect.value = data.ai_provider;
        }
    } catch (e) {}
});

closeAiConfigModalBtn.addEventListener('click', () => {
    aiConfigModal.classList.remove('open');
});

saveAiConfigBtn.addEventListener('click', async () => {
    const provider = aiProviderSelect.value;
    const apiKey = aiApiKeyInput.value.trim();
    if (!apiKey) {
        showToast('يرجى كتابة أو لصق مفتاح الـ API');
        return;
    }
    soundEngine.playClick();
    
    const payload = { ai_provider: provider };
    if (provider === 'gemini') payload.gemini_api_key = apiKey;
    else if (provider === 'groq') payload.groq_api_key = apiKey;
    else if (provider === 'openai') payload.openai_api_key = apiKey;

    try {
        localStorage.setItem('joo_api_key', apiKey);
        localStorage.setItem('joo_ai_provider', provider);

        const res = await fetch('/api/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        aiConfigModal.classList.remove('open');
        aiApiKeyInput.value = '';
        showToast(`تم حفظ مفتاح ${provider.toUpperCase()} بنجاح!`);
        appendTerminalLine(`[✔] AI Neural Provider connected: ${provider.toUpperCase()}`, 'success');
    } catch (e) {
        showToast('خطأ في حفظ إعدادات الـ AI');
    }
});

function appendLocalHistory(msgObj) {
    try {
        const hist = JSON.parse(localStorage.getItem('joo_chat_history') || '[]');
        hist.push(msgObj);
        if (hist.length > 50) hist.shift();
        localStorage.setItem('joo_chat_history', JSON.stringify(hist));
    } catch(e) {}
}

// Load Chat History from SQLite Database or LocalStorage (Vercel Serverless)
async function loadChatHistoryFromDB() {
    let messages = [];
    try {
        const res = await fetch('/api/history');
        messages = await res.json();
    } catch (e) {}

    // Fallback to localStorage if hosted on Vercel Serverless
    if (!messages || messages.length === 0) {
        try {
            messages = JSON.parse(localStorage.getItem('joo_chat_history') || '[]');
        } catch (e) {}
    }

    if (messages && messages.length > 0) {
        chatHistory.innerHTML = `
            <div class="system-message-banner">
                <i class="fa-solid fa-database text-green"></i>
                <span>تم استرجاع سجل الجلسات السابقة بنجاح</span>
            </div>
        `;
        messages.forEach(msg => {
            if (msg.role === 'user') {
                const userRow = document.createElement('div');
                userRow.className = 'message-row user-row';
                userRow.innerHTML = `
                    <div class="message-content-wrapper">
                        <div class="message-bubble user-bubble">
                            <p>${escapeHTML(msg.message)}</p>
                        </div>
                        <div class="message-meta">
                            <span>${msg.created_at ? msg.created_at.slice(11, 16) : ''}</span>
                            <i class="fa-solid fa-check-double text-green"></i>
                        </div>
                    </div>
                    <div class="avatar-box user-avatar">
                        <i class="fa-solid fa-user-secret"></i>
                    </div>
                `;
                chatHistory.appendChild(userRow);
            } else {
                renderHackerAIResponse({
                    title: msg.title || 'JOO AI DARK',
                    text: msg.message,
                    badge: msg.badge || 'RECORDED INTEL',
                    code: msg.code || ''
                }, false);
            }
        });
        scrollToBottom();
    }
}

// Trigger DB history load
window.addEventListener('DOMContentLoaded', () => {
    loadChatHistoryFromDB();
});
