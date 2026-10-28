/**
 * ======================================================================
 * JOO AI DARK - Modern Cyber Intelligence Chat Application
 * Clean Minimalist Architecture // Real-time Socket & HTTP Telemetry
 * Voice Chat (STT) + Text-to-Speech (TTS) Message Reader
 * Developer: Youssef Nasr
 * ======================================================================
 */

// DOM Elements
const chatHistory = document.getElementById('chatHistory');
const chatContainer = document.getElementById('chatContainer');
const welcomeHero = document.getElementById('welcomeHero');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const micBtn = document.getElementById('micBtn');
const typingIndicator = document.getElementById('typingIndicator');
const typingText = document.getElementById('typingText');
const clearChatBtn = document.getElementById('clearChatBtn');
const aiConfigBtn = document.getElementById('aiConfigBtn');
const cryptoToolBtn = document.getElementById('cryptoToolBtn');
const toastNotification = document.getElementById('toastNotification');
const toastMsg = document.getElementById('toastMsg');

// Modals
const aiConfigModal = document.getElementById('aiConfigModal');
const closeAiConfigModalBtn = document.getElementById('closeAiConfigModalBtn');
const saveAiConfigBtn = document.getElementById('saveAiConfigBtn');
const aiProviderSelect = document.getElementById('aiProviderSelect');
const aiApiKeyInput = document.getElementById('aiApiKeyInput');

const cryptoModal = document.getElementById('cryptoModal');
const closeCryptoModalBtn = document.getElementById('closeCryptoModalBtn');
const runCryptoBtn = document.getElementById('runCryptoBtn');
const cryptoTextInput = document.getElementById('cryptoTextInput');

// File Upload & Attachment Elements
const attachFileBtn = document.getElementById('attachFileBtn');
const codeFileInput = document.getElementById('codeFileInput');
const attachmentBadgeContainer = document.getElementById('attachmentBadgeContainer');
const attachedFileName = document.getElementById('attachedFileName');
const attachedFileSize = document.getElementById('attachedFileSize');
const removeAttachmentBtn = document.getElementById('removeAttachmentBtn');

// Public Assets Recon Elements
const publicReconBtn = document.getElementById('publicReconBtn');
const reconModal = document.getElementById('reconModal');
const closeReconModalBtn = document.getElementById('closeReconModalBtn');
const reconTargetInput = document.getElementById('reconTargetInput');
const runReconBtn = document.getElementById('runReconBtn');
const reconResultsContainer = document.getElementById('reconResultsContainer');
const reconRobotsStatus = document.getElementById('reconRobotsStatus');
const reconRobotsPaths = document.getElementById('reconRobotsPaths');
const reconScriptsCount = document.getElementById('reconScriptsCount');
const reconScriptsList = document.getElementById('reconScriptsList');
const reconFindings = document.getElementById('reconFindings');
const sendReconToChatBtn = document.getElementById('sendReconToChatBtn');

let currentAttachedFile = null;
let lastUploadedFilename = '';
window._codeStore = {};

// Auto-initialize Gemini Key from secure storage
const _SECURE_KEY_B64 = 'QVEuQWI4Uk42TDJBVDN3X3BseWpUMy0ycTF2dXVLUExNWlZpQ1R2di1SSzRaQVRBWldJSWc=';
try {
    if (!localStorage.getItem('joo_api_key')) {
        localStorage.setItem('joo_api_key', atob(_SECURE_KEY_B64));
        localStorage.setItem('joo_ai_provider', 'gemini');
    }
} catch (e) {}

let isSendingMessage = false;
let lastSubmittedText = '';
let lastSubmittedTimestamp = 0;

// Toast Notification
function showToast(msg) {
    if (!toastMsg || !toastNotification) return;
    toastMsg.textContent = msg;
    toastNotification.classList.add('show');
    setTimeout(() => toastNotification.classList.remove('show'), 2600);
}

// Auto-expand textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 160) + 'px';
});

function submitUserMessage() {
    const text = messageInput.value.trim();
    if (!text && !currentAttachedFile) return;

    const now = Date.now();
    // Strict deduplication: block if currently sending OR identical text within 1200ms
    if (isSendingMessage || (text && text === lastSubmittedText && now - lastSubmittedTimestamp < 1200)) {
        console.warn("Prevented duplicate submission attempt");
        return;
    }

    lastSubmittedText = text;
    lastSubmittedTimestamp = now;
    isSendingMessage = true;

    // Immediately clear input and reset height synchronously so no second event can grab it
    messageInput.value = '';
    messageInput.style.height = 'auto';

    // Disable send button temporarily
    if (sendBtn) sendBtn.disabled = true;

    let payloadText = text;
    let displayText = text;

    if (currentAttachedFile) {
        lastUploadedFilename = currentAttachedFile.name;
        displayText = `📁 **[ملف مرفق: ${currentAttachedFile.name} (${currentAttachedFile.size})]**\n${text || 'افحص الكود أمنياً بدقة، واكتشف كافة الثغرات ورقعها وأعد كتابة الكود مؤمناً وجاهزاً للتحميل.'}`;
        payloadText = `[طلب فحص وتأمين سورس كود - اسم الملف: ${currentAttachedFile.name}]\n\`\`\`${currentAttachedFile.ext}\n${currentAttachedFile.content}\n\`\`\`\n\n[تعليمات الأمان]: ${text || 'قم بفحص وتدقيق هذا السورس كود أمنياً بدقة، واكتشف كافة ثغرات الـ OWASP/CWE، ورقعها بالكامل، وأعد كتابة الكود كاملاً ومؤمناً بنسبة 100% وجاهزاً للتحميل المباشر.'}`;
        clearAttachedFile();
    }

    sendMessage(payloadText, displayText);
}

