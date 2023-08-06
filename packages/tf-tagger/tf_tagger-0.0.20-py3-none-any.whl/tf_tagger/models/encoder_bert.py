# -*- coding: utf-8 -*-
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import tensorflow as tf
from bert import BertModelLayer
from bert import params_from_pretrained_ckpt
from bert import load_stock_weights


class EncoderBert(tf.keras.Model):

    def __init__(self, model_dir=None, max_length=1024, bert_params=None, num_layers=None, trainable=False):
        super(EncoderBert, self).__init__(self)

        assert isinstance(max_length, int)
        assert bert_params is not None or model_dir is not None

        if bert_params is None:
            assert os.path.exists(model_dir)
            bert_params = params_from_pretrained_ckpt(model_dir)
        if isinstance(num_layers, int):
            bert_params.num_layers = num_layers

        l_bert = BertModelLayer.from_params(bert_params, name="bert")

        l_input_ids = tf.keras.layers.Input(shape=(max_length,), dtype='int32')

        output = l_bert(l_input_ids)
        model = tf.keras.Model(inputs=l_input_ids, outputs=output)
        model.build(input_shape=(None, max_length))
        model.trainable = trainable
        self.model = model

        if model_dir is not None:
            bert_ckpt_file = os.path.join(model_dir, "bert_model.ckpt")
            load_stock_weights(l_bert, bert_ckpt_file)

    def call(self, inputs, mask=None):
        return self.model(inputs)


if __name__ == "__main__":
    from ..utils.tokenizer import Tokenizer
    tokenizer = Tokenizer('./chinese_L-12_H-768_A-12/vocab.txt')
    ids = tokenizer.transform([['我', '爱', '你']])
    en = EncoderBert(model_dir='./chinese_L-12_H-768_A-12')
    r = en(ids)
    print(r)
