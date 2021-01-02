# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from dataLoader import Loader
import numpy as np
import os 
from tflite_support import flatbuffers
from tflite_support import metadata as _metadata
from tflite_support import metadata_schema_py_generated as _metadata_fb

loader = Loader()
train_data, train_labels, val_data, val_labels, test_data, test_labels = loader.load()
train_data = np.transpose(train_data,(0,2,1))
val_data   = np.transpose(val_data,(0,2,1))
test_data = np.transpose(test_data,(0,2,1))
print(train_data.shape)
print(val_data.shape)
print(test_data.shape)


model = tf.keras.Sequential([
  tf.keras.layers.InputLayer(input_shape=(7, 350)),
  tf.keras.layers.Reshape(target_shape=(7, 350, 1)),
  tf.keras.layers.Conv2D(filters=16, kernel_size=(3, 3), activation=tf.nn.relu),
  tf.keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation=tf.nn.relu),
  tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
  tf.keras.layers.Dropout(0.25),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(10)
])


# Define how to train the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


# Train the digit classification model
model.fit(train_data, train_labels, epochs=10)

# model.summary()
print("Evaluation in val set:")
model.evaluate(val_data, val_labels)
print("Evaluation in test set:")
model.evaluate(test_data, test_labels)

# Convert Keras model to TF Lite format.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_float_model = converter.convert()

# Show model size in KBs.
float_model_size = len(tflite_float_model) / 1024
print('Float model size = %dKBs.' % float_model_size)

# Re-convert the model to TF Lite using quantization.
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_quantized_model = converter.convert()

# Show model size in KBs.
quantized_model_size = len(tflite_quantized_model) / 1024
print('Quantized model size = %dKBs,' % quantized_model_size)
print('which is about %d%% of the float model size.'\
      % (quantized_model_size * 100 / float_model_size))

# Save the quantized model to file to the Downloads directory
f = open('python_model_training\model\mnist.tflite', "wb")
f.write(tflite_quantized_model)
f.close()


model_meta = _metadata_fb.ModelMetadataT()
model_meta.name = "IoTNet image classifier"
model_meta.description = ("Identifies the movement direction of foot.")
model_meta.version = "v2"
model_meta.author = "TensorFlow"
model_meta.license = ("Apache License. Version 2.0 "
                      "http://www.apache.org/licenses/LICENSE-2.0.")

# Creates input info.
input_meta = _metadata_fb.TensorMetadataT()

# Creates output info.
output_meta = _metadata_fb.TensorMetadataT()

input_meta.name = "Sensor_Data"
input_meta.description = (
    "Input Sensor Data to be classified. The expected Sensor Data is {0} x {1}."
    .format(7, 350))
input_meta.content = _metadata_fb.ContentT()
input_meta.content.contentProperties = _metadata_fb.ImagePropertiesT()
input_meta.content.contentProperties.colorSpace = (
    _metadata_fb.ColorSpaceType.GRAYSCALE)
input_meta.content.contentPropertiesType = (
    _metadata_fb.ContentProperties.ImageProperties)
# input_normalization = _metadata_fb.ProcessUnitT()
# input_normalization.optionsType = (
#     _metadata_fb.ProcessUnitOptions.NormalizationOptions)
# input_normalization.options = _metadata_fb.NormalizationOptionsT()
# input_normalization.options.mean = [127.5]
# input_normalization.options.std = [127.5]
# input_meta.processUnits = [input_normalization]
input_stats = _metadata_fb.StatsT()
input_stats.max = [1]
input_stats.min = [0]
input_meta.stats = input_stats


output_meta = _metadata_fb.TensorMetadataT()
output_meta.name = "probability"
output_meta.description = "Probabilities of the 10 labels respectively."
output_meta.content = _metadata_fb.ContentT()
output_meta.content.content_properties = _metadata_fb.FeaturePropertiesT()
output_meta.content.contentPropertiesType = (
    _metadata_fb.ContentProperties.FeatureProperties)
output_stats = _metadata_fb.StatsT()
output_stats.max = [1.0]
output_stats.min = [0.0]
output_meta.stats = output_stats
label_file = _metadata_fb.AssociatedFileT()
label_file.name = os.path.basename("python_model_training\data\labels.txt")
label_file.description = "Labels for movements that the model can recognize."
label_file.type = _metadata_fb.AssociatedFileType.TENSOR_VALUE_LABELS
output_meta.associatedFiles = [label_file]

subgraph = _metadata_fb.SubGraphMetadataT()
subgraph.inputTensorMetadata = [input_meta]
subgraph.outputTensorMetadata = [output_meta]
model_meta.subgraphMetadata = [subgraph]

b = flatbuffers.Builder(0)
b.Finish(
    model_meta.Pack(b),
    _metadata.MetadataPopulator.METADATA_FILE_IDENTIFIER)
metadata_buf = b.Output()

labelFile = open("python_model_training\data\labels.txt", "w")
labelFile.write("lf_front,lf_frontLeft,lf_left,lf_bottomLeft,lf_bottom")
labelFile.close()

populator = _metadata.MetadataPopulator.with_model_file("python_model_training\model\mnist.tflite")
populator.load_metadata_buffer(metadata_buf)
populator.load_associated_files(["python_model_training\data\labels.txt"])
populator.populate()

displayer = _metadata.MetadataDisplayer.with_model_file("python_model_training\model\mnist.tflite")
export_json_file = os.path.join("python_model_training\model\jsonFIleFolder/",
                    "mnist.tflite" + ".json")
json_file = displayer.get_metadata_json()
# Optional: write out the metadata as a json file
with open(export_json_file, "w") as f:
  f.write(json_file)