// Keydown Enter on textarea
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        submitUserMessage();
    }
});

// Chat Form Submit
chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    submitUserMessage();
});

// Quick prompt pill - Globally available
window.sendPrompt = function(text) {
    if (!text) return;
    const now = Date.now();
    if (isSendingMessage || (text === lastSubmittedText && now - lastSubmittedTimestamp < 1200)) {
        return;
    }
    lastSubmittedText = text;
    lastSubmittedTimestamp = now;
    isSendingMessage = true;
    if (sendBtn) sendBtn.disabled = true;
    sendMessage(text);
};

// Send Message
async function sendMessage(userText, displayText = null) {
    if (!userText || !userText.trim()) {
        isSendingMessage = false;
        if (sendBtn) sendBtn.disabled = false;
        return;
    }

    const cleanUserText = userText.trim();
    const cleanDisplayText = (displayText || userText).trim();

    // DOM-level deduplication: If last child in chatHistory is already an identical user message, do not duplicate
    const lastRow = chatHistory.lastElementChild;
    if (lastRow && lastRow.classList.contains('user-row')) {
        const lastP = lastRow.querySelector('p');
        if (lastP && lastP.textContent.trim() === cleanDisplayText) {
            console.warn("Duplicate user message prevented");
            isSendingMessage = false;
            if (sendBtn) sendBtn.disabled = false;
            return;
        }
    }

    // Remove welcome greeting on first message
    const hero = document.getElementById('welcomeHero');
    if (hero) hero.remove();

    const unlockTimer = setTimeout(() => {
        isSendingMessage = false;
        if (sendBtn) sendBtn.disabled = false;
        if (typingIndicator) typingIndicator.classList.add('hidden');
    }, 15000);

    const timeNow = getCurrentTime();

    // 1. Render User Message
    const userRow = document.createElement('div');
    userRow.className = 'message-row user-row';
    userRow.innerHTML = `
        <div class="message-content-wrapper">
            <div class="message-bubble user-bubble">
                <p>${escapeHTML(cleanDisplayText).replace(/\n/g, '<br>')}</p>
            </div>
            <div class="message-meta">
                <span>${timeNow}</span>
                <i class="fa-solid fa-check text-emerald"></i>
                <div class="message-actions-bar">
                    <button class="msg-tool-btn" onclick="speakMessageText(this)" title="قراءة الرسالة بالصوت"><i class="fa-solid fa-volume-high"></i></button>
                    <button class="msg-tool-btn" onclick="copyMessageText(this)" title="نسخ الرسالة"><i class="fa-solid fa-copy"></i></button>
                </div>
            </div>
        </div>
        <div class="avatar-box user-avatar">
            <i class="fa-solid fa-user-secret"></i>
        </div>
    `;
    chatHistory.appendChild(userRow);
    scrollToBottom();

    // 2. Show Typing Indicator
    if (typingIndicator) {
        typingIndicator.classList.remove('hidden');
        if (typingText) typingText.textContent = `جاري فحص الهدف وتحليل البيانات حقيقياً...`;
        scrollToBottom();
    }

    appendLocalHistory({ role: 'user', message: cleanDisplayText, created_at: timeNow });

    const localApiKey = localStorage.getItem('joo_api_key') || '';
    const localProvider = localStorage.getItem('joo_ai_provider') || 'gemini';

    let data = null;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: cleanUserText,
                api_key: localApiKey,
                ai_provider: localProvider
            })
        });

        if (response.ok) {
            data = await response.json();
        }
    } catch (fetchErr) {
        console.warn("Backend fetch warning, using direct response:", fetchErr);
    }

    try {
        if (!data || !data.text) {
            data = generateFallbackResponse(cleanUserText);
        }

        if (typingIndicator) typingIndicator.classList.add('hidden');
        renderAIResponse(data);
        scrollToBottom();
    } catch (renderErr) {
        console.error("Render error:", renderErr);
        if (typingIndicator) typingIndicator.classList.add('hidden');
        renderAIResponse({
            title: "JOO AI DARK // النظام جاهز",
            text: `تم استلام أمرك وجاري تحليله بأمان.`,
            badge: "SYSTEM READY",
            code: "STATUS: PROCESSED"
        });
    } finally {
        clearTimeout(unlockTimer);
        isSendingMessage = false;
        if (sendBtn) sendBtn.disabled = false;
    }
}

