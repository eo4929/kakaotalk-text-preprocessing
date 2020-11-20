import json
from get_features import get_features_all

with open('input.json', 'r', encoding='UTF8') as jsonf:
    args = json.load(jsonf)['args']

output_csv = 'id,average_message_length,emoticon_ratio,slang_ratio,my_message_stake\n'

id = 0
for arg in args:
    file_name = arg['fileName']
    user_name = arg['userName']
    features = get_features_all(file_name, user_name)
    output_csv += str(id) + ','
    output_csv += str(features['average_message_length']) + ','
    output_csv += str(features['emoticon_ratio']) + ','
    output_csv += str(features['slang_ratio']) + ','
    output_csv += str(features['my_message_stake']) + '\n'
    id += 1

with open('output.csv', 'w', encoding='UTF8') as f:
    f.write(output_csv)