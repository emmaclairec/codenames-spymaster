import json
import os


def create_dict(import_file):
    import os
    import pandas as pd
    games_dict = {}
    excel_import = pd.read_excel(os.path.join(os.getcwd(), import_file), header=None, sheet_name=None)
    col_nums = []
    [col_nums.append(x) for x in range(0, 20, 3)]
    for game in excel_import:
        card_count = 1
        df = excel_import[game]
        card_dict = {}
        for index, row in df.iterrows():
            for n in col_nums:
                if not pd.isnull(row[n]):
                    card_list = [row[n].upper(), row[n + 1].upper()]
                    card_dict.update({card_count: card_list})
                    card_count += 1
        games_dict.update({game: card_dict})

    store_content(games_dict, 'cards_dict.txt')

    return games_dict


def get_unique_words(games_dict, export_file):
    words_set = set()
    for game in games_dict:
        cards_dict = games_dict[game]
        for card in cards_dict:
            sides = cards_dict[card]
            words_set.add(sides[0])
            words_set.add(sides[1])
    words_list = list(words_set)
    words_list.sort()

    store_content(words_list, 'unique_words.txt')

    return words_list


def store_content(content, export_file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), export_file), 'w') as f:
        f.write(json.dumps(content))
        f.close()

def get_content(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file), 'r') as f:
        content = json.loads(f.read())
    return content


CODENAMES_DICT = get_content('cards_dict.txt')
UNIQUE_WORDS = get_content('unique_words.txt')

codenames = CODENAMES_DICT['Codenames']
undercover = CODENAMES_DICT['Undercover']
duet = CODENAMES_DICT['Duet']