# assets.py
"""أنماط CSS والموارد الثابتة للتطبيق."""


# ═══════════════════════════════════════════════════════════
# أنماط CSS
# ═══════════════════════════════════════════════════════════
CSS = r'''
<style>
/* ═══════════════════════════════════════════════════════════
   1) الأساسيات
   ═══════════════════════════════════════════════════════════ */
body, .nicegui-content {
    direction: rtl !important;
    background: #f5f5f5 !important;
    color: #000;
    font-family: 'Inter', 'Segoe UI', Tahoma, sans-serif;
    padding: 0 !important;
    gap: 0 !important;
    -webkit-font-smoothing: antialiased;
}
.q-card, .q-btn, .q-drawer, .q-field, .q-menu { box-shadow: none !important; }

/* ═══════════════════════════════════════════════════════════
   2) شاشة اختيار الهوية (تظهر قبل الدخول)
   ═══════════════════════════════════════════════════════════ */
.app-login-wrap {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    background: #f5f5f5;
    overflow-y: auto;
    z-index: 50;
}
.app-login-card {
    width: 100%;
    max-width: 420px;
    border: 1px solid #000;
    background: #fff;
    padding: 44px 36px 36px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.app-login-glove {
    width: 56px;
    height: 56px;
    margin: 0 auto 4px;
    color: #000;
    display: block;
}
.app-login-brand {
    font-size: 20px !important;
    font-weight: 700 !important;
    letter-spacing: 10px;
    text-align: center;
    margin-bottom: 4px;
}
.app-login-sub {
    font-size: 10px !important;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #999 !important;
    text-align: center;
    font-family: 'SF Mono','Consolas',monospace;
    margin-bottom: 28px;
}
.app-login-prompt {
    font-size: 13px !important;
    color: #666 !important;
    text-align: center;
    margin-bottom: 14px;
}
.app-login-users {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.app-login-user {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 18px;
    border: 1px solid #e8e8e8;
    background: #fff;
    cursor: pointer;
    transition: all 0.14s ease;
}
.app-login-user:hover {
    border-color: #000;
    background: #fafafa;
}
.app-login-user-name {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #000 !important;
}

/* ═══════════════════════════════════════════════════════════
   3) الشريط الجانبي
   ═══════════════════════════════════════════════════════════ */
.q-drawer {
    background: #fff !important;
    border-right: 1px solid #000 !important;
    border-left: none !important;
}
.q-drawer__content { padding: 0 !important; }

.brand-block {
    padding: 22px 20px;
    border-bottom: 1px solid #000;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.brand-left {
    display: flex;
    align-items: center;
    gap: 10px;
}
.brand-glove {
    width: 22px;
    height: 22px;
    color: #000;
    display: block;
}
.brand {
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 6px;
}
.brand-mark { font-size: 16px; }

.nav-list {
    padding: 16px 14px;
    gap: 0 !important;
    width: 100%;
}
.nav-btn {
    justify-content: flex-start !important;
    text-transform: none !important;
    color: #000 !important;
    font-weight: 400 !important;
    font-size: 13px !important;
    padding: 13px 16px !important;
    min-height: 46px !important;
    border: 1px solid #000 !important;
    border-radius: 0 !important;
    background: #fff !important;
    margin-bottom: -1px !important;
    position: relative;
    z-index: 1;
    transition: background 0.14s ease;
}
.nav-btn:hover {
    background: #f0f0f0 !important;
    z-index: 2;
}
.nav-btn.active {
    background: #000 !important;
    color: #fff !important;
    z-index: 3;
}
.nav-btn.active .q-icon { color: #fff !important; }
.nav-btn .q-icon {
    margin-left: 12px !important;
    margin-right: 0 !important;
}

/* بطاقة المستخدم أسفل الشريط الجانبي */
.sidebar-user {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    margin: 4px 14px 12px;
    border: 1px solid #000;
    background: #fafafa;
}
.sidebar-user-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    flex: 1;
    min-width: 0;
}
.sidebar-user-name {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #000 !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.sidebar-user-hint {
    font-size: 9px !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #999 !important;
    font-family: 'SF Mono','Consolas',monospace;
}
.sidebar-switch-btn {
    color: #000 !important;
    min-width: 28px !important;
    min-height: 28px !important;
    width: 28px !important;
    height: 28px !important;
    padding: 0 !important;
}
.sidebar-switch-btn:hover { background: #f0f0f0 !important; }

.footer-mark {
    font-size: 10px;
    letter-spacing: 3px;
    color: #999;
    padding: 14px 0;
    text-transform: uppercase;
    text-align: center;
    width: 100%;
    border-top: 1px solid #000;
}

/* ═══════════════════════════════════════════════════════════
   4) المحتوى العام (البطاقة)
   ═══════════════════════════════════════════════════════════ */
.content-wrap {
    width: 100%;
    min-height: 100vh;
    padding: 56px 48px;
    display: flex;
    align-items: flex-start;
    justify-content: center;
}
.card {
    background: #fff !important;
    border: 1px solid #000 !important;
    border-radius: 0 !important;
    padding: 0 !important;
    max-width: 1080px;
    width: 100%;
    gap: 0 !important;
}
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 28px;
    border-bottom: 1px solid #000;
}
.card-title {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}
.card-index {
    font-size: 11px;
    letter-spacing: 0.1em;
    font-family: 'SF Mono','Consolas',monospace;
    border: 1px solid #000;
    padding: 3px 9px;
    line-height: 1;
}
.card-body {
    padding: 44px 36px 36px !important;
    width: 100%;
    gap: 0 !important;
}

/* ═══════════════════════════════════════════════════════════
   5) العناوين
   ═══════════════════════════════════════════════════════════ */
.page-number {
    font-size: 12px;
    letter-spacing: 0.3em;
    color: #999;
    font-family: 'SF Mono','Consolas',monospace;
    margin-bottom: 8px;
}
.page-title {
    font-size: 36px !important;
    font-weight: 300 !important;
    line-height: 1.15;
    letter-spacing: -0.02em;
    margin-bottom: 22px;
}
.divider {
    width: 48px;
    height: 1px;
    background: #000;
    margin-bottom: 22px;
}
.hint-box {
    font-size: 14.5px !important;
    color: #666 !important;
    line-height: 1.9;
    margin-bottom: 32px;
}

/* ═══════════════════════════════════════════════════════════
   6) شريط حالة MQTT
   ═══════════════════════════════════════════════════════════ */
.mqtt-bar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 18px;
    border: 1px solid #000;
    background: #fafafa;
    margin-bottom: 20px;
}
.mqtt-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    border: 1px solid #999;
    flex-shrink: 0;
}
.mqtt-dot.on   { background: #1a7a4a; border-color: #1a7a4a; }
.mqtt-dot.off  { background: transparent; border-color: #c0392b; }
.mqtt-dot.wait { background: #999; border-color: #999; animation: pulse 1.2s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:.35;} 50%{opacity:1;} }

.mqtt-label {
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #000 !important;
}
.mqtt-meta {
    margin-inline-start: auto;
    font-family: 'SF Mono','Consolas',monospace;
    font-size: 11px !important;
    color: #999 !important;
    direction: ltr;
}

/* ═══════════════════════════════════════════════════════════
   7) شبكة الحساسات
   ═══════════════════════════════════════════════════════════ */
.sensor-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    width: 100%;
}
.sensor-block {
    border: 1px solid #000;
    background: #fff;
}
.sensor-block-title {
    padding: 12px 18px;
    border-bottom: 1px solid #000;
    background: #fafafa;
    font-size: 11px !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-weight: 600 !important;
    color: #000 !important;
}
.sensor-rows { padding: 8px 18px; }
.sensor-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #f0f0f0;
}
.sensor-row:last-child { border-bottom: none; }
.sensor-label {
    font-size: 12px !important;
    color: #333 !important;
    font-weight: 500 !important;
}
.sensor-value {
    font-family: 'SF Mono','Consolas',monospace;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #000 !important;
    text-align: left;
    direction: ltr;
    min-width: 90px;
    padding: 3px 10px;
    background: #f8f8f8;
    border: 1px solid #e8e8e8;
    line-height: 1;
}

/* ═══════════════════════════════════════════════════════════
   8) غرفة التواصل (chat.py)
   ═══════════════════════════════════════════════════════════ */
.chat-root { width: 100%; gap: 0 !important; }

/* الأفاتار */
.chat-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: inline-flex !important;
    align-items: center;
    justify-content: center;
    font-family: 'Inter', 'Segoe UI', sans-serif;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 0;
    flex-shrink: 0;
    line-height: 1;
    padding: 0 !important;
    direction: ltr;
}
.chat-avatar-sm { width: 26px; height: 26px; font-size: 12px; }
.chat-avatar-xs { width: 22px; height: 22px; font-size: 10px; }

/* الرأس */
.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 20px;
    background: #fafafa;
    border: 1px solid #000;
    border-bottom: none;
}
.chat-logo {
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 4px;
}
.chat-header-right {
    display: flex;
    align-items: center;
    gap: 14px;
}
.chat-me {
    display: flex;
    align-items: center;
    gap: 8px;
}
.chat-me-label {
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #000 !important;
}

/* منطقة الرسائل */
.chat-messages {
    border: 1px solid #000;
    background: #fff;
    height: 540px;
    overflow-y: auto;
    padding: 22px 22px 18px;
    display: flex !important;
    flex-direction: column;
    gap: 14px;
    width: 100%;
}
.chat-messages::-webkit-scrollbar { width: 6px; }
.chat-messages::-webkit-scrollbar-thumb { background: #ddd; }
.chat-messages::-webkit-scrollbar-track { background: transparent; }

.chat-empty {
    align-items: center;
    justify-content: center;
    flex: 1;
    gap: 8px !important;
    padding: 80px 20px;
    width: 100%;
}
.chat-empty-title {
    font-size: 13px !important;
    color: #999 !important;
}
.chat-empty-hint {
    font-size: 11px !important;
    color: #bbb !important;
}

/* فقاعة الرسالة */
.chat-msg {
    display: flex;
    flex-direction: column;
    max-width: 74%;
    gap: 6px;
    animation: chatpop 0.18s ease;
}
@keyframes chatpop {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
.chat-msg.own   { align-self: flex-end; }
.chat-msg.other { align-self: flex-start; }

.chat-msg-head {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0 4px;
    font-size: 11px;
}
.chat-msg.own .chat-msg-head { flex-direction: row-reverse; }

.chat-msg-name {
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em;
}
.chat-msg-time {
    font-family: 'SF Mono','Consolas',monospace;
    font-size: 10px !important;
    color: #999 !important;
    direction: ltr;
}
.chat-msg-edited {
    font-size: 9px !important;
    color: #999 !important;
    font-style: italic;
    letter-spacing: 0.04em;
}

/* إجراءات الرسالة (نسخ + تعديل) */
.chat-msg-actions {
    display: flex;
    gap: 2px;
    margin-inline-start: auto;
}
.chat-msg.own .chat-msg-actions {
    margin-inline-start: 0;
    margin-inline-end: auto;
}
.chat-copy-btn {
    opacity: 0;
    transition: opacity 0.14s ease !important;
    min-width: 22px !important;
    min-height: 22px !important;
    width: 22px !important;
    height: 22px !important;
    padding: 0 !important;
    margin: 0 !important;
    color: #999 !important;
}
.chat-copy-btn:hover { color: #000 !important; }
.chat-msg:hover .chat-copy-btn { opacity: 1; }
.chat-copy-btn .q-icon { font-size: 15px !important; }

.chat-msg-body {
    padding: 11px 15px;
    font-size: 14px;
    line-height: 1.6;
    word-break: break-word;
    border: 1px solid;
    max-width: 100%;
    overflow-wrap: anywhere;
}

.chat-msg-abd .chat-msg-body { background: #dbeafe; color: #1e3a8a; border-color: #93c5fd; }
.chat-msg-moh .chat-msg-body { background: #ede9fe; color: #5b21b6; border-color: #c4b5fd; }
.chat-msg-osa .chat-msg-body { background: #dcfce7; color: #14532d; border-color: #86efac; }
.chat-msg.own .chat-msg-body { box-shadow: 0 0 0 1px #000 inset; }

/* Markdown داخل الرسالة */
.chat-markdown { width: 100%; }
.chat-markdown p { margin: 0 0 6px 0; }
.chat-markdown p:last-child { margin-bottom: 0; }
.chat-markdown strong { font-weight: 700; }
.chat-markdown em { font-style: italic; }
.chat-markdown code {
    font-family: 'SF Mono','Consolas',monospace;
    font-size: 12px;
    background: rgba(0,0,0,0.08);
    padding: 1px 5px;
    border-radius: 2px;
    direction: ltr;
    display: inline-block;
}
.chat-markdown pre {
    background: rgba(0,0,0,0.08);
    padding: 8px 12px;
    overflow-x: auto;
    margin: 6px 0;
    font-size: 12px;
    direction: ltr;
    text-align: left;
}
.chat-markdown pre code {
    background: transparent;
    padding: 0;
    display: block;
}
.chat-markdown a {
    color: inherit;
    text-decoration: underline;
    font-weight: 600;
}
.chat-markdown ul,
.chat-markdown ol {
    padding-inline-start: 20px;
    margin: 4px 0;
}
.chat-markdown blockquote {
    border-inline-start: 3px solid currentColor;
    padding-inline-start: 10px;
    margin: 4px 0;
    opacity: 0.85;
}
.chat-markdown h1,
.chat-markdown h2,
.chat-markdown h3 {
    margin: 4px 0;
    font-weight: 700;
    line-height: 1.3;
}
.chat-markdown h1 { font-size: 18px; }
.chat-markdown h2 { font-size: 16px; }
.chat-markdown h3 { font-size: 14px; }

/* بطاقة الملف داخل الرسالة */
.chat-file {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 4px 0;
}
.chat-file-icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.55);
    border: 1px solid rgba(0,0,0,0.15);
    color: inherit;
    flex-shrink: 0;
}
.chat-file-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
    flex: 1;
}
.chat-file-name {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: inherit !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 220px;
    direction: ltr;
    text-align: left;
}
.chat-file-size {
    font-family: 'SF Mono','Consolas',monospace;
    font-size: 10px !important;
    opacity: 0.7;
}
.chat-file-dl {
    background: rgba(255,255,255,0.75) !important;
    color: inherit !important;
    border: 1px solid rgba(0,0,0,0.2) !important;
    border-radius: 0 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    padding: 6px 12px !important;
    min-height: 30px !important;
    text-transform: none !important;
    margin: 0 !important;
}
.chat-file-dl:hover {
    background: rgba(0,0,0,0.08) !important;
}

/* منطقة الإدخال */
.chat-input-area {
    display: flex;
    gap: 10px;
    padding: 14px 20px;
    background: #fafafa;
    border: 1px solid #000;
    border-top: none;
    align-items: center;
}
.chat-input-field {
    flex: 1;
    background: #fff !important;
    border: 1px solid #000 !important;
    padding: 0 !important;
}
.chat-input-field .q-field__control {
    padding: 0 16px !important;
    min-height: 46px !important;
    align-items: center !important;
}
.chat-input-field .q-field__native {
    font-size: 14px !important;
    color: #000 !important;
    font-family: 'Inter', 'Segoe UI', Tahoma, sans-serif;
    line-height: 1.5;
    padding: 12px 0 !important;
    resize: none !important;
    max-height: 160px;
    overflow-y: auto !important;
}

/* أزرار الأيقونات (إرفاق + كود) */
.chat-icon-btn {
    width: 46px !important;
    height: 46px !important;
    min-width: 46px !important;
    min-height: 46px !important;
    padding: 0 !important;
    margin: 0 !important;
    border: 1px solid #000 !important;
    border-radius: 0 !important;
    background: #fff !important;
    color: #000 !important;
    flex-shrink: 0;
}
.chat-icon-btn:hover { background: #f0f0f0 !important; }
.chat-icon-btn .q-icon { font-size: 20px !important; }
.chat-icon-btn.active {
    background: #000 !important;
    color: #fff !important;
}

/* زر الإرسال */
.chat-send-btn {
    background: #000 !important;
    color: #fff !important;
    border-radius: 0 !important;
    width: 46px !important;
    min-width: 46px !important;
    min-height: 46px !important;
    padding: 0 !important;
    margin: 0 !important;
}
.chat-send-btn:hover { background: #333 !important; }
.chat-send-btn .q-icon { font-size: 20px !important; }

/* تلميح أسفل الإدخال */
.chat-input-hint {
    font-size: 10px !important;
    color: #999 !important;
    letter-spacing: 0.04em;
    text-align: center;
    padding: 8px 0 0;
    margin-bottom: -6px;
}
.chat-input-hint code {
    font-family: 'SF Mono','Consolas',monospace;
    background: #f0f0f0;
    padding: 1px 4px;
    direction: ltr;
    display: inline-block;
}

/* نافذة تعديل الرسالة */
.chat-edit-dialog {
    min-width: 420px !important;
    max-width: 90vw !important;
    border: 1px solid #000 !important;
    border-radius: 0 !important;
    padding: 0 !important;
    background: #fff !important;
}
.chat-edit-title {
    padding: 14px 20px;
    border-bottom: 1px solid #000;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    background: #fafafa;
}
.chat-edit-input {
    margin: 20px !important;
    border: 1px solid #000 !important;
    padding: 8px 14px !important;
    background: #fff !important;
}
.chat-edit-input .q-field__control { padding: 0 !important; }
.chat-edit-input .q-field__native {
    font-size: 14px !important;
    font-family: 'SF Mono','Consolas',monospace;
    line-height: 1.5;
    padding: 6px 0 !important;
    min-height: 60px !important;
}
.chat-edit-actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    padding: 12px 20px;
    border-top: 1px solid #eee;
}
.chat-edit-cancel {
    border: 1px solid #000 !important;
    background: #fff !important;
    color: #000 !important;
    border-radius: 0 !important;
    font-size: 12px !important;
    min-height: 36px !important;
    padding: 0 18px !important;
    text-transform: none !important;
    margin: 0 !important;
}
.chat-edit-cancel:hover { background: #f0f0f0 !important; }
.chat-edit-save {
    background: #000 !important;
    color: #fff !important;
    border: 1px solid #000 !important;
    border-radius: 0 !important;
    font-size: 12px !important;
    min-height: 36px !important;
    padding: 0 22px !important;
    text-transform: none !important;
    font-weight: 600 !important;
    margin: 0 !important;
}
.chat-edit-save:hover { background: #333 !important; }

/* ═══════════════════════════════════════════════════════════
   9) مستودع الملفات (files.py)
   ═══════════════════════════════════════════════════════════ */
.repo-root { width: 100%; gap: 0 !important; }

/* الرأس */
.repo-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 20px;
    background: #fafafa;
    border: 1px solid #000;
    border-bottom: none;
}
.repo-logo {
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 4px;
}
.repo-header-right {
    display: flex;
    align-items: center;
    gap: 14px;
}
.repo-me {
    display: flex;
    align-items: center;
    gap: 8px;
}
.repo-me-label {
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #000 !important;
}

/* منطقة الرفع */
.repo-upload-area {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    padding: 22px 24px;
    background: #fafafa;
    border: 1px solid #000;
    border-top: none;
}
.repo-upload-text {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
    min-width: 0;
}
.repo-upload-icon {
    font-size: 26px !important;
    color: #000 !important;
    margin-bottom: 2px;
}
.repo-upload-title {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #000 !important;
}
.repo-upload-hint {
    font-size: 11px !important;
    color: #999 !important;
    font-family: 'SF Mono','Consolas',monospace;
    letter-spacing: 0.04em;
}

.repo-upload-btn {
    background: #000 !important;
    color: #fff !important;
    border-radius: 0 !important;
    min-height: 46px !important;
    padding: 0 20px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-transform: none !important;
    margin: 0 !important;
    flex-shrink: 0;
}
.repo-upload-btn:hover { background: #333 !important; }
.repo-upload-btn .q-uploader__header {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    min-height: auto !important;
    height: auto !important;
    color: #fff !important;
}
.repo-upload-btn .q-uploader__header-content {
    padding: 0 !important;
    color: #fff !important;
}
.repo-upload-btn .q-uploader__header-content .q-btn {
    color: #fff !important;
    min-height: 46px !important;
    padding: 0 !important;
    margin: 0 !important;
    font-weight: 600 !important;
}
.repo-upload-btn .q-uploader__list { display: none !important; }

/* شريط الإحصاءات */
.repo-stats {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 10px 20px;
    background: #fafafa;
    border: 1px solid #000;
    border-top: none;
    font-family: 'SF Mono','Consolas',monospace;
    font-size: 11px;
}
.repo-stat {
    font-size: 11px !important;
    color: #000 !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.repo-stat-muted { color: #999 !important; font-weight: 500 !important; }
.repo-stat-spacer { flex: 1; }

/* قائمة الملفات */
.repo-list {
    border: 1px solid #000;
    border-top: none;
    background: #fff;
    min-height: 340px;
    width: 100% !important;
}

/* الحالة الفارغة — كامل العرض وموسّط */
.repo-empty {
    display: flex !important;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 340px;
    width: 100% !important;
    padding: 60px 24px;
    gap: 12px !important;
    text-align: center;
    direction: rtl;
}
.repo-empty-icon {
    font-size: 44px !important;
    color: #ccc !important;
    margin-bottom: 4px;
}
.repo-empty-title {
    font-size: 15px !important;
    color: #666 !important;
    font-weight: 500 !important;
}
.repo-empty-hint {
    font-size: 12px !important;
    color: #999 !important;
}

/* صف الملف */
.repo-row {
    display: grid;
    grid-template-columns: minmax(0, 3fr) 100px 140px 160px 120px;
    align-items: center;
    gap: 12px;
    padding: 12px 20px;
    border-bottom: 1px solid #f0f0f0;
    transition: background 0.12s ease;
}
.repo-row:last-child { border-bottom: none; }
.repo-row:hover:not(.repo-row-head) { background: #fafafa; }

.repo-row-head {
    background: #fafafa;
    border-bottom: 1px solid #000;
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #666 !important;
    font-weight: 600;
    padding: 12px 20px;
}
.repo-row-head .repo-col {
    color: #666 !important;
    font-size: 10px !important;
    font-weight: 600 !important;
}

.repo-col { min-width: 0; }
.repo-col-name    { display: flex; align-items: center; gap: 10px; }
.repo-col-size    {
    font-family: 'SF Mono','Consolas',monospace;
    font-size: 12px !important;
    color: #666 !important;
    direction: ltr;
    text-align: left;
}
.repo-col-user    { display: flex; align-items: center; gap: 8px; }
.repo-col-date    {
    font-family: 'SF Mono','Consolas',monospace;
    font-size: 11px !important;
    color: #999 !important;
    direction: ltr;
    text-align: left;
}
.repo-col-actions { display: flex; gap: 2px; justify-content: flex-end; }

.repo-file-icon {
    font-size: 20px !important;
    color: #000 !important;
    flex-shrink: 0;
}
.repo-file-name {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #000 !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    direction: ltr;
    text-align: left;
    flex: 1;
    min-width: 0;
}
.repo-user-name {
    font-size: 12px !important;
    color: #333 !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* أزرار الإجراءات */
.repo-action-btn {
    width: 28px !important;
    height: 28px !important;
    min-width: 28px !important;
    min-height: 28px !important;
    padding: 0 !important;
    margin: 0 !important;
    color: #666 !important;
    border-radius: 0 !important;
}
.repo-action-btn:hover {
    background: #f0f0f0 !important;
    color: #000 !important;
}
.repo-action-btn .q-icon { font-size: 16px !important; }
.repo-action-danger:hover {
    background: #fee2e2 !important;
    color: #c0392b !important;
}

/* ═══════════════════════════════════════════════════════════
   10) Responsive
   ═══════════════════════════════════════════════════════════ */
@media (max-width: 900px) {
    .content-wrap { padding: 32px 20px; }
    .card-body { padding: 28px 20px 24px !important; }
    .page-title { font-size: 26px !important; }
    .sensor-grid { grid-template-columns: 1fr; }

    .repo-row {
        grid-template-columns: 1fr;
        gap: 8px;
        padding: 14px 16px;
    }
    .repo-row-head { display: none; }
    .repo-col-size::before {
        content: 'الحجم: ';
        color: #999;
        font-family: inherit;
        font-size: 11px;
    }
    .repo-col-date::before {
        content: 'التاريخ: ';
        color: #999;
        font-family: inherit;
        font-size: 11px;
    }
    .repo-col-user::before {
        content: 'الرافع: ';
        color: #999;
        font-family: inherit;
        font-size: 11px;
    }
    .repo-col-size,
    .repo-col-date,
    .repo-col-user { justify-content: flex-start; }
    .repo-col-actions { justify-content: flex-start; padding-top: 6px; }
    .repo-upload-area { flex-direction: column; align-items: stretch; }
    .repo-upload-btn { width: 100% !important; }
    .repo-header { padding: 12px 14px; }
}

@media (max-width: 720px) {
    .content-wrap { padding: 24px 16px; }
    .card-body { padding: 24px 16px 20px !important; }
    .page-title { font-size: 22px !important; }

    .chat-messages { height: 400px; padding: 14px; }
    .chat-msg { max-width: 88%; }
    .chat-header { padding: 12px 14px; }
    .chat-input-area { padding: 10px 14px; gap: 8px; }
    .chat-file-name { max-width: 140px; }
    .app-login-card { padding: 32px 22px 26px; }
}
/* زر الإرفاق المدمج (upload styled as icon) */
.chat-upload-inline {
    width: 46px !important;
    height: 46px !important;
    min-width: 46px !important;
    min-height: 46px !important;
    max-width: 46px !important;
    padding: 0 !important;
    margin: 0 !important;
    border: 1px solid #000 !important;
    border-radius: 0 !important;
    background: #fff !important;
    overflow: hidden !important;
    flex-shrink: 0;
}
.chat-upload-inline .q-uploader__header {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    height: 44px !important;
    min-height: 44px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.chat-upload-inline .q-uploader__header-content {
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    color: #000 !important;
}
.chat-upload-inline .q-uploader__header-content > span,
.chat-upload-inline .q-uploader__header-content > div:not(.q-btn) {
    display: none !important;
}
.chat-upload-inline .q-uploader__header .q-btn {
    min-width: 44px !important;
    width: 44px !important;
    height: 44px !important;
    min-height: 44px !important;
    padding: 0 !important;
    margin: 0 !important;
    border-radius: 0 !important;
    color: #000 !important;
}
.chat-upload-inline .q-uploader__header .q-btn:hover {
    background: #f0f0f0 !important;
}
.chat-upload-inline .q-uploader__header .q-btn .q-icon {
    font-size: 20px !important;
}
.chat-upload-inline .q-uploader__list { display: none !important; }
/* ═══════════════════════════════════════════════════════════
   11) زر إعدادات الصوت (الشريط الجانبي)
   ═══════════════════════════════════════════════════════════ */
.voice-open-btn {
    width: calc(100% - 28px) !important;
    margin: 0 14px 12px !important;
    border-radius: 0 !important;
    min-height: 40px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: none !important;
    border: 1px solid #000 !important;
    background: #fff !important;
    color: #000 !important;
    justify-content: flex-start !important;
}
.voice-open-btn:hover {
    background: #f0f0f0 !important;
}
.voice-open-btn .q-icon {
    margin-left: 10px !important;
    margin-right: 0 !important;
}

/* ═══════════════════════════════════════════════════════════
   12) حوار إعدادات الصوت
   ═══════════════════════════════════════════════════════════ */
.voice-dialog {
    min-width: 480px !important;
    max-width: 92vw !important;
    border: 1px solid #000 !important;
    border-radius: 0 !important;
    padding: 0 !important;
    background: #fff !important;
    gap: 0 !important;
}
.voice-title {
    padding: 16px 22px;
    border-bottom: 1px solid #000;
    background: #fafafa;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #000 !important;
    width: 100%;
}
.voice-row {
    padding: 16px 22px;
    border-bottom: 1px solid #f0f0f0;
    width: 100%;
}
.voice-row:last-of-type { border-bottom: none; }
.voice-row-inline {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
}
.voice-head {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
}
.voice-label {
    font-size: 12px !important;
    color: #000 !important;
    font-weight: 500 !important;
}
.voice-value {
    font-family: 'SF Mono','Consolas',monospace;
    font-size: 12px !important;
    color: #666 !important;
    background: #f8f8f8;
    border: 1px solid #e8e8e8;
    padding: 2px 8px;
    line-height: 1;
    direction: ltr;
}
.voice-slider { color: #000 !important; padding: 0 !important; }
.voice-slider .q-slider__track-container { height: 2px; }
.voice-slider .q-slider__thumb { color: #000 !important; }
.voice-select {
    width: 100% !important;
    border: 1px solid #000 !important;
    background: #fff !important;
    padding: 0 !important;
}
.voice-select .q-field__control {
    padding: 0 12px !important;
    min-height: 40px !important;
}
.voice-select .q-field__native {
    font-size: 12px !important;
    color: #000 !important;
    direction: ltr;
}
.voice-switch .q-toggle__track { opacity: 0.9; }
.voice-actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    padding: 14px 22px;
    border-top: 1px solid #000;
    background: #fafafa;
    width: 100%;
}
.voice-btn {
    border: 1px solid #000 !important;
    background: #fff !important;
    color: #000 !important;
    border-radius: 0 !important;
    font-size: 12px !important;
    min-height: 36px !important;
    padding: 0 18px !important;
    text-transform: none !important;
    font-weight: 500 !important;
    margin: 0 !important;
}
.voice-btn:hover { background: #f0f0f0 !important; }
.voice-btn-primary {
    background: #000 !important;
    color: #fff !important;
}
.voice-btn-primary:hover { background: #333 !important; }

/* ═══════════════════════════════════════════════════════════
   13) لوحة الجمل السريعة (soundboard.py)
   ═══════════════════════════════════════════════════════════ */
.sb-status {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 18px;
    border: 1px solid #000;
    background: #fafafa;
    margin-bottom: 24px;
}
.sb-status-icon {
    font-size: 20px !important;
    color: #000 !important;
}
.sb-status-label {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #000 !important;
}
.sb-status-meta {
    margin-inline-start: auto;
    display: flex;
    gap: 16px;
}
.sb-status-item {
    font-size: 11px !important;
    color: #666 !important;
    font-family: 'SF Mono','Consolas',monospace;
}

.sb-section { margin-bottom: 24px; }
.sb-section-title {
    font-size: 10px !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #666 !important;
    font-weight: 600 !important;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid #e8e8e8;
    display: block;
    width: 100%;
}
.sb-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    width: 100%;
}
.sb-btn {
    border-radius: 0 !important;
    min-height: 72px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    text-transform: none !important;
    border: 1px solid #000 !important;
    background: #fff !important;
    color: #000 !important;
    transition: all 0.14s ease !important;
    padding: 12px 16px !important;
    margin: 0 !important;
    justify-content: center !important;
}
.sb-btn:hover {
    background: #000 !important;
    color: #fff !important;
    transform: translateY(-2px);
}
.sb-btn:active {
    transform: translateY(0);
}

.sb-basic .sb-btn     { border-color: #1e40af !important; color: #1e40af !important; }
.sb-basic .sb-btn:hover { background: #1e40af !important; color: #fff !important; }
.sb-needs .sb-btn     { border-color: #7c3aed !important; color: #7c3aed !important; }
.sb-needs .sb-btn:hover { background: #7c3aed !important; color: #fff !important; }
.sb-urgent .sb-btn    { border-color: #c0392b !important; color: #c0392b !important; font-weight: 700 !important; }
.sb-urgent .sb-btn:hover { background: #c0392b !important; color: #fff !important; }
.sb-questions .sb-btn { border-color: #0f766e !important; color: #0f766e !important; }
.sb-questions .sb-btn:hover { background: #0f766e !important; color: #fff !important; }

/* ═══════════════════════════════════════════════════════════
   14) استوديو الذكاء الاصطناعي (ai_studio.py)
   ═══════════════════════════════════════════════════════════ */
.ai-status {
    border: 1px solid #000;
    background: #fafafa;
    padding: 12px 18px;
    margin-bottom: 20px;
}
.ai-status-row {
    display: flex;
    align-items: center;
    gap: 12px;
}
.ai-status-icon {
    font-size: 20px !important;
    color: #000 !important;
}
.ai-status-label {
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #000 !important;
}
.ai-status-value {
    font-size: 12px !important;
    font-weight: 700 !important;
    margin-inline-start: auto;
    padding: 3px 10px;
    border: 1px solid;
    letter-spacing: 0.06em;
    font-family: 'SF Mono','Consolas',monospace;
}
.ai-status-on  { background: #dcfce7; color: #15803d; border-color: #86efac; }
.ai-status-off { background: #fee2e2; color: #c0392b; border-color: #fca5a5; }

.ai-card {
    border: 1px solid #000;
    background: #fff;
    margin-bottom: 20px;
}
.ai-card-title {
    padding: 12px 18px;
    border-bottom: 1px solid #000;
    background: #fafafa;
    font-size: 11px !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-weight: 600 !important;
    color: #000 !important;
}
.ai-prediction {
    display: block;
    padding: 40px 24px;
    text-align: center;
    font-size: 36px !important;
    font-weight: 300 !important;
    color: #000 !important;
    letter-spacing: -0.01em;
    min-height: 120px;
    background: #fdfdfd;
}
.ai-actions {
    display: flex;
    gap: 8px;
    padding: 14px 18px;
    border-top: 1px solid #f0f0f0;
    background: #fafafa;
    flex-wrap: wrap;
}
.ai-btn {
    border: 1px solid #000 !important;
    background: #fff !important;
    color: #000 !important;
    border-radius: 0 !important;
    font-size: 12px !important;
    min-height: 38px !important;
    padding: 0 16px !important;
    text-transform: none !important;
    font-weight: 500 !important;
    margin: 0 !important;
}
.ai-btn:hover { background: #f0f0f0 !important; }
.ai-btn-primary {
    background: #000 !important;
    color: #fff !important;
}
.ai-btn-primary:hover { background: #333 !important; }

.ai-log {
    border: 1px solid #000;
    background: #fff;
    min-height: 200px;
}
.ai-log-title {
    padding: 12px 18px;
    border-bottom: 1px solid #000;
    background: #fafafa;
    font-size: 11px !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-weight: 600 !important;
    color: #000 !important;
}
.ai-log-empty {
    padding: 60px 20px;
    text-align: center;
    color: #999 !important;
    font-size: 13px !important;
    display: block;
    width: 100%;
}
.ai-log-row {
    display: grid;
    grid-template-columns: 100px 1fr;
    gap: 14px;
    padding: 10px 18px;
    border-bottom: 1px solid #f0f0f0;
    align-items: center;
}
.ai-log-row:last-child { border-bottom: none; }
.ai-log-time {
    font-family: 'SF Mono','Consolas',monospace;
    font-size: 11px !important;
    color: #999 !important;
    direction: ltr;
}
.ai-log-word {
    font-size: 14px !important;
    color: #000 !important;
    font-weight: 500 !important;
}

/* ═══════════════════════════════════════════════════════════
   15) Responsive للإضافات
   ═══════════════════════════════════════════════════════════ */
@media (max-width: 900px) {
    .sb-grid { grid-template-columns: repeat(2, 1fr); }
    .voice-dialog { min-width: 90vw !important; }
    .sb-status-meta { flex-direction: column; gap: 4px; }
}
@media (max-width: 600px) {
    .sb-grid { grid-template-columns: 1fr; }
    .sb-btn { min-height: 56px !important; font-size: 13px !important; }
    .ai-prediction { font-size: 26px !important; padding: 28px 16px; }
    .voice-actions { flex-direction: column; }
    .voice-btn { width: 100% !important; }
}
/* ═══════════════════════════════════════════════════════════
   16) استوديو الذكاء الاصطناعي
   ═══════════════════════════════════════════════════════════ */
.ai-section {
    border: 1px solid #000;
    background: #fff;
    margin-bottom: 20px;
    width: 100%;
}
.ai-section-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 18px;
    background: #fafafa;
    border-bottom: 1px solid #000;
}
.ai-section-title {
    font-size: 11px !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-weight: 600 !important;
    color: #000 !important;
}
.ai-section-tag {
    font-size: 10px !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #999 !important;
    font-family: 'SF Mono','Consolas',monospace;
}

/* النماذج */
.ai-form { padding: 18px 20px; }
.ai-field { display: flex; flex-direction: column; gap: 6px; }
.ai-field-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 14px;
}
.ai-label {
    font-size: 11px !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #666 !important;
    font-weight: 500 !important;
}
.ai-input, .ai-select {
    width: 100% !important;
    border: 1px solid #000 !important;
    background: #fff !important;
    padding: 0 !important;
}
.ai-input .q-field__control,
.ai-select .q-field__control {
    padding: 0 14px !important;
    min-height: 42px !important;
}
.ai-input .q-field__native,
.ai-select .q-field__native {
    font-size: 13px !important;
    color: #000 !important;
}

.ai-actions-row {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-top: 18px;
    flex-wrap: wrap;
}
.ai-rec-btn {
    border: 1px solid #c0392b !important;
    background: #fff !important;
    color: #c0392b !important;
    border-radius: 0 !important;
    font-size: 13px !important;
    min-height: 42px !important;
    padding: 0 22px !important;
    text-transform: none !important;
    font-weight: 600 !important;
    margin: 0 !important;
}
.ai-rec-btn:hover { background: #c0392b !important; color: #fff !important; }
.ai-rec-btn:disabled { opacity: 0.5; }

.ai-rec-status {
    font-size: 12px !important;
    color: #666 !important;
    font-family: 'SF Mono','Consolas',monospace;
}
.ai-rec-status.rec-active {
    color: #c0392b !important;
    animation: pulse 1s infinite;
    font-weight: 600;
}

/* الحركات */
.ai-stats {
    padding: 10px 20px;
    background: #f8f8f8;
    border-bottom: 1px solid #f0f0f0;
}
.ai-stats-text {
    font-size: 11px !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #666 !important;
    font-family: 'SF Mono','Consolas',monospace;
    font-weight: 600 !important;
}
.ai-gesture-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 20px;
    border-bottom: 1px solid #f0f0f0;
    transition: background 0.12s ease;
}
.ai-gesture-row:last-child { border-bottom: none; }
.ai-gesture-row:hover { background: #fafafa; }
.ai-gesture-icon {
    font-size: 18px !important;
    color: #666 !important;
}
.ai-gesture-name {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #000 !important;
    flex: 1;
}
.ai-gesture-count {
    font-family: 'SF Mono','Consolas',monospace;
    font-size: 12px !important;
    color: #666 !important;
    background: #f0f0f0;
    padding: 3px 10px;
    border: 1px solid #e0e0e0;
    min-width: 40px;
    text-align: center;
}
.ai-gesture-del {
    color: #999 !important;
    width: 28px !important;
    height: 28px !important;
    min-width: 28px !important;
    min-height: 28px !important;
    padding: 0 !important;
}
.ai-gesture-del:hover { color: #c0392b !important; background: #fee2e2 !important; }

.ai-empty {
    padding: 50px 24px;
    align-items: center;
    justify-content: center;
    gap: 10px !important;
    width: 100%;
    text-align: center;
}
.ai-empty-icon { font-size: 40px !important; color: #ccc !important; }
.ai-empty-title {
    font-size: 14px !important;
    color: #666 !important;
    font-weight: 500 !important;
}
.ai-empty-hint {
    font-size: 12px !important;
    color: #999 !important;
}

/* التدريب */
.ai-train-btn {
    border: 1px solid #1e40af !important;
    background: #fff !important;
    color: #1e40af !important;
    border-radius: 0 !important;
    font-size: 13px !important;
    min-height: 42px !important;
    padding: 0 22px !important;
    text-transform: none !important;
    font-weight: 600 !important;
    margin: 0 !important;
}
.ai-train-btn:hover { background: #1e40af !important; color: #fff !important; }
.ai-train-btn:disabled { opacity: 0.5; }

.ai-train-status {
    font-size: 12px !important;
    color: #666 !important;
    font-family: 'SF Mono','Consolas',monospace;
}
.ai-train-status.ok  { color: #1a7a4a !important; font-weight: 600; }
.ai-train-status.err { color: #c0392b !important; font-weight: 600; }

/* التنبؤ الحيّ */
.ai-live {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 14px;
}
.ai-live-pred {
    display: block;
    text-align: center;
    font-size: 42px !important;
    font-weight: 300 !important;
    color: #000 !important;
    padding: 30px 20px;
    background: #fafafa;
    border: 1px solid #e8e8e8;
    letter-spacing: -0.01em;
    min-height: 130px;
}
.ai-live-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
}
.ai-live-btn {
    border: 1px solid #000 !important;
    background: #000 !important;
    color: #fff !important;
    border-radius: 0 !important;
    font-size: 12px !important;
    min-height: 40px !important;
    padding: 0 18px !important;
    text-transform: none !important;
    font-weight: 500 !important;
    margin: 0 !important;
}
.ai-live-btn:hover { background: #333 !important; }
.ai-live-btn:disabled { opacity: 0.5; }

.ai-live-btn-2 {
    border: 1px solid #000 !important;
    background: #fff !important;
    color: #000 !important;
    border-radius: 0 !important;
    font-size: 12px !important;
    min-height: 40px !important;
    padding: 0 18px !important;
    text-transform: none !important;
    font-weight: 500 !important;
    margin: 0 !important;
}
.ai-live-btn-2:hover { background: #f0f0f0 !important; }

.ai-live-status {
    font-size: 11px !important;
    color: #666 !important;
    font-family: 'SF Mono','Consolas',monospace;
    text-align: center;
    letter-spacing: 0.04em;
}

@media (max-width: 720px) {
    .ai-field-row { grid-template-columns: 1fr; }
    .ai-live-pred { font-size: 30px !important; padding: 20px 12px; }
    .ai-live-actions { flex-direction: column; }
    .ai-live-btn, .ai-live-btn-2 { width: 100% !important; }
}
/* ═══════════════════════════════════════════════════════════
   11) صفحة الصوت (voice.py)
   ═══════════════════════════════════════════════════════════ */
.voice-layout {
    display: grid;
    grid-template-columns: 1fr 340px;
    gap: 16px;
    width: 100%;
}
.voice-block {
    border: 1px solid #000;
    background: #fff;
}
.voice-block-title {
    padding: 12px 18px;
    border-bottom: 1px solid #000;
    background: #fafafa;
    font-size: 11px !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-weight: 600 !important;
    color: #000 !important;
}
.voice-block-body {
    padding: 16px 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}
.voice-textarea {
    width: 100% !important;
    border: 1px solid #e8e8e8 !important;
    background: #fff !important;
    padding: 12px 14px !important;
}
.voice-textarea .q-field__control { padding: 0 !important; }
.voice-textarea .q-field__native {
    font-size: 15px !important;
    font-family: inherit !important;
    line-height: 1.7;
    min-height: 120px;
    direction: rtl;
}
.voice-select {
    width: 100% !important;
    border: 1px solid #e8e8e8 !important;
    background: #fff !important;
    padding: 8px 14px !important;
}
.voice-select .q-field__control { padding: 0 !important; }

.voice-slider-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 6px 0;
}
.voice-slider-label {
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #333 !important;
    min-width: 60px;
}
.voice-slider-unit {
    font-size: 11px !important;
    color: #999 !important;
    font-family: 'SF Mono','Consolas',monospace;
    min-width: 24px;
    direction: ltr;
}
.voice-number {
    flex: 1;
    border: 1px solid #e8e8e8 !important;
    background: #fff !important;
    padding: 4px 10px !important;
}
.voice-number .q-field__control { padding: 0 !important; min-height: 32px !important; height: 32px !important; }
.voice-number .q-field__native {
    font-size: 13px !important;
    color: #000 !important;
    font-family: 'SF Mono','Consolas',monospace;
    direction: ltr;
    text-align: center;
}

.voice-result { grid-column: 1 / -1; }
.voice-player {
    width: 100%;
    border: 1px solid #e8e8e8;
    background: #fafafa;
    padding: 8px;
}
.voice-actions {
    display: flex;
    gap: 10px;
}
.voice-generate-btn {
    background: #000 !important;
    color: #fff !important;
    border-radius: 0 !important;
    min-height: 44px !important;
    padding: 0 24px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-transform: none !important;
    flex: 1;
}
.voice-generate-btn:hover { background: #333 !important; }
.voice-download-btn {
    background: #fff !important;
    color: #000 !important;
    border: 1px solid #000 !important;
    border-radius: 0 !important;
    min-height: 44px !important;
    padding: 0 20px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-transform: none !important;
}
.voice-download-btn:hover { background: #f0f0f0 !important; }
.voice-download-btn.q-btn--disabled {
    opacity: 0.4 !important;
}
.voice-status {
    font-size: 12px !important;
    color: #999 !important;
    font-family: 'SF Mono','Consolas',monospace;
    letter-spacing: 0.04em;
    min-height: 18px;
    text-align: center;
}
.voice-status.ok  { color: #1a7a4a !important; }
.voice-status.err { color: #c0392b !important; }

/* ═══════════════════════════════════════════════════════════
   12) استوديو الذكاء الاصطناعي (ai_studio.py)
   ═══════════════════════════════════════════════════════════ */
.ai-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    width: 100%;
}
.ai-block {
    border: 1px solid #000;
    background: #fff;
}
.ai-block-title {
    padding: 12px 18px;
    border-bottom: 1px solid #000;
    background: #fafafa;
    font-size: 11px !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-weight: 600 !important;
    color: #000 !important;
}
.ai-block-body {
    padding: 14px 18px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.ai-row {
    display: grid;
    grid-template-columns: 1fr 130px 30px;
    align-items: center;
    gap: 10px;
    padding: 4px 0;
}
.ai-label {
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #333 !important;
}
.ai-unit {
    font-size: 11px !important;
    color: #999 !important;
    font-family: 'SF Mono','Consolas',monospace;
    direction: ltr;
}
.ai-number {
    width: 100% !important;
    border: 1px solid #e8e8e8 !important;
    background: #fff !important;
    padding: 4px 12px !important;
}
.ai-number .q-field__control {
    padding: 0 !important;
    min-height: 34px !important;
    height: 34px !important;
}
.ai-number .q-field__native {
    font-size: 13px !important;
    color: #000 !important;
    font-family: 'SF Mono','Consolas',monospace;
    direction: ltr;
    text-align: center;
}

.ai-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #f0f0f0;
}
.ai-stat:last-of-type { border-bottom: none; }
.ai-stat-label {
    font-size: 12px !important;
    color: #666 !important;
}
.ai-stat-value {
    font-family: 'SF Mono','Consolas',monospace;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #000 !important;
    direction: ltr;
}

.ai-progress {
    width: 100%;
    margin: 12px 0 6px;
    height: 4px !important;
}
.ai-progress .q-linear-progress__track { background: #e8e8e8 !important; }
.ai-progress .q-linear-progress__model { background: #000 !important; }

.ai-status {
    font-size: 12px !important;
    color: #999 !important;
    font-family: 'SF Mono','Consolas',monospace;
    text-align: center;
    letter-spacing: 0.04em;
    min-height: 18px;
}
.ai-status.ok  { color: #1a7a4a !important; }
.ai-status.err { color: #c0392b !important; }

.ai-actions {
    display: flex;
    gap: 10px;
    margin-top: 8px;
}
.ai-btn {
    border: 1px solid #000 !important;
    background: #fff !important;
    color: #000 !important;
    border-radius: 0 !important;
    min-height: 42px !important;
    padding: 0 20px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: none !important;
    flex: 1;
}
.ai-btn:hover { background: #f0f0f0 !important; }
.ai-btn-primary {
    background: #000 !important;
    color: #fff !important;
    font-weight: 600 !important;
}
.ai-btn-primary:hover { background: #333 !important; }
.ai-btn.q-btn--disabled { opacity: 0.35 !important; }

.ai-log-wrap {
    margin-top: 12px;
    border-top: 1px solid #f0f0f0;
    padding-top: 10px;
}
.ai-log-title {
    font-size: 10px !important;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #999 !important;
    margin-bottom: 8px;
}
.ai-log {
    width: 100%;
    max-height: 180px;
    overflow-y: auto;
    gap: 2px !important;
    border: 1px solid #f0f0f0;
    padding: 8px 12px;
    background: #fafafa;
}
.ai-log-line {
    font-family: 'SF Mono','Consolas',monospace;
    font-size: 11px !important;
    color: #333 !important;
    direction: ltr;
    text-align: left;
    white-space: pre;
}

@media (max-width: 900px) {
    .voice-layout { grid-template-columns: 1fr; }
    .ai-layout { grid-template-columns: 1fr; }
    .ai-row { grid-template-columns: 1fr 110px 30px; }
}
/* ═══ شريط حالة الحساسات ═══ */
.sensor-status {
    border: 1px solid #000;
    background: #fafafa;
    padding: 12px 18px;
    margin-bottom: 20px;
}
.sensor-status-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 4px;
}
.sensor-status-label {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #000 !important;
}
.sensor-status-label.on   { color: #1a7a4a !important; }
.sensor-status-label.warn { color: #d97706 !important; }
.sensor-status-label.off  { color: #c0392b !important; }
.sensor-status-meta {
    font-size: 11px !important;
    color: #999 !important;
    font-family: 'SF Mono','Consolas',monospace;
    direction: ltr;
    text-align: right;
}
/* ═══ اسم الإصبع (عربي + إنجليزي) ═══ */
.sensor-label-group {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
}
.sensor-label-en {
    font-size: 9px !important;
    color: #999 !important;
    font-family: 'SF Mono','Consolas',monospace;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    direction: ltr;
}
</style>
'''


