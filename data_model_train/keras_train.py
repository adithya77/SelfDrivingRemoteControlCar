# import cv2
import time
import numpy as np
import glob
import pickle
# import cPickle

from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Lambda, Conv1D, MaxPooling2D, Dropout, Dense, Flatten
from keras.callbacks import ModelCheckpoint
from keras import optimizers

IMAGE_HEIGHT, IMAGE_WIDTH = 240, 320
SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH)


def load_file(_file):
	with open(_file,'rb') as f:  
		# t, l = pickle.load(f, encoding='latin1')
		t, l = pickle.load(f)
		# t, l = cPickle.loads(f)
	#print("labels", l)
	return t, l

def load_train_data():
	#load first to see total size
	t, l = load_file('pickle/data.pkl')

	train_size = len(t)
	print('\nTotal trainning data size: '+str(train_size))

	# Start array
	total_train = np.zeros([train_size,240,320])
	total_label = np.zeros([train_size,3])
	i = 0

	print('Array ready, start loading data')
	#t = []
	#l = []
	for index in range(len(t)):
		total_train[i] = t[index]
		total_label[i] = l[index]
		i += 1
		#print("loading arrays")
	#print(total_label)
	return total_train, total_label

print(">> Loading data...")
e0 = time.time()
X, y = load_train_data()

print((('Data loaded! X shape: %s and y shape: %s')%(X.shape,y.shape)),e0)

# Separate into Train and test
print(">> Separating test and train...")
e1 = time.time()

train, test, train_labels, test_labels = train_test_split(X,y, test_size = 0.2)
#print(train_labels)

print((('Train split successful! Train shape: %s and Train_label shape: %s \n')%(train.shape,train_labels.shape)),e1)

print(">> Defining model...")
e2 = time.time()


learning_rates = [0.001,0.0001,0.00001]
#learning_rates = [0.001]
batch_sizes = [32,64,128]
#batch_sizes = [128]
optz_choices = ['Adam','SGD']
#optz_choices = ['Adam']

# learning_rates = [0.01]
# batch_sizes = [128]
# optz_choices = ['SGD']




# Batch size  https://stats.stackexchange.com/questions/164876/tradeoff-batch-size-vs-number-of-iterations-to-train-a-neural-network
EPOCHS = 25
# EPOCHS = 1
# BATCH_SIZE = 32


# model_tests = [64,32,16,8,4,2]
# model_tests = [100,50]
# for idx,layer1 in enumerate(model_tests):
# 	for idx2 in range(idx,len(model_tests)):
# 		layer2 = model_tests[idx2]
# 		if layer1 != layer2:

for lr in learning_rates:
	for bs in batch_sizes:
		for optz in optz_choices:
			layer1 = 100
			layer2 = 50

			log = '\n'
			log += (('\n\n==========\nExecuting for %s layers and %s, with %s epochs, with %s learning rate, with %s batch size, with %s optimizer. Executed at %s')%(layer1,layer2,EPOCHS,lr,bs,optz,e2))

			# input_shape = (1,SHAPE,3)
			# Create model
			model = Sequential()
			model.add(Lambda(lambda x: x/127.5-1.0, input_shape=SHAPE))

			model.add(Conv1D(36, (5), activation='elu', strides=(2)))
			model.add(Conv1D(24, (5), activation='elu', strides=(2)))
			model.add(Conv1D(48, (5), activation='elu', strides=(2)))
			model.add(Conv1D(64, (3), activation='elu'))
			model.add(Conv1D(64, (3), activation='elu'))

			model.add(Dropout(0.5))
			model.add(Flatten())

			model.add(Dense(layer1, input_dim=SHAPE, activation='elu'))
			model.add(Dense(layer2, activation='elu'))
			model.add(Dense(3))

			print(model.summary())
			print("Model defined!",e2)

			print(">> Compiling model...")
			e3 = time.time()

			# Compile model
			# learn_rate = 0.001
			learn_rate = lr
			BATCH_SIZE = bs
			if (optz == 'SGD'):
				opt = optimizers.SGD(lr=learn_rate)
			else:
				opt = optimizers.Adam(lr=learn_rate)

			model.compile(loss='mean_squared_error', optimizer=opt, metrics=['accuracy'])

			checkpoint = ModelCheckpoint('model-{epoch:03d}.h5',
								 monitor='val_loss',
								 verbose=0,
								 save_best_only=True,
								 mode='auto')

			print("Model compiled!", e3)

			print(">> Fiting model...")
			e4 = time.time()
			# Fit the model
			model.fit(train
					, train_labels
					, validation_data=(test, test_labels)
					, epochs=EPOCHS
					, batch_size=BATCH_SIZE
					, verbose=1)
			log += (('\n 	Train time: %s')%(time.time() - e4))
			print("Fit finished!", e4)

			print(">> Evaluating model...")
			e5 = time.time()

			# Evaluate
			scores_train = model.evaluate(train, train_labels)
			eval_train = (("\n 	Evaluate Train: %s: %.2f%%") % (model.metrics_names[1], scores_train[1]*100))
			log += '\n'+eval_train
			print(eval_train)

			# Evaluate
			scores_test = model.evaluate(test, test_labels)
			eval_test = (("\n 	Evaluate Test: %s: %.2f%%") % (model.metrics_names[1], scores_test[1]*100))
			log += '\n'+eval_test
			print(eval_test)

			log += (('\n\n 	Total time: %s')%(time.time() - e2))

			print("Evaluation finished!", e5)

			print(">> Saving model...")
			e6 = time.time()

			# save to json
			name = 'keras_model_'+str(lr)+'_learning_rate_'+str(bs)+'_batch_size_'+(optz)+'_optimizer_'+str(round(scores_test[1]*100))+'_acc'
			# name = MODEL_PATH+'keras_model_'+str(layer1)+'_'+str(layer2)+'_layers_'+str(EPOCHS)+'_epochs_'+str(round(scores_test[1]*100))+'_acc'
			log += (('\n\n 	saved with name "%s"')%(name))
			fileName = name+".model"
			print("saving to file --> ", fileName)
			model.save(fileName)

			# model_json = model.to_json()
			# with open(name+'.json','w') as json_file:
			# 	json_file.write(model_json)

			with open('models_log.txt','a') as log_file:
				log_file.write(log)

			print("Model saved!", e6)

print("Finished!!", e0)
