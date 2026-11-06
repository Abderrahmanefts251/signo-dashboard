# app.py
"""نقطة الدخول — 3 صفحات: الحساسات · الذكاء الاصطناعي · الصوت."""
import os
import shutil
import subprocess
import threading
import time

from nicegui import app, ui

import mqtt_client as mqtt
from assets import CSS, GLOVE_SVG

# ─── الصفحات ───
import sensors
import ai_studio
import voice


# ═══════════════════════════════════════════════════════════
# ترتيب الصفحات
# ═══════════════════════════════════════════════════════════
PAGES = [sensors, ai_studio, voice]


# ═══════════════════════════════════════════════════════════
# إعدادات البيئة
# ═══════════════════════════════════════════════════════════
PORT   = int(os.environ.get('PORT', 7860))
HOST   = os.environ.get('HOST', '0.0.0.0')
SECRET = os.environ.get('STORAGE_SECRET', 'signo-local-secret')
TUNNEL = os.environ.get('TUNNEL', '').strip().lower()
DEBUG  = os.environ.get('DEBUG', '0') == '1'


# ═══════════════════════════════════════════════════════════
# النفق (ngrok / cloudflared)
# ═══════════════════════════════════════════════════════════
def _find_binary(name):
    if os.path.exists(f'./{name}'):
        return f'./{name}'
    found = shutil.which(name)
    if found:
        return found
    home = os.path.expanduser('~')
    for p in (f'/usr/local/bin/{name}', f'{home}/bin/{name}',
              f'{home}/.local/bin/{name}'):
        if os.path.exists(p):
            return p
    return None


def _banner(url):
    line = '═' * 62
    print(f'\n{line}\n  🌍 الرابط العام جاهز:\n     {url}\n{line}\n', flush=True)


def _run_ngrok():
    binary = _find_binary('ngrok')
    if not binary:
        print('⚠️  ngrok غير موجود', flush=True)
        return
    domain = os.environ.get('NGROK_DOMAIN', '').strip()
    cmd = [binary, 'http', str(PORT), '--log', 'stdout']
    if domain:
        cmd.append(f'--url={domain}')
    print(f'[tunnel] {binary} http {PORT}' + (f' --url={domain}' if domain else ''), flush=True)
    
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, bufsize=1)
    except Exception as e:
        print(f'[tunnel] فشل: {e}', flush=True)
        return
        
    seen = False
    for line in proc.stdout:
        line = line.rstrip()
        if DEBUG:
            print(f'[ngrok] {line}', flush=True)
        if 'url=https://' in line and not seen:
            try:
                _banner(line.split('url=')[1].split()[0])
                seen = True
            except Exception:
                pass


