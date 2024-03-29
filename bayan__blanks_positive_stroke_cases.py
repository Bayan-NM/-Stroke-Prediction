# -*- coding: utf-8 -*-
"""Bayan_ Blanks_Positive_Stroke_Cases.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14ej1yldIY0o8n3YCtkuk0JHKNX3MxzVQ

# Full DL Solution
---
### **Case Study:** Stroke Prediction

**Objective:** The goal of this project is to walk you through a case study where you can apply the deep learning concepts that you learned about during the week. By the end of this project, you would have developed a solution that predicts if a person will have a stroke or not.

**Dataset Explanation:** We will be using the stroke dataset. Its features are:


* **id:** unique identifier
* **gender:** "Male", "Female" or "Other"
* **age:** age of the patient
* **hypertension:** 0 if the patient doesn't have hypertension, 1 if the patient has hypertension
* **heart_disease:** 0 if the patient doesn't have any heart diseases, 1 if the patient has a heart disease
* **ever_married:** "No" or "Yes"
* **work_type:** "children", "Govt_jov", "Never_worked", "Private" or "Self-employed"
* **Residence_type:** "Rural" or "Urban"
* **avg_glucose_level:** average glucose level in blood
* **bmi:** body mass index
* **smoking_status:** "formerly smoked", "never smoked", "smokes" or "Unknown"*
* **stroke:** 1 if the patient had a stroke or 0 if not

# Importing Libraries

We start by importing the libraries
"""

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""# Loading the Dataset

We load the dataset from a csv file, and see its first rows
"""

path = '/content/healthcare-dataset-stroke-data.csv'
data = pd.read_csv(path)
data.head()

"""# Exploratory Data Analysis

Now we start the exploratory data analysis.

### Shape of the data

First thing we need to know the shape of our data

**Question 1:** How many examples and features do we have?
"""

nrow = data.shape[0]
ncol = data.shape[1]


print(nrow, ncol)

"""### Types of different Columns

**Question 2:** Check the type of each feature.
"""

data.info()

"""### Dealing with categorical variables

**Question 3:** Use the .value_counts() functions to walk through the categorical variables that we have to see the categories and the counts of each of them.
"""

smoking_types =data['smoking_status'].value_counts()
smoking_types

residence_types =data ['Residence_type'].value_counts()
residence_types

work_types = data['work_type'].value_counts()
work_types

married_types = data['ever_married'].value_counts()
married_types

hypertension = data['hypertension'].value_counts()
hypertension

heart_disease= data['heart_disease'].value_counts()
heart_disease

stroke= data['stroke'].value_counts()
stroke

"""# Preprocessing

### Dealing with Nulls

**Question 4:** The bmi column contains nulls. Fill it with the appropriate measure.
"""

data['bmi'].fillna( value=data['bmi'].mean(), inplace=True)

"""#### Encoding Categorical Features

**Question 5:** Here you have to encode those categorical variables to be able to use them to train your DL model.
"""

from sklearn import preprocessing

encoder = preprocessing.LabelEncoder()
data['smoking_status'] = encoder.fit_transform(data['smoking_status'])
data['Residence_type'] = encoder.fit_transform(data['Residence_type'])
data['work_type'] = encoder.fit_transform(data['work_type'])
data['ever_married'] = encoder.fit_transform(data['ever_married'])
data['gender'] = encoder.fit_transform(data['gender'])

"""### Normalizing Features

**Question 6:** Normalize the input data
"""

data = (data - data.min()) / (data.max() - data.min())
data.describe()

"""### Removing Unnecessary Features

**Question 7:** From the features that you have, remove the feature(s) that is(are) irrelevant to your predictions.
"""

data = data.drop('id', axis=1)

"""# Building the DL Model

**Question 8:** Now it's time to build the actual model, and observe a summary of it.
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


model = Sequential()
model.add(Dense(32, input_dim=10, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(4, activation='relu'))
model.add(Dense(2, activation='relu'))
model.add(Dense(1, activation='sigmoid'))


model.summary()

"""### Compiling the model

**Question 9:**  Now we compile the model. Here we want to measure the accuracy as well as the precision and recall to know better about the performance of our model.
"""

model.compile(optimizer= 'adam',loss= 'binary_crossentropy' ,metrics=['Accuracy','Precision','Recall' ])

"""### Fitting the model

**Question 10:** Split the data and train the model

We take the first columns as features and the last column as a label, then we split our dataset between training (70%) and testing (30%).
"""

from sklearn.model_selection import train_test_split
x = data.iloc[:, :-1]
y = data.iloc[:, -1]


x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.3, stratify=y)

"""we fit the model on 80% training data, and validate on the rest. Later we will do the final test on the test data. The training happens for 15 epochs."""

history = model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=15)

"""# Improving DL Models

**Question 11:** Suggest ways to improve your model

### Checking For Data Imbalance

We check for imbalance because we have a poor recall and precision.
"""

data['stroke'].hist()

"""We have a huge imbalance in the data, this is why we fix it with oversamppling and undersampling.

We will oversample this time using the SMOTE() function instead of random oversampling, and this is because SMOTE will generate new data based on the data that we have, so we avoid overfitting.
"""

from imblearn.over_sampling import SMOTE

over = SMOTE()
x_new, y_new = over.fit_resample(x, y)


plt.hist([y_new])

"""Split the balanced dataset between 90% (training and validation), 10% testing
Then divide the 90% between 80% training and 20% validation
"""

from sklearn.model_selection import train_test_split


x_train_val, x_test, y_train_val, y_test = train_test_split(x_new, y_new, test_size=0.1, stratify=y_new)
x_train, x_val, y_train, y_val = train_test_split(x_train_val, y_train_val, test_size=0.2, stratify=y_train_val)

"""Now we will train the model on the balanced data, and tune it on the validation set"""

history = model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=15)

"""Evaluate your model on the test set that you kept aside at the beginning."""

model.evaluate(x_val, y_val)

"""We see that the performance gets better when our data became balanced.
Now we will try improving our model with other techniques that we learned through the week.

### Model Design

We will introduce batch normalization after each layer and then train the model
"""

from tensorflow.keras.layers import BatchNormalization
model = Sequential()

model.add(Dense(32, input_dim=10, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(16, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(8, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(4, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(2, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(1, activation='sigmoid'))

model.summary()

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', 'Precision', 'Recall'])

history2 = model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=15)

model.evaluate(x_val, y_val)

"""We see that we are achieving better metrics with batch normalization."""