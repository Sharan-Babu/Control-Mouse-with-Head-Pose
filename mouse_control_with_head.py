# Python program to control mouse based on head position (4 directional)
# Trained a CNN model that predicts 4 head poses (left,right,up and down)

# Import necessary modules
import numpy as np
import cv2
from time import sleep
import tensorflow.keras
from keras.preprocessing import image
import tensorflow as tf
import pyautogui

# Using laptop's webcam as source of video
cap = cv2.VideoCapture(0)

# Labels - The various possibilities
labels = ['Left','Right','Up','Down','Neutral']

# Loading the model weigths
model = tensorflow.keras.models.load_model('keras_model.h5')

while True:

	success, image = cap.read()

	if success == True:
		# Necessary to avoid conflict between left and right
		image = cv2.flip(image,1)
        
		cv2.imshow("Frame",image)

		# The model takes an image of dimensions (224,224) as input so let's reshape our img to the same.
		img = cv2.resize(image,(224,224))
		
        # Convert the image to a numpy array
		img = np.array(img,dtype=np.float32)
		
		img = np.expand_dims(img,axis=0)
		
        # Normalizing
		img = img/255
		
        # Predict the class
		prediction = model.predict(img)
		
        # Map the prediction to a class name
		predicted_class = np.argmax(prediction[0], axis=-1)
		predicted_class_name = labels[predicted_class]
		

		# Using pyautogui to get the current position of the mouse and move accordingly
		current_pos = pyautogui.position()
		current_x = current_pos.x
		current_y = current_pos.y

		print(predicted_class_name)

		if predicted_class_name == 'Neutral':
			sleep(1)
			continue
		elif predicted_class_name == 'Left':
		    pyautogui.moveTo(current_x-80,current_y,duration=1)
		    sleep(1)
		elif predicted_class_name == 'Right':
		    pyautogui.moveTo(current_x+80,current_y,duration=1)
		    sleep(1)
		elif predicted_class_name == 'Down':
		    pyautogui.moveTo(current_x,current_y+80,duration=1)
		    sleep(1)
		elif predicted_class_name == 'Up':
		    pyautogui.moveTo(current_x,current_y-80,duration=1)
		    sleep(1)  
		           	

	# Close all windows if one second has passed and 'q' is pressed
	if cv2.waitKey(1) & 0xFF == ord('q'):
	    break

# Release open connections
cap.release()
cv2.destroyAllWindows()	    	