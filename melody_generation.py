# This program uses a machine learning method to generate a single-line melody given
# a set of single-line melodies that I have composed.  The method used in this program
# can be generalized to compose a single-line melody given an input of any set of
# single-line melodies.  If the general learner determines that the piece it will
# generate is "melodic," then running this method will be the first step.

from music21 import *
import os
import random
import numpy as np
import tensorflow as tf

save_dir = 'melodies/'

melodies = os.listdir(save_dir)
scores = []

for melody in melodies:
    score = converter.parse(save_dir + melody)
    scores.append(score)

# scores[0].show('text')

# Transpose everything into C major or C minor

majormelodies = []
minormelodies = []
transposed_scores = []

for melody in scores:
    key = melody.analyze('key')
    k = str(key)
    interv = interval.Interval(key.tonic, pitch.Pitch('C'))
    transposed = melody.transpose(interv)
    if "major" in k:
        majormelodies.append(transposed)
    if "minor" in k:
        minormelodies.append(transposed)
    transposed_scores.append(transposed)

# print(majormelodies)
# print(minormelodies)

# Determine whether to generate a major or minor melody.

newkey = ""

frac_major = len(majormelodies) / (len(majormelodies) + len(minormelodies))
if random.random() < frac_major:
    newkey = "major"
else:
    newkey = "minor"

if newkey is "major":
    # Make lists of all the notes and their durations in each of the melodies.

    notes = [[] for score in majormelodies]
    durations = [[] for score in majormelodies]

    for i, melody in enumerate(majormelodies):
        for element in melody:
            if isinstance(element, stream.Part):
                for measure in element:
                    if isinstance(measure, stream.Measure):
                        for thing in measure:
                            if isinstance(thing, note.Note):
                                notes[i].append(thing.pitch)
                                durations[i].append(thing.duration.quarterLength)
elif newkey is "minor":
    notes = [[] for score in minormelodies]
    durations = [[] for score in minormelodies]

    for i, melody in enumerate(minormelodies):
        for element in melody:
            if isinstance(element, stream.Part):
                for measure in element:
                    if isinstance(measure, stream.Measure):
                        for thing in measure:
                            if isinstance(thing, note.Note):
                                notes[i].append(thing.pitch)
                                durations[i].append(thing.duration.quarterLength)

# Map unique notes and durations to integers
                                
uniqueNotes = np.unique([i for melody in notes for i in melody])
noteToInt = dict(zip(uniqueNotes, list(range(0, len(uniqueNotes)))))

uniqueDurations = np.unique([i for melody in durations for i in melody])
durationToInt = dict(zip(uniqueDurations, list(range(0, len(uniqueDurations)))))

# uniqueClasses = uniqueNotes * uniqueDurations
# classToInt = dict(zip(uniqueClasses, list(range(0, len(uniqueClasses)))))

intToNote = {i: n for n, i in noteToInt.items()}
intToDuration = {i: d for d, i in durationToInt.items()}

# print(len(uniqueNotes))
# print(len(uniqueDurations))

sequenceLength = 32
trainNotes = []
trainDurations = []
targetNotes = []
targetDurations = []

# Construct training and target sequences

for score in range(len(notes)):
    noteInts = [noteToInt[n] for n in notes[score]]
    durationInts = [durationToInt[d] for d in durations[score]]
    for i in range(len(noteInts) - sequenceLength):
        trainNotes.append(noteInts[i:i+sequenceLength])
        trainDurations.append(durationInts[i:i+sequenceLength])
        targetNotes.append(noteInts[i+1])
        targetDurations.append(durationInts[i+1])

numSamples = np.shape(trainNotes)[0]
numNotes = np.shape(trainNotes)[1]
numDurations = np.shape(trainDurations)[1]

inputDim = numNotes * sequenceLength
embedDim = 64

noteInput = tf.keras.layers.Input(shape = (None,))
durationInput = tf.keras.layers.Input(shape = (None,))

noteEmbedding = tf.keras.layers.Embedding(numNotes, embedDim, input_length = sequenceLength)(noteInput)
durationEmbedding = tf.keras.layers.Embedding(numDurations, embedDim, input_length = sequenceLength)(durationInput)

mergeLayer = tf.keras.layers.Concatenate(axis = 1)([noteEmbedding, durationEmbedding])
lstmLayer = tf.keras.layers.LSTM(512, return_sequences = True)(mergeLayer)
denseLayer = tf.keras.layers.Dense(256)(lstmLayer)

noteOutput = tf.keras.layers.Dense(numNotes, activation = 'softmax')(denseLayer)
durationOutput = tf.keras.layers.Dense(numDurations, activation = 'softmax')(denseLayer)

lstm = tf.keras.Model(inputs = [noteInput, durationInput], outputs = [noteOutput, durationOutput])
lstm.compile(loss = 'categorical_crossentropy', optimizer = 'rmsprop')
lstm.fit([trainNotes, trainDurations], [targetNotes, targetDurations], epochs = 500, batch_size = 64)

initialNotes = np.expand_dims(trainNotes[0,:].copy(), 0)
initialDurations = np.expand_dims(trainDurations[0,:].copy(), 0)

def predict(noteSequence, durationSequence):
    predictedNotes, predictedDurations = model.predict(model.predict([noteSequence, durationSequence]))
    return np.argmax(predictedNotes), np.argmax(predictedDurations)

newNotes, newDurations = [], []

for i in range(500):
    newNote, newDuration = predict(initialNotes, initialDurations)
    newNotes.append(newNote)
    newDurations.append(newDuration)
    initialNotes[0][:-1] = initialNotes[0][1:]
    initialNotes[0][-1] = newNote
    initialDurations[0][:-1] = initialDurations[0][1:]
    initialDurations[0][-1] = newDuration

generatedStream = stream.Stream()
generatedStream.append(instrument.Piano())

for i in range(len(noteSequence)):
    generatedStream.append(note.Note(noteSequence[i].replace('.', ' '), quarterType = durationSequence[i])) # would need to modify this line if there were chords rather than just notes

generatedStream.write('midi', fp=generated_dir+'lstm.mid')
generatedStream.show()
