import sys
import re
from datetime import date
from convert_txt_to_json import covert_text_to_dict


def is_within_month(saved_date, sent_date):
    saved_year, saved_month, saved_date = [int(x) for x in saved_date.split('-')]
    sent_year, sent_month, sent_date = [int(x) for  x in sent_date.split('-')]
    d0 = date(saved_year, saved_month, saved_date)
    d1 = date(sent_year, sent_month, sent_date)
    diff = d0 - d1
    print(diff.days)
    if diff.days <= 31:
        return True
    else:
        return False

# 전체 메세지
# 평균 메세지 길이
def get_average_message_length(chat_room_dict):
    sum_message_length = 0
    num_messages = 0

    for message in chat_room_dict['messages']:
        if is_within_month(chat_room_dict['savedDate'], message['sentDate']):
            sum_message_length += len(message['content'])
            num_messages += 1
    
    if num_messages == 0:
        return 0
    else:
        return sum_message_length / num_messages

# 내 메세지
# 이모티콘이 포함된 메세지 수 / 내 메세지 수
def get_emoticon_ratio(chat_room_dict, user_name):
    num_emoticon_messages = 0
    num_my_messages = 0

    for message in chat_room_dict['messages']:
        if is_within_month(chat_room_dict['savedDate'], message['sentDate']):
            if message['content'] == '이모티콘' and message['senderName'] == user_name:
                num_emoticon_messages += 1
            if message['senderName'] == user_name:
                num_my_messages += 1
    
    if num_my_messages == 0:
        return 0
    else:
        return num_emoticon_messages / num_my_messages

# 내 메세지
# 슬랭이 포함된 메세지 수 / 내 메세지 수
def get_slang_ratio(chat_room_dict, user_name):
    num_slang_messages = 0
    num_my_messages = 0

    for message in chat_room_dict['messages']:
        if is_within_month(chat_room_dict['savedDate'], message['sentDate']):
            results = re.search('[ㄱ-ㅎ|ㅏ-ㅣ]+', message['content'])
            if results != None and message['senderName'] == user_name:
                num_slang_messages += 1
            if message['senderName'] == user_name:
                num_my_messages += 1
    
    if num_my_messages == 0:
        return 0
    else:
        return num_slang_messages / num_my_messages

# |내 메세지 수 / 전체 메세지 수 - 1 / n|
# n: 한 번이라도 메세지를 보낸 사람의 수
def get_my_message_stake(chat_room_dict, user_name):
    num_my_messages = 0
    num_messages = 0
    users = set()

    for message in chat_room_dict['messages']:
        if is_within_month(chat_room_dict['savedDate'], message['sentDate']):
            if message['senderName'] == user_name:
                num_my_messages += 1
            num_messages += 1
            users.add(message['senderName'])
    
    if num_messages == 0 or len(users) == 0:
        return 0
    else:
        return abs(num_my_messages / num_messages - 1 / len(users))

def get_features_all(text_filename, user_name):
    chat_room_dict = covert_text_to_dict(text_filename)

    return {
        'average_message_length': get_average_message_length(chat_room_dict),
        'emoticon_ratio': get_emoticon_ratio(chat_room_dict, user_name),
        'slang_ratio': get_slang_ratio(chat_room_dict, user_name),
        'my_message_stake': get_my_message_stake(chat_room_dict, user_name)
    }


if __name__ == "__main__":
    text_filename = sys.argv[1]
    user_name = sys.argv[2]

    chat_room_dict = covert_text_to_dict(text_filename)

    print(get_features_all(text_filename, user_name))
