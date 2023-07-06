from googletrans import Translator
import argparse
import clipboard
import json
import re
import os

translator = Translator()

# arguments 

parser = argparse.ArgumentParser()
 
parser.add_argument("-en", "--en_output", help = "Save Output to a file in json format in english ")
parser.add_argument("-es", "--es_output", help = "Save Output to a file in json format in spanish")
parser.add_argument("-k", "--key", help = "json key name for inserting the word ")

args = parser.parse_args()

def translate(english_word):
    translation = translator.translate(english_word, dest="es")
    key_name = re.sub(r'[^\w\s]', '', english_word).replace(" ", "_").lower()

    json_file_en = open(args.en_output, 'r')
    en_data = json.load(json_file_en)
    json_file_en.close()

    with open(args.en_output,'w') as en_file:
        if args.key:
            new_key = args.key.replace(' ', '_').lower()
            if new_key not in en_data['translation']:
                en_data['translation'][new_key] = {}
            en_data['translation'][new_key][key_name] = english_word
        else:
            en_data['translation'][key_name] = english_word
        json.dump(en_data, en_file,ensure_ascii=False)

    json_file_es = open(args.es_output, 'r')
    es_data = json.load(json_file_es)
    json_file_es.close()
    with open(args.es_output, 'w') as es_file:
        if args.key:
            new_key = args.key.replace(' ', '_').lower()
            if new_key not in es_data['translation']: 
                es_data['translation'][new_key] = {}
            es_data['translation'][new_key][key_name] = translation.text
        else:
            es_data['translation'][key_name] = translation.text
        json.dump(es_data, es_file, ensure_ascii=False)
    print("english word: " + english_word, "spanish word: " + translation.text)
    print(key_name)
    clipboard.copy(key_name)

if __name__ == "__main__":
    if args.en_output:
        if os.path.exists(args.en_output) == False:
            with open(args.en_output, 'w') as en_file:
                json.dump({'translation':{}}, en_file)
    if args.es_output:
        if os.path.exists(args.es_output) == False:
            with open(args.es_output, 'w') as es_file:
                json.dump({'translation':{}}, es_file)
    while True:
        english_word = input("Enter a word to translate: ")
        if english_word == "exit()":
            print("Exiting...")
            break
        translate(english_word)

