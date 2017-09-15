import random

import tensorflow as tf
import pandas as pd
import numpy as np

import model
import common
from process import get_dataset


FILEPATH = "/home/mory/data/captcha/all_data.csv"
SAMPLES = 3000
RATE = 0.8
SLICES_POINT = SAMPLES * RATE
def padding(X):
    """ pad the X make it become 2^N """
    XS = [np.pad(x.reshape(60, 250), ((2, 2), (3, 3)), 'constant', 
                 constant_values=(1, )) for x in X]
    XS = np.array(XS)
    return XS.reshape((-1, 64, 256, 1))
          

# training data
df, X_data, y_data = get_dataset(FILEPATH, SAMPLES)
X_data = padding(X_data)
# df = None 
index = list(range(SAMPLES))
random.shuffle(index)

X_train = X_data[index][:SLICES_POINT]
X_test = X_data[index][SLICES_POINT:]
y_train = y_data[index][:SLICES_POINT]
y_test = y_data[index][SLICES_POINT:]


x, y, params = model.get_training_model()
y_ = tf.placeholder(tf.float32, [None, 5 * len(common.CHARS)])


# train
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), 
                                              reduction_indices=[1]))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
# evaluate
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# commit training
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

BATCH_SIZE = 100
TRAIN_SIZE = X_train.shape[0]
train_index = list(range(TRAIN_SIZE))
saver = tf.train.Saver()
best_accuracy = 0

print('begin training..., train dataset size:{0}'.format(TRAIN_SIZE))
outputfile = open('log.txt', 'w')

for i in range(300):
    random.shuffle(train_index)  #每个epoch都shuffle一下效果更好
    X_train, y_train = X_train[train_index], y_train[train_index]

    for j in range(0,TRAIN_SIZE,BATCH_SIZE):
        print('epoch {0}, train {1} samples done...'.format(i,j))
        train_step.run(feed_dict={x:X_train[j:j+BATCH_SIZE], 
                                  y_:y_train[j:j+BATCH_SIZE]})

    current_accuracy = accuracy.eval(feed_dict={x:X_test, y_:y_test})
    if best_accuracy < current_accuracy:
        best_accuracy = current_accuracy
        saver.save(sess, "captcha.model", global_step=i)
    print("the accracy is: %.3f" % current_accuracy)
    print("epoch %d, accuracy: %.3f" % (i, current_accuracy), file=outputfile)
print("best accuracy: %.3f" % best_accuracy, file=outputfile)