import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
import random

# Tokeningiz
TOKEN = "8557905355:AAFWyRPx2tz0s0I9Bxlq6QcsGOM1wyGTotY"
bot = telebot.TeleBot(TOKEN)

# Kanal username
CHANNEL = "https://youtube.com/shorts/DCuFCv4XR0A?si=TqiHxKSL_D6SBt_D"  # o'zingizning kanal nomingizni yozing

# Havolalar
LINK_UC = "https://t.me/tangaz_bot/app?startapp=r_5995516854"
LINK_PUL = "https://t.me/lemon_casher_bot/LEMONCASH/?startapp=r_Mo0yxYlz2bQDZAm"

# Foydalanuvchi holati
user_states = {}

# /start komandasi
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        f"👋 Salom, {message.from_user.first_name}!\n\n"
        f"Botdan foydalanish uchun avval shu shortsdagi {CHANNEL} kanaliga a’zo bo‘ling va 📸 *screenshot* yuboring.",
        parse_mode="Markdown"
    )
    user_states[message.chat.id] = "waiting_for_screenshot"

# Screenshot yuborilsa
@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    if user_states.get(message.chat.id) == "waiting_for_screenshot":
        bot.send_message(message.chat.id, "✅ Tashakkur! Endi botdan foydalanishingiz mumkin.")
        send_main_menu(message.chat.id)
        user_states[message.chat.id] = "main_menu"
    else:
        bot.send_message(message.chat.id, "📸 Bu joyda screenshot kerak emas.")

# Asosiy menyu
def send_main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🎁 Tekin UC olish"),
        KeyboardButton("💰 Pul ishlash")
    )
    markup.add(
        KeyboardButton("👨‍💼 Admin"),
        KeyboardButton("📸 QR code yasash")
    )
    bot.send_message(chat_id, "👇 Quyidagi menyudan tanlang:", reply_markup=markup)

# 🎁 Tekin UC olish
@bot.message_handler(func=lambda m: m.text == "🎁 Tekin UC olish")
def uc_link(message):
    bot.send_message(message.chat.id, f"🎯 Tekin UC olish uchun bu yerga kiring 👇\n{LINK_UC}")

# 💰 Pul ishlash
@bot.message_handler(func=lambda m: m.text == "💰 Pul ishlash")
def pul_link(message):
    bot.send_message(message.chat.id, f"💸 Pul ishlash uchun quyidagi havolaga kiring 👇\n{LINK_PUL}")

# 👨‍💼 Admin
@bot.message_handler(func=lambda m: m.text == "👨‍💼 Admin")
def admin(message):
    bot.send_message(message.chat.id, "👨‍💼 Adminimiz sizga yordam beradi:\n@Legenda_70_75")

# 📸 QR code yasash
@bot.message_handler(func=lambda m: m.text == "📸 QR code yasash")
def ask_text(message):
    bot.send_message(message.chat.id, "✍️ QR code yasamoqchi bo‘lgan matningizni yuboring (uzun bo‘lsa ham bo‘ladi):")
    user_states[message.chat.id] = "awaiting_qr_text"

# QR kod yasash (bitta, hatto uzun matn uchun)
@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == "awaiting_qr_text")
def make_qr(message):
    text = message.text.strip()

    fg_color = random.choice(["#1E90FF", "#FF6347", "#32CD32", "#FF00FF", "#FFA500"])
    bg_color = "#FFFFFF"

    # Juda katta hajm uchun versionni None qilib, qrcode o‘zi moslashtiradi
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(text.encode("utf-8", "ignore"))  # uzun matnni UTF-8 da kodlash
    qr.make(fit=True)

    img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert("RGB")

    # Ramka bilan chiroyli qilish
    border_img = Image.new("RGB", (img.size[0] + 60, img.size[1] + 60), "#000000")
    border_img.paste(img, (30, 30))
    draw = ImageDraw.Draw(border_img)
    draw.rectangle([0, 0, border_img.size[0] - 1, border_img.size[1] - 1], outline=fg_color, width=10)

    # Yuborish
    bio = BytesIO()
    border_img.save(bio, format="PNG")
    bio.seek(0)

    bot.send_photo(message.chat.id, photo=bio, caption="✅ Sizning QR kodingiz tayyor (bitta to‘liq)!")

    send_main_menu(message.chat.id)
    user_states[message.chat.id] = "main_menu"

print("🤖 Bot ishga tushdi...")
bot.polling(none_stop=True)
