# -*- coding: utf-8 -*-
import os
import random
from flask import Flask
from threading import Thread
import telebot
from telebot import types

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Running"

@app.route('/health')
def health():
    return "OK", 200

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "7145036494"))

FORCE_CHANNEL = "pkwbiwjwbekeekkw"
FORCE_LINK = "https://t.me/pkwbiwjwbekeekkw"

bot = telebot.TeleBot(TOKEN, threaded=False)
os.makedirs("database", exist_ok=True)

def get_points(uid):
    try:
        with open(f"database/{uid}.txt","r",encoding="utf-8") as f:
            return int(f.read().strip() or 0)
    except:
        return 0

def add_points(uid, n):
    with open(f"database/{uid}.txt","w",encoding="utf-8") as f:
        f.write(str(get_points(uid)+n))

def is_sub(uid):
    try:
        s = bot.get_chat_member(f"@{FORCE_CHANNEL}", uid).status
        return s in ['member','administrator','creator']
    except:
        return True

def sub_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("اشترك هنا", url=FORCE_LINK))
    kb.add(types.InlineKeyboardButton("تحققت", callback_data="check"))
    return kb

PRICES = {
"design":5,"filter":5,"text":5,"hd":5,"logo":10,"card":10,"banner":10,"poster":10,"qr":5,"cv":10,
"email1":5,"email2":5,"email3":5,"email4":5,"email5":15,"email6":10,
"charge":5,"track":5,"coupon":5,"invoice":5,
"daman1":5,"daman2":5,"daman3":5,"daman4":5,"daman5":5,"daman6":5,
"follow":15,"like":15,"view":15,"member":15,
"unban":15,"num":15,"usnum":25,"whats":15,
"ad1":20,"ad2":30,"ad3":50,"ad4":100
}

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    if not is_sub(uid):
        bot.send_message(uid, f"اشترك اولا\n{FORCE_LINK}", reply_markup=sub_kb())
        return
    pts = get_points(uid)
    kb = types.InlineKeyboardMarkup(row_width=2)

    kb.add(types.InlineKeyboardButton("قناتنا", url=FORCE_LINK))
    
    kb.add(types.InlineKeyboardButton("--- ضمان ---", callback_data="no"))
    kb.add(types.InlineKeyboardButton("ضمان متجر", callback_data="daman1"), types.InlineKeyboardButton("ضمان حساب", callback_data="daman2"))
    kb.add(types.InlineKeyboardButton("ضمان ارقام", callback_data="daman3"), types.InlineKeyboardButton("ضمان ايميل", callback_data="daman4"))
    kb.add(types.InlineKeyboardButton("ضمان شحن", callback_data="daman5"), types.InlineKeyboardButton("ضمان متابعين", callback_data="daman6"))

    kb.add(types.InlineKeyboardButton("--- ايميل ---", callback_data="no"))
    kb.add(types.InlineKeyboardButton("ايميل وهمي 5", callback_data="email1"), types.InlineKeyboardButton("تفعيل 5", callback_data="email2"))
    kb.add(types.InlineKeyboardButton("كود 5", callback_data="email3"), types.InlineKeyboardButton("10 دقايق 5", callback_data="email4"))
    kb.add(types.InlineKeyboardButton("دائم 15", callback_data="email5"), types.InlineKeyboardButton("مشفر 10", callback_data="email6"))

    kb.add(types.InlineKeyboardButton("--- شحن ---", callback_data="no"))
    kb.add(types.InlineKeyboardButton("شحن 5", callback_data="charge"), types.InlineKeyboardButton("تتبع 5", callback_data="track"))
    kb.add(types.InlineKeyboardButton("خصم 5", callback_data="coupon"), types.InlineKeyboardButton("فاتورة 5", callback_data="invoice"))

    kb.add(types.InlineKeyboardButton("--- زيده ---", callback_data="no"))
    kb.add(types.InlineKeyboardButton("متابعين 15", callback_data="follow"), types.InlineKeyboardButton("لايكات 15", callback_data="like"))
    kb.add(types.InlineKeyboardButton("مشاهدات 15", callback_data="view"), types.InlineKeyboardButton("اعضاء 15", callback_data="member"))

    kb.add(types.InlineKeyboardButton("--- تفعيل ---", callback_data="no"))
    kb.add(types.InlineKeyboardButton("فك حظر 15", callback_data="unban"), types.InlineKeyboardButton("رقم وهمي 15", callback_data="num"))
    kb.add(types.InlineKeyboardButton("امريكي 25", callback_data="usnum"), types.InlineKeyboardButton("واتس 15", callback_data="whats"))

    kb.add(types.InlineKeyboardButton("--- تصميم ---", callback_data="no"))
    kb.add(types.InlineKeyboardButton("تصميم 5", callback_data="design"), types.InlineKeyboardButton("فلتر 5", callback_data="filter"))
    kb.add(types.InlineKeyboardButton("كتابة 5", callback_data="text"), types.InlineKeyboardButton("جودة 5", callback_data="hd"))
    kb.add(types.InlineKeyboardButton("لوجو 10", callback_data="logo"), types.InlineKeyboardButton("بطاقة 10", callback_data="card"))
    kb.add(types.InlineKeyboardButton("بانر 10", callback_data="banner"), types.InlineKeyboardButton("بوستر 10", callback_data="poster"))
    kb.add(types.InlineKeyboardButton("سيفي 10", callback_data="cv"), types.InlineKeyboardButton("QR 5", callback_data="qr"))

    kb.add(types.InlineKeyboardButton("--- اعلان ---", callback_data="no"))
    kb.add(types.InlineKeyboardButton("نشر 20", callback_data="ad1"), types.InlineKeyboardButton("تثبيت 30", callback_data="ad2"))
    kb.add(types.InlineKeyboardButton("ممول 50", callback_data="ad3"), types.InlineKeyboardButton("بث 100", callback_data="ad4"))

    kb.add(types.InlineKeyboardButton(f"رصيدك {pts}", callback_data="bal"))
    kb.add(types.InlineKeyboardButton("شراء نقاط", callback_data="buy"))

    bot.send_message(uid, f"متجر زيده - 40 زر\nرصيدك {pts}\nكل شي تلقائي\n{FORCE_LINK}", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    try:
        uid = c.from_user.id
        chat = c.message.chat.id
        data = c.data

        if data == "check":
            if is_sub(uid):
                bot.answer_callback_query(c.id, "تم")
                try: bot.delete_message(chat, c.message.message_id)
                except: pass
                start(c.message)
            else:
                bot.answer_callback_query(c.id, "ما اشتركت", show_alert=True)
            return

        if data == "no":
            bot.answer_callback_query(c.id)
            return

        bot.answer_callback_query(c.id)

        if not is_sub(uid):
            bot.send_message(chat, f"اشترك\n{FORCE_LINK}", reply_markup=sub_kb())
            return

        if data == "buy":
            bot.send_message(chat, f"شراء نقاط\n5=1000 ريال\n15=2500\n30=5000\nالكريمي: [حط رقمك]\nايدك: {uid}\nارسل الاثبات")
            return

        if data == "bal":
            bot.send_message(chat, f"رصيدك {get_points(uid)}")
            return

        price = PRICES.get(data, 5)
        if get_points(uid) < price:
            bot.send_message(chat, f"تحتاج {price} رصيدك {get_points(uid)}")
            return

        add_points(uid, -price)
        
        responses = {
            "design": f"تم التصميم\nالنص: متجر زيده\n{FORCE_LINK}",
            "filter": "تم الفلتر - صورة محسنة",
            "text": "تمت الكتابة على الصورة",
            "hd": "تم تحسين الجودة",
            "logo": "تم تصميم اللوجو",
            "card": "تم تصميم البطاقة",
            "banner": "تم تصميم البانر",
            "poster": "تم تصميم البوستر",
            "qr": f"تم QR\n{FORCE_LINK}",
            "cv": "تم السيفي",
            "email1": f"ايميل: {random.randint(1000,9999)}@tempmail.com\nباس: {random.randint(100000,999999)}",
            "email2": f"تفعيل: user{random.randint(100,999)}@gmail.com\nكود: {random.randint(100000,999999)}",
            "email3": f"كود: {random.randint(100000,999999)}",
            "email4": f"ايميل: {random.randint(1000,9999)}@10min.com",
            "email5": f"دائم: store{random.randint(100,999)}@gmail.com",
            "email6": f"مشفر: {random.randint(1000,9999)}@protonmail.com",
            "charge": "تم شحن 10$",
            "track": f"تتبع: TRK{random.randint(10000000,99999999)} - في الطريق",
            "coupon": f"كود خصم: ZAYDA{random.randint(10,99)} - 20%",
            "invoice": f"فاتورة: INV{random.randint(1000,9999)} مدفوعة",
            "daman1": f"ضمان متجر\nذهبي 7 ايام\n{FORCE_LINK}",
            "daman2": f"ضمان حساب\n3 ايام\n{FORCE_LINK}",
            "daman3": f"ضمان ارقام\nنظيف\n{FORCE_LINK}",
            "daman4": f"ضمان ايميل\nشغال\n{FORCE_LINK}",
            "daman5": f"ضمان شحن\nسريع\n{FORCE_LINK}",
            "daman6": f"ضمان متابعين\n30 يوم\n{FORCE_LINK}",
            "follow": "تم 1000 متابع - بدأ التنفيذ",
            "like": "تم 500 لايك - بدأ",
            "view": "تم 1000 مشاهدة",
            "member": "تم 200 عضو",
            "unban": "تم فك الحظر",
            "num": f"رقم: +1{random.randint(1000000000,9999999999)}\nكود: {random.randint(100000,999999)}",
            "usnum": f"امريكي: +1{random.randint(1000000000,9999999999)}",
            "whats": f"واتس كود: {random.randint(100000,999999)}",
            "ad1": f"تم النشر\n{FORCE_LINK}",
            "ad2": f"تم التثبيت\n{FORCE_LINK}",
            "ad3": "تم الممول - يبدأ خلال ساعة",
            "ad4": "تم البث للكل - 1000 مشترك"
        }

        txt = responses.get(data, f"تم {data}")
        bot.send_message(chat, f"{txt}\n\nخصم {price} - رصيدك {get_points(uid)}\n/start")
        
    except Exception as e:
        print(f"Error: {e}")
        try:
            bot.send_message(c.message.chat.id, "حصل خطأ بسيط جرب /start")
        except:
            pass

@bot.message_handler(commands=['add'])
def add(m):
    if m.from_user.id != ADMIN_ID:
        return
    try:
        _, uid, pts = m.text.split()
        add_points(int(uid), int(pts))
        bot.send_message(int(uid), f"تم شحن {pts} - رصيدك {get_points(int(uid))}")
        bot.send_message(m.chat.id, "تم")
    except Exception as e:
        bot.send_message(m.chat.id, f"خطأ: {e}")

def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Polling error: {e}")

if __name__ == "__main__":
    Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, threaded=True)