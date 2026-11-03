
import os
import re
import httpx
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Welcome to ViralBoost 50K!\n\n"
        "Apna YouTube video link bhejiye.\n"
        "Main video ka analysis karunga aur genuine views "
        "badhaane ke liye promotion tips dunga."
    )

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    match = re.search(
        r"https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+",
        message
    )

    if not match:
        await update.message.reply_text(
            "❌ Please valid YouTube video link bhejiye."
        )
        return

    url = match.group(0)

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                "https://www.youtube.com/oembed",
                params={"url": url, "format": "json"}
            )
            response.raise_for_status()
            data = response.json()

        title = data.get("title", "Unknown")
        author = data.get("author_name", "Unknown")

        result = (
            "✅ VIDEO ANALYSIS\n\n"
            f"🎬 Title: {title}\n"
            f"👤 Channel: {author}\n\n"
            "🚀 PROMOTION PLAN\n"
            "1. Attractive thumbnail banayein.\n"
            "2. Title mein relevant keywords rakhein.\n"
            "3. Short clips banakar share karein.\n"
            "4. Relevant Telegram aur social communities mein "
            "video share karein.\n"
            "5. Audience retention improve karein.\n\n"
            "🎯 Target: 50,000 genuine views\n"
            "Note: Views guaranteed nahi hain. "
            "Bot fake views generate nahi karta."
        )

        await update.message.reply_text(result)

    except Exception:
        await update.message.reply_text(
            "Video details nahi mil paayi. Link check karke dobara bhejein."
        )

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable missing")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, analyze)
    )
    app.run_polling()

if __name__ == "__main__":
    main()
