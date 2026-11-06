# ai_studio.py
"""استوديو الذكاء الاصطناعي — جمع بيانات، تدريب، تنبؤ حيّ، نطق."""
import asyncio
import csv
import pickle
import time
from pathlib import Path

from nicegui import ui

import audio
import mqtt_client


TITLE = 'استوديو الذكاء الاصطناعي'
ICON  = 'auto_awesome'
DESC  = ('جمع بيانات الإشارات من القفاز، تدريب نموذج تصنيف، '
         'ثم التنبؤ الحيّ والنطق التلقائي للكلمات.')


# ═══════════════════════════════════════════════════════════
# المسارات
# ═══════════════════════════════════════════════════════════
DATA_DIR   = Path('data')
MODELS_DIR = Path('models')
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODELS_DIR / 'signo_model.pkl'


# ═══════════════════════════════════════════════════════════
# القنوات
# ═══════════════════════════════════════════════════════════
CHANNELS = ['flex1', 'flex2', 'flex3', 'flex4', 'flex5',
            'gx', 'gy', 'gz', 'ax', 'ay', 'az']


# ═══════════════════════════════════════════════════════════
# أدوات الملفات
# ═══════════════════════════════════════════════════════════
def list_gestures() -> dict:
    """يرجع {label: عدد العينات}."""
    result = {}
    if not DATA_DIR.exists():
        return result
    for d in sorted(DATA_DIR.iterdir()):
        if d.is_dir():
            n = len(list(d.glob('*.csv')))
            if n > 0:
                result[d.name] = n
    return result


def save_sample(label: str, samples: list) -> Path:
    """يحفظ عينة واحدة كـ CSV."""
    safe = ''.join(c for c in label if c.isalnum() or c in '_- ')
    safe = safe.strip().replace(' ', '_')
    if not safe:
        safe = 'gesture'

    label_dir = DATA_DIR / safe
    label_dir.mkdir(exist_ok=True)

    existing = sorted(label_dir.glob('*.csv'))
    idx = len(existing) + 1
    path = label_dir / f'sample_{idx:03d}.csv'

    with open(path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['time'] + CHANNELS
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for s in samples:
            row = {'time': s.get('time', 0)}
            for ch in CHANNELS:
                row[ch] = s.get(ch, 0)
            w.writerow(row)

    return path


def delete_gesture(label: str) -> int:
    """يحذف كل عينات حركة معينة. يرجع عدد المحذوفات."""
    label_dir = DATA_DIR / label
    if not label_dir.exists():
        return 0
    n = 0
    for f in label_dir.glob('*.csv'):
        f.unlink()
        n += 1
    try:
        label_dir.rmdir()
    except Exception:
        pass
    return n


# ═══════════════════════════════════════════════════════════
# استخراج الميزات
# ═══════════════════════════════════════════════════════════
def extract_features(samples: list) -> list:
    """من قائمة حزم، استخرج متجه ميزات إحصائي."""
    feats = []
    for ch in CHANNELS:
        vals = [float(s.get(ch, 0)) for s in samples]
        if not vals:
            feats.extend([0.0] * 7)
            continue

        n = len(vals)
        mean = sum(vals) / n
        var = sum((v - mean) ** 2 for v in vals) / n
        std = var ** 0.5
        vmin = min(vals)
        vmax = max(vals)

        feats.extend([
            mean,
            std,
            vmin,
            vmax,
            vmax - vmin,
            vals[0],
            vals[-1],
        ])
    return feats


def load_all_samples():
    """يقرأ كل ملفات CSV ويستخرج الميزات."""
    X, y = [], []
    if not DATA_DIR.exists():
        return X, y

    for d in sorted(DATA_DIR.iterdir()):
        if not d.is_dir():
            continue
        label = d.name
        for f in sorted(d.glob('*.csv')):
            try:
                rows = []
                with open(f, 'r', encoding='utf-8') as fh:
                    reader = csv.DictReader(fh)
                    for row in reader:
                        rows.append(row)
                if len(rows) < 3:
                    continue
                feats = extract_features(rows)
                X.append(feats)
                y.append(label)
            except Exception as e:
                print(f'[load] {f}: {e}', flush=True)

    return X, y


# ═══════════════════════════════════════════════════════════
# التدريب
# ═══════════════════════════════════════════════════════════
def train_model(n_estimators: int, max_depth, test_size: float) -> dict:
    """يدرّب نموذج ويحفظه. يرجع dict بالنتائج."""
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score
    except ImportError:
        return {'error': 'مكتبة scikit-learn غير مثبتة. نفّذ: pip install scikit-learn'}

    X, y = load_all_samples()

    if len(X) < 4:
        return {'error': f'عدد العينات قليل ({len(X)}). اجمع 4 على الأقل.'}

    classes = sorted(set(y))
    if len(classes) < 2:
        return {'error': f'تحتاج حركتين على الأقل. لديك: {classes}'}

    from collections import Counter
    counts = Counter(y)
    min_count = min(counts.values())
    if min_count < 2:
        return {'error': f'كل حركة تحتاج عينتين على الأقل. {dict(counts)}'}

    try:
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y,
        )
    except ValueError:
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=test_size, random_state=42,
        )

    clf = RandomForestClassifier(
        n_estimators=int(n_estimators),
        max_depth=(int(max_depth) if max_depth else None),
        random_state=42,
        n_jobs=-1,
    )
    clf.fit(X_tr, y_tr)
    y_pred = clf.predict(X_te)
    acc = float(accuracy_score(y_te, y_pred))

    bundle = {
        'model':      clf,
        'classes':    list(clf.classes_),
        'acc':        acc,
        'trained_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'n_train':    len(X_tr),
        'n_test':     len(X_te),
        'features':   len(X[0]) if X else 0,
    }
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(bundle, f)

    return {
        'acc':      acc,
        'n_train':  len(X_tr),
        'n_test':   len(X_te),
        'classes':  list(clf.classes_),
        'features': len(X[0]) if X else 0,
    }


