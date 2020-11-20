import sys
import re
from convert_txt_to_json import covert_text_to_dict

# 전체 메세지
# 평균 메세지 길이
def get_average_message_length(chat_room_dict):
    sum_message_length = 0

    for message in chat_room_dict['messages']:
        sum_message_length += len(message['content'])
    
    return sum_message_length / len(chat_room_dict['messages'])

# 내 메세지
# 이모티콘이 포함된 메세지 수 / 내 메세지 수
def get_emoticon_ratio(chat_room_dict, user_name):
    num_emoticon_messages = 0
    num_my_messages = 0

    for message in chat_room_dict['messages']:
        if message['content'] == '이모티콘' and message['senderName'] == user_name:
            num_emoticon_messages += 1
        if message['senderName'] == user_name:
            num_my_messages += 1
    
    return num_emoticon_messages / num_my_messages

# 내 메세지
# 슬랭이 포함된 메세지 수 / 내 메세지 수
def get_slang_ratio(chat_room_dict, user_name):
    num_slang_messages = 0
    num_my_messages = 0

    for message in chat_room_dict['messages']:
        results = re.search('[ㄱ-ㅎ|ㅏ-ㅣ]+', message['content'])
        if results != None and message['senderName'] == user_name:
            num_slang_messages += 1
        if message['senderName'] == user_name:
            num_my_messages += 1
    
    return num_slang_messages / num_my_messages

# |내 메세지 수 / 전체 메세지 수 - 1 / n|
# n: 한 번이라도 메세지를 보낸 사람의 수
def get_my_message_stake(chat_room_dict, user_name):
    num_my_messages = 0
    users = set()

    for message in chat_room_dict['messages']:
        if message['senderName'] == user_name:
            num_my_messages += 1
        users.add(message['senderName'])
    
    return abs(num_my_messages / len(chat_room_dict['messages']) - 1 / len(users))

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

    print(
        get_average_message_length(chat_room_dict),
        get_emoticon_ratio(chat_room_dict, user_name),
        get_slang_ratio(chat_room_dict, user_name),
        get_my_message_stake(chat_room_dict, user_name)
    )

    print(get_features_all(text_filename, user_name))
