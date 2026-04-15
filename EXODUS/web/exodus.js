/**
 * EXODUS — Personal AI Companion
 * Web Frontend Brain (V2.2 Cleaned)
 */

'use strict';

// ============================================================
// STATE 
// ============================================================

const state = { mode: 'PUBLIC' };
let currentSessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6);

// Global UI state for replies and uploads
let stagedFile = null;
let replyTargetId = null;
let currentAbortController = null;
let isProcessing = false;

// ============================================================
// UI UTILITIES
// ============================================================

function fireModule(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.add('firing');
  setTimeout(() => el.classList.remove('firing'), 800);
}

function updateActiveSkill(icon, name, desc) {
  const el = document.getElementById('active-skill-display');
  if (!el) return;
  el.querySelector('.skill-icon').textContent = icon;
  el.querySelector('.skill-name').textContent = name;
  el.querySelector('.skill-desc').textContent = desc;
}

function logSession(msg) {
  const log = document.getElementById('session-log');
  if (!log) return;
  const entry = document.createElement('div');
  entry.className = 'log-entry';
  const t = new Date().toLocaleTimeString('en-IN', { hour12: false });
  entry.textContent = `[${t}] ${msg}`;
  log.appendChild(entry);
  log.scrollTop = log.scrollHeight;
}

function showAlert(msg) {
  const bar = document.getElementById('alert-bar');
  if (!bar) return;
  bar.textContent = '⚠ ' + msg;
  bar.classList.remove('hidden');
  setTimeout(() => bar.classList.add('hidden'), 5000);
}

function showTyping() {
  const feed = document.getElementById('chat-feed');
  if (!feed) return;
  const el = document.createElement('div');
  el.className = 'msg assistant';
  el.id = 'typing-indicator';
  el.innerHTML = `
    <div class="msg-avatar">⬢</div>
    <div class="msg-body">
      <div class="msg-meta">EXODUS · processing</div>
      <div class="msg-bubble">
        <div class="typing-indicator">
          <span class="thinking-spinner"></span>
          <span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>
        </div>
      </div>
    </div>`;
  feed.appendChild(el);
  feed.scrollTop = feed.scrollHeight;
}

function hideTyping() {
  const el = document.getElementById('typing-indicator');
  if (el) el.remove();
}

// ============================================================
// CHAT RENDERING
// ============================================================

function renderMessage(role, text, type = '', msgId = null, replyToId = null) {
  const feed = document.getElementById('chat-feed');
  if (!feed) return;
  
  const msg = document.createElement('div');
  msg.className = `msg ${role} ${type}`;
  if (msgId) msg.dataset.id = msgId;
  
  const avatar = role === 'user' ? '👤' : '⬢';
  const meta = role === 'user' ? 'YOU' : 'EXODUS';
  const time = new Date().toLocaleTimeString('en-IN', { hour12: false });

  // Handle Reply Quote
  let quoteHtml = '';
  if (replyToId) {
    const parentMsg = document.querySelector(`.msg[data-id="${replyToId}"]`);
    const parentText = parentMsg ? parentMsg.querySelector('.msg-bubble').innerText.substring(0, 60) + '...' : 'Original message';
    quoteHtml = `<div class="reply-quote" onclick="scrollToMessage(${replyToId})">📎 Replying to: ${parentText}</div>`;
  }

  // Handle Image Detection
  let contentHtml = text;
  const imageRegex = /\[IMAGE_URL:\s*(.*?)\]/g;
  contentHtml = contentHtml.replace(imageRegex, (match, url) => {
    return `<div class="msg-image"><img src="${url.trim()}" alt="Generated Image" onload="scrollToBottom()"></div>`;
  });

  msg.innerHTML = `
    <div class="msg-avatar">${avatar}</div>
    <div class="msg-body">
      <div class="msg-meta">${meta} // ${time}</div>
      <div class="msg-bubble">
        ${quoteHtml}
        ${contentHtml.replace(/\n/g, '<br>')}
      </div>
    </div>
    <div class="msg-reply-trigger" title="Reply" onclick="setReplyTarget(${msgId || 'null'}, '${text.replace(/'/g, "\\'").substring(0, 40)}')">↩</div>
  `;
  
  feed.appendChild(msg);
  feed.scrollTop = feed.scrollHeight;
  return msg;
}

function scrollToBottom() {
  const feed = document.getElementById('chat-feed');
  if (feed) feed.scrollTop = feed.scrollHeight;
}

function scrollToMessage(id) {
  const el = document.querySelector(`.msg[data-id="${id}"]`);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    el.classList.add('highlight-flash');
    setTimeout(() => el.classList.remove('highlight-flash'), 2000);
  }
}

