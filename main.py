from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

last_user = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("📩 ارسال پیام ناشناس", url=f"https://t.me/{context.bot.username}")]]
    )
    await update.message.reply_text(
        "سلام 👋\nبه ربات پیام ناشناس خوش اومدی.\nپیامتو بفرست تا ناشناس برسه به ادمین.",
        reply_markup=btn
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_user
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        last_user[ADMIN_ID] = user_id
        msg = f"📩 پیام جدید ناشناس:\n\n{update.message.text}"
        await context.bot.send_message(ADMIN_ID, msg)
        await update.message.reply_text("✅ پیامت ناشناس ارسال شد.")
    else:
        if ADMIN_ID in last_user:
            target_id = last_user[ADMIN_ID]
            await context.bot.send_message(target_id, f"📬 پاسخ ادمین:\n\n{update.message.text}")
            await update.message.reply_text("✅ پاسخ ارسال شد.")
        else:
            await update.message.reply_text("❌ هیچ پیامی برای پاسخ وجود ندارد.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
