
import tensorflow as tf

def earth_movers_distance(y_true, y_pred):
    cdf_true = tf.cumsum(y_true, axis=-1)
    cdf_pred = tf.cumsum(y_pred, axis=-1)
    emd = tf.sqrt(tf.reduce_mean(tf.square(cdf_true - cdf_pred), axis=-1))
    return tf.reduce_mean(emd)
