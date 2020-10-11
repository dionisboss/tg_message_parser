import configparser
import logging

from telethon.sync import TelegramClient, \
    events
from telethon.tl.types import Channel


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id = int(config['Telegram']['api_id'])
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
USER_TO_SEND = "Sofya_1999"
CHAT_LIST = [-1001062351210, -1001403651762, -1001221148335] + [-1001425875581, -1001471337719,
                                                                -1001274730605, -1001404652265,
                                                                -1001244025771, -1001405491023, -1001392392805]
KEY_WORDS = {"test", }
KEY_WORDS_2 = {"test2", }

client = TelegramClient(username, api_id, api_hash)


def to_lower(word: str):
    return word.lower()


@client.on(events.NewMessage(chats=CHAT_LIST))
async def message_parser(event: events.newmessage.NewMessage.Event):
    global KEY_WORDS, KEY_WORDS_2
    base_len = len(KEY_WORDS)
    base_len_2 = len(KEY_WORDS_2)
    message_text_set = event.raw_text.split(" ")
    message_text_set = set(map(to_lower, message_text_set))
    new_len = len(KEY_WORDS - message_text_set)
    new_len_2 = len(KEY_WORDS_2 - message_text_set)
    if (new_len < base_len) and (new_len_2 < base_len_2):
        channel_id_ = event.chat_id
        group_: Channel = await client.get_entity(channel_id_)
        uname_ = group_.username
        if username:
            link_ = f"https://t.me/{uname_}"
        else:
            link_ = "У этой группы нет ссылки для доступа."
        await event.forward_to(USER_TO_SEND)
        await client.send_message(USER_TO_SEND, f"{KEY_WORDS_2 & message_text_set} and {KEY_WORDS & message_text_set}"
                                                f"\n"
                                                f"Группа: {link_}")


with client:
    client.run_until_disconnected()
