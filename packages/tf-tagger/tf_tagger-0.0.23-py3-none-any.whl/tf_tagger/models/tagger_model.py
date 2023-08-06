# -*- coding: utf-8 -*-
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import tensorflow as tf

from .embed import Embed
from .encoder import Encoder
from .decoder import Decoder
from .encoder_bert import EncoderBert
from .char_cnn import CharCNN
from .decoder_softmax import DecoderSoftmax

class TaggerModel(tf.keras.Model):
    def __init__(self,
                 embedding_size,
                 hidden_size,
                 vocab_size,
                 tag_size,
                 dropout,
                 layer_size,
                 bidirectional,
                 use_char=False,
                 char_vocab_size=None,
                 char_embedding_size=None,
                 max_word_length=None,
                 char_hidden_size=None,
                 embedding_weights=None,
                 embedding_trainable=True,
                 bert=False,
                 bert_model_dir=None,
                 bert_max_length=4096,
                 bert_params=None,
                 bert_num_layers=None,
                 bert_trainable=False):
        super(TaggerModel, self).__init__(self)
        self.char_emb = None
        if use_char:
            self.char_emb = Embed(char_embedding_size, char_vocab_size)
            self.char_encoder = CharCNN(max_word_length, char_embedding_size, char_hidden_size)
        self.bert = bert
        if bert:
            self.emb = EncoderBert(
                max_length=bert_max_length,
                model_dir=bert_model_dir,
                bert_params=bert_params,
                num_layers=bert_num_layers,
                trainable=bert_trainable
            )
        else:
            self.emb = Embed(
                embedding_size=embedding_size,
                vocab_size=vocab_size,
                weights=embedding_weights,
                trainable=embedding_trainable
            )
        self.en = Encoder(
            embedding_size=embedding_size + char_hidden_size if use_char else embedding_size,
            hidden_size=hidden_size,
            layer_size=layer_size,
            bidirectional=bidirectional
        )
        self.project = tf.keras.models.Sequential([
            # tf.keras.layers.Dense(hidden_size, activation='tanh'),
            tf.keras.layers.Dense(tag_size)
        ])
        self.project.build(input_shape=(None, hidden_size))
        self.de = Decoder(tag_size=tag_size)
        # self.de = DecoderSoftmax(tag_size=tag_size)
        # self.dropout = tf.keras.layers.Dropout(
        #     dropout, noise_shape=None, seed=None)
        self.dropout = dropout

    def logits(self, inputs, training=False, char_inputs=None):
        lengths = tf.reduce_sum(tf.cast(tf.math.greater(inputs, 0), tf.int32), axis=-1)
        mask = tf.greater(inputs, 0)
        x = inputs
        x = self.emb(x)
        if self.char_emb is not None:
            xc = char_inputs
            xc = self.char_emb(xc)
            if training:
                xc = tf.nn.dropout(xc, rate=self.dropout)
            xc = self.char_encoder(xc)
            x = tf.concat([x, xc], axis=-1)

        if training:
            x = tf.nn.dropout(x, rate=self.dropout)
        x = self.en(x, mask)
        if training:
            x = tf.nn.dropout(x, rate=self.dropout)
        x = self.project(x)
        return x, lengths

    def call(self, inputs, char_inputs=None):
        logits, lengths = self.logits(inputs, char_inputs=char_inputs)
        return self.de(logits, lengths)

    def compute_loss(self, inputs, tags, char_inputs=None):
        logits, lengths = self.logits(inputs, training=True, char_inputs=char_inputs)
        return self.de.compute_loss(logits, lengths, tags)


if __name__ == "__main__":
    tm = TaggerModel(
        embedding_size=None,
        hidden_size=768,
        vocab_size=None,
        tag_size=10,
        dropout=.0,
        layer_size=None,
        bidirectional=None,
        bert=True,
        bert_model_dir='./chinese_L-12_H-768_A-12',
        bert_max_length=4096)
    from ..utils.tokenizer import Tokenizer
    tokenizer = Tokenizer('./chinese_L-12_H-768_A-12/vocab.txt')
    ids = tokenizer.transform([['我', '爱', '你']])
    r = tm(ids)
    print(r)