function setReplyTarget(id, snippet) {
  replyTargetId = id;
  const bar = document.getElementById('reply-preview-bar');
  const text = document.getElementById('reply-text');
  if (bar && text) {
    text.textContent = `Replying to: "${snippet}..."`;
    bar.classList.remove('hidden');
  }
  document.getElementById('user-input')?.focus();
}

function cancelReply() {
  replyTargetId = null;
  document.getElementById('reply-preview-bar')?.classList.add('hidden');
}

function removeStagedFile() {
  stagedFile = null;
  document.getElementById('staged-file-bar')?.classList.add('hidden');
  const fileInput = document.getElementById('file-input');
  if (fileInput) fileInput.value = '';
}

// ============================================================
// MAIN SEND LOGIC
// ============================================================

async function sendMessage() {
  if (isProcessing) {
    if (currentAbortController) {
      currentAbortController.abort();
      isProcessing = false;
      hideTyping();
      const sendIcon = document.getElementById('send-icon');
      if (sendIcon) sendIcon.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>`;
      logSession('Generation stopped.');
    }
    return;
  }

  const inputEl = document.getElementById('user-input');
  const text = inputEl?.value.trim() || '';
  
  if (!text && !stagedFile) return;

  const currentText = text;
  const currentFile = stagedFile;
  const currentReplyId = replyTargetId;

  if (inputEl) {
    inputEl.value = '';
    inputEl.style.height = 'auto';
  }
  cancelReply();
  removeStagedFile();

  isProcessing = true;
  const sendIcon = document.getElementById('send-icon');
  if (sendIcon) sendIcon.innerHTML = '<span style="font-size: 20px;">⏹</span>';

  // 1. Render locally
  const localDisplay = currentFile ? `[FILE: ${currentFile.name}] ${currentText}` : currentText;
  renderMessage('user', localDisplay, '', null, currentReplyId);

  // 2. Prepare Request
  const formData = new FormData();
  formData.append('user_input', currentText || "[Uploaded File]");
  formData.append('session_id', currentSessionId);
  const apiKey = localStorage.getItem('exodus_api_key');
  if (apiKey) formData.append('api_key', apiKey);
  if (currentReplyId) formData.append('reply_to_id', currentReplyId);
  if (currentFile) formData.append('file', currentFile);

  showTyping();
  currentAbortController = new AbortController();

  try {
    const res = await fetch('http://127.0.0.1:8000/api/chat', {
      method: 'POST',
      body: formData,
      signal: currentAbortController.signal
    });
    
    if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
    
    const data = await res.json();
    hideTyping();

    if (data.status === "success") {
      renderMessage('assistant', data.response, '', Date.now(), currentReplyId);
      logSession('Response received.');
      loadChatHistory();
    } else {
      renderMessage('assistant', data.response, 'violation');
    }

  } catch (err) {
    if (err.name === 'AbortError') return;
    hideTyping();
    renderMessage('assistant', `⚠️ **ERROR:** ${err.message}`, 'violation');
  } finally {
    isProcessing = false;
    if (sendIcon) sendIcon.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
        <line x1="22" y1="2" x2="11" y2="13"></line>
        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
      </svg>`;
    currentAbortController = null;
  }
}

// ============================================================
// BOOT & HISTORY
// ============================================================

const BOOT_MESSAGES = [
  '[KERNEL] Initialising EXODUS v2.2 runtime...',
  '[MEMORY] Loading session context... OK',
  '[GUARDIAN] Drift detection engine... ACTIVE',
  '[RULES] Enforcing Constitution... OK',
  '[VISION] Analysis engine... READY',
  '[NET] Free-tier API routing... CONFIGURED',
  '✔ EXODUS ONLINE. Standing by.',
];

async function runBootSequence() {
  const log = document.getElementById('boot-log');
  const bar = document.getElementById('boot-bar');
  if (!log || !bar) return;

  for (let i = 0; i < BOOT_MESSAGES.length; i++) {
    await new Promise(r => setTimeout(r, 150 + Math.random() * 100));
    const line = document.createElement('div');
    line.className = 'boot-log-line';
    line.textContent = BOOT_MESSAGES[i];
    log.appendChild(line);
    log.scrollTop = log.scrollHeight;
    bar.style.width = `${((i + 1) / BOOT_MESSAGES.length) * 100}%`;
  }

  await new Promise(r => setTimeout(r, 600));
  document.getElementById('boot-screen').classList.add('fade-out');
  const app = document.getElementById('app');
  if (app) app.classList.remove('hidden');

  await new Promise(r => setTimeout(r, 800));
  document.getElementById('boot-screen').style.display = 'none';

  renderMessage('assistant', `**EXODUS V2.2 ONLINE.**\n\nUnified Uploads, Vision, and Replies are active.\n*How can I assist you today?*`, 'welcome');
  logSession('System active.');
}

async function loadChatHistory() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/sessions');
    const data = await res.json();
    const list = document.getElementById('history-list');
    if (!list) return;
    list.innerHTML = '';
    
    for (const session of data.sessions) {
      const item = document.createElement('div');
      item.className = 'history-item' + (session.id === currentSessionId ? ' active' : '');
      item.innerHTML = `
        <div class="history-item-title">${session.title}</div>
        <button class="history-item-delete" data-id="${session.id}">✕</button>
      `;
      item.onclick = (e) => {
        if (e.target.classList.contains('history-item-delete')) return;
        loadSession(session.id);
      };
      const delBtn = item.querySelector('.history-item-delete');
      if (delBtn) {
        delBtn.onclick = async (e) => {
          e.stopPropagation();
          await fetch(`http://127.0.0.1:8000/api/sessions/${session.id}`, { method: 'DELETE' });
          loadChatHistory();
        };
      }
      list.appendChild(item);
    }
  } catch (err) { console.error('History load failed:', err); }
}

