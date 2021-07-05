from music21 import *

# f = open("chords.txt", "w")

c1 = converter.parse("May_14_mvt1.mxl")
c2 = converter.parse("May_14_mvt2.mxl")
# c1.show('text')
# c1.show()                        # 
# print(len(c.recurse().getElementsByClass('Note')))
# for part in c.parts:
#     print(part)

chords1 = c1.chordify()
chords2 = c2.chordify()
# chords1.show('text')
# chords1.show()
# f.close()

# This part of the program determines which chords (e.g. I, iv, VI)
# these are given the notes in each chord.

# This part of the program is a machine learning generative model for
# coming up with a harmony part given a single-line melody.x

