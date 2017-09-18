import json


def load_json_data(file_path):
    try:
        with open(file_path) as f:
            data = json.load(f)
    except:
        return None

    return data


def get_popular_words(words_list, count=10):
    word_counter = {}
    for word in words_list:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    popular_words = sorted(word_counter, key=word_counter.get, reverse=True)
    return (popular_words[:count], word_counter)

