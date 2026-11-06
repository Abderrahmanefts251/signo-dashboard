# simulator.py
# محاكي ESP32 - يرسل بيانات وهمية إلى MQTT
import time
import json
import random
import math
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
TOPIC = "signo_v1_morocco_fattasse_2026"

# إعداد الاتصال
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, 1883, 60)
client.loop_start()

print("🚀 بدء المحاكي... (اضغط Ctrl+C للإيقاف)")
print("يرسل البيانات إلى:", TOPIC)

t = 0
try:
    while True:
        # 1. محاكاة الأصابع (تفتح وتغلق ببطء)
        # نستخدم دالة الموجة (sin) لجعل الحركة سلسة وطبيعية
        wave = (math.sin(t / 5) + 1) / 2  # تتراوح بين 0 و 1
        
        # القيم تتراوح بين 1750 (مفتوح) و 2150 (مغلق)
        base_flex = 1750 + (wave * 400)
        
        # نضيف اهتزاز بسيط لكل إصبع ليكونوا مختلفين قليلاً
        flex1 = int(base_flex + random.randint(-20, 20))
        flex2 = int(base_flex + random.randint(-20, 20))
        flex3 = int(base_flex + random.randint(-20, 20))
        flex4 = int(base_flex + random.randint(-20, 20))
        flex5 = int(base_flex + random.randint(-20, 20))

        # 2. محاكاة الحركة (Gyro & Accel)
        gx = round(random.uniform(-5, 5) + (wave * 20), 2)
        gy = round(random.uniform(-5, 5), 2)
        gz = round(random.uniform(-5, 5), 2)
        
        ax = round(random.uniform(-0.2, 0.2) + (wave * 0.5), 3)
        ay = round(random.uniform(-0.2, 0.2), 3)
        az = round(1.0 + random.uniform(-0.1, 0.1), 3) # الجاذبية

        # 3. تجهيز الحزمة
        payload = {
            "time": int(time.time() * 1000),
            "flex1": flex1,
            "flex2": flex2,
            "flex3": flex3,
            "flex4": flex4,
            "flex5": flex5,
            "ax": ax, "ay": ay, "az": az,
            "gx": gx, "gy": gy, "gz": gz
        }

        # 4. الإرسال
        client.publish(TOPIC, json.dumps(payload))
        
        # طباعة في الطرفية كل 10 حزم
        if t % 10 == 0:
            print(f"📨 إرسال: flex1={flex1} | gx={gx}")
        
        t += 1
        time.sleep(0.1) # إرسال 10 مرات في الثانية

except KeyboardInterrupt:
    print("\n🛑 تم إيقاف المحاكي.")
    client.loop_stop()
    client.disconnect()