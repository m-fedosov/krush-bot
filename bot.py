import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import TelegramError

from config import BOT_TOKEN, GROUP_ID, GROUP_LINK
from db import init_db, get_user, register_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
 
    member = await context.bot.get_chat_member(chat_id=GROUP_ID, user_id=user.id)
    in_group = member.status in ("member", "administrator", "creator")
 
    if not in_group:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Вступить в группу", url=GROUP_LINK)]])
        await update.message.reply_text(
            "Чтобы участвовать, вступи в группу и снова отправь /start 🏃",
            reply_markup=keyboard
        )
        return
 
    await update.message.reply_text(f"✅ {user.first_name}, ты в игре! Жди стартового сигнала 🏁")
 

init_db()
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
 