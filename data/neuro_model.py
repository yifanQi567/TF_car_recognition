import tensorflow as tf

from data.dataset import ImageSet


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

class Neuro(object):
    def run(self):
        x = tf.placeholder(tf.float32, shape=[None, 64 * 64])

        W = tf.Variable(tf.zeros([64 * 64, 2]))
        b = tf.Variable(tf.zeros([2]))

        # model on it's own
        y = tf.nn.softmax(tf.matmul(x, W) + b)

        # correct values
        y_ = tf.placeholder(tf.float32, [None, 2])

        cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

        train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

        sess = tf.InteractiveSession()

        tf.global_variables_initializer().run()

        # train model
        for i in range(1000):
            print('Started {} training'.format(i + 1))
            batch_xs, batch_ys = ImageSet.get_batch(amount=100)
            sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        test_xs, test_ys = ImageSet.get_batch(test=True)
        print(sess.run(accuracy, feed_dict={x: test_xs, y_: test_ys}))
