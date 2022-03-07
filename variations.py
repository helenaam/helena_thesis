from music21 import *

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
def variation3(melody, timesig):
    for note in melody.recurse().getElementsByClass('Note'):
        note_value = 1
    return

# This function changes a melody in simple time to be in composite time, and
# vice versa.
def variation4(melody):
    ...

# This function makes every note twice as long (aka slows it down).
def variation5(melody):
    for n in melody.recurse().getElementsByClass('GeneralNote'):
        return

# This function reduces the length of every note by half (speeds it up).
def variation6(melody):
    ...

# This variation replaces each note e.g. C --> C B C D in the key of C major,
# if the value of the note is a quarter note or greater
def variation7(melody, key):
    ...

melody1 = converter.parse('melodies/melody1.mxl')

variation2(melody1, key.Key('F', 'major'))
