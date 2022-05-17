from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import os
import json
from cards import UNIQUE_WORDS


def get_all_nynms(a_synset, the_depth):
    all_nyms = []
    hyper = lambda s: s.hypernyms()
    hypo = lambda s: s.hyponyms()
    s_holo = lambda s: s.substance_holonyms()
    m_holo = lambda s: s.member_holonyms()
    p_holo = lambda s: s.part_holonyms()
    s_mero = lambda s: s.substance_meronyms()
    m_mero = lambda s: s.member_meronyms()
    p_mero = lambda s: s.part_meronyms()
    ent = lambda s: s.entailments()
    nym_types = [hyper, hypo, s_holo, m_holo, p_holo, s_mero, m_mero, p_mero, ent]
    for nym in nym_types:
        nym_list = list(a_synset.closure(nym, depth=the_depth))
        for item in nym_list:
            lemma_name_list = [x.name().lower() for x in item.lemmas()]
            for lemma in lemma_name_list:
                if lemma not in all_nyms:
                    all_nyms.append(lemma)
    return all_nyms


def get_score_dict(upper_word):
    word = upper_word.lower()
    lemma_score_dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
    sets = wn.synsets(word)
    for a_set in sets:
        lemma_syns = [x.name().lower() for x in a_set.lemmas()]
        for lemma in lemma_syns:
            if '_' in lemma:
                split_lemma = lemma.split('_')
                for a_lemma in split_lemma:
                    if word not in a_lemma:
                        if lemma not in lemma_score_dict[0]:
                            lemma_score_dict[0].append(a_lemma)
            elif word not in lemma:
                if lemma not in lemma_score_dict[0]:
                    lemma_score_dict[0].append(lemma)
    for n in range(1, 6):
        for a_set in sets:
            all_lemmas = get_all_nynms(a_set, n)
            filtered_lemmas = []
            for lemma in all_lemmas:
                if '_' in lemma:
                    split_lemmas = lemma.split('_')
                    for one_lemma in split_lemmas:
                        if word not in one_lemma:
                            in_dict_already = False
                            for check_past in range(0, n):
                                if one_lemma in lemma_score_dict[check_past]:
                                    in_dict_already = True
                                    break
                            if not in_dict_already:
                                filtered_lemmas.append(one_lemma)
                elif word not in lemma:
                    in_dict_already = False
                    for check_past in range(0, n):
                        if lemma in lemma_score_dict[check_past]:
                            in_dict_already = True
                            break
                    if not in_dict_already:
                        filtered_lemmas.append(lemma)
            for item in filtered_lemmas:
                if item not in lemma_score_dict[n]:
                    lemma_score_dict[n].append(item)
    return lemma_score_dict


def all_words_scores(word_list):
    all_words_dict = {}
    for word in word_list:
        all_words_dict.update({word: get_score_dict(word)})
    store_content(all_words_dict, 'scores_dict.txt')
    return all_words_dict


def store_content(content, export_file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), export_file), 'w') as f:
        f.write(json.dumps(content))
        f.close()


def get_content(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file), 'r') as f:
        content = json.loads(f.read())
    return content


# scores_dict = all_words_scores(UNIQUE_WORDS)

#scores_dict = get_content('scores_dict.txt')

amb = wn.synset('ambulance.n.01')
hos1 = wn.synset('health.n.01')
hos2 = wn.synset('health.n.02')

print(amb.lowest_common_hypernyms(hos1))
print(amb.lowest_common_hypernyms(hos2))