def _run_cloudflared():
    binary = _find_binary('cloudflared')
    if not binary:
        print('⚠️  cloudflared غير موجود', flush=True)
        return
    print(f'[tunnel] {binary} tunnel', flush=True)
    
    try:
        proc = subprocess.Popen(
            [binary, 'tunnel', '--url', f'http://localhost:{PORT}', '--no-autoupdate'],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    except Exception as e:
        print(f'[tunnel] فشل: {e}', flush=True)
        return
        
    seen = False
    for line in proc.stdout:
        line = line.rstrip()
        if DEBUG:
            print(f'[cloudflared] {line}', flush=True)
        if 'trycloudflare.com' in line and not seen:
            for tok in line.split():
                if tok.startswith('https://') and 'trycloudflare.com' in tok:
                    _banner(tok)
                    seen = True
                    break


def _start_tunnel():
    if not TUNNEL:
        return
    def _run():
        time.sleep(2)
        if TUNNEL == 'ngrok':
            _run_ngrok()
        elif TUNNEL == 'cloudflared':
            _run_cloudflared()
    threading.Thread(target=_run, daemon=True).start()


# ═══════════════════════════════════════════════════════════
# MQTT
# ═══════════════════════════════════════════════════════════
mqtt.start()


@app.on_shutdown
def _shutdown():
    mqtt.stop()


# ═══════════════════════════════════════════════════════════
# الصفحة
# ═══════════════════════════════════════════════════════════
@ui.page('/')
async def main_page():
    ui.add_head_html(CSS)

    state = {'i': 0}
    card_elems = []
    page_refs = []
    nav_buttons = []
    esp = {}

    def select(i):
        state['i'] = i
        for k, c in enumerate(card_elems):
            c.set_visibility(k == i)
        for k, b in enumerate(nav_buttons):
            b.classes(add='active') if k == i else b.classes(remove='active')
        if hasattr(PAGES[i], 'on_enter'):
            try:
                PAGES[i].on_enter()
            except Exception as e:
                print(f'[on_enter] {e}', flush=True)

    # ═══ الشريط الجانبي ═══
    with ui.left_drawer(value=True, bordered=False).props('width=250').classes('p-0'):
        with ui.column().classes('w-full h-full gap-0'):

            with ui.element('div').classes('brand-block'):
                with ui.element('div').classes('brand-left'):
                    ui.html(GLOVE_SVG).classes('brand-glove')
                    ui.label('SIGNO').classes('brand')
                ui.label('◼').classes('brand-mark')

            with ui.column().classes('nav-list'):
                for i, page in enumerate(PAGES):
                    btn = ui.button(
                        getattr(page, 'TITLE', f'صفحة {i+1}'),
                        icon=getattr(page, 'ICON', 'circle'),
                        on_click=lambda k=i: select(k),
                    ).props('flat no-caps align=left').classes('nav-btn w-full')
                    nav_buttons.append(btn)

            # ─── بطاقة ESP ───
            with ui.element('div').classes('esp-card'):
                with ui.element('div').classes('esp-head'):
                    ui.label('Sensors · ESP32').classes('esp-title')
                    esp['dot'] = ui.element('div').classes('esp-dot wait')
                esp['label'] = ui.label('بانتظار ESP...').classes('esp-label')
                esp['meta']  = ui.label('—').classes('esp-meta')
                with ui.element('div').classes('esp-stats'):
                    esp['total'] = ui.label('0 حزمة')
                    esp['rate']  = ui.label('0.0 /ث')

            ui.space()
            ui.label('V 1.0').classes('footer-mark')

    # ═══ المحتوى ═══
    with ui.element('div').classes('content-wrap'):
        for idx, page in enumerate(PAGES):
            with ui.column().classes('card') as card:
                with ui.element('div').classes('card-header'):
                    ui.label('لوحة التحكم').classes('card-title')
                    ui.label(f'{idx+1:02d} / {len(PAGES):02d}').classes('card-index')
                with ui.column().classes('card-body'):
                    page_refs.append(page.build())
                with ui.element('div').classes('card-footer'):
                    ui.label('SIGNO SYSTEM').classes('footer-label')
                    with ui.element('div').style('display:flex;gap:5px'):
                        for _ in PAGES:
                            ui.element('div').style(
                                'width:6px;height:6px;'
                                'border:1px solid #000;border-radius:50%')
            card_elems.append(card)

    select(0)

    # ═══ التحديث ═══
    _rate = {'last_total': 0, 'last_ts': time.time(), 'rate': 0.0}

    async def refresh():
        # تحديث بطاقة ESP
        try:
            st = mqtt.esp_status()
            esp['dot'].classes(remove='on off warn wait').classes(add=st['color'])
            esp['label'].text = st['label']
            esp['label'].classes(remove='on warn off')
            if st['color'] in ('on', 'warn', 'off'):
                esp['label'].classes(add=st['color'])
                
            if st['ago'] is not None:
                esp['meta'].text = f'آخر رسالة منذ {st["ago"]:.1f} ث'
            elif mqtt.STATE['connected']:
                esp['meta'].text = 'الوسيط متصل · لا حزم'
            else:
                esp['meta'].text = 'الوسيط غير متصل'
                
            total = mqtt.STATE['total']
            esp['total'].text = f'{total} حزمة'
            
            now = time.time()
            if now - _rate['last_ts'] >= 2.0:
                dt = now - _rate['last_ts']
                dn = total - _rate['last_total']
                _rate['rate'] = (dn / dt) if dt > 0 else 0.0
                _rate['last_total'] = total
                _rate['last_ts'] = now
                
            esp['rate'].text = f'{_rate["rate"]:.1f} /ث'
        except Exception as e:
            print(f'[esp] {e}', flush=True)

        # تحديث الصفحة النشطة
        try:
            page = PAGES[state['i']]
            await page.refresh(page_refs[state['i']])
        except Exception as e:
            print(f'[refresh] {e}', flush=True)

    ui.timer(0.1, refresh)


# ═══════════════════════════════════════════════════════════
# التشغيل
# ═══════════════════════════════════════════════════════════
if TUNNEL:
    print(f'\n🚇 النفق: {TUNNEL}')

_start_tunnel()

ui.run(
    host=HOST,
    port=PORT,
    title='SIGNO',
    language='ar',
    dark=False,
    favicon='🧤',
    reload=False,
    storage_secret=SECRET,
    show=False,
)