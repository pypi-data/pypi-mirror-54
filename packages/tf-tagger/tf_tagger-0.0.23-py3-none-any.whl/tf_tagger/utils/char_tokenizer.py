# -*- coding: utf-8 -*-
import os

import numpy as np
import tensorflow as tf

from .label import PAD, SOS, EOS, UNK

CHARS = (
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '0123456789'
    '-'
)


class CharTokenizer:
    def __init__(self, max_word_length=50):
        self.word_index = {
            PAD: 0,
            UNK: 1,
            SOS: 2,
            EOS: 3
        }
        for c in CHARS:
            self.word_index[c] = len(self.word_index)
        self.vocab_size = len(self.word_index)
        self.index_word = {v: k for k, v in self.word_index.items()}
        self.max_word_length = max_word_length

    def fit(self, X):
        pass         

    def transform(self, X):
        word_pad = [self.word_index[PAD]] * self.max_word_length
        max_length = max([len(x) for x in X]) + 2
        ret = []
        for sent in X:
            sent_vec = [word_pad]
            for word in sent:

                word_vec = []
                word_vec.append(self.word_index[SOS])
                for c in word:
                    word_vec.append(self.word_index.get(c, self.word_index[UNK]))
                word_vec.append(self.word_index[EOS])

                if len(word_vec) < self.max_word_length:
                    left_pad = (self.max_word_length - len(word_vec)) // 2
                    right_pad = self.max_word_length - len(word_vec) - left_pad
                    word_vec = [self.word_index[PAD]] * left_pad + word_vec + [self.word_index[PAD]] * right_pad
                elif len(word_vec) > self.max_word_length:
                    word_vec = word_vec[:self.max_word_length]

                sent_vec.append(word_vec)
            sent_vec.append(word_pad)
            if len(sent_vec) < max_length:
                while len(sent_vec) < max_length:
                    sent_vec.append(word_pad)
            ret.append(sent_vec)
        ret = np.array(ret, dtype=np.int32)
        return ret


if __name__ == "__main__":
    tokenizer = CharTokenizer()
    v = tokenizer.transform([['hello', 'my', 'Friend']])
    print(v.shape)
    import pdb; pdb.set_trace()
    from ..models.embed import Embed
    emb = Embed(30, tokenizer.vocab_size)
    r = emb(v)
    print(r)
    from ..models.char_cnn import CharCNN
    cc = CharCNN()
    c = cc(r)
    print(c)