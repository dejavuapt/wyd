import constants;

from datetime import time as t;

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


# Показывает что когда и где работает не так.
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def callback_answer(context: ContextTypes.DEFAULT_TYPE):
    # Beep the person who called this alarm:
    await context.bot.send_message(
        chat_id=context.job.chat_id, 
        text=f'Что делаешь，{context.job.data}?'
        )
    
async def callback_in_day(context: ContextTypes.DEFAULT_TYPE):
    context.job_queue.run_repeating(
        callback_answer, 
        interval = 10, 
        first = t.fromisoformat("08:00:00+05:00"),
        last = t.fromisoformat("23:59:00+05:00"),
        data = context.job.data['name'], 
        chat_id = context.job.data['chat_id'])



async def callback_daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    name = update.effective_chat.full_name
    await context.bot.send_message(
        chat_id = chat_id, 
        text = '[INFO] starting interval job...'
        )
    # Set the alarm:
    context.job_queue.run_daily(
        callback_in_day,
        time = t.fromisoformat("22:54:00+05:00"),
        data = {'name': name, 'chat_id': chat_id},
        chat_id = chat_id,
    )
    print(context.job_queue.jobs())


#команда деланья
async def doing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_doing: str = ' '.join(context.args) # получаем аргументы от команды и дальше уже можно парсировать.
    print(text_doing)
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = '[INFO] Result: 0'
    )


# main часть
if __name__ == '__main__':
    application = ApplicationBuilder().token(constants.TOKEN_BOT_API).build()

    doing_handler = CommandHandler('doing', doing)
    application.add_handler(doing_handler)

    timer_handler = CommandHandler('oneday', callback_daily)
    application.add_handler(timer_handler)

    
    application.run_polling()