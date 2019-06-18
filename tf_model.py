#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:24:39 2019

@author: zjy
"""
import tensorflow as tf
import numpy as np
import os


tf.app.flags.DEFINE_string("model_dir", "model_dir",
                           help="dir where model checkpoints are saved")
tf.app.flags.DEFINE_string('export_dir', "export_dir",
                           help="Use half floats instead of full floats if True.")
tf.app.flags.DEFINE_string('model_version', "1",
                           help="the export model version")
# TODO: model version trail
FLAGS = tf.app.flags.FLAGS


class Model:
    """ Model class """
    def __init__(self, mode, params):
        """ Initialization"""
        self.mode = mode
        self.params = params
        self.addition_layer = AdditionLayer()

    def __call__(self, features):
        return self.addition_layer(features["x"], features["y"])


class AdditionLayer(tf.layers.Layer):
    """ Model Layer class"""
    def __init__(self):
        super(AdditionLayer, self).__init__()

    def call(self, x, y, *args, **kwargs):
        return x + y


def model_fn(features, labels, mode, params):
    # Create model and get output logits.
    model = Model(features, mode)
    results = model(features)
    # prediction
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(tf.estimator.ModeKeys.PREDICT, predictions={"sum": results})
    else:
        global_step = tf.train.get_global_step()
        return tf.estimator.EstimatorSpec(mode=mode, loss=tf.constant(0), train_op=tf.assign_add(global_step, 1))


def dummy_input_fn():
    x_samples, y_samples = np.random.rand(10), np.random.rand(10)
    dataset = tf.data.Dataset.from_tensor_slices((x_samples, y_samples))

    def parse_fn(*tensors):
        tensor_names = ['x', 'y']
        dict_element = {k: v for k, v in zip(tensor_names, tensors)}
        return dict_element, tensors[-1]

    return dataset.map(parse_fn)


def export_input_fn():
    def preprocess(float_plh):
        # this part is only for emphasizing the difference between
        # the raw placeholders and the maybe-preprocessed features
        return float_plh

    x_plh = tf.placeholder(dtype=tf.float32, shape=(None,), name='x')
    y_plh = tf.placeholder(dtype=tf.float32, shape=(None,), name='y')
    receiver_tensors = {"x": x_plh, "y": y_plh}
    features = {"x": preprocess(x_plh), "y": preprocess(y_plh)}
    return tf.estimator.export.ServingInputReceiver(features, receiver_tensors)


def export(*args, **kwargs):
    # create model using estimator api
    model = tf.estimator.Estimator(
        model_fn=model_fn,
        model_dir=FLAGS.model_dir,
        params=FLAGS.flag_values_dict(),
        config=None)

    # run a dummy example and save model
    model.train(input_fn=dummy_input_fn, steps=1)

    # export model
    export_dir = os.path.join(FLAGS.export_dir, FLAGS.model_version)
    model.export_savedmodel(export_dir, export_input_fn)


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main=export)
