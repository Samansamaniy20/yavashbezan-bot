import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = -1004419228211

# کد فیلم: شناسه پیام فیلم در کانال
MOVIES = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        code = context.args[0]
        if code in MOVIES:
            keyboard = [[InlineKeyboardButton(
                "🎬 دریافت فیلم",
                callback_data=f"get_{code}"
            )]]
            await update.message.reply_text(
                "فیلم موردنظرت آماده است:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

    await update.message.reply_text(
        "سلام! 🎬 به ربات یواش بزن خوش اومدی.\n\n"
        "کد فیلم رو بفرست تا برات پیداش کنم."
    )

async def receive_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()
    if code in MOVIES:
        await update.message.reply_text(
            "برای دریافت فیلم روی دکمه زیر بزن:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🎬 دریافت فیلم",
                                     callback_data=f"get_{code}")
            ]])
        )
    else:
        await update.message.reply_text(
            "این کد فیلم پیدا نشد. لطفاً کد رو بررسی کن."
        )

async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    code = query.data[4:]

    if code not in MOVIES:
        await query.message.reply_text("فیلم پیدا نشد.")
        return

    message_id = MOVIES[code]
    await context.bot.copy_message(
        chat_id=query.message.chat_id,
        from_chat_id=CHANNEL_ID,
        message_id=message_id,
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(get_movie, pattern=r"^get_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_code))
    app.run_polling()

if __name__ == "__main__":
    main()