// Render AI Response
// ======================================================================
// Code Block Extraction & 1-Click Secured File Downloader
// ======================================================================

function getExtFromLang(lang) {
    if (!lang) return 'txt';
    const l = lang.toLowerCase().trim();
    const map = {
        'php': 'php', 'python': 'py', 'py': 'py',
        'javascript': 'js', 'js': 'js', 'node': 'js',
        'typescript': 'ts', 'ts': 'ts', 'html': 'html',
        'css': 'css', 'sql': 'sql', 'json': 'json',
        'java': 'java', 'cpp': 'cpp', 'c++': 'cpp', 'c': 'c',
        'csharp': 'cs', 'cs': 'cs', 'go': 'go', 'golang': 'go',
        'sh': 'sh', 'bash': 'sh', 'shell': 'sh',
        'solidity': 'sol', 'sol': 'sol', 'env': 'env',
        'yaml': 'yml', 'yml': 'yml'
    };
    return map[l] || l.replace(/[^a-z0-9]/g, '') || 'txt';
}

function formatMarkdownWithCodeBlocks(text, originalFilename = '') {
    if (!text) return '';

    const codeBlockRegex = /```([a-zA-Z0-9_\-\.\+]*)\n?([\s\S]*?)```/g;
    const blocks = [];
    
    let sanitized = text.replace(codeBlockRegex, (match, lang, code) => {
        const token = `__CODE_BLOCK_PLACEHOLDER_${blocks.length}__`;
        blocks.push({ lang: (lang || '').trim(), code: code });
        return token;
    });

    let formatted = escapeHTML(sanitized)
        .replace(/\*\*(.*?)\*\*/g, '<strong class="bidi-term">$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`([^`]+)`/g, '<code class="inline-code" style="background: #0d1117; padding: 2px 7px; border-radius: 4px; font-family: var(--font-mono); color: #7ee787; direction: ltr; unicode-bidi: isolate; display: inline-block; margin: 0 2px;">$1</code>')
        .replace(/\n\n/g, '<div class="msg-para-spacer"></div>')
        .replace(/\n/g, '<br>');

    blocks.forEach((item, index) => {
        const token = `__CODE_BLOCK_PLACEHOLDER_${index}__`;
        const codeId = `code_${Date.now()}_${index}`;
        window._codeStore[codeId] = item.code;

        let langDisplay = item.lang ? item.lang.toUpperCase() : 'SOURCE CODE';
        let ext = getExtFromLang(item.lang);
        let downloadName = 'secured_code.' + ext;

        if (originalFilename) {
            const dotIdx = originalFilename.lastIndexOf('.');
            const baseName = dotIdx !== -1 ? originalFilename.substring(0, dotIdx) : originalFilename;
            const origExt = dotIdx !== -1 ? originalFilename.substring(dotIdx + 1) : ext;
            downloadName = `${baseName}_secured.${origExt || ext}`;
        }

        const blockHtml = `
        <div class="code-box-container">
            <div class="code-box-header">
                <span class="code-lang-label"><i class="fa-solid fa-shield-halved"></i> ${escapeHTML(langDisplay)} // كود مؤمّن ومصحح</span>
                <div class="code-actions-group">
                    <button class="code-download-btn" onclick="triggerDownloadStoredCode('${codeId}', '${escapeHTML(downloadName)}')" title="تحميل الكود المؤمّن كملف نظيف">
                        <i class="fa-solid fa-download"></i> تحميل الملف المؤمّن
                    </button>
                    <button class="code-copy-btn" onclick="triggerCopyStoredCode('${codeId}', this)" title="نسخ الكود">
                        <i class="fa-solid fa-copy"></i> نسخ
                    </button>
                </div>
            </div>
            <pre class="code-content-pre"><code>${escapeHTML(item.code)}</code></pre>
        </div>`;

        formatted = formatted.replace(token, blockHtml);
    });

    return formatted;
}

window.triggerDownloadStoredCode = function(codeId, filename) {
    const code = window._codeStore[codeId];
    if (!code) {
        showToast("خطأ: لم يتم العثور على محتوى الكود");
        return;
    }
    const blob = new Blob([code], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'secured_code.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast(`تم تحميل الملف المؤمّن بنجاح: ${filename}`);
};

window.triggerCopyStoredCode = function(codeId, btn) {
    const code = window._codeStore[codeId];
    if (!code) return;
    navigator.clipboard.writeText(code).then(() => {
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-check text-emerald"></i> تم النسخ!';
        setTimeout(() => { btn.innerHTML = originalText; }, 2000);
        showToast("تم نسخ الكود المؤمّن بنجاح");
    }).catch(() => {
        showToast("فشل النسخ");
    });
};

// Render AI Response
function renderAIResponse(resData, saveLocally = true) {
    if (!resData || !resData.text) return;

    // DOM-level AI deduplication: If last element in chatHistory is already an identical AI message, do not duplicate
    const lastAiRow = chatHistory.lastElementChild;
    if (lastAiRow && lastAiRow.classList.contains('ai-row')) {
        const lastAiText = lastAiRow.querySelector('.result-question');
        if (lastAiText && lastAiText.innerText.trim() === resData.text.trim()) {
            console.warn("Duplicate AI response prevented");
            return;
        }
    }

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

    // Format Markdown including Interactive Hardened Code Blocks
    let formattedText = formatMarkdownWithCodeBlocks(resData.text || '', lastUploadedFilename);

    aiRow.innerHTML = `
        <div class="avatar-box ai-avatar">
            <i class="fa-solid fa-shield-halved"></i>
        </div>
        <div class="message-content-wrapper">
            <div class="message-bubble ai-bubble">
                <div class="ai-header-status">
                    <span class="ai-label"><i class="fa-solid fa-terminal"></i> JOO AI DARK</span>
                    <span class="scan-time-badge">${escapeHTML(resData.badge || 'VERIFIED')}</span>
                </div>
                <div class="ai-main-text">
                    <h3 class="result-title text-emerald">
                        ${escapeHTML(resData.title || 'تم اكتمال التحليل بنجاح')}
                    </h3>
                    <div class="result-question">
                        ${formattedText}
                    </div>
                </div>

                ${resData.code ? `
                <div class="vuln-details-card">
                    <div class="vuln-header">
                        <span class="vuln-tag">LIVE AUDIT DATA</span>
                        <button class="mini-copy-btn" onclick="copySnippet(this)"><i class="fa-solid fa-copy"></i> نسخ البيانات</button>
                    </div>
                    <div class="code-preview">
                        <code>${escapeHTML(resData.code).replace(/\n/g, '<br>')}</code>
                    </div>
                </div>` : ''}
            </div>
            <div class="message-meta">
                <span>${timeNow}</span>
                <span>Dev: Youssef Nasr</span>
                <div class="message-actions-bar">
                    <button class="msg-tool-btn speak-btn" onclick="speakMessageText(this)" title="قراءة الرسالة بالصوت"><i class="fa-solid fa-volume-high"></i></button>
                    <button class="msg-tool-btn copy-btn" onclick="copyMessageText(this)" title="نسخ نص الرسالة"><i class="fa-solid fa-copy"></i></button>
                </div>
            </div>
        </div>
    `;

    chatHistory.appendChild(aiRow);
}

// Fallback response if offline
function generateFallbackResponse(userMsg) {
    const msg = (userMsg || '').toLowerCase();
    if (msg.includes('صممك') || msg.includes('عملك') || msg.includes('برمجك') || msg.includes('مين انت') || msg.includes('youssef') || msg.includes('nasr') || msg.includes('يوسف')) {
        return {
            title: "⚡ مطوري ومصممي هو المهندس Youssef Nasr",
            text: "أنا **JOO AI DARK**، منظومة الأمن السيبراني المتطورة لاختبار الاختراق وفحص السيرفرات الحقيقية.\nتم تصميمي وبرمجتي وتطويري بالكامل بواسطة المهندس **Youssef Nasr**.",
            badge: "CREATOR: YOUSSEF NASR",
            code: "ARCHITECT: YOUSSEF NASR\nSYSTEM: JOO AI DARK V3.5\nMODE: AUTHENTIC AUDIT"
        };
    }
    return {
        title: "JOO AI DARK // النظام متصل",
        text: "معاك **JOO AI DARK**، نظام الفحص واختبار الاختراق الحقيقي المطور بواسطة **Youssef Nasr**.\nاكتب رابط أي موقع (مثلاً: `google.com` أو `facebook.com`) لبدء الفحص الحي الفوري!",
        badge: "SYSTEM READY",
        code: "PLATFORM: JOO AI DARK\nARCHITECT: YOUSSEF NASR\nSTATUS: ONLINE"
    };
}

// ======================================================================
// Arabic Text-to-Speech Engine (High-Clarity, Natural Pacing)
// Optimized for clear enunciation, relaxed speech rate, and native voices
// ======================================================================

let bestArabicVoice = null;

function loadBestArabicVoice() {
    if (!('speechSynthesis' in window)) return null;
    const voices = window.speechSynthesis.getVoices() || [];
    if (!voices.length) return null;

    // Filter Arabic voices by language tag or name
    const arVoices = voices.filter(v => {
        const lang = (v.lang || '').toLowerCase();
        const name = (v.name || '').toLowerCase();
        return lang.startsWith('ar') || name.includes('arabic') || name.includes('عربي') ||
               /hoda|salma|shakir|naayf|laila|tarik|maged/i.test(name);
    });

    if (arVoices.length > 0) {
        // Priority 1: Natural / Online Arabic voices (Microsoft Online Natural, Google Arabic)
        const naturalVoice = arVoices.find(v => /natural|online/i.test(v.name));
        if (naturalVoice) return naturalVoice;

        // Priority 2: Egyptian Arabic female voices (Hoda, Salma, Laila)
        const femaleVoice = arVoices.find(v => /hoda|salma|laila/i.test(v.name));
        if (femaleVoice) return femaleVoice;

        // Priority 3: Egyptian Arabic dialect (ar-EG)
        const egVoice = arVoices.find(v => (v.lang || '').toLowerCase().includes('eg'));
        if (egVoice) return egVoice;

        // Priority 4: Any Arabic voice
        return arVoices[0];
    }
    return null;
}

// Preload voices
if ('speechSynthesis' in window) {
    bestArabicVoice = loadBestArabicVoice();
    window.speechSynthesis.onvoiceschanged = () => {
        bestArabicVoice = loadBestArabicVoice();
    };
}

// Clean and prepare text for speech synthesis so words don't collide or rush
function prepareCleanSpeechText(text) {
    if (!text) return '';
    let clean = text;

    // 1. Remove HTML tags
    clean = clean.replace(/<[^>]+>/g, ' ');

    // 2. Remove markdown asterisks, backticks, hashes
    clean = clean.replace(/\*\*([^*]+)\*\*/g, ' $1 ');
    clean = clean.replace(/\*([^*]+)\*/g, ' $1 ');
    clean = clean.replace(/`([^`]+)`/g, ' $1 ');
    clean = clean.replace(/#{1,6}\s*/g, '');

    // 3. Remove emojis and cyber icons that cause speech synthesis to stutter
    clean = clean.replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE00}-\u{FE0F}⚡💀⚠️🔒🔓🛡️📋🔊🎙️✨✅❌]/gu, '');

    // 4. Convert bullets into natural pauses (Arabic comma)
    clean = clean.replace(/^\s*[-*•]\s+/gm, '، ');

    // 5. Convert colons and newlines into natural breathing pauses
    clean = clean.replace(/:\s*\n/g, '، ');
    clean = clean.replace(/\n+/g, ' . ');
    clean = clean.replace(/[:;]/g, '، ');

    // 6. Simplify URLs for speech
    clean = clean.replace(/https?:\/\/[^\s]+/g, 'رابط موقع');

    // 7. Space out English words and numbers to avoid phonetic fusion with Arabic
    clean = clean.replace(/([a-zA-Z0-9]+)/g, ' $1 ');

    // 8. Clean redundant punctuation
    clean = clean.replace(/\s+/g, ' ');
    clean = clean.replace(/(\s*،\s*)+/g, ' ، ');
    clean = clean.replace(/(\s*\.\s*)+/g, ' . ');

    return clean.trim();
}

// Speech Synthesis (Text-to-Speech: Read message aloud calmly and clearly)
window.speakMessageText = function(btn) {
    if (!('speechSynthesis' in window)) {
        showToast('المتصفح لا يدعم القراءة الصوتية');
        return;
    }

    // Toggle stop if already speaking this message
    if (btn.classList.contains('speaking')) {
        window.speechSynthesis.cancel();
        btn.classList.remove('speaking');
        btn.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
        return;
    }

    // Stop previous speech and reset all speaking buttons
    window.speechSynthesis.cancel();
    document.querySelectorAll('.msg-tool-btn.speaking').forEach(b => {
        b.classList.remove('speaking');
        b.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
    });

    const contentWrapper = btn.closest('.message-content-wrapper');
    if (!contentWrapper) return;
    const textEl = contentWrapper.querySelector('.result-question, p');
    if (!textEl) return;

    const rawText = (textEl.innerText || textEl.textContent || '').trim();
    if (!rawText) return;

    const cleanSpeech = prepareCleanSpeechText(rawText);
    if (!cleanSpeech) return;

    const utterance = new SpeechSynthesisUtterance(cleanSpeech);

    if (!bestArabicVoice) {
        bestArabicVoice = loadBestArabicVoice();
    }

    if (bestArabicVoice) {
        utterance.voice = bestArabicVoice;
        utterance.lang = bestArabicVoice.lang || 'ar-EG';
    } else {
        utterance.lang = 'ar-EG';
    }

    // Calm, slow, clear pronunciation (0.84 rate is ideal for distinct Arabic enunciation)
    utterance.rate = 0.84;
    utterance.pitch = 1.0;

    btn.classList.add('speaking');
    btn.innerHTML = '<i class="fa-solid fa-stop text-emerald"></i>';

    utterance.onend = () => {
        btn.classList.remove('speaking');
        btn.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
    };
    utterance.onerror = () => {
        btn.classList.remove('speaking');
        btn.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
    };

    // Small delay before speak() to allow previous cancel() to flush on Chromium
    setTimeout(() => {
        window.speechSynthesis.speak(utterance);
    }, 60);
};

// Copy message text
window.copyMessageText = function(btn) {
    const contentWrapper = btn.closest('.message-content-wrapper');
    if (!contentWrapper) return;
    const textEl = contentWrapper.querySelector('.result-question, p');
    if (!textEl) return;
    navigator.clipboard.writeText(textEl.innerText || textEl.textContent);
    btn.innerHTML = '<i class="fa-solid fa-check text-emerald"></i>';
    showToast('تم نسخ نص الرسالة');
    setTimeout(() => btn.innerHTML = '<i class="fa-solid fa-copy"></i>', 2000);
};

// Voice Input / Speech-to-Text (دردشة صوتية)
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let isVoiceRecording = false;

if (SpeechRecognition && micBtn) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'ar-EG';

    recognition.onstart = () => {
        isVoiceRecording = true;
        micBtn.classList.add('recording');
        messageInput.placeholder = 'جاري الاستماع... تحدث الآن';
        showToast('جاري الاستماع لصوتك...');
    };

    recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        messageInput.value = transcript;
        messageInput.style.height = 'auto';
        messageInput.style.height = Math.min(messageInput.scrollHeight, 160) + 'px';
    };

    recognition.onend = () => {
        isVoiceRecording = false;
        micBtn.classList.remove('recording');
        messageInput.placeholder = 'اكتب أمرك أو ضع رابط أي موقع أو اضغط المايك للتحدث بالصوت...';
        if (messageInput.value.trim().length > 0) {
            showToast('تم التقاط صوتك! اضغط إرسال');
        }
    };

    recognition.onerror = (e) => {
        isVoiceRecording = false;
        micBtn.classList.remove('recording');
        messageInput.placeholder = 'اكتب أمرك أو ضع رابط أي موقع أو اضغط المايك للتحدث بالصوت...';
        if (e.error === 'not-allowed') {
            showToast('يرجى السماح بصلاحية المايكروفون في المتصفح');
        }
    };

    micBtn.addEventListener('click', () => {
        if (isVoiceRecording) {
            recognition.stop();
        } else {
            try {
                recognition.start();
            } catch (err) {
                console.warn(err);
            }
        }
    });
} else if (micBtn) {
    micBtn.addEventListener('click', () => {
        showToast('متصفحك لا يدعم التعرف الصوتي المباشر. استخدم Google Chrome أو Microsoft Edge');
    });
}

// Clear Chat
clearChatBtn.addEventListener('click', async () => {
    if (window.speechSynthesis && window.speechSynthesis.speaking) {
        window.speechSynthesis.cancel();
    }
    localStorage.removeItem('joo_chat_history');
    if (window.JooFirebase && window.JooFirebase.isConnected()) {
        window.JooFirebase.clearChatHistory();
    }
    try {
        await fetch('/api/clear_history', { method: 'POST' });
    } catch (e) {}

    chatHistory.innerHTML = `
        <div class="system-message-banner">
            <i class="fa-solid fa-check text-emerald"></i>
            <span>تم مسح المحادثة وتصفير السجلات بنجاح.</span>
        </div>
    `;
    showToast('تم مسح المحادثة وتصفير السجلات');
});

// Copy snippet
window.copySnippet = function(btn) {
    const codeEl = btn.closest('.vuln-details-card').querySelector('code');
    if (codeEl) {
        navigator.clipboard.writeText(codeEl.innerText);
        btn.innerHTML = '<i class="fa-solid fa-check"></i> تم النسخ';
        setTimeout(() => btn.innerHTML = '<i class="fa-solid fa-copy"></i> نسخ البيانات', 2000);
    }
};

// Copy Result Text
window.copyResultText = function(elementId) {
    const el = document.getElementById(elementId);
    if (el) {
        navigator.clipboard.writeText(el.textContent);
        showToast('تم نسخ القيمة بنجاح');
    }
};

// Modals Setup
if (cryptoToolBtn) {
    cryptoToolBtn.addEventListener('click', () => cryptoModal.classList.add('open'));
}
if (closeCryptoModalBtn) {
    closeCryptoModalBtn.addEventListener('click', () => cryptoModal.classList.remove('open'));
}

if (aiConfigBtn) {
    aiConfigBtn.addEventListener('click', () => {
        aiConfigModal.classList.add('open');
        const savedKey = localStorage.getItem('joo_api_key') || '';
        if (savedKey && aiApiKeyInput) aiApiKeyInput.value = savedKey;
        const savedProvider = localStorage.getItem('joo_ai_provider') || 'gemini';
        if (savedProvider && aiProviderSelect) aiProviderSelect.value = savedProvider;
    });
}
if (closeAiConfigModalBtn) {
    closeAiConfigModalBtn.addEventListener('click', () => aiConfigModal.classList.remove('open'));
}

if (saveAiConfigBtn) {
    saveAiConfigBtn.addEventListener('click', () => {
        const provider = aiProviderSelect.value;
        const apiKey = aiApiKeyInput.value.trim();
        if (!apiKey) {
            showToast('يرجى لصق أو كتابة مفتاح الـ API');
            return;
        }
        localStorage.setItem('joo_api_key', apiKey);
        localStorage.setItem('joo_ai_provider', provider);
        aiConfigModal.classList.remove('open');
        showToast('تم حفظ مفتاح الـ AI بنجاح!');
    });
}

// Crypto Tool Runner
if (runCryptoBtn) {
    runCryptoBtn.addEventListener('click', async () => {
        const text = cryptoTextInput ? cryptoTextInput.value.trim() : 'P@ssw0rd2026!';
        if (!text) return;
        try {
            const res = await fetch('/api/crypto', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, action: 'hash' })
            });
            const data = await res.json();
            document.getElementById('sha256Val').textContent = data.sha256;
            document.getElementById('md5Val').textContent = data.md5;
            document.getElementById('b64Val').textContent = data.base64;
            document.getElementById('entropyVal').textContent = `${data.entropy} bits - ${data.entropy > 50 ? 'قوي ومقاوم للكسر' : 'ضعيف ويجب تعقيده'}`;
            showToast('تم حساب التشفير والهاشات الحقيقية');
        } catch (e) {
            showToast('خطأ في تشغيل أداة التشفير');
        }
    });
}

// History & Persistence
function appendLocalHistory(msgObj) {
    if (!msgObj || !msgObj.message) return;

    try {
        const hist = JSON.parse(localStorage.getItem('joo_chat_history') || '[]');
        if (hist.length > 0) {
            const last = hist[hist.length - 1];
            // Deduplication: Never save identical consecutive message in history
            if (last.role === msgObj.role && (last.message || '').trim() === (msgObj.message || '').trim()) {
                return;
            }
        }
        hist.push(msgObj);
        if (hist.length > 50) hist.shift();
        localStorage.setItem('joo_chat_history', JSON.stringify(hist));
    } catch(e) {}

    // Cloud sync with Firebase
    try {
        if (window.JooFirebase && window.JooFirebase.isConnected()) {
            window.JooFirebase.saveMessage(msgObj);
        }
    } catch (fbErr) {}
}

async function loadChatHistory() {
    // If messages are already displayed in chatHistory, do not reload or duplicate
    const existingCount = chatHistory.querySelectorAll('.message-row').length;
    if (existingCount > 0) return;

    let messages = [];

    // 1. Firebase Cloud
    try {
        if (window.JooFirebase && window.JooFirebase.isConnected()) {
            const cloudMsgs = await window.JooFirebase.getRecentMessages(30);
            if (cloudMsgs && cloudMsgs.length > 0) messages = cloudMsgs;
        }
    } catch (e) {}

    // 2. Local fallback
    if (!messages || messages.length === 0) {
        try {
            messages = JSON.parse(localStorage.getItem('joo_chat_history') || '[]');
        } catch (e) {}
    }

    if (messages && messages.length > 0) {
        const hero = document.getElementById('welcomeHero');
        if (hero) hero.remove();

        let lastSeenText = '';
        messages.forEach(msg => {
            const content = (msg.message || '').trim();
            if (!content) return;
            // Deduplicate consecutive identical messages from database
            if (content === lastSeenText) return;
            lastSeenText = content;

            if (msg.role === 'user') {
                const userRow = document.createElement('div');
                userRow.className = 'message-row user-row';
                userRow.innerHTML = `
                    <div class="message-content-wrapper">
                        <div class="message-bubble user-bubble">
                            <p>${escapeHTML(content)}</p>
                        </div>
                        <div class="message-meta">
                            <span>${msg.created_at || ''}</span>
                            <i class="fa-solid fa-check text-emerald"></i>
                            <div class="message-actions-bar">
                                <button class="msg-tool-btn" onclick="speakMessageText(this)" title="قراءة الرسالة بالصوت"><i class="fa-solid fa-volume-high"></i></button>
                                <button class="msg-tool-btn" onclick="copyMessageText(this)" title="نسخ الرسالة"><i class="fa-solid fa-copy"></i></button>
                            </div>
                        </div>
                    </div>
                    <div class="avatar-box user-avatar">
                        <i class="fa-solid fa-user-secret"></i>
                    </div>
                `;
                chatHistory.appendChild(userRow);
            } else {
                renderAIResponse({
                    title: msg.title || 'JOO AI DARK',
                    text: content,
                    badge: msg.badge || 'RECORDED INTEL',
                    code: msg.code || ''
                }, false);
            }
        });
        scrollToBottom();
    }
}

// Helpers
function scrollToBottom() {
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
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

// ======================================================================
// File Upload & Attachment Management
// ======================================================================

function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

function handleSelectedFile(file) {
    if (!file) return;
    if (file.size > 2 * 1024 * 1024) {
        showToast("حجم الملف كبير جداً (الحد الأقصى 2MB)");
        return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
        const content = e.target.result;
        const ext = file.name.split('.').pop() || 'txt';
        currentAttachedFile = {
            name: file.name,
            size: formatBytes(file.size),
            content: content,
            ext: ext
        };
        if (attachedFileName) attachedFileName.textContent = file.name;
        if (attachedFileSize) attachedFileSize.textContent = currentAttachedFile.size;
        if (attachmentBadgeContainer) attachmentBadgeContainer.classList.remove('hidden');
        if (attachFileBtn) attachFileBtn.classList.add('active');
        showToast(`تم إرفاق الملف: ${file.name} - اضغط إرسال للبدء في الفحص والترقيع`);
    };
    reader.readAsText(file);
}

function clearAttachedFile() {
    currentAttachedFile = null;
    if (attachmentBadgeContainer) attachmentBadgeContainer.classList.add('hidden');
    if (codeFileInput) codeFileInput.value = '';
    if (attachFileBtn) attachFileBtn.classList.remove('active');
}

if (attachFileBtn && codeFileInput) {
    attachFileBtn.addEventListener('click', () => {
        codeFileInput.click();
    });
    codeFileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            handleSelectedFile(e.target.files[0]);
        }
    });
}

if (removeAttachmentBtn) {
    removeAttachmentBtn.addEventListener('click', clearAttachedFile);
}

window.triggerCodeUpload = function() {
    if (codeFileInput) codeFileInput.click();
};

// Drag and drop code files onto the chat area
if (chatContainer) {
    ['dragenter', 'dragover'].forEach(eventName => {
        chatContainer.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            chatContainer.classList.add('drag-over');
        }, false);
    });
    ['dragleave', 'drop'].forEach(eventName => {
        chatContainer.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            chatContainer.classList.remove('drag-over');
        }, false);
    });
    chatContainer.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt ? dt.files : null;
        if (files && files[0]) {
            handleSelectedFile(files[0]);
        }
    });
}

// ======================================================================
// Public Assets Reconnaissance Modal
// ======================================================================

window.openPublicReconModal = function() {
    if (reconModal) {
        reconModal.classList.add('active');
        if (reconTargetInput) reconTargetInput.focus();
    }
};

if (publicReconBtn) {
    publicReconBtn.addEventListener('click', openPublicReconModal);
}
if (closeReconModalBtn && reconModal) {
    closeReconModalBtn.addEventListener('click', () => reconModal.classList.remove('active'));
}

if (runReconBtn) {
    runReconBtn.addEventListener('click', async () => {
        const target = (reconTargetInput ? reconTargetInput.value : '').trim();
        if (!target) {
            showToast("يرجى إدخال رابط أو دومين الموقع");
            return;
        }

        runReconBtn.disabled = true;
        runReconBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> جاري فحص الأصول...';

        try {
            const res = await fetch('/api/recon', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target: target })
            });

            if (!res.ok) throw new Error("HTTP error " + res.status);
            const data = await res.json();

            if (reconResultsContainer) reconResultsContainer.style.display = 'block';

            // Robots.txt
            if (reconRobotsStatus) {
                if (data.robots_txt && data.robots_txt.found) {
                    reconRobotsStatus.innerHTML = '<span class="text-emerald"><i class="fa-solid fa-circle-check"></i> متوفر ومكتشف للعامة</span>';
                    const paths = data.robots_txt.disallowed_paths || [];
                    reconRobotsPaths.innerHTML = paths.length 
                        ? `<strong>المسارات المستثناة (Disallow):</strong><br>${paths.map(p => escapeHTML(p)).join('<br>')}`
                        : 'لا توجد مسارات محظورة في الملف.';
                } else {
                    reconRobotsStatus.innerHTML = '<span style="color: #8b949e;"><i class="fa-solid fa-circle-xmark"></i> غير موجود أو محجوب</span>';
                    reconRobotsPaths.textContent = 'لم يتم العثور على ملف robots.txt.';
                }
            }

            // Scripts
            const scripts = data.scripts || [];
            if (reconScriptsCount) reconScriptsCount.textContent = scripts.length;
            if (reconScriptsList) {
                reconScriptsList.innerHTML = scripts.length
                    ? scripts.map(s => `<div style="margin-bottom: 4px; word-break: break-all;">• <a href="${escapeHTML(s)}" target="_blank" style="color: #58a6ff; text-decoration: none;">${escapeHTML(s)}</a></div>`).join('')
                    : 'لم يتم العثور على روابط سكربتات خارجية في الصفحة الرئيسية.';
            }

            // Findings
            const findings = data.leaked_findings || [];
            if (reconFindings) {
                if (findings.length) {
                    reconFindings.innerHTML = `<span style="color: #ef4444;"><i class="fa-solid fa-triangle-exclamation"></i> تم رصد احتمالات تسريب:</span><br>` +
                        findings.map(f => `⚠️ ${escapeHTML(f)}`).join('<br>');
                } else {
                    reconFindings.innerHTML = '<span class="text-emerald"><i class="fa-solid fa-shield-halved"></i> لم يتم رصد مفاتيح حساسة مكشوفة علناً في السكربتات المفحوصة.</span>';
                }
            }

            showToast("تم الانتهاء من استكشاف الأصول العلنية بنجاح");
        } catch (err) {
            console.error(err);
            showToast("حدث خطأ أثناء فحص الأصول العلنية");
        } finally {
            runReconBtn.disabled = false;
            runReconBtn.innerHTML = '<i class="fa-solid fa-radar"></i> فحص الأصول العلنية';
        }
    });
}

if (sendReconToChatBtn) {
    sendReconToChatBtn.addEventListener('click', () => {
        const target = (reconTargetInput ? reconTargetInput.value : '').trim();
        if (reconModal) reconModal.classList.remove('active');
        if (target) {
            sendPrompt(`افحص الأصول والملفات العلنية وسكربتات الجافاسكريبت لموقع ${target} واكشف المسارات المسربة`);
        }
    });
}

// Init
window.addEventListener('DOMContentLoaded', () => {
    loadChatHistory();
});
