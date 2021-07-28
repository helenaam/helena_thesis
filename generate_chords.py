from music21 import *
import os
import random
from copy import deepcopy

# Create the corpus.  (Ultimately, the corpus might end up being passed in from
# the main file, so this part may eventually get taken out.)

save_dir = 'chords/'

chords = os.listdir(save_dir)
scores = []

for piece in chords:
    s = converter.parse(save_dir + piece)
    # These next few lines are specific to the input pieces I was using to test
    # this program, since music21 was misidentifying the keys of these pieces.
    if "eminor" in piece:
        s.keySignature = key.Key('E', 'minor')
    elif "aminor" in piece:
        s.keySignature = key.Key('A', 'minor')
    elif "cminor" in piece:
        s.keySignature = key.Key('C', 'minor')
    elif "fmajor" in piece:
        s.keySignature = key.Key('F', 'major')
    elif "bflatmajor" in piece:
        s.keySignature = key.Key('B-', 'major')
    elif "dminor" in piece:
        s.keySignature = key.Key('D', 'minor')
    elif "cmajor" in piece:
        s.keySignature = key.Key('C', 'major')
    scores.append(s)

# The generate1(melody, unique_chords) function assigns a chord to each note
# by randomly selecting a chord containing that note from the chord bank.
def generate1(melody, chordbank):
    for note in melody.recurse().getElementsByClass('Note'):
        for chord in chordbank:
            return

# The determineResolutions() function returns a sequence of Booleans that state
# whether each note in the melody (in order) is a resolution.
def determineResolutions():
    return

def contains(chord, note):
    pitches = chord.pitches
    # print(pitches)
    if note.pitch in pitches:
        return True
    else:
        return False

# The generate2(melody, chordsequence) function assigns a chord to each note based on
# the probabilities of each chord coming after the previous chord.
def generate2(melody, key, chordsequence):
    chords = []
    
    # Choose chord for first note (if not pickup note, use tonic chord if it fits)

    # Setting the initial value of prevchord to something very unlikely, so that the
    # program can use this to determine whether it's on the first note.
    prevchord = chord.Chord(["F7", "B7"])
    for n in melody.recurse().getElementsByClass('Note'):
        # print(n.pitch)
        note4 = deepcopy(n)
        note4.octave = 4
        note5 = deepcopy(n)
        note5.octave = 5
        # print(n.octave)
        # print(note4.octave)
        # print(note5.octave)
        # If it's the first note...
        if prevchord == chord.Chord(["F7", "B7"]):
            # Get chord for first note -- for now, am using tonic chord as placeholder
            # tonic = chord.Chord([0, 4, 7])
            tonic = chord.Chord(["C4", "F4", "A4"])
            chords.append(tonic)
            prevchord = tonic
        else:
            nextt = []
            for i, c in enumerate(chordsequence):
                prevroman = roman.romanNumeralFromChord(prevchord, key)
                if roman.romanNumeralFromChord(c, key) == prevroman and i+1 < len(chordsequence):
                    nextch = chordsequence[i+1]
                    if note4.pitch in nextch.pitches or note5.pitch in nextch.pitches:
                        nextt.append(nextch)
            
            # Choose a random chord from next
            #print(len(nextt))
            #print(nextt)
            if len(nextt) == 0:
                # print(note4.pitch)
                # print(note4.octave)
                # print(note.octave)
                # choose a random chord containing the note to be nextchord.
                for c in chordsequence:
                    #print("checking chord {0}".format(c))
                    if note4.pitch in c.pitches or note5.pitch in c.pitches:
                        #print("success!")
                        nextt.append(c)                
                # Alternatively: leave that note without a matching chord
                # nextchord = chord.Chord([note.pitch])
            # else:
            #     print("chord found")
                
            nextchord = nextt[random.randint(0, len(nextt)-1)]
            chords.append(nextchord)
            prevchord = nextchord

    return chords

    # for note in melody.recurse().getElementsByClass('Note'):
    #     print(note)
    
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
            #piece_chords.show('text')
            transposed_scores.append(piece_chords)
            
    # Get a list of all the unique chords in the works that share a mode
    # (major/minor) with this melody.
    unique_chords = []
    roman_numerals = []
    chord_sequence = []
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
            chord_sequence.append(c)
            rn = roman.romanNumeralFromChord(c, key)
            if rn not in roman_numerals:
                roman_numerals.append(rn)
                unique_chords.append(c)

    # print(unique_chords)
    # print(roman_numerals)
    # for chord in unique_chords:
    #     print(chord)
    # print(chord_sequence)

    new_chords = generate2(melody, key, chord_sequence)

    # Add the chords into the melody
    #melody_chords = []
    #melody_notes = melody.recurse().notes
    with_chords = melody.chordify()
    # melody.show('text')
    for i, n in enumerate(with_chords.recurse().getElementsByClass('Chord')):
        #n = chord.Chord([n.pitch])
        for pitch in new_chords[i]:
            n.add(pitch)
            #print("adding pitch")
        # print(n)
        #melody_chords.append(n)

    with_chords.show()

    # Build new score using these chords
    # newscore = stream.Score()
    # print(newscore)
    # print(melody)
    # # newscore.show('text')
    # i = 0
    # for x in melody.recurse():
    #     if x in melody.recurse().notes:
    #         newscore.show('text')
    #         #newscore.append(melody_chords[i])
    #     else:
    #         newscore.append(x)

    #newscore.show('text')
    

# Create a melody to test the generateChords function
melody = converter.parse('melodies/melody1.mxl')
# print(melody.analyze('key'))

generateChords(melody, melody.analyze('key'))

# c1 = chord.Chord(["C4", "F4", "A4"])
# n1 = note.Note("A3")
# print(contains(c1, n1))
