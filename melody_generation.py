# This program uses a machine learning method to generate a single-line melody given
# a set of single-line melodies that I have composed.  The method used in this program
# can be generalized to compose a single-line melody given an input of any set of
# single-line melodies.  If the general learner determines that the piece it will
# generate is "melodic," then running this method will be the first step.

from music21 import *
import os
import random

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

for i, melody in enumerate(scores):
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


