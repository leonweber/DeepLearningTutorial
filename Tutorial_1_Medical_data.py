import sys; print('Python %s on %s' % (sys.version, sys.platform))

# Create first network with Keras
from keras.models import Sequential
from keras.layers import Dense
import numpy
import urllib2
from sklearn.metrics import confusion_matrix
from os.path import expanduser

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# load pima indians dataset and store to disk
url = 'https://github.com/RaikOtto/DeepLearningTutorial/raw/master/pima-indians-diabetes.csv'
response = urllib2.urlopen( url )
data = response.read()

home = expanduser("~")
filename = home + "/pima-indians-diabetes.csv"

with open( filename, 'w'  ) as write_handle:
    write_handle.write(data)

# load pima indians dataset
dataset = numpy.loadtxt(filename, delimiter=",")
dataset
    
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]
# create model
model = Sequential()
model.add(Dense(12, input_dim=8, init='uniform', activation='relu'))
model.add(Dense(8, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))
# Compile model
model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy'])
# Fit the model
history = model.fit(
    X,
    Y,
    epochs=150,
    batch_size=10,
    verbose=2)

# Evaluate the network
loss, accuracy = model.evaluate(X, Y)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))
# calculate predictions
probabilities = model.predict(X)
predictions = [float(x>0.5) for x in probabilities]

# visualizations
import matplotlib.pyplot as plt

loss = history.history['loss']
#val_loss = history.history['val_loss']

epochs = range(1, len(loss) + 1)

plt.plot(epochs, loss, 'bo', label='Training loss')
#plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()

cm = confusion_matrix(Y, predictions)
print ("True positives:  %.0f" % cm[1,1])
print ("False positives: %.0f" % cm[0,1])
print ("True negatives:  %.0f" % cm[0,0])
print ("False negatives: %.0f" % cm[1,0])
