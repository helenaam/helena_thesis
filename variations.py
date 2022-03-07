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
# I'm passing in the time signature as an input because music21 doesn't
# recognize that it already has a time signature (even though there is
# already a time signature object in the music21 representation of the melody)
def variation5(melody, timeSig):
    chords = melody.chordify()
    new_melody = stream.Stream()
    #melody.timeSignature = None
    #new_melody.insert(0, meter.TimeSignature('{0}/{1}'.format(timeSig.numerator * 2, timeSig.denominator)))
    new_melody.timeSignature = meter.TimeSignature('{0}/{1}'.format(timeSig.numerator * 2, timeSig.denominator))
    for n in melody.recurse().getElementsByClass('GeneralNote'):
        old_duration = n.quarterLength
        n.quarterLength = old_duration * 2
        new_melody.append(n)
    #melody.timeSignature = timeSig
    #print(melody.timeSignature)
    #melody.measure(1).timeSignature = meter.TimeSignature('{0}/{1}'.format(timeSig.numerator * 2, timeSig.denominator))
    new_melody.show()

# This function reduces the length of every note by half (speeds it up).
def variation6(melody):
    ...

# This variation replaces each note e.g. C --> C B C D in the key of C major,
# if the value of the note is a quarter note or greater
def variation7(melody, key):
    ...

melody1 = converter.parse('melodies/melody1.mxl')
melody5 = converter.parse('melodies/melody5.mxl')

#variation2(melody1, key.Key('F', 'major'))
#variation5(melody1, meter.TimeSignature('4/4'))
variation5(melody5, meter.TimeSignature('2/4'))
