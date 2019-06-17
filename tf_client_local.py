#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:24:39 2019

@author: zjy
"""
import random
import tensorflow as tf
from tensorflow.contrib import predictor
import os

tf.app.flags.DEFINE_string('export_dir', "export_dir",
                           help="Use half floats instead of full floats if True.")
tf.app.flags.DEFINE_string('model_version', "1",
                           help="the export model version")
# TODO: model version trail
FLAGS = tf.app.flags.FLAGS


if __name__ == '__main__':
    # Send data by POST method
    """ review of model input/output information (showed by saved_model_cli in run_server.sh)
    The given SavedModel SignatureDef contains the following input(s):
        inputs['x'] tensor_info:
            dtype: DT_FLOAT
            shape: (-1)
            name: x:0
        inputs['y'] tensor_info:
            dtype: DT_FLOAT
            shape: (-1)
            name: y:0
    The given SavedModel SignatureDef contains the following output(s):
        outputs['sum'] tensor_info:
            dtype: DT_FLOAT
            shape: (-1)
            name: add:0
    """

    model_full_path = os.path.join(FLAGS.export_dir, FLAGS.model_version)
    server = predictor.from_saved_model(model_full_path)

    # sample data
    sample_data = {"x": [random.random() for i in range(4)],
                   "y": [random.random() for i in range(4)]}
    # get addition result
    result = server(sample_data)

    print("inputs:")
    print(sample_data)
    print()
    print("outputs:")
    print(result)