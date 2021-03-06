import tensorflow as tf
import numpy as np
import datetime
import os
import json
from azure.storage.file import FileService

SAVER = "saver"
SAVER_FOLDER = "./" + SAVER
TRAIN_DATA = "data-04-zoo.csv"
RESULT_FILE = 'result.json'
FILE_SHARE = 'meltingpang-savedata'

for file in os.listdir(SAVER_FOLDER):
    os.remove(SAVER_FOLDER + "/" + file);

file_service = FileService(account_name='meltingpang', account_key='aS/W8kwqNXDicJgQNnobqkWItcr9vNW3+KO8n+V5qRqY0X3Z+XGBS1sUeLfYtyneUwaose59rbhEziPpFs2qKw==')

file_service.get_file_to_path(FILE_SHARE, None, TRAIN_DATA, TRAIN_DATA)
file_service.create_directory(FILE_SHARE, SAVER);

xy = np.loadtxt(TRAIN_DATA, delimiter=',', dtype=np.float32)
x_data = xy[:,0:-1]
y_data = xy[:,[-1]]
nb_classes = 7

X = tf.placeholder(tf.float32, [None, 16])
Y = tf.placeholder(tf.int32, [None, 1])

Y_one_hot = tf.one_hot(Y, nb_classes)
Y_one_hot = tf.reshape(Y_one_hot, [-1, nb_classes])

W = tf.Variable(tf.random_normal([16, nb_classes]), name='weight')
b = tf.Variable(tf.random_normal([nb_classes]), name='bias')

logits = tf.matmul(X,W) + b
hypothesis = tf.nn.softmax(logits)
cost_i = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y_one_hot)
cost = tf.reduce_mean(cost_i)
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)


prediction = tf.argmax(hypothesis, 1)
correct_prediction = tf.equal(prediction, tf.argmax(Y_one_hot, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    
    for step in range(2001):
        sess.run(optimizer, feed_dict={X: x_data, Y: y_data})
        if step % 100 == 0:
            print(step, sess.run([cost, accuracy], feed_dict={X: x_data, Y: y_data}))

    saver.save(sess,"./saver/save.{}.ckpt".format(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")))
    saver.save(sess,"./saver/save.last.ckpt")

    pred = sess.run(prediction, feed_dict={X: x_data})

    pw, pb = sess.run([W, b])
    result = {'W': pw.tolist(), 'b': pb.tolist()}
    print(result)

    with open(RESULT_FILE, 'w') as outfile:
        json.dump(result, outfile)

    for p, y in zip(pred, y_data.flatten()):
        print("[{}] Prediction: {} True Y: {}".format(p == int(y), p, int(y)))

file_service.create_file_from_path(FILE_SHARE, None, RESULT_FILE, RESULT_FILE)

for file in os.listdir(SAVER_FOLDER):
    print(file)
    file_service.create_file_from_path(FILE_SHARE, "saver", file, SAVER_FOLDER + "/" + file)
    