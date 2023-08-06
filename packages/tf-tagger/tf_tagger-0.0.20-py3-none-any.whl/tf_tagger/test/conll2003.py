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
    x_dev, y_dev = text_reader(dev_path)
    x_test, y_test = text_reader(test_path)

    it = TFTagger(
        embedding_size=200,
        hidden_size=200,
        layer_size=2
    )

    save_best='/tmp/conll2003.pkl'
    it.fit(x_train, y_train, x_dev, y_dev, batch_size=256, save_best=save_best)
    pred = it.predict(x_test, verbose=True)
    print(pred[:3])
    print(it.score_table(x_test, y_test))


if __name__ == '__main__':
    test()