# ═══════════════════════════════════════════════════════════
# موارد ثابتة
# ═══════════════════════════════════════════════════════════
GLOVE_SVG = '''
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
     stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"
     width="100%" height="100%">
    <path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0"/>
    <path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v2"/>
    <path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8"/>
    <path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/>
</svg>
'''


CHAT_INPUT_JS = r'''
<script>
(function() {
    if (window.__signo_chat_js_ready) return;
    window.__signo_chat_js_ready = true;
    document.addEventListener('keydown', function(e) {
        if (e.key !== 'Enter') return;
        if (e.shiftKey || e.ctrlKey || e.metaKey) return;
        var t = e.target;
        if (!t || t.tagName !== 'TEXTAREA') return;
        if (!t.closest('.chat-input-area')) return;
        e.preventDefault();
        var area = t.closest('.chat-input-area');
        var btn = area && area.querySelector('.chat-send-btn');
        if (btn) btn.click();
    });
})();

</script>
'''
AUDIO_JS = r'''
<script>
(function() {
    if (window.__signo_audio_js) return;
    window.__signo_audio_js = true;

    let voicesCache = [];

    function pickVoice(voices, preferred) {
        if (!voices || !voices.length) return null;
        if (preferred) {
            const exact = voices.find(v => v.name === preferred);
            if (exact) return exact;
        }
        const arSA = voices.find(v => v.lang === 'ar-SA');
        if (arSA) return arSA;
        const arAny = voices.find(v => (v.lang || '').toLowerCase().startsWith('ar'));
        if (arAny) return arAny;
        return null;
    }

    function loadVoices() {
        if (!window.speechSynthesis) return;
        voicesCache = window.speechSynthesis.getVoices() || [];
        if (typeof emitEvent === 'function' && voicesCache.length) {
            const list = voicesCache.map(v => ({name: v.name, lang: v.lang}));
            emitEvent('voices_ready', {voices: list});
        }
    }

    if (window.speechSynthesis) {
        loadVoices();
        window.speechSynthesis.onvoiceschanged = loadVoices;
    }

    window.signoSpeak = function(data) {
        if (!window.speechSynthesis || !data || !data.text) return;
        try {
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(String(data.text));
            u.rate   = data.rate   || 1.0;
            u.pitch  = data.pitch  || 1.0;
            u.volume = data.volume == null ? 1.0 : data.volume;

            const voices = window.speechSynthesis.getVoices() || [];
            const v = pickVoice(voices, data.voice);
            if (v) { u.voice = v; u.lang = v.lang; }
            else   { u.lang = 'ar-SA'; }

            window.speechSynthesis.speak(u);
        } catch (e) {
            console.warn('[signoSpeak]', e);
        }
    };

    window.signoListVoices = function() {
        loadVoices();
    };
})();
</script>
'''