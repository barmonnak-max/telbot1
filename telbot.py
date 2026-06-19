from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import os


TOKEN = os.getenv("BOT_TOKEN")


ADMIN_ID = 8325235691  # آیدی عددی تلگرام خودت

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(
            "به ربات ما خوش امدید برای خرید از دسطور new/ استفاده کنید",

        )]
    ]

async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(
            "اشتراک ۱ ماه نامحدود - ۱۵۰ هزار تومان",
            callback_data="buy_1month"
        )]
    ]

    await update.message.reply_text(
        "پلن مورد نظر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buy_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = """
💳 شماره کارت:
6219-8614-5895-1216

👤 نام صاحب کارت:
بارمان اکبرزاده

✅ پس از واریز، عکس رسید را در همین صفحه ارسال کنید.
"""

    await query.message.reply_text(text)

async def receive_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    photo = update.message.photo[-1]

    caption = f"""
📥 رسید جدید

🆔 User ID: {user.id}
👤 Name: {user.full_name}
📛 Username: @{user.username if user.username else 'ندارد'}
"""

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=caption
    )

    await update.message.reply_text(
        "✅ رسید شما دریافت شد و در انتظار بررسی است."
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("new", new))
    app.add_handler(CallbackQueryHandler(buy_plan))
    app.add_handler(MessageHandler(filters.PHOTO, receive_receipt))

    app.run_polling()

if __name__ == "__main__":
    main()
    start()
