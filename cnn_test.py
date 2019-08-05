# -*- coding: utf-8 -*
import tensorflow as tf
import numpy as np
import logging
from logging.handlers import RotatingFileHandler

def read_and_decode(filename_queue):
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)  # 返回文件名和文件
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'wordMatrix': tf.FixedLenFeature([40000], tf.float32),
                                           'label': tf.FixedLenFeature([10], tf.int64),
                                       })
    wordMatrix = features['wordMatrix']
    label = features['label']
    return wordMatrix, label


def batchreader(filenames, batch_size, read_threads, num_epochs=None):
    filename_queue = tf.train.string_input_producer(filenames, num_epochs=num_epochs, shuffle=True)
    featurelists, labels = read_and_decode(filename_queue)
    min_after_dequeue = 1000
    capacity = min_after_dequeue + 3 * batch_size
    featurelists_batch, labels_batch = tf.train.shuffle_batch([featurelists, labels], batch_size=batch_size,
                                                              capacity=capacity, min_after_dequeue=min_after_dequeue,
                                                              num_threads=read_threads)
    return featurelists_batch, labels_batch



def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='VALID')



def max_pool_one(x):
    return tf.nn.max_pool(x, ksize=[1, 198, 1, 1], strides=[1, 1, 1, 1], padding='VALID')


if __name__ == "__main__":

    logger = logging.getLogger()
    fh = logging.FileHandler('./test.log', 'w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    xs = tf.placeholder("float", [None, 200 * 200])
    ys = tf.placeholder("float", [None, 10])
    x_wordMatrix = tf.reshape(xs, [-1, 200, 200, 1])
    # 卷积层，卷积核高度3，宽度200，跟词向量矩阵一样，个数是128个
    W_conv = weight_variable([3, 200, 1, 128])
    b_conv = bias_variable([128])
    # 原矩阵200*200*1，卷积后198*1*128
    h_conv = tf.nn.relu(conv2d(x_wordMatrix, W_conv) + b_conv)
    # 池化层，池化之后,1*1*128
    h_pool = max_pool_one(h_conv)

    # 全连接层
    W_fc1 = weight_variable([1 * 1 * 128, 64])
    b_fc1 = bias_variable([64])
    h_pool_flat1 = tf.reshape(h_pool, [-1, 1 * 1 * 128])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool_flat1, W_fc1) + b_fc1)

    # dropout操作，避免过拟合
    keep_prob = tf.placeholder("float")
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # 输出层，softmax归一化处理
    W_fc2 = weight_variable([64, 10])
    b_fc2 = bias_variable([10])
    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    cross_entropy = -tf.reduce_sum(ys * tf.log(y_conv))
    # 此函数是Adam优化算法：是一个寻找全局最优点的优化算法，引入了二次方梯度校正。
    # 相比于基础SGD算法，不容易陷于局部优点，速度更快
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    # 计算准确率
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(ys, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    word_matrix_batch, label_batch = batchreader(["train_1000.tfrecords"], 10, 3)
    test_wordmatrix_batch, test_label_batch = batchreader(["test_100.tfrecords"], 10, 3)
    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
    with tf.Session() as sess:
        sess.run(init_op)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        test_accuracy = 0
        try:
            logger.error("Training.............................................\n\r")
            for i in range(5000):
                word_matrix, label = sess.run([word_matrix_batch, label_batch])
                if i %  50== 0:
                    train_accuracy = accuracy.eval(feed_dict={xs: word_matrix, ys: label, keep_prob: 1.0})
                    logger.error("step %d, training accuracy %g \n\r" % (i, train_accuracy))
                train_step.run(feed_dict={xs: word_matrix, ys: label, keep_prob: 0.5})
            logger.error("Testing.............................................\n\r")
            for j in range(1000):
                test_word_matrix, test_label = sess.run([test_wordmatrix_batch, test_label_batch])
                tmp_test_accuracy = accuracy.eval(feed_dict={xs: test_word_matrix, ys: test_label, keep_prob: 1.0})
                test_accuracy = tmp_test_accuracy + test_accuracy
                if j % 50 == 0:
                    logger.error("step %d, testing accuracy %g \n\r" % (j, tmp_test_accuracy))
            logger.error("The whole testing accuracy %g \n\r" % (test_accuracy/1000))
        except tf.errors.OutOfRangeError:
            logger.error('Done training -- epoch limit reached')
        finally:
            coord.request_stop()
            coord.join(threads)
            sess.close()
            
            
            
            111111111111111111
