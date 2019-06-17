#!/usr/bin/env python3

echo 'show model exportation...'
saved_model_cli show --dir export_dir/1 --tag_set serve --signature_def serving_default

docker run -p 8900:8500 -p 8901:8501 \
  -v "/home/zjy/workspace/NLP_code/serving/tf_serving_tutorial/export_dir/1:/models/my_model/1" \
  -e MODEL_NAME=my_model \
  -t tensorflow/serving:1.12.0 --enable_batching --batching_parameters_file="models/my_model/1/batchingParameters.proto" --tensorflow_session_parallelism=8