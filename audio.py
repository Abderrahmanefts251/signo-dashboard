# audio.py
"""النطق الفوري داخل المتصفح (Web Speech API) للتنبؤات."""
import json

from nicegui import app, ui


# ═══════════════════════════════════════════════════════════
# الإعدادات الافتراضية
# ═══════════════════════════════════════════════════════════
DEFAULTS = {
    'rate':   1.0,      # سرعة النطق 0.5 - 2.0
    'pitch':  1.0,      # النبرة 0.0 - 2.0
    'volume': 1.0,      # مستوى الصوت 0.0 - 1.0
    'voice':  '',       # اسم الصوت (فارغ = الافتراضي العربي)
    'auto':   True,     # النطق التلقائي للتنبؤات
}

_KEY = 'signo_voice'


# ═══════════════════════════════════════════════════════════
# قراءة / كتابة الإعدادات
# ═══════════════════════════════════════════════════════════
def get():
    """يقرأ الإعدادات من cookie المتصفح (تبقى عبر إعادة التحميل)."""
    try:
        s = app.storage.browser.get(_KEY)
        if not isinstance(s, dict):
            return dict(DEFAULTS)
        merged = dict(DEFAULTS)
        merged.update(s)
        return merged
    except Exception:
        return dict(DEFAULTS)


def set(**kwargs):
    """يحدّث الإعدادات."""
    s = get()
    s.update(kwargs)
    try:
        app.storage.browser[_KEY] = s
    except Exception:
        pass
    return s


# ═══════════════════════════════════════════════════════════
# النطق
# ═══════════════════════════════════════════════════════════
def speak(text, **overrides):
    """ينطق النص بالعربية في المتصفح."""
    if not text:
        return
    s = get()
    s.update(overrides)
    
    payload = json.dumps({
        'text':   str(text),
        'rate':   float(s.get('rate', 1.0)),
        'pitch':  float(s.get('pitch', 1.0)),
        'volume': float(s.get('volume', 1.0)),
        'voice':  s.get('voice', '') or '',
    }, ensure_ascii=False)
    
    try:
        ui.run_javascript(
            f'window.signoSpeak && window.signoSpeak({payload})'
        )
    except Exception as e:
        print(f'[audio] speak failed: {e}', flush=True)


def speak_prediction(text):
    """يُستخدم من استوديو الذكاء الاصطناعي — ينطق إذا كان auto مُفعّلاً."""
    if get().get('auto', True):
        speak(text)


def stop():
    """يوقف النطق الحالي."""
    try:
        ui.run_javascript(
            'window.speechSynthesis && window.speechSynthesis.cancel()'
        )
    except Exception:
        pass


def refresh_voices():
    """يطلب من المتصفح قائمة الأصوات المتاحة."""
    try:
        ui.run_javascript('window.signoListVoices && window.signoListVoices()')
    except Exception:
        pass