def load_model():
    """يحمّل النموذج المحفوظ."""
    if not MODEL_PATH.exists():
        return None
    try:
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f'[model] {e}', flush=True)
        return None


# ═══════════════════════════════════════════════════════════
# الواجهة
# ═══════════════════════════════════════════════════════════
def build() -> dict:
    refs = {}
    st = {
        'recording':  False,
        'predicting': False,
    }
    refs['st'] = st

    ui.label('02').classes('page-number')
    ui.label(TITLE).classes('page-title')
    ui.element('div').classes('divider')
    ui.label(DESC).classes('hint-box')

    # ═══════════════════════════════════════════════════════
    # شريط حالة الاتصال
    # ═══════════════════════════════════════════════════════
    with ui.element('div').classes('ai-status'):
        with ui.element('div').classes('ai-status-row'):
            ui.icon('sensors').classes('ai-status-icon')
            ui.label('اتصال الحساسات').classes('ai-status-label')
            refs['conn_dot'] = ui.element('div').classes('mqtt-dot wait')
            refs['conn_lbl'] = ui.label('جارٍ الاتصال...').classes('ai-status-value')

    # ═══════════════════════════════════════════════════════
    # 1) جمع البيانات
    # ═══════════════════════════════════════════════════════
    with ui.element('div').classes('ai-section'):
        with ui.element('div').classes('ai-section-head'):
            ui.label('1 · جمع البيانات').classes('ai-section-title')
            ui.label('Record').classes('ai-section-tag')

        with ui.element('div').classes('ai-form'):
            with ui.element('div').classes('ai-field'):
                ui.label('اسم الحركة (الكلمة)').classes('ai-label')
                label_input = ui.input(placeholder='مثال: شكراً، نعم، مرحباً...') \
                    .props('borderless').classes('ai-input')

            with ui.element('div').classes('ai-field-row'):
                with ui.element('div').classes('ai-number-wrap'):
                    ui.label('المدة').classes('ai-label')
                    dur_in = ui.number(value=3.0, min=0.5, max=60, step=0.5,
                                       format='%.1f').props('borderless dense') \
                        .classes('ai-number')
                    ui.label('ث').classes('ai-unit')

                with ui.element('div').classes('ai-number-wrap'):
                    ui.label('التكرارات').classes('ai-label')
                    rep_in = ui.number(value=5, min=1, max=100, step=1,
                                       format='%d').props('borderless dense') \
                        .classes('ai-number')
                    ui.label('مرة').classes('ai-unit')

            # زر التسجيل
            with ui.element('div').classes('ai-actions-row'):
                rec_btn = ui.button('بدء التسجيل',
                                    icon='fiber_manual_record') \
                    .props('flat no-caps').classes('ai-rec-btn')
                rec_status = ui.label('').classes('ai-rec-status')

            async def start_recording():
                label = (label_input.value or '').strip()
                if not label:
                    ui.notify('اكتب اسم الحركة أولاً', type='negative')
                    return
                if st['recording']:
                    return
                if not mqtt_client.STATE.get('connected'):
                    ui.notify('MQTT غير متصل', type='negative')
                    return

                duration = float(dur_in.value or 3.0)
                repeats  = int(rep_in.value or 5)

                if duration < 0.5:
                    ui.notify('المدة يجب أن تكون 0.5 ثانية على الأقل', type='warning')
                    return
                if repeats < 1:
                    ui.notify('عدد التكرارات 1 على الأقل', type='warning')
                    return

                st['recording'] = True
                rec_btn.disable()
                rec_status.text = 'جارٍ التسجيل...'
                rec_status.classes(add='rec-active')

                try:
                    for i in range(repeats):
                        rec_status.text = f'جمع العينة {i+1}/{repeats}...'
                        samples = []
                        t0 = time.time()
                        while time.time() - t0 < duration:
                            latest = mqtt_client.STATE.get('latest')
                            if latest:
                                samples.append(dict(latest))
                            await asyncio.sleep(0.05)

                        if len(samples) >= 3:
                            save_sample(label, samples)

                        if i < repeats - 1:
                            rec_status.text = f'انتظر... {i+1}/{repeats}'
                            await asyncio.sleep(0.8)

                    rec_status.text = f'✅ حُفظت {repeats} عينة لـ «{label}»'
                    rec_status.classes(add='ok')
                    ui.notify(f'حُفظت {repeats} عينة لـ «{label}»',
                              type='positive', position='top')
                    label_input.value = ''
                    gestures_view.refresh()

                except Exception as e:
                    rec_status.text = f'خطأ: {e}'
                    rec_status.classes(add='err')
                    print(f'[record] {e}', flush=True)

                finally:
                    st['recording'] = False
                    rec_btn.enable()
                    rec_status.classes(remove='rec-active')

            rec_btn.on_click(start_recording)

    # ═══════════════════════════════════════════════════════
    # 2) الحركات المسجلة
    # ═══════════════════════════════════════════════════════
    with ui.element('div').classes('ai-section'):
        with ui.element('div').classes('ai-section-head'):
            ui.label('2 · الحركات المسجلة').classes('ai-section-title')
            ui.label('Dataset').classes('ai-section-tag')

        @ui.refreshable
        def gestures_view():
            gestures = list_gestures()
            if not gestures:
                with ui.column().classes('ai-empty'):
                    ui.icon('inbox').classes('ai-empty-icon')
                    ui.label('لا توجد بيانات بعد').classes('ai-empty-title')
                    ui.label('سجّل حركتك الأولى أعلاه').classes('ai-empty-hint')
                return

            total = sum(gestures.values())
            with ui.element('div').classes('ai-stats'):
                ui.label(f'{len(gestures)} حركة · {total} عينة') \
                    .classes('ai-stats-text')

            for label, count in gestures.items():
                with ui.element('div').classes('ai-gesture-row'):
                    ui.icon('gesture').classes('ai-gesture-icon')
                    ui.label(label).classes('ai-gesture-name')
                    ui.label(f'{count}').classes('ai-gesture-count')

                    def make_del(l=label):
                        def _del():
                            n = delete_gesture(l)
                            ui.notify(f'حُذف {n} عينة',
                                      type='warning', position='top')
                            gestures_view.refresh()
                        return _del

                    ui.button(icon='delete', on_click=make_del()) \
                        .props('flat dense round size=sm') \
                        .classes('ai-gesture-del')

        gestures_view()

    # ═══════════════════════════════════════════════════════
    # 3) التدريب
    # ═══════════════════════════════════════════════════════
    with ui.element('div').classes('ai-section'):
        with ui.element('div').classes('ai-section-head'):
            ui.label('3 · تدريب النموذج').classes('ai-section-title')
            ui.label('Train').classes('ai-section-tag')

        with ui.element('div').classes('ai-field-row'):
            with ui.element('div').classes('ai-number-wrap'):
                ui.label('الأشجار').classes('ai-label')
                n_est = ui.number(value=100, min=10, max=1000, step=10,
                                  format='%d').props('borderless dense') \
                    .classes('ai-number')
                ui.label('شجرة').classes('ai-unit')

            with ui.element('div').classes('ai-number-wrap'):
                ui.label('العمق').classes('ai-label')
                depth_in = ui.number(value=0, min=0, max=100, step=1,
                                     format='%d').props('borderless dense') \
                    .classes('ai-number')
                ui.label('0=لا حد').classes('ai-unit')

            with ui.element('div').classes('ai-number-wrap'):
                ui.label('الاختبار').classes('ai-label')
                test_in = ui.number(value=0.2, min=0.05, max=0.5, step=0.05,
                                    format='%.2f').props('borderless dense') \
                    .classes('ai-number')
                ui.label('0-1').classes('ai-unit')

        with ui.element('div').classes('ai-actions-row'):
            train_btn = ui.button('تدريب النموذج', icon='school') \
                .props('flat no-caps').classes('ai-train-btn')
            train_status = ui.label('').classes('ai-train-status')

            def do_train():
                train_btn.disable()
                train_status.text = 'جارٍ التدريب...'
                train_status.classes(remove='ok err')
                try:
                    depth = int(depth_in.value or 0)
                    result = train_model(
                        int(n_est.value or 100),
                        depth if depth > 0 else None,
                        float(test_in.value or 0.2),
                    )
                    if 'error' in result:
                        train_status.text = f'❌ {result["error"]}'
                        train_status.classes(add='err')
                        ui.notify(result['error'], type='negative', position='top')
                    else:
                        acc_pct = result['acc'] * 100
                        train_status.text = (
                            f'✅ {acc_pct:.1f}% · تدريب {result["n_train"]} · '
                            f'اختبار {result["n_test"]} · '
                            f'{len(result["classes"])} فئات'
                        )
                        train_status.classes(add='ok')
                        ui.notify(f'اكتمل — دقة {acc_pct:.1f}%',
                                  type='positive', position='top')
                        bundle = load_model()
                        if bundle:
                            live_status.text = (
                                f'النموذج جاهز · دقة {bundle["acc"]*100:.1f}% · '
                                f'فئات: {", ".join(bundle["classes"])}'
                            )
                except Exception as e:
                    train_status.text = f'❌ خطأ: {e}'
                    train_status.classes(add='err')
                    print(f'[train] {e}', flush=True)
                finally:
                    train_btn.enable()

            train_btn.on_click(do_train)

    # ═══════════════════════════════════════════════════════
    # 4) التنبؤ الحيّ
    # ═══════════════════════════════════════════════════════
    with ui.element('div').classes('ai-section'):
        with ui.element('div').classes('ai-section-head'):
            ui.label('4 · التنبؤ الحيّ').classes('ai-section-title')
            ui.label('Live').classes('ai-section-tag')

        with ui.element('div').classes('ai-live'):
            pred_lbl = ui.label('—').classes('ai-live-pred')

            with ui.element('div').classes('ai-live-actions'):
                live_btn = ui.button('بدء المراقبة', icon='play_arrow') \
                    .props('flat no-caps').classes('ai-live-btn')

                ui.button('نطق مجدداً', icon='volume_up',
                          on_click=lambda: audio.speak(pred_lbl.text)
                            if pred_lbl.text and pred_lbl.text != '—' else None) \
                    .props('flat no-caps').classes('ai-live-btn-2')

                ui.button('إيقاف', icon='stop',
                          on_click=lambda: st.update(predicting=False)) \
                    .props('flat no-caps').classes('ai-live-btn-2')

            live_status = ui.label('').classes('ai-live-status')

        async def prediction_loop():
            bundle = load_model()
            if not bundle:
                live_status.text = 'لا يوجد نموذج مدرب'
                return

            model = bundle['model']
            window = 1.2
            last_pred = None
            last_time = 0.0

            while st['predicting']:
                samples = []
                t0 = time.time()
                while time.time() - t0 < window and st['predicting']:
                    latest = mqtt_client.STATE.get('latest')
                    if latest:
                        samples.append(dict(latest))
                    await asyncio.sleep(0.05)

                if len(samples) < 3:
                    continue

                try:
                    feats = extract_features(samples)
                    pred = model.predict([feats])[0]
                    try:
                        prob = max(model.predict_proba([feats])[0])
                    except Exception:
                        prob = 0.0

                    pred_lbl.text = str(pred)

                    now = time.time()
                    if pred != last_pred or (now - last_time) > 4.0:
                        audio.speak_prediction(str(pred))
                        last_pred = pred
                        last_time = now

                    live_status.text = (
                        f'ثقة: {prob*100:.0f}% · {len(samples)} عينة'
                    )

                except Exception as e:
                    live_status.text = f'خطأ: {e}'
                    print(f'[predict] {e}', flush=True)
                    await asyncio.sleep(0.5)

        async def start_prediction():
            if st['predicting']:
                return
            if not load_model():
                ui.notify('درّب النموذج أولاً', type='warning', position='top')
                return
            st['predicting'] = True
            live_btn.disable()
            live_status.text = 'جارٍ المراقبة...'
            try:
                await prediction_loop()
            finally:
                st['predicting'] = False
                live_btn.enable()
                live_status.text = 'متوقف'

        live_btn.on_click(start_prediction)

    # تهيئة
    bundle = load_model()
    if bundle:
        live_status.text = (
            f'النموذج جاهز · دقة {bundle["acc"]*100:.1f}% · '
            f'فئات: {", ".join(bundle["classes"])}'
        )

    return refs


# ═══════════════════════════════════════════════════════════
# التحديث الدوري
# ═══════════════════════════════════════════════════════════
async def refresh(refs):
    if not refs:
        return
    try:
        s = mqtt_client.STATE
        dot = refs.get('conn_dot')
        if dot is not None:
            dot.classes(remove='on off wait warn')
            if s.get('connected'):
                dot.classes(add='on')
                refs['conn_lbl'].text = f'متصل · {s.get("total", 0)} حزمة'
            elif 'فشل' in s.get('reason', '') or 'انقطع' in s.get('reason', ''):
                dot.classes(add='off')
                refs['conn_lbl'].text = s.get('reason', 'غير متصل')
            else:
                dot.classes(add='wait')
                refs['conn_lbl'].text = s.get('reason', 'جارٍ الاتصال...')
    except Exception as e:
        print(f'[ai refresh] {e}', flush=True)


def on_enter():
    pass