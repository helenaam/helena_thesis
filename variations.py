from music21 import *
from copy import deepcopy
import random

# This function adds intermediate pitches on transitions between notes.
# The input "melody" is a music21.stream.Score object.
def variation0(melody):
    ...

# For each note, divide into 4 notes.  Keep the first one the same pitch as
# the original note, and, for each of the other 3 notes, choose randomly
# between pitches in between that of the original note and the (original)
# next note and a rest.
def variation1(melody, key):
    new_melody = stream.Stream()
    for i, n in enumerate(melody.recurse().getElementsByClass('GeneralNote')):
        if i < len(melody.recurse().getElementsByClass('GeneralNote')) - 1:
            next_obj = melody.recurse().getElementsByClass('GeneralNote')[i+1]
            j = i+1
            while j < len(melody.recurse().getElementsByClass('GeneralNote')) - 1 and not isinstance(next_obj, note.Note):
                j += 1
                next_obj = melody.recurse().getElementsByClass('GeneralNote')[j]
            if isinstance(n, note.Note) and isinstance(next_obj, note.Note):
                orig_len = n.quarterLength
                num_halfsteps = interval.Interval(n, next_obj).semitones
                n1 = note.Note(n.pitch)

                if num_halfsteps != 0:
                    n2_steps = random.randrange(abs(num_halfsteps))
                    n2_interval = interval.Interval(n2_steps)
                    n2_interval.noteStart = n
                    n2 = n2_interval.noteEnd
                    n3_steps = random.randrange(abs(num_halfsteps))
                    n3_interval = interval.Interval(n3_steps)
                    n3_interval.noteStart = n
                    n3 = n3_interval.noteEnd
                    n4_steps = random.randrange(abs(num_halfsteps))
                    n4_interval = interval.Interval(n4_steps)
                    n4_interval.noteStart = n
                    n4 = n4_interval.noteEnd

                else:
                    degree = key.getScaleDegreeAndAccidentalFromPitch(n.pitch)[0]
                    n2 = note.Note(key.pitchFromDegree(degree - 1))
                    n2.octave = n1.octave
                    n3 = note.Note(n.pitch)
                    n4 = note.Note(key.pitchFromDegree(degree + 1))
                    n4.octave = n1.octave
                    if lower_than(n4.pitch, n1.pitch):
                        n4.octave += 1
                    if higher_than(n2.pitch, n1.pitch):
                        n2.octave -= 1

                n1.quarterLength = orig_len / 4
                n2.quarterLength = orig_len / 4
                n3.quarterLength = orig_len / 4
                n4.quarterLength = orig_len / 4
                new_melody.append(n1)
                new_melody.append(n2)
                new_melody.append(n3)
                new_melody.append(n4)
            else:
                new_melody.append(n)
    new_melody.show()

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
    prev_note = None
    old_prev = None
    for curr_note in melody.recurse().getElementsByClass('GeneralNote'):
        old_curr = deepcopy(curr_note)
        if isinstance(prev_note, note.Note) or isinstance(prev_note, chord.Chord):
            if isinstance(curr_note, note.Note) or isinstance(curr_note, chord.Chord):
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
    

# higher_than(pitch1, pitch2) returns True if pitch1 is higher than pitch2 and
# false otherwise.
def higher_than(pitch1, pitch2):
    testchord = chord.Chord([pitch1, pitch2])
    if testchord.bass() == pitch2 and pitch1 != pitch2:
        return True
    else:
        return False

    
# lower_than(pitch1, pitch2) returns True if pitch1 is lower than pitch2 and
# false otherwise.
def lower_than(pitch1, pitch2):
    testchord = chord.Chord([pitch1, pitch2])
    if testchord.bass() == pitch1 and pitch1 != pitch2:
        return True
    else:
        return False

    
# This variation replaces each note e.g. C --> C B C D in the key of C major,
# if the value of the note is a quarter note or greater
def variation7(melody, key):
    new_melody = stream.Stream()
    for n in melody.recurse().getElementsByClass('GeneralNote'):
        if isinstance(n, note.Note):
            orig_len = n.quarterLength
            degree = key.getScaleDegreeAndAccidentalFromPitch(n.pitch)[0]
            n1 = note.Note(n.pitch)
            n2 = note.Note(key.pitchFromDegree(degree - 1))
            n2.octave = n1.octave
            n3 = note.Note(n.pitch)
            n4 = note.Note(key.pitchFromDegree(degree + 1))
            n4.octave = n1.octave
            if lower_than(n4.pitch, n1.pitch):
                n4.octave += 1
            if higher_than(n2.pitch, n1.pitch):
                n2.octave -= 1
            n1.quarterLength = orig_len / 4
            n2.quarterLength = orig_len / 4
            n3.quarterLength = orig_len / 4
            n4.quarterLength = orig_len / 4
            new_melody.append(n1)
            new_melody.append(n2)
            new_melody.append(n3)
            new_melody.append(n4)
        else:
            new_melody.append(n)
    new_melody.show()

