import re
import sys
import json


def covert_text_to_dict(text_filename):
    chat_room_dict = {
        'roomName': '',
        'savedDate': '',
        'savedTime': '',
        'messages': [
            # {
            #     'senderName': '',
            #     'sentDate': '',
            #     'sentTime': '',
            #     'content': ''
            # }
        ]
    }

    with open(text_filename, 'r', encoding='UTF8') as f:
        lines = f.readlines()

    results = re.search('(.*) 님과 카카오톡 대화', lines[0])
    chat_room_dict['roomName'] = results.group(1)
    results = re.search('저장한 날짜 : (\d*-\d*-\d*) (\d*:\d*):\d*', lines[1])
    chat_room_dict['savedDate'] = results.group(1)
    chat_room_dict['savedTime'] = results.group(2)

    message = None
    for i in range(3, len(lines)):
        line = lines[i]
        if re.search('---------------.*---------------', line) != None:
            results = re.search('--------------- (\d*)년 (\d*)월 (\d*)일 .*---------------', line)
            day = results.group(1) + '-' + results.group(2) + '-' + results.group(3)
        elif re.search('\[.*\] \[.*\]', line) != None:
            if message != None:
                chat_room_dict['messages'].append(message)
            results = re.search('\[(.*)\] \[(.*) (\d*):(\d*)\] (.*)', line)
            hour = int(results.group(3))
            if results.group(2) == '오후':
                hour += 12
            time = str(hour) + ':' + results.group(4)
            message = {
                'senderName': results.group(1),
                'sentDate': day,
                'sentTime': time,
                'content': results.group(5)
            }
        elif message != None:
            message['content'] += line
    if message != None:
        chat_room_dict['messages'].append(message)
    
    return chat_room_dict


if __name__ == "__main__":
    text_filename = sys.argv[1]
    json_filename = text_filename[:-4] + '.json'

    chat_room_dict = covert_text_to_dict(text_filename)

    with open(json_filename, 'w', encoding='UTF8') as jsonf:
        json.dump(chat_room_dict, jsonf, ensure_ascii=False)