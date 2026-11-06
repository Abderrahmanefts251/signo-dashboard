# voice.py
"""صفحة تحويل النص إلى صوت — أصوات متعددة (Edge TTS + gTTS fallback)."""
import base64
import io

from nicegui import ui

try:
    import edge_tts
    HAS_EDGE = True
except ImportError:
    HAS_EDGE = False

try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False


TITLE = 'تحويل النص إلى صوت'
ICON  = 'record_voice_over'
DESC  = ('اكتب نصاً، اختر الصوت (عربي، فرنسي، إنجليزي)، واستمع أو حمّل الملف.')

# ═══════════════════════════════════════════════════════════
# قائمة الأصوات (Edge TTS)
# ═══════════════════════════════════════════════════════════
VOICES = {
    # ─── العربية ───
    'عربي · المغرب · منى (أنثى)':      'ar-MA-MounaNeural',
    'عربي · المغرب · جمال (ذكر)':      'ar-MA-JamalNeural',
    'عربي · السعودية · زارية (أنثى)':  'ar-SA-ZariyahNeural',
    'عربي · السعودية · حامد (ذكر)':    'ar-SA-HamedNeural',
    'عربي · مصر · سلمى (أنثى)':        'ar-EG-SalmaNeural',
    'عربي · مصر · شاكر (ذكر)':         'ar-EG-ShakirNeural',
    'عربي · الإمارات · فاطمة (أنثى)':  'ar-AE-FatimaNeural',
    'عربي · الإمارات · حمدان (ذكر)':   'ar-AE-HamdanNeural',
    'عربي · الجزائر · أمينة (أنثى)':   'ar-DZ-AminaNeural',
    'عربي · الجزائر · إسماعيل (ذكر)':  'ar-DZ-IsmaelNeural',
    'عربي · العراق · رنا (أنثى)':       'ar-IQ-RanaNeural',
    'عربي · العراق · باسل (ذكر)':       'ar-IQ-BasselNeural',
    'عربي · الكويت · نورة (أنثى)':      'ar-KW-NouraNeural',
    'عربي · الكويت · فهد (ذكر)':        'ar-KW-FahedNeural',
    'عربي · لبنان · ليلى (أنثى)':       'ar-LB-LaylaNeural',
    'عربي · لبنان · رامي (ذكر)':        'ar-LB-RamiNeural',
    'عربي · سوريا · أماني (أنثى)':      'ar-SY-AmanyNeural',
    'عربي · سوريا · ليث (ذكر)':         'ar-SY-LaithNeural',
    'عربي · تونس · ريم (أنثى)':         'ar-TN-ReemNeural',
    'عربي · تونس · هادي (ذكر)':         'ar-TN-HediNeural',
    'عربي · قطر · أمل (أنثى)':          'ar-QA-AmalNeural',
    'عربي · قطر · معاذ (ذكر)':          'ar-QA-MoazNeural',
    'عربي · الأردن · سناء (أنثى)':      'ar-JO-SanaNeural',
    'عربي · الأردن · ليث (ذكر)':        'ar-JO-LaithNeural',

    # ─── الفرنسية ───
    'فرنسي · فرنسا · دينيس (أنثى)':     'fr-FR-DeniseNeural',
    'فرنسي · فرنسا · هنري (ذكر)':       'fr-FR-HenriNeural',
    'فرنسي · فرنسا · إلويز (أنثى)':     'fr-FR-EloiseNeural',
    'فرنسي · فرنسا · ألان (ذكر)':       'fr-FR-AlainNeural',
    'فرنسي · كندا · سيلفي (أنثى)':      'fr-CA-SylvieNeural',
    'فرنسي · كندا · جان (ذكر)':         'fr-CA-JeanNeural',
    'فرنسي · بلجيكا · شارلين (أنثى)':   'fr-BE-CharlineNeural',
    'فرنسي · بلجيكا · جيرارد (ذكر)':    'fr-BE-GerardNeural',
    'فرنسي · سويسرا · أريان (أنثى)':    'fr-CH-ArianeNeural',
    'فرنسي · سويسرا · فابريس (ذكر)':    'fr-CH-FabriceNeural',

    # ─── الإنجليزية ───
    'إنجليزي · أمريكي · جيني (أنثى)':   'en-US-JennyNeural',
    'إنجليزي · أمريكي · غاي (ذكر)':     'en-US-GuyNeural',
    'إنجليزي · أمريكي · آريا (أنثى)':   'en-US-AriaNeural',
    'إنجليزي · أمريكي · ديفيس (ذكر)':   'en-US-DavisNeural',
    'إنجليزي · بريطاني · سونيا (أنثى)': 'en-GB-SoniaNeural',
    'إنجليزي · بريطاني · رايان (ذكر)':  'en-GB-RyanNeural',
    'إنجليزي · أسترالي · ناتاشا (أنثى)':'en-AU-NatashaNeural',
    'إنجليزي · أسترالي · ويليام (ذكر)': 'en-AU-WilliamNeural',
    'إنجليزي · كندي · كلارا (أنثى)':    'en-CA-ClaraNeural',
    'إنجليزي · كندي · ليام (ذكر)':      'en-CA-LiamNeural',
    'إنجليزي · هندي · نيرجا (أنثى)':    'en-IN-NeerjaNeural',
    'إنجليزي · هندي · برابهات (ذكر)':   'en-IN-PrabhatNeural',
}

DEFAULT_VOICE = 'عربي · المغرب · منى (أنثى)'


