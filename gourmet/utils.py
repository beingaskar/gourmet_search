def get_popular_words(words_list, count=10):
    word_counter = {}
    for word in words_list:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    popular_words = sorted(word_counter, key=word_counter.get, reverse=True)
    return popular_words[:count], word_counter


