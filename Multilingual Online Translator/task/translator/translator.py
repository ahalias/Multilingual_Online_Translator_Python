import requests
from bs4 import BeautifulSoup
import argparse


class Translator:
    translation_languages = {'1': 'arabic', '2': 'german', '3': 'english', '4': 'spanish', '5': 'french', '6': 'hebrew',
                             '7': 'japanese', '8': 'dutch', '9': 'polish', '10': 'portuguese',
                             '11': 'romanian', '12': 'russian', '13': 'turkish'}

    def __init__(self, from_language, to_language, word):
        self.source_language = from_language
        self.target_language = to_language
        self.word = word
        self.request_content = ''
        self.words = []
        self.sentences = []

    def translate(self):
        if self.target_language == 'all':
            for lang in Translator.translation_languages.values():
                if lang != self.source_language:
                    self.words = []
                    self.sentences = []
                    self.target_language = lang
                    self.print_data()
        elif self.source_language not in Translator.translation_languages.values():
            print(f"Sorry, the program doesn't support {self.source_language}")
            exit()
        elif self.target_language not in Translator.translation_languages.values():
            print(f"Sorry, the program doesn't support {self.target_language}")
            exit()
        else:
            self.print_data()

    def process_request(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        url_construct = f'{self.source_language}-{self.target_language}'
        url = f'https://context.reverso.net/translation/{url_construct}/{self.word}'
        r = requests.get(url, headers=headers)
        self.request_content = r.content
        return r.status_code

    def fetch_data(self):
        soup = BeautifulSoup(self.request_content, 'html.parser')
        translations = soup.find_all('span', {'class': 'display-term'})
        [self.words.append(text.text.strip()) for text in translations]
        sentences = soup.find_all('div', {'class': ['src ltr', 'rg rtl arabic', 'trg rtl arabic', 'trg ltr', 'trg rtl']})
        [self.sentences.append(sent.text.strip()) for sent in sentences]

    def print_data(self):
        status_code = self.process_request()
        if status_code == 200:
            self.fetch_data()
            file_content = \
f"""{self.target_language.title()} Translations: 
{self.words[0]} 
{self.target_language.title()} Example: 
{self.sentences[0]}
{self.sentences[1]}"""
            with open(f'{self.word}.txt', 'a', encoding='UTF-8') as f:
                print(file_content, file=f)
            output = ''
            with open(f'{self.word}.txt', 'r', encoding="utf-8") as f:
                for line in f:
                    output += line
            print(output)
        elif status_code == 404:
            print(f'Sorry, unable to find {self.word}')
            exit()
        else:
            print('Something wrong with your internet connection')
            exit()


parser = argparse.ArgumentParser(description='input source language, target language and word to translate')
parser.add_argument('source_language')
parser.add_argument('target_language')
parser.add_argument('word_to_translate')
args = parser.parse_args()
translator = Translator(args.source_language, args.target_language, args.word_to_translate)
translator.translate()
