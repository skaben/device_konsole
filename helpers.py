import os
import random


class WordGen(object):

    password = ''

    def __init__(self, wordset_dir, word_quantity=16, word_len=8):
        self.quantity = word_quantity
        self.word_len = word_len
        self.vocabulary = self.load_vocabulary(os.path.join(wordset_dir, 'words{}.txt'.format(word_len)))

    @staticmethod
    def load_vocabulary(file_path):
        """loads meaningful words of defined size from file"""
        with open(file_path, 'r') as fh:
            return [word.strip('\n\t ') for word in fh.readlines() if word]

    @staticmethod
    def compare(target, source):
        i = 0
        count = 0
        for char in target:
            try:
                if char == source[i]:
                    count += 1
            except IndexError:
                pass
            i += 1
        return count

    @property
    def words(self):
        self.password = random.choice(self.vocabulary)

        words_max = []  # Слова, максимально похожие по расположению букв на слово-пароль
        words_zero = []  # Слова, совершенно не имеющие одинаково расположенных букв с паролем
        words_other = []  # Все прочие слова из списка
        words_selected = []  # Слова, которые будут использоваться непосредственно в игре
        word_delta = 2

        while len(words_max) == 0:
            i = 0
            for word in self.vocabulary:
                if word != self.password:
                    c = self.compare(word, self.password)
                    if c == 0:
                        words_zero.append(word)
                    elif c == (self.word_len - 1):
                        words_max.append(word)
                    elif c == (self.word_len - word_delta):
                        words_max.append(word)
                    else:
                        words_other.append(word)
            word_delta += 1

        words_selected.append(self.password)  # Пароль

        if len(words_max) > 0:  # Одно слово, максимально близкое к паролю
            words_selected.append(random.choice(words_max))

        if len(words_zero) > 0:  # Одно слово, которое совершенно не похоже на пароль
            words_selected.append(random.choice(words_zero))

        i = 0
        while i < self.quantity - 3:  # Добавляем ещё слов из общего списка
            word = random.choice(words_other)
            if word not in words_selected:
                words_selected.append(word)
                i += 1

        random.shuffle(words_selected)
        return words_selected

    def __repr__(self):
        return f'<WordList>'
