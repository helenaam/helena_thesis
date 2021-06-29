from music21 import *

# f = open("chords.txt", "w")

c1 = converter.parse("~/Dropbox/May_14_mvt1.mxl")
c2 = converter.parse("~/Dropbox/May_14_mvt2.mxl")
# c1.show('text')
# c1.show()                        # 
# print(len(c.recurse().getElementsByClass('Note')))
# for part in c.parts:
#     print(part)

chords = c1.chordify()
# chords.show('text')
# chords.show()
# f.close()

# This part of the program determines which chords (e.g. I, iv, VI)
# these are given the notes in each chord.

# This part of the program is a machine learning generative model for
# coming up with a harmony part given a single-line melody.

