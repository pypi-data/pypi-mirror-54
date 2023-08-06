# -*- coding: utf-8 -*-
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import tensorflow as tf


class CharCNN(tf.keras.Model):

    def __init__(self, max_word_length, embedding_size, filters, kernel_size=3):
        super(CharCNN, self).__init__(self)
        inputs = tf.keras.layers.Input(
            shape=(max_word_length, embedding_size),
            dtype=tf.float32)
        x = inputs
        x = tf.keras.layers.Conv1D(filters, kernel_size, padding='same', activation='tanh')(x)
        x = tf.keras.layers.GlobalMaxPool1D()(x)
        self.model = tf.keras.Model(inputs=[inputs], outputs=[x])

    def call(self, inputs):
        batch_size, sentence_size, word_size, word_embedding_size = inputs.shape
        x = inputs
        x = tf.reshape(x, (batch_size * sentence_size, word_size, word_embedding_size))
        x = self.model(x)
        x = tf.reshape(x, (batch_size, sentence_size, -1))
        return x