# ═══════════════════════════════════════════════════════════
# توليد الصوت
# ═══════════════════════════════════════════════════════════
async def _generate_edge(text: str, voice_id: str, rate: int, pitch: int) -> bytes:
    communicate = edge_tts.Communicate(
        text, voice_id,
        rate=f'{rate:+d}%',
        pitch=f'{pitch:+d}Hz',
    )
    buf = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk.get('type') == 'audio':
            buf.write(chunk['data'])
    return buf.getvalue()


def _generate_gtts(text: str, voice_id: str, slow: bool = False) -> bytes:
    # استخراج اللغة من معرّف الصوت (مثلاً ar-MA-MounaNeural -> ar)
    lang = voice_id.split('-')[0]
    tts = gTTS(text=text, lang=lang, slow=slow)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════════
# الواجهة
# ═══════════════════════════════════════════════════════════
def build() -> dict:
    refs = {'audio_state': {'data': b'', 'name': 'voice.mp3'}}

    ui.label('03').classes('page-number')
    ui.label(TITLE).classes('page-title')
    ui.element('div').classes('divider')
    ui.label(DESC).classes('hint-box')

    with ui.element('div').classes('voice-layout'):

        # ─── النص ───
        with ui.element('div').classes('voice-block'):
            ui.label('النص').classes('voice-block-title')
            with ui.element('div').classes('voice-block-body'):
                refs['text'] = (
                    ui.textarea(placeholder='اكتب النص هنا...')
                    .props('borderless autogrow rows=5')
                    .classes('voice-textarea')
                )

        # ─── الإعدادات ───
        with ui.element('div').classes('voice-block'):
            ui.label('الصوت').classes('voice-block-title')
            with ui.element('div').classes('voice-block-body'):
                refs['voice'] = (
                    ui.select(options=list(VOICES.keys()),
                              value=DEFAULT_VOICE,
                              label='اختر الصوت')
                    .props('borderless')
                    .classes('voice-select')
                )

                with ui.element('div').classes('voice-slider-row'):
                    ui.label('السرعة').classes('voice-slider-label')
                    refs['rate'] = (
                        ui.number(value=0, min=-50, max=100, step=5, format='%d')
                        .props('borderless dense').classes('voice-number')
                    )
                    ui.label('٪').classes('voice-slider-unit')

                with ui.element('div').classes('voice-slider-row'):
                    ui.label('النبرة').classes('voice-slider-label')
                    refs['pitch'] = (
                        ui.number(value=0, min=-50, max=50, step=5, format='%d')
                        .props('borderless dense').classes('voice-number')
                    )
                    ui.label('Hz').classes('voice-slider-unit')

        # ─── النتيجة ───
        with ui.element('div').classes('voice-block voice-result'):
            ui.label('النتيجة').classes('voice-block-title')
            with ui.element('div').classes('voice-block-body'):

                async def generate():
                    text = (refs['text'].value or '').strip()
                    if not text:
                        ui.notify('اكتب نصاً أولاً', type='warning', position='top')
                        return

                    voice_label = refs['voice'].value
                    voice_id = VOICES.get(voice_label)
                    if not voice_id:
                        ui.notify('اختر صوتاً', type='warning', position='top')
                        return

                    refs['status'].text = 'جارٍ التوليد...'
                    refs['status'].classes(remove='ok err')
                    refs['generate_btn'].props('loading')

                    try:
                        if HAS_EDGE:
                            audio = await _generate_edge(
                                text, voice_id,
                                int(refs['rate'].value or 0),
                                int(refs['pitch'].value or 0)
                            )
                        elif HAS_GTTS:
                            audio = _generate_gtts(text, voice_id)
                        else:
                            raise Exception("لا توجد مكتبة صوتية مثبتة (edge-tts أو gTTS)")
                    except Exception as e:
                        # في حال فشل Edge TTS (خطأ 403)، جرب gTTS
                        if HAS_GTTS:
                            refs['status'].text = 'تعذر استخدام Edge TTS، جاري استخدام gTTS...'
                            try:
                                audio = _generate_gtts(text, voice_id)
                            except Exception as e2:
                                refs['status'].text = f'فشل: {e2}'
                                refs['status'].classes(add='err')
                                refs['generate_btn'].props(remove='loading')
                                return
                        else:
                            refs['status'].text = f'فشل: {e}'
                            refs['status'].classes(add='err')
                            refs['generate_btn'].props(remove='loading')
                            return

                    refs['generate_btn'].props(remove='loading')

                    if not audio:
                        refs['status'].text = 'لم يُنتج أي صوت'
                        refs['status'].classes(add='err')
                        return

                    b64 = base64.b64encode(audio).decode()
                    refs['audio_state']['data'] = audio
                    refs['audio_state']['name'] = f'voice_{voice_id[:4]}.mp3'

                    refs['player'].source = f'data:audio/mp3;base64,{b64}'
                    refs['player'].update()
                    refs['download_btn'].enable()
                    refs['status'].text = f'✓ جاهز · {len(audio) // 1024} KB'
                    refs['status'].classes(remove='err').classes(add='ok')

                def download():
                    data = refs['audio_state']['data']
                    if data:
                        ui.download(data, refs['audio_state']['name'])

                refs['player'] = ui.audio('').classes('voice-player')

                with ui.element('div').classes('voice-actions'):
                    refs['generate_btn'] = ui.button(
                        'توليد الصوت', icon='play_arrow', on_click=generate
                    ).props('flat no-caps').classes('voice-generate-btn')
                    refs['download_btn'] = ui.button(
                        'تحميل', icon='download', on_click=download
                    ).props('flat no-caps').classes('voice-download-btn')

                refs['download_btn'].disable()
                refs['status'] = ui.label('').classes('voice-status')

    return refs


async def refresh(refs): pass
def on_enter(): pass