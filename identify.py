import csv
from collections import Counter
from functools import lru_cache

supported_languages = [
    "English",
    "Spanish",
    "French",
    "Dutch",
    "Russian",
    "Latin",
    "Hindi",
    "Korean",
    "Chinese",
    "Japanese",
    "Urdu",
    "Arabic",
]

show_incorrect = False

def get_examples(language):
    """
    Returns all examples for `language`
    """
    
    with open('texts.csv') as f:
        return [r['text'] for r in csv.DictReader(f) if r['language'] == language]

def get_corpus(language):
    """
    Returns the combined text corpus for the given `language`
    """
    
    return ' '.join(get_examples(language)[:-100])

def get_character_ngrams(text, n=3):
    """
    Converts a text to a list of overlapping ngrams

    >>> get_character_ngrams('hello')
    ['hel', 'ell', 'llo']

    >>> get_character_ngrams('hi you')
    ['hi ', 'i y', ' yo', 'you']

    >>> get_character_ngrams('مرحبا')
    ['مرح', 'رحب', 'حبا']
    """

@lru_cache()
def get_top_ngrams(language, top_n=3, ngram_len=3):
    """
    Returns the top ngrams for a given language.

    Return value is a list of (ngram, probability) tuples.

    It is recommended to use a `Counter` in your implementation.

    >>> get_top_ngrams('English', top_n=1)
    [(' th', 0.015728688279572814)]

    >>> get_top_ngrams('English', top_n=2)[1][0]
    'the'
    
    >>> get_top_ngrams('Spanish', top_n=1, ngram_len=5)[0][0]
    ' de l'
    """

def identify(text):
    """ 
    Returns a language identification for a given sample

    >>> identify("The cats are hungry")
    'English'

    >>> identify("Los gatos tienen hambre")
    'Spanish'
    """

    # Bag of words approach
    words = Counter(text.lower().split())
    en_articles = sum(words[n] for n in ['the', 'a', 'an'])
    es_articles = sum(words[n] for n in ['los', 'las', 'el', 'la','un','una'])

    if es_articles > en_articles:
        return 'Spanish'
    else:
        return 'English'

if __name__ == '__main__':
    correct = Counter()

    for language in supported_languages:
        for text in get_examples(language)[-100:]:
            predicted_language = identify(text)
            if predicted_language == language:
                correct[language] += 1
            elif show_incorrect:
                print(f"{predicted_language} != {language}\n{text}")

        # Report sensitivity (true positive rate) by language
        print(f"{language} sensitivity: {correct[language] / 100}")

    print(f"Overall sensitivity: {sum(correct.values()) / (100 * len(supported_languages))}")
