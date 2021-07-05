# helena_thesis

The ultimate goal of this project is to create a domain-specific language (DSL) to represent a music composition process, and to create learner that takes a body of work as input and produces a DSL program (a compositional process) that generates a piece of music in that style.

The first step that the learner will take is to determine whether it should start by generating a melody for one of the instrumental lines or if it should start by generating chords.  If x% of the given works are chordal rather than melodic, then the model has an x% chance of generating something chordal and a 100-x% chance of generating something melodic.

To generate something "melodic," the learner begins by generating a starting melody.  To generate something "chordal," it begins by generating a starting sequence of chords.