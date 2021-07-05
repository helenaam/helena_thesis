# This program will generate a Mozart string quartet using machine learning.
# Currently, this program creates a list of representations of all the Mozart
# string quartets in the music21 corpus.

import os
from music21 import *

# Bach: 433 works in corpus
# Essen Folksongs ('essenFolksong'): 31 works in corpus
# Mozart: 16 works in corpus
# Beethoven: 26 works in corpus
works = corpus.getComposer('mozart') # can put any composer's name here
# print(len(works))
del(works[11]) # This removes the only one of the Mozart pieces that is not a string quartet.

scores = []

for piece in works:
    print(piece)
    score = converter.parse(piece)
    scores.append(score)
    # score.show()

# scores[0].show()
