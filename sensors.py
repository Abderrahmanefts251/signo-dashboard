# sensors.py
"""لوحة الحساسات — عرض حيّ + آخر قراءة معروفة."""
from datetime import datetime
from nicegui import ui

import mqtt_client


TITLE = 'لوحة الحساسات'
ICON  = 'sensors'
DESC  = ('قراءات حية من قفاز الإشارة عبر MQTT — خمسة مستشعرات '
         'انحناء (ADC) وحساس حركة 6-DoF.')


# ═══════════════════════════════════════════════════════════
# أدوات الوقت
# ═══════════════════════════════════════════════════════════
def _fmt_duration(ms: int) -> str:
    """يحول الفارق الزمني إلى صيغة مقروءة (ثواني / دقائق)."""
    ms = max(0, ms)
    if ms < 1000:
        return f'{ms} ms'
    secs = ms / 1000
    if secs < 60:
        return f'{secs:.2f} ث'
    mins, rem = divmod(secs, 60)
    return f'{int(mins)} د {rem:.1f} ث'


def _fmt_timestamp(ms: int) -> str:
    """يحول الملي ثانية (Unix Timestamp) إلى تاريخ ووقت مقروء."""
    if not ms:
        return '—'
    try:
        # نقسم على 1000 لأن بايثون يتعامل بالثواني
        dt = datetime.fromtimestamp(ms / 1000.0)
        return dt.strftime('%Y-%m-%d · %H:%M:%S')
    except Exception:
        return f'{ms} ms'


# ═══════════════════════════════════════════════════════════
# بناء الواجهة
# ═══════════════════════════════════════════════════════════
def build() -> dict:
    refs = {}

    ui.label('01').classes('page-number')
    ui.label(TITLE).classes('page-title')
    ui.element('div').classes('divider')
    ui.label(DESC).classes('hint-box')

    # ─── شريط حالة الاتصال ───
    with ui.element('div').classes('sensor-status'):
        with ui.element('div').classes('sensor-status-row'):
            refs['status_dot'] = ui.element('div').classes('mqtt-dot wait')
            refs['status_label'] = ui.label('جارٍ الاتصال...') \
                .classes('sensor-status-label')
        refs['status_meta'] = ui.label('—').classes('sensor-status-meta')

    # ─── الشبكة ───
    with ui.element('div').classes('sensor-grid'):

        # الوقت والتاريخ
        with ui.element('div').classes('sensor-block'):
            ui.label('الوقت').classes('sensor-block-title')
            with ui.element('div').classes('sensor-rows'):
                for key, lbl in (
                    ('start',   'بدأ عند'),
                    ('now',     'الآن'),
                    ('elapsed', 'الوقت المنقضي'),
                ):
                    with ui.element('div').classes('sensor-row'):
                        ui.label(lbl).classes('sensor-label')
                        refs[key] = ui.label('—').classes('sensor-value')

        # Flex (الأصابع)
        with ui.element('div').classes('sensor-block'):
            ui.label('الأصابع · Flex Sensors').classes('sensor-block-title')
            with ui.element('div').classes('sensor-rows'):
                finger_map = [
                    ('flex1', 'السبابة',  'Index'),
                    ('flex2', 'الوسطى',   'Middle'),
                    ('flex3', 'البنصر',   'Ring'),
                    ('flex4', 'الخنصر',   'Pinky'),
                    ('flex5', 'الإبهام',  'Thumb'),
                ]
                for key, ar_name, en_name in finger_map:
                    with ui.element('div').classes('sensor-row'):
                        with ui.element('div').classes('sensor-label-group'):
                            ui.label(ar_name).classes('sensor-label')
                            ui.label(en_name).classes('sensor-label-en')
                        refs[key] = ui.label('—').classes('sensor-value')

        # الجيروسكوب
        with ui.element('div').classes('sensor-block'):
            ui.label('الجايروسكوب · Gyro').classes('sensor-block-title')
            with ui.element('div').classes('sensor-rows'):
                for key in ('gx', 'gy', 'gz'):
                    with ui.element('div').classes('sensor-row'):
                        ui.label(key).classes('sensor-label')
                        refs[key] = ui.label('—').classes('sensor-value')

        # التسارع
        with ui.element('div').classes('sensor-block'):
            ui.label('التسارع · Accel').classes('sensor-block-title')
            with ui.element('div').classes('sensor-rows'):
                for key in ('ax', 'ay', 'az'):
                    with ui.element('div').classes('sensor-row'):
                        ui.label(key).classes('sensor-label')
                        refs[key] = ui.label('—').classes('sensor-value')

    return refs


# ═══════════════════════════════════════════════════════════
# التحديث الدوري
# ═══════════════════════════════════════════════════════════
async def refresh(refs):
    s = mqtt_client.STATE

    # ─── شريط الحالة ───
    try:
        st = mqtt_client.esp_status()
        dot = refs['status_dot']
        dot.classes(remove='on off warn wait')
        dot.classes(add=st['color'])

        refs['status_label'].text = st['label']
        refs['status_label'].classes(remove='on warn off')
        if st['color'] in ('on', 'warn', 'off'):
            refs['status_label'].classes(add=st['color'])

        if s['total'] == 0:
            refs['status_meta'].text = (
                f'{mqtt_client.BROKER} · لم يصل أي payload'
            )
        elif st['ago'] is not None:
            refs['status_meta'].text = (
                f'{s["total"]} حزمة · آخر رسالة منذ {st["ago"]:.1f} ث'
            )
        else:
            refs['status_meta'].text = f'{s["total"]} حزمة'
    except Exception as e:
        print(f'[sensors status] {e}', flush=True)

    # ─── القيم ───
    latest = s.get('latest')
    if latest is None:
        return

    # Flex
    for i in range(1, 6):
        key = f'flex{i}'
        refs[key].text = str(latest.get(key, '—'))

    # Gyro + Accel
    for key in ('gx', 'gy', 'gz', 'ax', 'ay', 'az'):
        val = latest.get(key)
        if val is not None:
            refs[key].text = f'{float(val):+.2f}'

    # ─── الوقت والتاريخ ───
    first = s.get('first_time')
    now_time = latest.get('time', 0)
    
    if first is not None:
        refs['start'].text = _fmt_timestamp(first)
        refs['elapsed'].text = _fmt_duration(now_time - first)
    else:
        refs['start'].text = '—'
        refs['elapsed'].text = '—'

    refs['now'].text = _fmt_timestamp(now_time)


def on_enter():
    pass