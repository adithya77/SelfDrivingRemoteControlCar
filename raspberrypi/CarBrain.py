import keras.backend.tensorflow_backend
from keras.backend import clear_session
from keras.models import load_model
import tensorflow as tf
import threading
import time

"""
Predictions
"""
class CarBrain(object):
	def __init__(self):
		#Utils.print_log("Init. Model",1)
		print('Init carbrain')
		self.model = load_model('keras_model_0.001_learning_rate_32_batch_size_Adam_optimizer_88.0_acc.model')
		print('Init carbrain model loaded')
		self.graph = tf.get_default_graph()
		print('Init carbrain done')
			
	def get_direction(self,_image):
		#t = time.time()
		
		res =  self.model.predict(_image, batch_size=1)
		#t = Utils.print_log('Model Predict',3,t)
		
		#print(res)
		max_val = 0
		move = -1
		for idx,val in enumerate(res[0]):
			if val > max_val:
				max_val = val
				move = idx	

		direction = []
		if move == 0:
			direction = ['FORWARD']
		elif move == 1:
			direction = ['LEFT','FORWARD']
		elif move == 2:
			direction = ['RIGHT','FORWARD']
		return direction