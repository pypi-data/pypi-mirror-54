# -*- coding: utf-8 -*-
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import tensorflow as tf


class Embed(tf.keras.Model):

    def __init__(self, embedding_size, vocab_size, weights=None, trainable=True):
        super(Embed, self).__init__(self)
        with tf.device('/CPU:0'):
            if weights is not None:
                assert len(weights.shape) == 2
                assert weights.shape[0] == vocab_size
                assert weights.shape[1] == embedding_size
                weights = [tf.convert_to_tensor(weights, dtype=tf.float32)]
            self.emb = tf.keras.layers.Embedding(
                vocab_size,
                embedding_size,
                weights=weights
            )
        inputs = tf.keras.layers.Input(
            shape=(None,),
            dtype=tf.int32)
        x = self.emb(inputs)
        self.model = tf.keras.Model(inputs=[inputs], outputs=[x])
        self.model.trainable = trainable

    def call(self, inputs):
        x = inputs
        x = self.model(x)
        return x

