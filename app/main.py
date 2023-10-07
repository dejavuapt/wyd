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
        text=f'[NOTIFICATION] What are you doing, {context.job.data}? '
        )
    

# напоминалка с утра до вечера каждый час 
async def callback_in_day(context: ContextTypes.DEFAULT_TYPE):
    context.job_queue.run_repeating(
        callback_answer, 
        interval = constants.INTERVAL_REMINDER, 
        first = t.fromisoformat("07:00:00+05:00"),
        last = t.fromisoformat("22:00:00+05:00"),
        data = context.job.data['name'], 
        chat_id = context.job.data['chat_id'])



async def callback_daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    name = update.effective_chat.full_name
    await context.bot.send_message(
        chat_id = chat_id, 
        text = '[INFO] Starting interval job...'
        )
    # Set the alarm:
    context.job_queue.run_daily(
        callback_in_day,
        time = t.fromisoformat("06:00:00+05:00"),
        data = {'name': name, 'chat_id': chat_id},
        chat_id = chat_id,
    )


async def stop_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if(len(context.job_queue.jobs()) > 1):
        context.job_queue.jobs()[0].schedule_removal() # удаляем тот что дневной если он включен, ажедневный оставляем
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = '[INFO] Stop callback. Next tomorrow!'
    )

#команда деланья
async def doing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_doing: str = ' '.join(context.args) # получаем аргументы от команды и дальше уже можно парсировать.
    print(text_doing)
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = '[INFO] Writed!'
    )


# main часть
if __name__ == '__main__':
    application = ApplicationBuilder().token(constants.TOKEN_BOT_API).build()

    doing_handler = CommandHandler('doing', doing)
    application.add_handler(doing_handler)

    stop_callback_handler = CommandHandler('stop_callback', stop_callback)
    application.add_handler(stop_callback_handler)

    timer_handler = CommandHandler('oneday', callback_daily)
    application.add_handler(timer_handler)

    
    application.run_polling()