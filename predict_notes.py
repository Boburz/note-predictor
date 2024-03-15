# reads csv-file with images of bars and predicts note names

import os
from pathlib import Path
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import numpy as np

# recieves number "num" and returns respective note name
# 0->c, 1->d, etc
def number_to_note(num):
    note_list = 'cdefgabC'
    return note_list[num]

########################################################################
########################################################################
########################################################################

# separate lines
os.system('python py\\separate_lines.py')

# separate bars
os.system('python py\\separate_bars.py')

# turn images to csv
os.system('python py\\image_to_csv.py')

########################################################################
########################################################################
########################################################################

print('Predicting note names...')

# load model for the NN
model = load_model('NN_model')

# load notes from csv-file
predict_data_file = open("grayscales.csv", "r")
X_data_lines = predict_data_file.readlines()
X_data_list = [line.split(",") for line in X_data_lines]
predict_data_file.close()

X_data_scaled = []
for image in X_data_list:
    X_data_scaled.append([int(x) / 255 for x in image])

# make predictions
predictions = model.predict(X_data_scaled, verbose=0)
y_predicted_notes = [number_to_note(np.argmax(i)) for i in predictions]

# print predictions
print('')
print('Predicted notes: ', end='')
for note in y_predicted_notes:
    print(note, end=' ')
print('')
print('')











