from music21 import *
from copy import deepcopy

# This function adds intermediate pitches on transitions between notes.
# The input "melody" is a music21.stream.Score object.
def variation1(melody):
    ...

# This function changes the music from major to minor, or vice versa.
def variation2(melody, key):
    tonic_note = key.tonic
    new_melody = melody.chordify()
    for note in new_melody.recurse().getElementsByClass('Chord'):
        old_pitches = note.pitches
        for pitch in old_pitches:
            if pitch == key.pitchFromDegree(3) or pitch == key.pitchFromDegree(6):
                if "major" in str(key):
                    new_pitch = pitch.transpose(-1)
                    note.add(new_pitch)
                    note.remove(pitch)
                elif "minor" in str(key):
                    new_pitch = pitch.transpose(1)
                    note.add(new_pitch)
                    note.remove(pitch)
    new_melody.show()

# This function changes two consecutive quarter notes to a dotted quarter
# note followed by an eigth note, and two consecutive eighth notes to a
# dotted eighth note followed by a 16th note.
def variation3(melody):
    #last_2_notes = (None, None)
    prev_note = None
    old_prev = None
    for curr_note in melody.recurse().getElementsByClass('GeneralNote'):
        #last_2_notes[0] = last_2_notes[1]
        #last_2_notes[1] = note
        old_curr = deepcopy(curr_note)
        if isinstance(prev_note, note.Note) or isinstance(prev_note, chord.Chord):
            if isinstance(curr_note, note.Note) or isinstance(curr_note, chord.Chord):
                #print("2 notes in a row")
                # If the previous note has not already been modified
                if old_prev.quarterLength == prev_note.quarterLength:
                    # If the previous note and current note are same length
                    if old_prev.quarterLength == curr_note.quarterLength:
                        prev_note.quarterLength *= 1.5
                        curr_note.quarterLength /= 2
        old_prev = old_curr
        prev_note = curr_note
    melody.show()
    return

# This function changes a melody in simple time to be in composite time, and
# vice versa.
def variation4(melody):
    ...

# This function makes every note twice as long (aka slows it down).
# I'm passing in the time signature as an input because music21 doesn't
# recognize that it already has a time signature (even though there is
# already a time signature object in the music21 representation of the
# melody).
# The score displayed by this function does not include a key signature, but
# the notes are still stored correctly (it's just the score that shows up
# wrong).
def variation5(melody, timeSig):
    # chords = melody.chordify()
    new_melody = stream.Stream()
    new_melody.timeSignature = meter.TimeSignature('{0}/{1}'.format(timeSig.numerator * 2, timeSig.denominator))
    for n in melody.recurse().getElementsByClass('GeneralNote'):
        old_duration = n.quarterLength
        n.quarterLength = old_duration * 2
        new_melody.append(n)
    new_melody.show()

# This function reduces the length of every note by half (speeds it up).
def variation6(melody, timeSig):
    new_melody = stream.Stream()
    new_melody.timeSignature = timeSig
    for n in melody.recurse().getElementsByClass('GeneralNote'):
        old_duration = n.quarterLength
        n.quarterLength = old_duration / 2
        new_melody.append(n)
    new_melody.show()

# This variation replaces each note e.g. C --> C B C D in the key of C major,
# if the value of the note is a quarter note or greater
def variation7(melody, key):
    ...

melody1 = converter.parse('melodies/melody1.mxl')
melody5 = converter.parse('melodies/melody5.mxl')
melody2 = converter.parse('melodies/melody2.mxl')

#variation2(melody1, key.Key('F', 'major'))
#variation5(melody1, meter.TimeSignature('4/4'))
#variation5(melody5, meter.TimeSignature('2/4'))
#variation6(melody5, meter.TimeSignature('2/4'))
variation3(melody2)
#variation3(melody1)
#variation3(melody5)
