import google.generativeai as genai
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables (lokal aja, Render nanti pakai cara lain)
load_dotenv()

# API Keys dari ENV Variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Konfigurasi Google AI
genai.configure(api_key=GEMINI_API_KEY)

# Logging biar gampang debug
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Yo! Gue bot AI paling gaul. Kirim pesan, dan gue bakal jawab! 😎")

async def chat(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    try:
        model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
        response = model.generate_content(
            [
                {"role": "user", "parts": [{"text": "Jawab dengan santai, sedikit sarkas, dan gaul."}]},
                {"role": "user", "parts": [{"text": user_message}]}
            ],
            generation_config={"temperature": 1, "top_p": 0.95, "top_k": 64, "max_output_tokens": 50}
        )

        reply_text = response.candidates[0].content.parts[0].text.strip() if response and response.candidates else "Gue lagi ngelag... coba lagi deh. 🤯"
    except Exception as e:
        reply_text = "Sabar woi! Gantian bales chatnya. 🤦‍♂️"

    await update.message.reply_text(reply_text)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command
    app.add_handler(CommandHandler("start", start))

    # Semua chat user akan diproses
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Run bot
    logging.info("Bot berjalan! 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