# Variation 8
def variation8(melody, key):
    new_melody = stream.Stream()
    for i, n in enumerate(melody.recurse().getElementsByClass('GeneralNote')):
        if i < len(melody.recurse().getElementsByClass('GeneralNote')) - 1:
            next_obj = melody.recurse().getElementsByClass('GeneralNote')[i+1]
            j = i+1
            while j < len(melody.recurse().getElementsByClass('GeneralNote')) - 1 and not isinstance(next_obj, note.Note):
                j += 1
                next_obj = melody.recurse().getElementsByClass('GeneralNote')[j]
            if isinstance(n, note.Note) and isinstance(next_obj, note.Note):
                orig_len = n.quarterLength
                num_halfsteps = interval.Interval(n, next_obj).semitones
                n1 = note.Note(n.pitch)

                if num_halfsteps <= -3 or num_halfsteps >= 3:
                    n2_steps = round(num_halfsteps / 3)
                    n2_interval = interval.Interval(n2_steps)
                    n2_interval.noteStart = n
                    n2 = n2_interval.noteEnd
                    n3_steps = 2 * n2_steps
                    n3_interval = interval.Interval(n3_steps)
                    n3_interval.noteStart = n
                    n3 = n3_interval.noteEnd
                    
                    n1.quarterLength = orig_len / 2
                    n2.quarterLength = orig_len / 4
                    n3.quarterLength = orig_len / 4
                    new_melody.append(n1)
                    new_melody.append(n2)
                    new_melody.append(n3)

                elif num_halfsteps == 0:
                    degree = key.getScaleDegreeAndAccidentalFromPitch(n.pitch)[0]
                    n2 = note.Note(key.pitchFromDegree(degree - 1))
                    n2.octave = n1.octave
                    n3 = note.Note(key.pitchFromDegree(degree + 1))
                    n3.octave = n1.octave
                    if lower_than(n3.pitch, n1.pitch):
                        n3.octave += 1
                    if higher_than(n2.pitch, n1.pitch):
                        n2.octave -= 1

                    n1.quarterLength = orig_len / 4
                    n2.quarterLength = orig_len / 4
                    n3.quarterLength = orig_len / 2
                    new_melody.append(n1)
                    new_melody.append(n2)
                    new_melody.append(n3)

                elif num_halfsteps == -1 or num_halfsteps == 1:
                    n2_interval = interval.Interval(2)
                    n2_interval.noteStart = n
                    n2 = n2_interval.noteEnd

                    n1.quarterLength = orig_len / 2
                    n2.quarterLength = orig_len / 2
                    new_melody.append(n1)
                    new_melody.append(n2)

                else: # number of half steps is +/- 2
                    n2_interval = interval.Interval(1)
                    n2_interval.noteStart = n
                    n2 = n2_interval.noteEnd

                    n1.quarterLength = 3 * orig_len / 4
                    n2.quarterLength = orig_len / 4
                    new_melody.append(n1)
                    new_melody.append(n2)
                    
            else:
                new_melody.append(n)
    new_melody.show()


melody1 = converter.parse('melodies/melody1.mxl')
melody5 = converter.parse('melodies/melody5.mxl')
melody2 = converter.parse('melodies/melody2.mxl')
melody4 = converter.parse('melodies/melody4.mxl')
melody3 = converter.parse('melodies/melody3.mxl')

#variation2(melody1, key.Key('F', 'major'))
#variation5(melody1, meter.TimeSignature('4/4'))
#variation5(melody5, meter.TimeSignature('2/4'))
#variation6(melody5, meter.TimeSignature('2/4'))
#variation3(melody2)
#variation3(melody1)
#variation3(melody5)
#variation7(melody2, key.Key('F', 'major'))
#variation7(melody5, key.Key('C', 'minor'))
#variation1(melody4, key.Key('C', 'minor'))

#variation8(melody4, key.Key('C', 'minor'))
#variation8(melody2, key.Key('F', 'major'))
#variation8(melody5, key.Key('C', 'minor'))
#variation8(melody3, key.Key('C', 'major'))
variation1(melody3, key.Key('C', 'major'))
