from music21 import *

# f = open("chords.txt", "w")

c = converter.parse("~/Dropbox/May_14_mvt1.mxl")
# c.show('text')
# c.show()                        # 
# print(len(c.recurse().getElementsByClass('Note')))
# for part in c.parts:
#     print(part)

chords = c.chordify()
# chords.show('text')
# chords.show()
# f.close()

# This part of the program determines which chords (e.g. I, iv, VI)
# these are given the notes in each chord.

