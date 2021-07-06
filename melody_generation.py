# This program uses a machine learning method to generate a single-line melody given
# a set of single-line melodies that I have composed.  The method used in this program
# can be generalized to compose a single-line melody given an input of any set of
# single-line melodies.  If the general learner determines that the piece it will
# generate is "melodic," then running this method will be the first step.

from music21 import *
import os

save_dir = 'melodies/'

melodies = os.listdir(save_dir)
scores = []

for melody in melodies:
    score = converter.parse(save_dir + melody)
    scores.append(score)

# scores[0].show('text')

notes = [[] for score in scores]
durations = [[] for score in scores]
keys = []

for i, melody in enumerate(scores):
    # print(str(i))
    keys.append(str(melody.analyze('key')))
    for element in melody:
        if isinstance(element, stream.Part):
            for measure in element:
                if isinstance(measure, stream.Measure):
                    for thing in measure:
                        # print(element)
                        if isinstance(thing, note.Note):
                            notes[i].append(thing.pitch)
                            durations[i].append(thing.duration.quarterLength)
                        # In this case, since all the melodies are a single line,
                        # every note is a Note and not a Chord.

# print(notes)
# print(durations)
