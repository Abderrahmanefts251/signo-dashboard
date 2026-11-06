# ==========================================
# SIGNO V2 - ESP32-S3 DATA COLLECTION
# MicroPython / Thonny
# ==========================================

import network
import time
import json
from machine import Pin, ADC, I2C
from umqtt.simple import MQTTClient

# ==========================================
# 1. إعدادات Wi-Fi و MQTT
# ==========================================
WIFI_SSID = "اسم_شبكتك_هنا"        # ← غيّر هذا
WIFI_PASSWORD = "كلمة_السر_هنا"    # ← غيّر هذا

MQTT_HOST   = "broker.hivemq.com"
MQTT_PORT   = 1883
MQTT_TOPIC  = b"signo_v1_morocco_fattasse_2026"
MQTT_CLIENT = b"signo_glove_01"

SEND_INTERVAL_MS = 100  # إرسال 10 حزم في الثانية

# ==========================================
# 2. إعداد حساسات الانحناء (Flex)
# ==========================================
flex_thumb  = ADC(Pin(9))
flex_index  = ADC(Pin(4))
flex_middle = ADC(Pin(3))
flex_ring   = ADC(Pin(2))
flex_pinky  = ADC(Pin(1))

flex_sensors = [flex_thumb, flex_index, flex_middle, flex_ring, flex_pinky]

for sensor in flex_sensors:
    sensor.atten(ADC.ATTN_11DB) # قراءة حتى 3.3V
    sensor.width(ADC.WIDTH_12BIT) # نطاق 0-4095

# دالة لجلب متوسط 5 قراءات لتقليل الاهتزاز
def read_flex(adc_sensor):
    total = 0
    for _ in range(5):
        total += adc_sensor.read()
        time.sleep_ms(2)
    return total // 5

# ==========================================
# 3. إعداد MPU6050
# ==========================================
i2c = I2C(0, scl=Pin(6), sda=Pin(5), freq=400000)
MPU_ADDR = 0x68

# إيقاظ الحساس وإعداد الحساسية
i2c.writeto_mem(MPU_ADDR, 0x6B, b"\x00")
i2c.writeto_mem(MPU_ADDR, 0x1C, b"\x00") # +/- 2g
i2c.writeto_mem(MPU_ADDR, 0x1B, b"\x00") # +/- 250 deg/s
time.sleep_ms(100)

def to_signed(val):
    if val > 32767: val -= 65536
    return val

def read_mpu6050():
    data = i2c.readfrom_mem(MPU_ADDR, 0x3B, 14)
    
    ax = to_signed(int.from_bytes(data[0:2], "big")) / 16384.0
    ay = to_signed(int.from_bytes(data[2:4], "big")) / 16384.0
    az = to_signed(int.from_bytes(data[4:6], "big")) / 16384.0
    
    gx = to_signed(int.from_bytes(data[8:10], "big")) / 131.0
    gy = to_signed(int.from_bytes(data[10:12], "big")) / 131.0
    gz = to_signed(int.from_bytes(data[12:14], "big")) / 131.0
    
    return ax, ay, az, gx, gy, gz

# ==========================================
# 4. الاتصال بـ Wi-Fi
# ==========================================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        return wlan

    print(f"[WiFi] جاري الاتصال بـ {WIFI_SSID}...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    timeout = 20
    while not wlan.isconnected() and timeout > 0:
        print(".", end="")
        time.sleep(1)
        timeout -= 1
        
    if not wlan.isconnected():
        raise RuntimeError("[WiFi] فشل الاتصال! تحقق من الاسم وكلمة السر.")
        
    print(f"\n[WiFi] ✅ متصل · IP: {wlan.ifconfig()[0]}")
    return wlan

# ==========================================
# 5. الاتصال بـ MQTT
# ==========================================
def connect_mqtt():
    print(f"[MQTT] جاري الاتصال بـ {MQTT_HOST}...")
    client = MQTTClient(MQTT_CLIENT, MQTT_HOST, port=MQTT_PORT, keepalive=60)
    try:
        client.connect()
        print(f"[MQTT] ✅ متصل · الموضوع: {MQTT_TOPIC.decode()}")
        return client
    except Exception as e:
        print(f"[MQTT] ❌ فشل: {e}")
        return None

# ==========================================
# 6. البرنامج الرئيسي
# ==========================================
print("\n" + "═"*55)
print("  🧤 SIGNO Glove · ESP32-S3")
print("═"*55)

connect_wifi()
mqtt_client = connect_mqtt()

print("\n" + "─"*55)
print("  بدء إرسال القيم... (أوقف بـ Ctrl+C في Thonny)")
print("─"*55)

last_send = 0
count = 0

while True:
    try:
        now = time.ticks_ms()
        
        # التحقق من وقت الإرسال (كل 100ms)
        if time.ticks_diff(now, last_send) < SEND_INTERVAL_MS:
            time.sleep_ms(10)
            continue
            
        last_send = now
        count += 1

        # 1. قراءة الأصابع (بالمتوسط)
        f_thumb  = read_flex(flex_thumb)
        f_index  = read_flex(flex_index)
        f_middle = read_flex(flex_middle)
        f_ring   = read_flex(flex_ring)
        f_pinky  = read_flex(flex_pinky)

        # 2. قراءة الحركة
        ax, ay, az, gx, gy, gz = read_mpu6050()

        # 3. بناء حزمة JSON (مطابقة للموقع)
        payload = json.dumps({
            "time":  now,
            "flex1": f_index,   # السبابة
            "flex2": f_middle,  # الوسطى
            "flex3": f_ring,    # البنصر
            "flex4": f_pinky,   # الخنصر
            "flex5": f_thumb,   # الإبهام
            "ax": round(ax, 3), "ay": round(ay, 3), "az": round(az, 3),
            "gx": round(gx, 2), "gy": round(gy, 2), "gz": round(gz, 2),
        })

        # 4. الإرسال
        if mqtt_client:
            try:
                mqtt_client.ping() # الحفاظ على الاتصال
                mqtt_client.publish(MQTT_TOPIC, payload)
                
                # طباعة كل 10 حزم (كل ثانية) لعدم إغراق الشاشة
                if count % 10 == 0:
                    print(f"[{count:04d}] I:{f_index} M:{f_middle} R:{f_ring} P:{f_pinky} T:{f_thumb} | ax:{ax:+.2f} gx:{gx:+.1f}")
                    
            except Exception as e:
                print(f"\n[MQTT] ⚠️ انقطع الاتصال: {e}")
                mqtt_client = connect_mqtt() # إعادة الاتصال

        time.sleep_ms(10)

    except KeyboardInterrupt:
        print("\n⏹️ تم الإيقاف بواسطة المستخدم.")
        break
    except Exception as e:
        print(f"\n[خطأ] {e}")
        time.sleep(1)