async function loadSession(sessionId) {
  try {
    currentSessionId = sessionId;
    const res = await fetch(`http://127.0.0.1:8000/api/sessions/${sessionId}/messages`);
    const data = await res.json();
    const feed = document.getElementById('chat-feed');
    if (feed) feed.innerHTML = '';
    
    for (const msg of data.messages) {
      renderMessage(msg.role, msg.content, '', msg.id, msg.reply_to_id);
    }
    loadChatHistory();
    logSession(`Session loaded: ${sessionId.substr(0,8)}`);
  } catch (err) { console.error('Session load failed:', err); }
}

// ============================================================
// EVENT LISTENERS
// ============================================================

function initEvents() {
  document.getElementById('send-btn')?.addEventListener('click', sendMessage);
  
  document.getElementById('user-input')?.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  document.getElementById('user-input')?.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
  });

  document.getElementById('api-save-btn')?.addEventListener('click', () => {
    const key = document.getElementById('api-key-input')?.value.trim();
    if (key) {
      localStorage.setItem('exodus_api_key', key);
      const input = document.getElementById('api-key-input');
      if (input) {
        input.value = '';
        input.placeholder = '✔ Key saved!';
      }
      logSession('API configured.');
    }
  });

  document.getElementById('new-chat-btn')?.addEventListener('click', () => {
    currentSessionId = 'session_' + Date.now();
    const feed = document.getElementById('chat-feed');
    if (feed) feed.innerHTML = '';
    renderMessage('assistant', 'New session started.', 'system');
    loadChatHistory();
  });

  document.getElementById('attach-btn')?.addEventListener('click', () => {
    document.getElementById('file-input')?.click();
  });

  document.getElementById('file-input')?.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
      stagedFile = file;
      const bar = document.getElementById('staged-file-bar');
      const name = document.getElementById('staged-file-name');
      if (bar && name) {
        name.textContent = file.name;
        bar.classList.remove('hidden');
      }
    }
  });

  document.getElementById('remove-file-btn')?.addEventListener('click', removeStagedFile);
  document.getElementById('cancel-reply-btn')?.addEventListener('click', cancelReply);
  
  document.querySelectorAll('[data-template]').forEach(item => {
    item.addEventListener('click', () => {
      const template = item.dataset.template.replace(/\\n/g, '\n');
      const input = document.getElementById('user-input');
      if (input) {
        input.value = template;
        input.focus();
        input.dispatchEvent(new Event('input'));
      }
    });
  });

  document.getElementById('export-pdf-btn')?.addEventListener('click', () => {
    const feed = document.getElementById('chat-feed');
    if (!feed) return;
    let content = "EXODUS LOG\n\n" + feed.innerText;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `exodus_${Date.now()}.txt`;
    a.click();
  });
}

// ============================================================
// BOOT
// ============================================================

window.addEventListener('DOMContentLoaded', () => {
  // Start Clock
  const clockEl = document.getElementById('stat-time');
  if (clockEl) {
    setInterval(() => {
      clockEl.textContent = new Date().toLocaleTimeString('en-IN', { hour12: false });
    }, 1000);
  }

  initEvents();
  loadChatHistory();
  runBootSequence();
});
