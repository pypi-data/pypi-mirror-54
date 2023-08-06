import tensorflow as tf

tf.enable_eager_execution()


def just_add_tfe():
    vec = tf.random.uniform(shape=(3,))
    out1 = vec + 1
    out2 = vec + 2
    print(out1, out2)
