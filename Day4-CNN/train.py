# -*- coding: utf-8 -*-
'''
train mnist

image is grayscale with 28*28 size.
'''

# 导入包
from lenet import LeNet
from keras.datasets import mnist
from keras.optimizers import Adam
from keras.optimizers import RMSprop
from keras.utils import np_utils
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from loader import  SimpleDatasetLoader
from processor import SimplePreprocessor
from imutils import paths
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# 全局常量
LR = 0.0005
BATCH_SIZE = 128
EPOCHS = 10

TARGET_IMAGE_WIDTH = 48
TARGET_IMAGE_HEIGHT = 48

# 全局变量
accuracy_plot_path = 'plots/accuracy.png'
loss_plot_path = 'plots/loss.png'
output_model_path = 'models/face_expression.hdf5'
dataset_path = 'dataset'

#initialize utils
sp = SimplePreprocessor(TARGET_IMAGE_WIDTH, TARGET_IMAGE_HEIGHT)
sdl = SimpleDatasetLoader(preprocessors=[sp])

################################################
# 第一部分：数据预处理
# grab the MNIST dataset
#print('[INFO] 下载数据集...')
#((trainData, trainLabels), (testData, testLabels)) = mnist.load_data()

# matrix shape should be: num_samples x rows x columns x depth
#trainData = trainData.reshape((trainData.shape[0], 28, 28, 1))
#testData = testData.reshape((testData.shape[0], 28, 28, 1))

# scale data to the range of [0,1]
#trainData = trainData.astype('float32') / 255.0
#testData = testData.astype('float32') / 255.0

# transform the training and testing labels into vectors
#in the range [0, classes]
#trainLabels = np_utils.to_categorical(trainLabels, 10)
#testLabels = np_utils.to_categorical(testLabels, 10)

# Load images
print("[INFO] loading images...")
image_paths = list(paths.list_images(dataset_path)) # path included
(X, y) = sdl.load(image_paths, verbose=500, grayscale = True)

# Flatten (reshape the data matrix)
# convert from (13164,32,32) into (13164,32*32)
X = X.reshape((X.shape[0], TARGET_IMAGE_WIDTH,TARGET_IMAGE_HEIGHT,1))
X = X.astype("float") / 255.0

# Show some information on memory consumption of the images
print("[INFO] features matrix: {:.1f}MB"
      .format(X.nbytes / (1024 * 1024.0)))

# Label encoder
le = LabelEncoder()
y = to_categorical(le.fit_transform(y), 3)

# 拆分数据集
(X_train, X_test, y_train, y_test) = train_test_split(X, y,
                                                      test_size=0.05,
                                                      random_state=42)


################################################3
# 第二部分：创建并训练模型
# initialize the optimizer and model
print('[INFO] 编译模型...')
opt = RMSprop(lr = LR)
model = LeNet.build(48,48,3,'',1)
model.compile(loss = 'categorical_crossentropy',
              optimizer=opt, metrics = ['accuracy'])

# train model
print('[INFO] 训练模型...')
H = model.fit(X_train, y_train,
              validation_data=(X_test, y_test),
              batch_size = BATCH_SIZE, epochs = EPOCHS, verbose = 1)


################################################
# 第三部分：评估模型

# 画出accuracy曲线
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(1, EPOCHS+1), H.history["acc"], label="train_acc")
plt.plot(np.arange(1, EPOCHS+1), H.history["val_acc"],label="val_acc")
plt.title("Training Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Accuracy")
plt.legend()
plt.savefig(accuracy_plot_path)

# 画出loss曲线
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(1,EPOCHS+1),H.history["loss"], label="train_loss")
plt.plot(np.arange(1,EPOCHS+1),H.history["val_loss"],label="val_loss")
plt.title("Training Loss")
plt.xlabel("Epoch #")
plt.ylabel("Loss")
plt.legend()
plt.savefig(loss_plot_path)

# 打印分类报告
# show accuracy on the testing set
print('[INFO] 评估模型...')
predictions = model.predict(X_test, batch_size=32)
print(classification_report(y_test.argmax(axis=1),
	                        predictions.argmax(axis=1),
                            target_names=[str(i) for i in range(2)]))


################################################
# 第四部分：保存模型
model.save(output_model_path)