import tensorflow as tf

WORDVECDEM = 100
GRAM_K = 3

INPUT_NODE = 1000
HIDDEN_ONE = 200
OUTPUT_NODE = 2

BATCH_SIZE = 50
READ_THREADS = 3

LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY = 0.99
REGULARIZATION_RATE = 0.0001
TRAINING_STEPS = 10000
TEST_STEPS = 2000
MOVING_AVERAGE_DECAY = 0.99

TRAIN_INPUT_FILE = "training.txt.tfrecords"
TEST_INPUT_FILE = "test.txt.tfrecords"

def file_reader(filename_queue):
  reader = tf.TFRecordReader()
  _, serialized_example = reader.read(filename_queue)
  features = tf.parse_single_example(
    serialized_example,
    # Defaults are not specified since both keys are required.
    features={
        'label': tf.FixedLenFeature([2], tf.float32),
		'values': tf.VarLenFeature(tf.float32)
    })
  label = features['label']
  featurelist = features['values']
  return label, featurelist

def batchreader(filenames, batch_size, read_threads, num_epochs=None):
  filename_queue = tf.train.string_input_producer(filenames, num_epochs=num_epochs, shuffle=True)
  labels, featurelists = file_reader(filename_queue)
  min_after_dequeue = 1000
  capacity = min_after_dequeue + 3 * batch_size
  labels_batch, featurelists_batch = tf.train.shuffle_batch([labels, featurelists], batch_size=batch_size, capacity=capacity, min_after_dequeue=min_after_dequeue, num_threads=read_threads)
  dense_values = tf.sparse_to_dense(featurelists_batch.indices, featurelists_batch.dense_shape, featurelists_batch.values)
  return labels_batch, dense_values

def inference(input_featuers, avg_class, weights1, weights2, biases2, weights3, biases3):
  lines = []
  for index in range(BATCH_SIZE):
    line_index = input_featuers[index]
    line_index_reshape = tf.reshape(line_index, [-1, WORDVECDEM*GRAM_K*2])
    line = []
    for pair_index in range(8244):
      try:
        pair = line_index_reshape[pair_index]
        pair_reshape = tf.reshape(pair, [WORDVECDEM, GRAM_K*2])
        pair_trans = tf.matmul(pair_reshape, weights1)
        if line == []:
          line = pair_trans
        else:
          line = tf.concat([line, pair_trans], 0)
      except Exception:
        break
    line = tf.reshape(line, [-1, WORDVECDEM, INPUT_NODE])
    line = tf.reduce_mean(line, 0)
    line = tf.reshape(line, [-1])
    if lines == []:
      lines = line
    else:
      lines = tf.concat([lines, line], 0)
  lines = tf.reshape(lines, [-1, WORDVECDEM*INPUT_NODE])
  if avg_class == None: 
    hidden1 = tf.tanh(tf.matmul(lines, weights2) + biases2)
    return tf.tanh(tf.matmul(hidden1, weights3) + biases3)
  else:
    hidden1 = tf.tanh(tf.matmul(lines, avg_class.average(weights2)) + avg_class.average(biases2))
    return tf.tanh(tf.matmul(hidden1, avg_class.average(weights3)) + avg_class.average(biases3))

def main(argv=None):
  ################multi threads readersess = tf.Session()
  #coord = tf.train.Coordinator()
  #threads = tf.train.start_queue_runners(sess=sess, coord=coord)
  #
  default_x = [[0 for i in range(600)] for j in range(5)]
  x = tf.placeholder_with_default(default_x, [None, None])
  y_ = tf.placeholder(tf.float32, [None, 2])
  weights1 = tf.Variable(tf.truncated_normal([GRAM_K*2, INPUT_NODE], stddev=0.1))
  weights2 = tf.Variable(tf.truncated_normal([WORDVECDEM*INPUT_NODE, HIDDEN_ONE], stddev=0.1))
  biases2 = tf.Variable(tf.constant(0.1, shape=[HIDDEN_ONE]))
  weights3 = tf.Variable(tf.truncated_normal([HIDDEN_ONE, OUTPUT_NODE], stddev=0.1))
  biases3 = tf.Variable(tf.constant(0.1, shape=[OUTPUT_NODE]))
  y = inference(x, None, weights1, weights2, biases2, weights3, biases3)
  global_step = tf.Variable(0, trainable=False)
  variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
  variables_averages_op = variable_averages.apply(tf.trainable_variables())
  average_y = inference(x, variable_averages, weights1, weights2, biases2, weights3, biases3)
  cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y)
  cross_entropy_mean = tf.reduce_mean(cross_entropy)
  regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
  regularization = regularizer(weights3) + regularizer(weights2)
  loss = cross_entropy_mean + regularization
  learning_rate= tf.train.exponential_decay(LEARNING_RATE_BASE, global_step, 5000 / BATCH_SIZE, LEARNING_RATE_DECAY)
  train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step = global_step)
  train_op = tf.group(train_step, variables_averages_op)
  correct_prediction = tf.equal(tf.argmax(average_y, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  
  sess = tf.InteractiveSession()
  labels_input, values_input = batchreader([TRAIN_INPUT_FILE], BATCH_SIZE, READ_THREADS)
  test_labels_input, test_values_input = batchreader([TEST_INPUT_FILE], BATCH_SIZE, READ_THREADS)
  coord = tf.train.Coordinator()
  threads = tf.train.start_queue_runners(sess=sess, coord=coord)
  
  init = tf.global_variables_initializer()
  sess.run(init)

  for _ in range(TRAINING_STEPS):
    numpy_values, numpy_labels = sess.run([values_input, labels_input])
    sess.run(train_op, feed_dict={x: numpy_values, y_: numpy_labels})
    
  result = open('result', 'a')
  test_accuracy = 0
  for __ in range(TEST_STEPS):
    test_numpy_values, test_numpy_labels = sess.run([test_values_input, test_labels_input])
    tmp_test_accuracy = sess.run(accuracy, feed_dict={x: test_numpy_values, y_: test_numpy_labels})
    test_accuracy = tmp_test_accuracy + test_accuracy
    if __ % 20 == 0:
      result.write("average accuracy is %.4f when steps is %g\n" % (tmp_test_accuracy, (__+1)))
  result.write("accuracy is %.4f\n" % (test_accuracy/TEST_STEPS))
  result.close()
  coord.request_stop()
  coord.join(threads)


if __name__ == '__main__':
  tf.app.run()
