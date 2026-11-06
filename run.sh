#!/bin/bash
# ═══════════════════════════════════════════════════════════
# SIGNO · تشغيل الموقع مع Cloudflare Tunnel
# الاستخدام: ./run.sh
# ═══════════════════════════════════════════════════════════

cd "$(dirname "$0")" || exit 1

# ─── الألوان ───
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ─── 1) إيقاف النسخ القديمة ───
echo -e "${BLUE}🔧 تنظيف النسخ القديمة...${NC}"
pkill -f "python app.py" 2>/dev/null
pkill -f "cloudflared tunnel" 2>/dev/null
sleep 1

# ─── 2) تفعيل البيئة ───
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo -e "${RED}❌ لم أجد مجلد venv${NC}"
    exit 1
fi

# ─── 3) التحقق من cloudflared ───
if [ -x "./cloudflared" ]; then
    CF="./cloudflared"
elif command -v cloudflared >/dev/null 2>&1; then
    CF="cloudflared"
else
    echo -e "${RED}❌ cloudflared غير موجود${NC}"
    echo ""
    echo -e "${YELLOW}ثبته بأمر واحد:${NC}"
    echo "  wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared"
    echo "  chmod +x cloudflared"
    exit 1
fi

# ─── 4) الإعدادات ───
export PORT=${PORT:-7860}
export HOST="0.0.0.0"
export TUNNEL=""    # النفق يديره run.sh

echo ""
echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo -e "${GREEN}  🧤 SIGNO · Smart Sign Glove Dashboard${NC}"
echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo -e "  📍 محلياً : ${BLUE}http://localhost:$PORT${NC}"
echo -e "  🚇 النفق  : ${YELLOW}Cloudflare${NC}"
echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo ""

# ─── 5) تشغيل app.py في الخلفية ───
echo -e "${BLUE}🚀 بدء تشغيل الموقع...${NC}"
python app.py &
APP_PID=$!
sleep 3

if ! kill -0 $APP_PID 2>/dev/null; then
    echo -e "${RED}❌ فشل تشغيل app.py${NC}"
    exit 1
fi

# ─── 6) تنظيف عند الإيقاف ───
cleanup() {
    echo ""
    echo -e "${YELLOW}⏹️  إيقاف الموقع والنفق...${NC}"
    kill $APP_PID 2>/dev/null
    pkill -f "cloudflared tunnel" 2>/dev/null
    sleep 1
    echo -e "${GREEN}✅ تم الإيقاف.${NC}"
    exit 0
}
trap cleanup INT TERM

# ─── 7) تشغيل Cloudflare Tunnel ───
echo ""
echo -e "${BLUE}🌍 جاري إنشاء الرابط العام...${NC}"
echo -e "${YELLOW}(انتظر 5-10 ثوانٍ — سيظهر الرابط في صندوق أدناه)${NC}"
echo ""

$CF tunnel --url "http://localhost:$PORT" --no-autoupdate