# -*- coding: utf-8 -*-
import os

import numpy as np
import tensorflow as tf

from .label import PAD, SOS, EOS, UNK

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


class Tokenizer:
    def __init__(self, vocab_file=None):
        self.word_index = {
            PAD: 0,
            UNK: 1,
            SOS: 2,
            EOS: 3
        }
        if isinstance(vocab_file, (list, tuple)):
            self.word_index = {}
            for i, w in enumerate(vocab_file):
                self.word_index[w] = i
            self.index_word = {v: k for k, v in self.word_index.items()}
            self.vocab_size = len(self.word_index)
        elif isinstance(vocab_file, str):
            self.word_index = {}
            with open(vocab_file, 'r') as fp:
                i = 0
                for line in fp:
                    if line.endswith('\n'):
                        line = line[:-1]
                    if len(line):
                        self.word_index[line] = i
                        i += 1
            self.index_word = {v: k for k, v in self.word_index.items()}
            self.vocab_size = len(self.word_index)

    def fit(self, X):
        for sent in X:
            for word in sent:
                if word not in self.word_index:
                    self.word_index[word] = len(self.word_index)
        self.vocab_size = len(self.word_index)
        self.index_word = {v: k for k, v in self.word_index.items()}

    def inverse_transform(self, X):
        ret = []
        for sent in X:
            words = []
            for w in sent:
                if w <= 0:
                    break
                if w in self.index_word:
                    words.append(self.index_word[w])
            ret.append(words)
        return ret

    def transform(self, X):
        batch_size = len(X)
        max_length = max([len(x) for x in X]) + 2
        result = np.zeros((batch_size, max_length), dtype=np.int32)
        for sent_id, sent in enumerate(X):
            result[sent_id][0] = self.word_index[SOS]
            for word_id, word in enumerate(sent):
                result[sent_id][word_id + 1] = self.word_index.get(word, self.word_index[UNK])
            result[sent_id][len(sent) + 1] = self.word_index[EOS]
        return result


if __name__ == "__main__":
    tokenizer = Tokenizer('./chinese_L-12_H-768_A-12/vocab.txt')
    print(tokenizer.transform([['[CLS]', '我', '爱', '你', '[SEP]']]))
    print(tokenizer.transform([['我', '爱', '你']]))