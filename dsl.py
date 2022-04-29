from music21 import *

def getAttribute(n, attrib_name):
    if attrib_name == "pitch":
        return n.pitch
    if attrib_name == "duration":
        return n.duration
    else:
        return


# n is a Note object, and condition and attribute are strings.
# This function checks whether the note n satisfies the given condition.
def checkCondition(n, condition, attribute):
    if attribute == "pitch":
        # We can assume "==" will not be in a condition.
        if ">=" in condition:
            comparison_note_str = condition.split(">=")[1].strip()
            if comparison_note_str not in sigma:
                try:
                    comparison_note = note.Note(comparison_note_str)
                except:
                    print("Invalid note")
            else:
                comparison_note = sigma(comparison_note_str)             
            return n.pitch >= comparison_note.pitch
        
        elif "<=" in condition:
            comparison_note_str = condition.split("<=")[1].strip()
            if comparison_note_str not in sigma:
                try:
                    comparison_note = note.Note(comparison_note_str)
                except:
                    print("Invalid note")
            else:
                comparison_note = sigma(comparison_note_str)
            return n.pitch <= comparison_note.pitch
        
        elif "!=" in condition:
            comparison_note_str = condition.split("!=")[1].strip()
            if comparison_note_str not in sigma:
                try:
                    comparison_note = note.Note(comparison_note_str)
                except:
                    print("Invalid note")
            else:
                comparison_note = sigma(comparison_note_str)
            return n.pitch != comparison_note.pitch
        
        elif ">" in condition:
            comparison_note_str = condition.split(">")[1].strip()
            if comparison_note_str not in sigma:
                try:
                    comparison_note = note.Note(comparison_note_str)
                except:
                    print("Invalid note")
            else:
                comparison_note = sigma(comparison_note_str)
            return n.pitch > comparison_note.pitch
        
        elif "<" in condition:
            comparison_note_str = condition.split("<")[1].strip()
            if comparison_note_str not in sigma:
                try:
                    comparison_note = note.Note(comparison_note_str)
                except:
                    print("Invalid note")
            else:
                comparison_note = sigma(comparison_note_str)
            return n.pitch < comparison_note.pitch
        #else:
            #...

    
# Returns a dictionary and a list.
def I0(selector, curr_notes):
    sigma = {}
    
    # Split the selector string at commas (delineates notes in a sequence)
    selector_parts = re.split("==|>=|<=|>|<|=", selector)
    if "pitch" in selector_parts[0]: # "pitch" is also a substring of "pitches"
        attribute = "pitch"
    elif "duration" in selector_parts[0]: # "duration" is a substring of "durations"
        attribute = "duration"
    else:
        attribute = None
    selector_seq = selector_parts[1].split(',')
    
    # Set variables in dictionary
    if "x" in selector_seq:
        sigma["x"] = curr_notes[selector_seq.indexof("x")]
    for i, condition in enumerate(selector_seq):
        if "|" in condition:
            variable_set = condition.split("|")
            var_name = variable_set[0].strip()
            sigma[var_name] = curr_notes[i]

    # Iterate through and check conditions
    sequence = []
    for i, condition in enumerate(selector_seq):
        [var_name, inequality] = condition.split("|")
        if inequality == "":
            # check if the note corresponding to var_name in sigma matches current note
            if var_name in sigma and sigma[var_name].pitch == curr_notes[i].pitch:
                # Add note to sequence
                sequence.append(curr_notes[i])
            else:
                return [{}, []]
        elif checkCondition(curr_notes[i], inequality, "pitch"):
            sequence.append(curr_notes[i])
        else:
            return [{}, []]

        
# selector is a string; melody_notes is a list of Notes.
def I(selector, melody_notes):
    i = 0
    while i < melody_notes.length:
        note_seq = I0(selector, melody_notes[i:])[1]
        if len(note_seq) != 0:
            i += len(note_seq)
        else:
            i += 1
