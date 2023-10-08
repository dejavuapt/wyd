import constants;
import logs_constants as lc;

from parsers.doing_parser import DoingParser

from datetime import time as t;
from datetime import date as d;

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# take of a statistic
CSV_TRACK_PATH = './log.csv'

parser = DoingParser(csv_path=CSV_TRACK_PATH)
parser.RefreshCSV()
parser.AddDateRow(d.today())


"""
Send message `What are you doing?` to user.
"""
async def callback_answer(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=context.job.chat_id, 
        text = f'👀 What are you doing, {context.job.data}?'
        )
    

"""
Run bot's job from `first` time to `last` time, every `interval` seconds.
Call -> callback_answer
Interval -> default 60*60 seconds = 1 hour.
"""
async def callback_in_day(context: ContextTypes.DEFAULT_TYPE):
    parser.AddDateRow(d.today())
    context.job_queue.run_repeating(
        callback_answer, 
        interval = constants.INTERVAL_REMINDER, 
        first = t.fromisoformat("07:00:00+05:00"),
        last = t.fromisoformat("22:00:00+05:00"),
        data = context.job.data['name'], 
        chat_id = context.job.data['chat_id'])


"""
Run bot's job every day from `time` time.
Check if jobs already started
"""
async def callback_daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    name = update.effective_chat.full_name

    text_message: str = f'{lc.LogoutsTags.NOTIFICATIONS.value} return '
    if(len(context.job_queue.jobs()) != 0):
        text_message += '1 | already launched ⏱'
    else:
        text_message += '0 | launch soon... ⏱'
        context.job_queue.run_daily(
            callback_in_day,
            time = t.fromisoformat("06:00:00+05:00"),
            data = {'name': name, 'chat_id': chat_id},
            chat_id = chat_id,
        )

    await context.bot.send_message(
        chat_id = chat_id, 
        text = text_message
        )


"""
Stop bot's jobs.
"""
async def stop_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_message: str = f'{lc.LogoutsTags.INFO.value}'
    count_jobs: int = len(context.job_queue.jobs()) 

    if(count_jobs >= 1): 
        context.job_queue.stop()
        text_message += ' 0 | stop all ⏱'
    else:
        text_message += ' 0 | so everything is off ⏱'


    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = text_message
    )

"""
Function for get user's answer. Parsing and write in csv file(temporary).
//TODO not csv -> google sheets
"""
async def doing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_doing: str = ' '.join(context.args) 

    parser.SetSeparate(text_doing)
    parser.WriteInCSV()
    
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = f'{lc.LogoutsTags.INFO.value} 0'
    )


async def get_statistic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    args_password: str = ''.join(context.args)
    if(args_password == constants.ARG_FOR_GET_STATISTIC):
        document = open(CSV_TRACK_PATH, 'rb')
        await context.bot.send_document(chat_id=chat_id, document=document)
        parser.RefreshCSV()
        
    

# main часть
if __name__ == '__main__':
    application = ApplicationBuilder().token(constants.TOKEN_BOT_API).build()

    doing_handler = CommandHandler('doing', doing)
    application.add_handler(doing_handler)


    # start/stop reminder 
    stop_callback_handler = CommandHandler('stop_callback', stop_callback)
    application.add_handler(stop_callback_handler)
    timer_handler = CommandHandler('start_callback', callback_daily)
    application.add_handler(timer_handler)

    #send_static
    get_statistic_handler = CommandHandler('get_statistic', get_statistic)
    application.add_handler(get_statistic_handler)


    
    application.run_polling()