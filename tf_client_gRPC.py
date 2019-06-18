#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:24:39 2019

@author: zjy
"""
import random
import grpc
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
import argparse
parser = argparse.ArgumentParser(description='Tensorflow serving client test')
parser.add_argument('-url', type=str, default='0.0.0.0:8500',
                    help='url of server that supports GRPC')
args = parser.parse_args()


if __name__ == '__main__':
    # Send data through grpc
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
    sample_data = {"x": [random.random() for i in range(4)],
                   "y": [random.random() for i in range(4)]}
    # request setting: model server
    channel = grpc.insecure_channel(args.url)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'my_model'
    request.model_spec.signature_name = 'serving_default'
    # request setting: inputs
    request.inputs['x'].CopyFrom(tf.contrib.util.make_tensor_proto(sample_data["x"], shape=[4]))
    request.inputs['y'].CopyFrom(tf.contrib.util.make_tensor_proto(sample_data["y"], shape=[4]))

    # prediction
    result_future = stub.Predict.future(request, 10.25)  # 5 seconds
    result = result_future.result().outputs["sum"].float_val
    print("inputs:")
    print(sample_data)
    print()
    print("outputs:")
    print(result)