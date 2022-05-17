import os
import json
from cards import UNIQUE_WORDS


def get_ranges(max_count):
    ranges = []
    score = 0
    interval = round((max_count / 201) * 2) / 2
    interval_start = max_count
    while score <= 100:
        if score == 100:
            interval_end = 0
        else:
            interval_end = interval_start - interval
        ranges.append([interval_start, interval_end, score])
        score += 0.5
        interval_start = interval_end
    return ranges


def wiki_score(count, ranges):
    score = 'Error'  # to get rid of PhCharm Error
    for a_range in ranges:
        if a_range[1] < count <= a_range[0]:
            score = a_range[2]
            break
    return score


def wordnet_score(z_to_s):
    score = round(z_to_s * (16 + (2 / 3)) * 2) / 2
    return score


export_path = os.path.join(os.getcwd(), 'combined_score')
wiki_import_path = os.path.join(os.getcwd(), 'wiki_counts')
wordnet_scores_path = os.path.join(os.getcwd(), 'wordnet_scores_dict.txt')

empty_dict = {}
for i in range(100, -1, -1):
    if i == 100:
        empty_dict.update({i: []})
    else:
        empty_dict.update({i+0.5: []})
        empty_dict.update({i: []})


with open(wordnet_scores_path, 'r') as f:
    full_wordnet_dict = json.loads(f.read())
    f.close()

for word in UNIQUE_WORDS:
    with open(os.path.join(export_path, word + '_scores.txt'), 'r') as final:
        comb_scores = json.loads(final.read())
        final.close()
    with open(os.path.join(wiki_import_path, word + '_wiki_count.txt'), 'r') as f:
        wiki_dict = json.loads(f.read())
        f.close()
    first_word = True
    the_ranges = 'Error'  # to remove pycharm error
    for wiki_word in wiki_dict:
        if first_word:
            the_ranges = get_ranges(wiki_dict[wiki_word])
            first_word = False
        the_score = wiki_score(wiki_dict[wiki_word], the_ranges)
        comb_scores[the_score].append(wiki_word)
        wiki_dict[wiki_word] = the_score
    wordnet_dict = full_wordnet_dict[word]
    for wn_score in wordnet_dict:
        the_score = wordnet_score(wn_score)
        for wn_word in wordnet_dict[wn_score]:
            if wn_word in wiki_dict:
                if the_score > wiki_dict[wn_word]:
                    comb_scores[(wiki_dict[wn_word])].remove(wn_word)
                    comb_scores[the_score].append(wn_word)
            else:
                comb_scores[the_score].append(wn_word)
    with open(os.path.join(export_path, word + '_scores.txt'), 'w') as final:
        final.write(json.dumps(comb_scores))
        final.close()

