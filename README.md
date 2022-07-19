# helena_thesis

The ultimate goal of this project is to create a domain-specific language (DSL) to represent a music composition process, and to create a learner that takes a body of musical works as input and generates a melody or a harmonization in that style.

The file "melody_generation.py" takes a set of single-line melodies as input and uses an LSTM neural network to generate a new single-line melody in the same style as these.

The files "generate_chords.py," "generate_chords_reverse.py," and "generate_chords_bothends.py" each try a different method of using Markov chains to generate chords for an inputted single-line melody, using a body of works in the same style.

The file "variations.py" contains functions, written in Python, to implement several different variations on a musical piece.  The file "dsl.py" contains the working implementation of the DSL, and "Documentation.docx" contains the documentation for it.

All of the files in this project that require inputs of musical pieces require these inputs to be XML-format files of the score.