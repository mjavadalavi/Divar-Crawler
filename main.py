import sys
import telepot
from time import sleep
from src.divar import divar
from src.model import session, Ads
from telepot.loop import MessageLoop

BOT_TOKEN = sys.argv[1]
ADMIN_USER_ID = sys.argv[2]
DIVAR_URI = sys.argv[3]


def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        command = msg['text']
        if command == '/start':
            bot.sendMessage(chat_id, 'Hello! I am your bot. How can I help you?')
        elif command == '/help':
            check_ads(chat_id=chat_id)
            bot.sendMessage(chat_id, 'This is a simple bot. You can use /start enjoy bot.')
        else:
            bot.sendMessage(chat_id, 'I do not understand that command. Try /help for assistance.')


def check_ads(chat_id, divar_url):
    divar_ads = divar(divar_url)
    ads_list = divar_ads.get_ads()
    for ads_item in ads_list:
        job_data = ads_item.split('/')
        ads_db = session.query(Ads).filter(
            Ads.hash_code == job_data[-1]).first()
        if not ads_db:
            bot.sendMessage(chat_id, f"آگهی جدیدی با نام: {job_data[4].replace('_', ' ')} \n\n در آدرس زیر در دسترس است \n\n {ads_item}")
        ads_item = Ads(hash_code=job_data[-1], chat_id=chat_id)
        try:
            session.add(ads_item)
            session.commit()
        except Exception:
            session.rollback()
            raise Exception


bot = telepot.Bot(BOT_TOKEN)
MessageLoop(bot, handle_message).run_as_thread()
print('Bot is listening. Press Ctrl+C to exit.')

while True:
    check_ads(ADMIN_USER_ID, DIVAR_URI)
    sleep(300)
