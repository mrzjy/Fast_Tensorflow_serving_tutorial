#!/usr/bin/env python3

echo 'show model exportation...'
saved_model_cli show --dir export_dir/1 --tag_set serve --signature_def serving_default

tensorflow_model_server --enable_batching \
    --model_name="my_model" \
    --model_base_path="/home/zjy/workspace/NLP_code/serving/tf_serving_tutorial/export_dir" \
    --batching_parameters_file="export_dir/batchingParameters.proto" \
    --tensorflow_session_parallelism=8 \
    --rest_api_port=8501 --port=8500  #  the REST is exposed in port 8501 and GRPC interface in port 8500