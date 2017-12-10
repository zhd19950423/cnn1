# -*- coding: utf-8 -*
import tensorflow as tf
import numpy as np
import logging
from logging.handlers import RotatingFileHandler
def trans2tfRecord(trainFileX,trainFileY,name):
    fx = open(trainFileX, 'r')
    fy = open(trainFileY, 'r')
    filename = name + '.tfrecords'
    writer = tf.python_io.TFRecordWriter(filename)
    count = 0
    while 1:
        wordMatrix = fx.readline()
        label = fy.readline()
        if label != '':
            wordMatrix = wordMatrix.strip('\n')
            wordMatrix = wordMatrix.split(' ')
            wordMatrix = [float(w) for w in wordMatrix ]
            label= int(label[0:1])
            a_label = _transLabel2Array(label)
            example = tf.train.Example(features=tf.train.Features(feature={
                 'wordMatrix': _float_feature(wordMatrix),
                 'label': _int64_feature(a_label)
            }))
            writer.write(example.SerializeToString())
        else:
            break
    fx.close()
    fy.close()
    writer.close()

def _transLabel2Array(label):
    if label == 0:
        a_label = [1,0,0,0,0,0,0,0,0,0]
    elif label == 1:
        a_label = [0,1,0,0,0,0,0,0,0,0]
    elif label == 2:
        a_label = [0,0,1,0,0,0,0,0,0,0]
    elif label == 3:
        a_label = [0,0,0,1,0,0,0,0,0,0]
    elif label == 4:
        a_label = [0,0,0,0,1,0,0,0,0,0]
    elif label == 5:
        a_label = [0,0,0,0,0,1,0,0,0,0]
    elif label == 6:
        a_label = [0,0,0,0,0,0,1,0,0,0]
    elif label == 7:
        a_label = [0,0,0,0,0,0,0,1,0,0]
    elif label == 8:
        a_label = [0,0,0,0,0,0,0,0,1,0]
    elif label == 9:
        a_label = [0,0,0,0,0,0,0,0,0,1]
    return a_label
def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

if __name__ == "__main__":
    logger = logging.getLogger()
    fh = logging.FileHandler('./test.log', 'w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    trans2tfRecord('testX.txt','testY.txt','test_100')