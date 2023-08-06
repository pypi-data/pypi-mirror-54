import tensorflow as tf


def just_add():
    with tf.Session() as sess:
        vec = tf.random.uniform(shape=(3,))
        out1 = vec + 1
        out2 = vec + 2
        print(sess.run((out1, out2)))
