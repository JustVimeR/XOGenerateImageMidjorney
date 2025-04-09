from gradio_client import Client
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import time

TELEGRAM_BOT_TOKEN = 'bot-token'

# Створюємо клієнт Hugging Face Space
client = Client("mukaist/Midjourney")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Напиши мені промпт, і я згенерую для тебе зображення у стилі Midjourney! 🎨")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text("⏳ Генерую зображення, зачекай...")

    try:
        result = client.predict(
            prompt,  # prompt
            "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck",  # negative_prompt
            True,  # use_negative_prompt
            "2560 x 1440",  # style
            0,  # seed
            1024,  # width
            1024,  # height
            6,  # guidance_scale
            True,  # randomize_seed
            api_name="/run"
        )

        # Отримуємо зображення
        image_data = result[0][0]  # перший об'єкт у галереї
        image_url = image_data['image']
        await update.message.reply_photo(photo=image_url)

    except Exception as e:
        await update.message.reply_text(f"😢 Помилка при генерації зображення: {e}")

# Ініціалізуємо бота
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))
app.run_polling()
