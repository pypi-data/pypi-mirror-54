# -*- coding: utf-8 -*-
import os
import pickle
from appdirs import user_cache_dir
from ..tf_tagger import TFTagger
from ..utils.text_reader import text_reader
from .get_conll2003 import main as get_conll2003


def test():
    
    cache_dir = user_cache_dir(appname='tf-tagger')

    train_path, dev_path, test_path = [
        os.path.join(cache_dir, x)
        for x in [
            'conll2003_eng_train.txt',
            'conll2003_eng_valid.txt',
            'conll2003_eng_test.txt'
        ]
    ]

    if not os.path.exists(train_path):
        get_conll2003()

    x_train, y_train = text_reader(train_path)
    x_test, y_test = text_reader(test_path)

    x_train = [[xx.lower() for xx in x] for x in x_train]
    x_test = [[xx.lower() for xx in x] for x in x_test]

    it = TFTagger(
        embedding_size=768,
        hidden_size=200,
        layer_size=1,
        bert=True,
        bert_model_dir='./multi_cased_L-12_H-768_A-12',
        bert_max_length=4096,
        bert_num_layers=4,
        bert_trainable=False,
        vocab_file='./multi_cased_L-12_H-768_A-12/vocab.txt')

    it.fit(x_train, y_train, x_test, y_test, batch_size=16)
    pred = it.predict(x_test, verbose=True)
    print(pred[:3])
    print(it.score_table(x_test, y_test))


if __name__ == '__main__':
    test()
