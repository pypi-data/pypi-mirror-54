# -*- coding: utf-8 -*-
import os

import numpy as np
from sklearn.preprocessing import LabelEncoder

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


PAD = '[PAD]'
SOS = '[CLS]'
EOS = '[SEP]'
UNK = '[UNK]'


class Label:

    def fit(self, y):
        tags = []
        for yy in y:
            tags += yy
        tags = sorted(set(tags))
        self.classes = [PAD, SOS, EOS] + tags
        self.tag_index = {}
        for i, t in enumerate(self.classes):
            self.tag_index[t] = i
        self.index_tag = {
            v: k
            for k, v in self.tag_index.items()
        }
        self.label_size = len(self.classes)

    def transform(self, y):
        batch_size = len(y)
        max_length = int(np.max([len(yy) for yy in y])) + 2
        result = np.zeros((batch_size, max_length), dtype=np.int32)
        for sent_id, sent in enumerate(y):
            result[sent_id][0] = self.tag_index[SOS]
            for word_id, word in enumerate(sent):
                result[sent_id][word_id + 1] = self.tag_index[word]
            result[sent_id][len(sent) + 1] = self.tag_index[EOS]
        return result

    def inverse_transform(self, y):
        return [
            [
                self.index_tag.get(yyy, UNK)
                for yyy in yy
            ]
            for yy in y
        ]
