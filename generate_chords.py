from music21 import *
import os

# Create the corpus.  (Ultimately, the corpus might end up being passed in from
# the main file, so this part may eventually get taken out.)

save_dir = 'chords/'

chords = os.listdir(save_dir)
scores = []

for piece in chords:
    score = converter.parse(save_dir + piece)
    # These next few lines are specific to the input pieces I was using to test
    # this program, since music21 was misidentifying the keys of these pieces.
    if "eminor" in piece:
        score.keySignature = key.Key('E', 'minor')
    elif "aminor" in piece:
        score.keySignature = key.Key('A', 'minor')
    elif "cminor" in piece:
        score.keySignature = key.Key('C', 'minor')
    elif "fmajor" in piece:
        score.keySignature = key.Key('F', 'major')
    elif "bflatmajor" in piece:
        score.keySignature = key.Key('B-', 'major')
    elif "dminor" in piece:
        score.keySignature = key.Key('D', 'minor')
    elif "cmajor" in piece:
        score.keySignature = key.Key('C', 'major')
    scores.append(score)

    
# The "melody" input is a music21.stream.Score object.
# The "key" input is a music21.key.Key object.
def generateChords(melody, key):

    # Transpose the chords from the input works into the key of the melody.
    transposed_scores = []
    k = str(key)
    for piece in scores:
        # Commented this line out because it was incorrectly determining the keys
        # of my inputs
        # start_key = piece.analyze('key')
        
        # These next few lines are specific to this set of input works that I was
        # using to test the program.
        # print(piece)
        start_keys = piece.getKeySignatures()
        start_key = start_keys[0]
        
        k_start = str(start_key)
        # print(k_start)
        if "major" in k_start and "major" in k or "minor" in k_start and "minor" in k:
            interv = interval.Interval(start_key.tonic, key.tonic)
            transposed = piece.transpose(interv)
            piece_chords = transposed.chordify()
            transposed_scores.append(piece_chords)
            
    # Get a list of all the unique chords in the works that share a mode
    # (major/minor) with this melody.
    unique_chords = []
    roman_numerals = []
    for piece in transposed_scores:
        for c in piece_chords.recurse().getElementsByClass('Chord'):
            # Put them all in closed position and in the same octave so that
            # the same chord with notes in different octaves isn't counted as
            # multiple different chords.  Different inversions still count as
            # "different" chords.
            c.closedPosition(forceOctave = 4, inPlace = True)
            
            # Add the chord to the list if it's not already there.
            # if c not in unique_chords:
            #     unique_chords.append(c)       
            rn = roman.romanNumeralFromChord(c, key)
            if rn not in roman_numerals:
                roman_numerals.append(rn)
                unique_chords.append(c)

    # print(unique_chords)
    # print(roman_numerals)
    for chord in unique_chords:
        print(chord)

# Create a melody to test the generateChords function
melody = converter.parse('melodies/melody1.mxl')
# print(melody.analyze('key'))
generateChords(melody, melody.analyze('key'))
