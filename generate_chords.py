from music21 import *
import os

# Create the corpus.  (Ultimately, the corpus might end up being passed in from
# the main file, so this part may eventually get taken out.)

save_dir = 'chords/'

chords = os.listdir(save_dir)
scores = []

for piece in chords:
    score = converter.parse(save_dir + piece)
    scores.append(score)

# Transpose everything into C major or C minor

# majorpieces = []
# minorpieces = []
# transposed_scores = []

# for i, piece in enumerate(scores):
#     key = piece.analyze('key')
#     k = str(key)
#     interv = interval.Interval(key.tonic, pitch.Pitch('C'))
#     transposed = piece.transpose(interv)
#     piece_chords = transposed.chordify()
#     if "major" in k:
#         majorpieces.append(piece_chords)
#     if "minor" in k:
#         minorpieces.append(piece_chords)
#     transposed_scores.append(piece_chords)


# The "melody" input is a music21.stream.Score object.
# The "key" input is a music21.key.Key object.
def generateChords(melody, key):

    # Transpose the chords from the input works into the key of the melody.
    transposed_scores = []
    k = str(key)
    for piece in scores:
        start_key = piece.analyze('key')
        k_start = str(start_key)
        if "major" in k_start and "major" in k or "minor" in k_start and "minor" in k:
            interv = interval.Interval(start_key.tonic, key.tonic)
            transposed = piece.transpose(interv)
            piece_chords = transposed.chordify()
            transposed_scores.append(piece_chords)
            
    # Get a list of all the unique chords in the works that share a mode
    # (major/minor) with this melody.
    unique_chords = []
    for piece in transposed_scores:
        for c in piece_chords.recurse().getElementsByClass('Chord'):
            # Put them all in closed position and in the same octave so that
            # the same chord with notes in different octaves isn't counted as
            # multiple different chords.  Different inversions still count as
            # "different" chords.
            c.closedPosition(forceOctave = 4, inPlace = True)
            # Add the chord to the list if it's not already there.
            if c not in unique_chords:
                unique_chords.append(c)
