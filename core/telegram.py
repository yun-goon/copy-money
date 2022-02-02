import sys
import time
import telepot
from telepot.loop import MessageLoop

TOKEN = '5095481267:AAEYDylalwUwg1oU0fzmB2s3B0UhDKIHbiI'  # get token from command-line

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type)
    print(chat_type)
    print(chat_id)

    if content_type == 'text':
        bot.sendMessage('-1001792622831', msg['text'])

TOKEN = '5095481267:AAEYDylalwUwg1oU0fzmB2s3B0UhDKIHbiI'  # get token from command-line

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)