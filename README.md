**Selfdriving RC Car**

In this project I've used relays to control the car which not a very good idea but it is easy for me to start with as I don't have great understanding of the controller in that RC car.

Below is the car I've bought in amazon and broke it and connected it to raspberry pi using relay switch.
https://www.amazon.in/AJUDIYA-ENTERPRISE-Rechargeable-Crawler-Monster/dp/B081X18S33

---

## Prerequisites

1. Install python3
2. Install opencv2 in the raspberrypi
3. Install tensorflow and keras

Below is the GPIO PINS configuration
1. 'FORWARD':32 
2. 'BACKWARD':35
3. 'LEFT':31
4. 'RIGHT':33}

These pins will be activated when the direction is predicted. So the raspberry pi should be ready to accept the values and move the car in that direction when the respective PIN is activated.

---

## Steps to run

**Step 1** : Capture Data
	How to generate training data here. We need to control the car manually in the path and parallely record the data.
	What is the data we record -
	For every movement of the car we capture an image of the path infornt of the car and record it with Label as the direction the car is moving.
	
	Command - python3 raspberrypi/captureData.py
	
**Step 2**: Flip Data
	In this step we are creating more data with the existing data.
	For example there is an image for left turn. In that case we flip the image and record it as a new train data for right. This way we can generate more traiing data.
	
	Command - python3 data_model_train/FlipData.py

**Step 3**:  Generate Train Data
	This is the crucial step we shoud create training data from the images captured. Here we load all the images and labels into a pickle package which would be easy for training. This step is optional, you can modify the training code to directly use the images, but this is recommended.
	
	command - python3 data_model_train/TrainData.py
	
**Step 4**: Training the model
	This step will use the generated pickle data from step 3. It will train using mulitple optimizers and multiple learning rates and generates all the models with accuracy in the name of the file. Based on the highest accuracy we can pick the model and proceed to next step.
	
	command - python3 keras_train.py
	
**Step 5**: Testing with the RC car
	
	command - python3 raspberrypi/SelfDrive.py

---
