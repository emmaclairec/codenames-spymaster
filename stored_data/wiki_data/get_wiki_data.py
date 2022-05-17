import os
import json
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import multiprocessing as mp
import logging
import time
import sys
import re
from cards import UNIQUE_WORDS

start_time = time.time()

mp_count = int(sys.argv[1])


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

tokenizer = RegexpTokenizer(r'\w+')


class WikiArticle:

    def __init__(self, article):
        self.article = article
        self.article_text = self.clean_article()

    def clean_article(self):
        article_json = json.loads(self.article)
        art_text = article_json['text']
        rep = {'i.e. ': '', 'e.g. ': '', 'bullet::::': '. ', 'colspan': '. ', '\n!': '. ', 'class=': '. '}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        art_text = pattern.sub(lambda m: rep[re.escape(m.group(0))], art_text.lower())
        art_text = art_text.split('. ')
        return art_text


class WikiDictChange:

    def __init__(self, a_word, folder):
        self.word = a_word
        self.folder = folder
        self.dict = None

    def open_dict(self):
        with open(os.path.join(path, self.folder, '_By Word', self.word + '_wiki_count.txt'), 'r') as y:
            self.dict = json.loads(y.read())
            y.close()
            return self.dict

    def update(self, token_list):
        for token in token_list:
            if token not in stop_words:
                if self.word.lower() not in token and isEnglish(token):
                    if token in self.dict:
                        self.dict[token] += 1
                    else:
                        self.dict.update({token: 1})
        self.close_dict()

    def close_dict(self):
        with open(os.path.join(path, self.folder, '_By Word', self.word + '_wiki_count.txt'), 'w') as z:
            z.write(json.dumps(self.dict))
            z.close()
            self.dict.clear()


def FolderWorker(queue):
    while not queue.empty():
        # Get the work from the queue
        folder = queue.get()
        process_folder(folder)


def DictWorker(queue):
    while not queue.empty():
        # Get the work from the queue
        a_word, folder_list = queue.get()
        logging.info('%s combining and sorting %s', mp.current_process().name, a_word)
        combine_dicts(a_word, folder_list)


def get_all_stopwords():
    the_stopwords = {'also', 'one', 'first', 'new', 'two', 'used', 'would', 'world', 'may', 'many',
                     'including', 'states', 'made', 'use', 'year', 'years', 'known', 'later', 'three', 'four',
                     'five', 'six', 'seven', 'eight', 'nine', 'like', 'called', 'became', 'early', 'since',
                     'however', 'system', 'part', 'could', 'number', 'people', 'state', 'century', 'second',
                     'often', 'include', 'although', 'several', 'following', 'example', 'example',
                     'around', 'found', 'another', 'end', 'according', 'likes', 'even', 'much', 'due', 'name',
                     'using', 'within', 'along', 'general', 'set', 'de', 'based', 'group', 'among', 'said',
                     'ii', 'days', 'day', 'form', 'began', 'life', 'area', 'common', 'still', 'us',
                     'different', 'back', 'well', 'time', 'times'}
    wn_stopwords = set(stopwords.words('english'))
    for stopword in wn_stopwords:
        the_stopwords.add(stopword)
    return the_stopwords


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def process_folder(the_folder):
    file_path = os.path.join(path, the_folder)
    file_list = os.listdir(file_path)
    file_list.sort()
    if '_By Word' in file_list:
        file_list.remove('_By Word')
    else:
        os.mkdir(os.path.join(file_path, '_By Word'))
    for word in UNIQUE_WORDS:
        with open(os.path.join(file_path, '_By Word', word + '_wiki_count.txt'), 'w+') as empty_dict:
            empty_dict.write(json.dumps({}))
            empty_dict.close()
    if '.DS_Store' in file_list:
        file_list.remove('.DS_Store')
    for file in file_list:
        process_file(file, file_path, the_folder)


def process_file(the_file, file_path, the_folder):
    with open(os.path.join(file_path, the_file), 'r') as source_f:
        articles = source_f.readlines()
        for article in articles:
            for sentence in WikiArticle(article).article_text:
                word_tokens = tokenizer.tokenize(sentence)
                for the_word in UNIQUE_WORDS:
                    if the_word.lower() in word_tokens:
                        word_class = WikiDictChange(the_word, the_folder)
                        word_class.open_dict()
                        word_class.update(word_tokens)
        source_f.close()
    logging.info('%s done processing %s - %s', mp.current_process().name, the_folder, the_file)


def combine_dicts(word, folder_list):
    comb_dict = {}
    for folder in folder_list:
        with open(os.path.join(path, folder, '_By Word', word + '_wiki_count.txt'), 'r') as y:
            a_dict = json.loads(y.read())
            y.close()
        for item in a_dict:
            if item in comb_dict:
                comb_dict[item] = comb_dict[item] + a_dict[item]
            else:
                comb_dict.update({item: a_dict[item]})
    sort_dict(word, comb_dict)


def sort_dict(a_word, unsorted):
    sorted_dict = {}
    for k, v in sorted(unsorted.items(), key=lambda item: item[1], reverse=True):
        sorted_dict.update({k: v})
    with open(os.path.join(path, '_By Word', a_word + '_wiki_count.txt'), 'w+') as final:
        final.write(json.dumps(sorted_dict))
        final.close()


def mp_folders(folder_list):
    ts = time.time()
    queue = mp.Queue()
    processes = [mp.Process(target=FolderWorker, args=(queue,)) for x in range(mp_count)]
    for a_folder in folder_list:
        logging.info('Queueing %s', a_folder)
        queue.put(a_folder)
    for p in processes:
        p.start()
    checking = True
    while checking:
        if queue.empty():
            for p in processes:
                p.join()
            checking = False
    logging.info('Folder Processing Took %s', time.time() - ts)


def mp_dicts(folder_list):
    ts = time.time()
    queue = mp.Queue()
    processes = [mp.Process(target=DictWorker, args=(queue,)) for x in range(mp_count)]
    for a_word in UNIQUE_WORDS:
        logging.info('Queueing %s', a_word)
        queue.put([a_word, folder_list])
    for p in processes:
        p.start()
    checking = True
    while checking:
        if queue.empty():
            for p in processes:
                p.join()
            checking = False
    logging.info('Sorting Files Took %s', time.time() - ts)


def get_folder_list(a_path):
    folder_list = os.listdir(a_path)
    ignore = ['.DS_Store', '_By Word', 'zz_Store Done']
    new_list = []
    for item in folder_list:
        if item not in ignore:
            new_list.append(item)
    new_list.sort()
    return new_list


stop_words = get_all_stopwords()
path = os.path.join(os.getcwd(), 'text')
wiki_folder_list = get_folder_list(path)

if __name__ == "__main__":
    mp_folders(wiki_folder_list)
    mp_dicts(wiki_folder_list)
logging.info('Done in %s.', time.time() - start_time)
