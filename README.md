# Fast_Tensorflow_serving_tutorial
This is a fast and simple tutorial on how to apply Tensorflow serving. It covers minimal functionalities to get a tensorflow server-client system working, with 3 steps to follow.

## Step 1. create a model and export it
**(Step 1 is actually skippable for I've already done this for you)**
In the tf.model.py file, a tensorflow model is implemented that simply does addition operation to two given variables. We would create this model in model_dir, and export it to export_dir by simply running:
~~~
python tf_model.py
~~~
You could quickly test the exported model (load the model locally and feed some data to it) by running:
~~~
python tf_client_local.py
~~~
- **In order to follow the next steps normally:**
Make sure you change the export path to export_dir/1, and there is batchingParameters.proto file present inside it (take a look at the current repo and you'll understand what I'm saying)
(Again, all this is only necessary if you decide to redo the step 1 yourself, and if so, you may want to clear the export_dir and model_dir first)


## Step 2. Serve the model (Create the server)
There are multiple ways to serve the model, in this simple tutorial, however, we'd only focus on applying "tensorflow-serving" ways.
### Choice 1: The original way
The original way is the direct and standard command of tensorflow_model_server, which could be installed as described here: https://www.tensorflow.org/tfx/serving/setup (Section "using APT" or "Build from source")

Once you've successfully installed it, simply run the example code:
~~~
sh tf_run_server_original_way.sh
~~~
The server will take up two ports (8500 and 8501 by default), the port 8501 support REST interface and port 8500 supports GRPC interface. In other words, the tensorflow serving supports both REST and gRPC simultaneously.

### Choice 2: The Docker way
The Docker way is more recommanded because all you need to do is to download the Docker image that already contains everything you need, instead of installing everything yourself just as in the "2.1 The original way". Of course you need to get Docker installed first (https://www.docker.com/).

Once you've get docker functioning, simply run the example code:
~~~
sh tf_run_server_docker_way.sh
~~~
Basically it's the same outcome as "Choice 1: The original way", except the port usage. Here we applied port mapping: port mapped to 8901 and 8900 in the above code. So the requests that you make later should instead be sent to 8901 or 8900. (To see why we use port mapping for Docker, please refer to https://docs.docker.com/config/containers/container-networking/)

## Step 3. Create the client (Make request to server)
Once the server is set up normally, it naturally supports 2 ways of how data is accepted and returned, namely the REST and gRPC (You could find a brief introduction/comparison of them at https://code.tutsplus.com/tutorials/rest-vs-grpc-battle-of-the-apis--cms-30711). Hence, there are 2 ways to create the client.

### Choice 1: The REST way
Basically, the REST way is about sending and receiving data in **JSON** format, simply run:
~~~
# change 8501 to 8901 if the model server is created through Docker
python tf_client_REST.py -url=http://0.0.0.0:8501/v1/models/my_model:predict
~~~

### Choice 2: The gRPC way
As opposed to REST, the gRPC way is about sending and receiving data in **Protobuf** format, simply run:
~~~
# change 8500 to 8900 if the model server is created through Docker
python tf_client_gRPC.py -url=0.0.0.0:8500
~~~
Normally, you should see the client inputs and the server outputs printed in the console in either client choice.

**Follow-ups**
- **The server-side batching functionality**
This is one of the strong and convinient feature of tensorflow-serving, which is enabled by "--enable_batching" command flag. Besides, the batching behaviour could be customized by a "batchingParameters.proto" file. You may explore this youself (e.g., https://stackoverflow.com/questions/42635873/tensorflow-serving-batching-parameters)
- **Alternative ways to serve a model**
There are unlimited ways to serve a model, https://github.com/hanxiao/bert-as-service is one of them using ZeroMQ. Also, if concurrency is not your concern, or you only have CPUs (for which batching brings less concurrency boost), a direct web framework (e.g., Tornado, Flask) + loading the model locally is quite enough actually.
- **More details**
Feel free to explore more details, such as https://towardsdatascience.com/using-tensorflow-serving-grpc-38a722451064 
