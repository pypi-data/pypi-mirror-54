# -*- coding: utf-8 -*-
import os
import pickle
import numpy as np
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
    x_dev, y_dev = text_reader(dev_path)
    x_test, y_test = text_reader(test_path)

    vocab_file = 'glove_vocab.txt'
    words = open(vocab_file, 'r').read().split('\n')
    words_index = {k: True for k in words}

    add_words = []

    def word_trans(w):
        if w in words_index:
            return w
        # if w.lower() in words_index:
        #     return w.lower()
        # if w.upper() in words_index:
        #     return w.upper()
        if w not in add_words:
            add_words.append(w)
        return w

    # y_train = [y for x, y in zip(x_train, y_train) if x[0] != '-DOCSTART-']
    # y_dev = [y for x, y in zip(x_dev, y_dev) if x[0] != '-DOCSTART-']
    # y_test = [y for x, y in zip(x_test, y_test) if x[0] != '-DOCSTART-']

    # x_train = [[word_trans(xx) for xx in x] for x in x_train if x[0] != '-DOCSTART-']
    # x_dev = [[word_trans(xx) for xx in x] for x in x_dev if x[0] != '-DOCSTART-']
    # x_test = [[word_trans(xx) for xx in x] for x in x_test if x[0] != '-DOCSTART-']

    x_train = [[word_trans(xx) for xx in x] for x in x_train]
    x_dev = [[word_trans(xx) for xx in x] for x in x_dev]
    x_test = [[word_trans(xx) for xx in x] for x in x_test]

    print(f'new words {len(add_words)}')

    new_words = words + add_words

    print('load glove')
    embedding_weights = pickle.load(open('glove_embedding.pkl', 'rb'))

    new_embedding = np.concatenate([embedding_weights, np.random.uniform(-.5, .5, (len(add_words), 100))])
    with open('/tmp/conll2003_glove.txt', 'w') as fp:
        fp.write('\n'.join(new_words))


    it = TFTagger(
        embedding_size=100,
        hidden_size=200,
        layer_size=1,
        dropout=0.5,
        vocab_file='/tmp/conll2003_glove.txt',
        embedding_weights=new_embedding,
        use_char=True,
        embedding_trainable=True
    )

    save_best = '/tmp/conll2003_glove.pkl'
    it.fit(x_train, y_train, x_dev, y_dev, batch_size=64, save_best=save_best, epoch=50)
    print(it.score_table(x_test, y_test))
    with open(save_best, 'rb') as fp:
        it = pickle.load(fp)
        print(it.score_table(x_test, y_test))


if __name__ == '__main__':
    test()
