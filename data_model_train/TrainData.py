import numpy as np
import pickle
import time
import cv2
import os

"""
Train Data
"""
#Green
#lowerBound = np.array([33,80,40])
#upperBound = np.array([102,255,255])

#White
lowerBound = np.array([0,0,240], dtype=np.uint8)
upperBound = np.array([255,15,255], dtype=np.uint8)

class TrainData(object):
	def __init__(self):
		self.image_array = [np.zeros((240,320,3))]
		self.label_array = [np.zeros((3))]
		self.labels = np.zeros((3,3))
		for i in range(3):
			self.labels[i,i] = 1
		self.labelcode = {'FORWARD':0,'LEFT':1,'RIGHT':2}

	def save(self):
		train = self.image_array[1:]
		label = self.label_array[1:]
		pickleDataPath = 'pickle'
		if not os.path.exists(pickleDataPath):
			os.makedirs(pickleDataPath)
		if(len(train) > 0):
			name = pickleDataPath+'/'+'data'+'.pkl'
			#print(label)
			with open(name,'wb') as f:
				print("writing model to file")
				pickle.dump([train, label], f)

	def load(self):
		pth = "data"
		for (dirpath, dirnames, filenames) in os.walk(pth):
			if len(filenames) != 0:
				dirnames = dirpath.split("\\")
				dirname = dirnames[len(dirnames)-1]
				print(dirname)
				for filename in filenames:
					print(dirpath+"/"+filename)
					#process(dirpath+"/"+filename, dirname, filename)
					#imgs_list.append(dirpath+"/"+filename)
					im = cv2.imread(dirpath+"/"+filename)
					img = cv2.resize(im, (320,240))
					imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
					mask = cv2.inRange(imgHSV, lowerBound, upperBound)
					#mask = cv2.bitwise_and(img, img, mask=mask1)
					#im = cv2.imread(dirpath+"/"+filename)
					im_array = np.zeros([1,240,320])
					im_array[0] = mask
					self.image_array.append(im_array)
					print(self.labelcode[dirname])
					self.label_array.append(self.labels[self.labelcode[dirname]])
					outDir = 'processedData/'+dirname
					if not os.path.exists(outDir):
						os.makedirs(outDir)
					cv2.imwrite(outDir+'/'+filename, mask)

print("Loading")
trainData = TrainData()
trainData.load()
trainData.save()
print("Finished Loading")