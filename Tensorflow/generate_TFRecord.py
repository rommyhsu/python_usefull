import os
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


def _int64_feature(value):
    """Wrapper for inserting int64 features into Example proto."""
    if not isinstance(value, list):
        value = [value]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def _bytes_feature(value):
    """Wrapper for inserting bytes features into Example proto."""
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def write_TFRecord():
    cwd = './pic/'
    classes = {'cat', 'mario'}  # class catgories
    writer = tf.python_io.TFRecordWriter(
        "./TFRecords/dog_train.tfrecords")  # TFrecord file

    for index, name in enumerate(classes):
        class_path = cwd+name+'/'
        for img_name in os.listdir(class_path):
            img_path = class_path+img_name

            img = Image.open(img_path)
            img = img.resize((128, 128))
            img_raw = img.tobytes()
            # features=tf.train.Features({ 'label': tf.FixedLenFeature([], tf.int64), 'img_raw' : tf.FixedLenFeature([], tf.string)})
            img.save('./tmp.png')
            with tf.gfile.GFile('./tmp.png', 'rb') as fid:
                encoded_jpg = fid.read()
            # example = tf.train.Example(features)
            example = tf.train.Example(features=tf.train.Features(feature={
                # 'height': _int64_feature(height),
                # 'width': _int64_feature(width),
                'image_string': _bytes_feature(encoded_jpg),
                'label': _int64_feature([index])
            }))

            writer.write(example.SerializeToString())
            os.remove('./tmp.png')
    writer.close()


def read_and_decode(filename):  # Read TFRecord file
    filename_queue = tf.train.string_input_producer(
        [filename])  # genereate File sequence

    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)  # filenaes and file
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'image_string': tf.FixedLenFeature([], tf.string),
                                           'label': tf.FixedLenFeature([], tf.int64)
                                       })  # get features

    img = tf.decode_raw(features['img_string'], tf.uint8)
    img = tf.reshape(img, [128, 128, 3])  # reshapeto 128*128 3channel image
    img = tf.cast(img, tf.float32) * (1. / 255) - \
        0.5  # image tensor to image data
    label = tf.cast(features['label'], tf.int32)  # label tensor to label data
    return img, label


def test():
    cwd = './pic/test'
    filename_queue = tf.train.string_input_producer(
        ["./TFRecords/dog_train.tfrecords"])  
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue) 
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'label': tf.FixedLenFeature([], tf.int64),
                                           'img_raw': tf.FixedLenFeature([], tf.string),
                                       })  
    image = tf.decode_raw(features['img_raw'], tf.uint8)
    image = tf.reshape(image, [128, 128, 3])
    label = tf.cast(features['label'], tf.int32)
    with tf.Session() as sess:  
        init_op = tf.initialize_all_variables()
        sess.run(init_op)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        for i in range(20):
            example, l = sess.run([image, label])  
            img = Image.fromarray(example, 'RGB')  
            img.save(cwd+str(i)+'_''Label_'+str(l)+'.jpg') 
            print(example, l)
        coord.request_stop()
        coord.join(threads)


def main():
    write_TFRecord()
    img, label = read_and_decode("./TFRecords/dog_train.tfrecords")


if __name__ == '__main__':
    # main()
    test()
