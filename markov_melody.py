from music21 import *
import os
import random
import copy

def doubles(lst):
    """ 
    Generates doubles from a given list - for example [1,2,3,4,5] would become [(1,2),(2,3),(3,4),(4,5)]
    """ 
    res=[]
    for lst in lst:
        if len(lst) < 2:
            pass
        
        for i in range(len(lst) - 1):
            res.append((lst[i], lst[i+1]))
    return res

def triples(lst):
    """ 
    Generates triples from a given list - for example [1,2,3,4,5] would become [(1,2,3),(2,3,4),(3,4,5)]
    """ 
    res=[]
    for lst in lst:
        if len(lst) < 3:
            pass
        
        for i in range(len(lst) - 2):
            res.append((lst[i], lst[i+1], lst[i+2]))
    return res

def quadrouples(lst):
    """ 
    Generates quadrouples from a given list - for example [1,2,3,4,5] would become [(1,2,3,4),(2,3,4,5)]
    """ 
    res=[]
    for lst in lst:
        if len(lst) < 4:
            pass
        
        for i in range(len(lst) - 3):
            res.append((lst[i], lst[i+1], lst[i+2], lst[i+3]))
    return res


def markov_table_1(doubles,database={}):
    for double in doubles:
        w1, w2 = double
        key = w1
        if key in database:
            database[key].append(w2)
        else:
            database[key] = [w2]
    return database

            
def markov_table_2(triples,database={}):
    for triple in triples:
        w1, w2, w3 = triple
        key = (w1, w2)
        if key in database:
            database[key].append(w3)
        else:
            database[key] = [w3]
    return database

def markov_table_3(quadrouples,database={}):
    for quadrouple in quadrouples:
        w1, w2, w3, w4 = quadrouple
        key = (w1, w2, w3)
        if key in database:
            database[key].append(w4)
        else:
            database[key] = [w4]
    return database

def generate_string_1(note_seed, rhythm_seed,length,note_database,rhythm_database):
    """
    Given a note seed in the format [first note], a rhythm seed in the format [quarter length for first note]
    the length of the desired output melody, a markov dictionary for the melody, and a markov dictionary for the rhythm, this function returns a tuple of lists
    in the format ([notes],[durations])
    """
    rhythm_output=[]
    note_output=[]
    note_output.append(note_seed[0])
    rhythm_output.append(rhythm_seed[0])

    for i in range(length-1):
        i=i+1
        key=note_output[i-1]
        options=note_database.get(key,["C","D","E","F","G","A","B"])
        next_state=random.choice(options)
        note_output.append(next_state)
        rhythm_key=rhythm_output[i-1]
        rhythm_options=rhythm_database.get(rhythm_key)
        next_rhythm_state=random.choice(rhythm_options,[0.25,0.5,0.5,1.0,1.0,1.0,1.0,2.0,2.0,2.0])
        rhythm_output.append(next_rhythm_state)

    return (note_output,rhythm_output)



def generate_string_2(note_seed,length,note_database,rhythm_database,rhythm_seed=[2.0,2.0]):
    """
    Given a note seed in the format [first note, second note], a rhythm seed in the format [quarter length for first note, quarter length for second note]
    the length of the desired output melody, a markov dictionary for the melody, and a markov dictionary for the rhythm, this function returns a tuple of lists
    in the format ([notes],[durations])
    """
    rhythm_output=[]
    note_output=[]
    note_output.append(note_seed[0])
    note_output.append(note_seed[0])
    rhythm_output.append(rhythm_seed[0])
    rhythm_output.append(rhythm_seed[0])

    for i in range(length-2):
        i=i+2
        key=(note_output[i-2],note_output[i-1])
        options=note_database.get(key,["C","D","E","F","G","A","B"])
        next_state=random.choice(options)
        note_output.append(next_state)
        rhythm_key=(rhythm_output[i-2],rhythm_output[i-1])
        rhythm_options=rhythm_database.get(rhythm_key,[0.25,0.5,0.5,1.0,1.0,1.0,1.0,2.0,2.0,2.0])
        next_rhythm_state=random.choice(rhythm_options)
        rhythm_output.append(next_rhythm_state)

    return (note_output,rhythm_output)

def generate_string_3(note_seed,length,note_database,rhythm_database,rhythm_seed=[2.0,1.0,1.0]):
    """
    Given a note seed in the format [first note, second note,third note], a rhythm seed in the format [quarter length for first note, quarter length for second
    note, quarter length for third note]
    the length of the desired output melody, a markov dictionary for the melody, and a markov dictionary for the rhythm, this function returns a tuple of lists
    in the format ([notes],[durations])
    """
    rhythm_output=[]
    note_output=[]
    note_output.append(note_seed[0])
    note_output.append(note_seed[0])
    note_output.append(note_seed[0])
    rhythm_output.append(rhythm_seed[0])
    rhythm_output.append(rhythm_seed[0])
    rhythm_output.append(rhythm_seed[0])

    for i in range(length-3):
        i=i+3
        key=(note_output[i-3],note_output[i-2],note_output[i-1])
        options=note_database.get(key,["C","D","E","F","G","A","B"])
        next_state=random.choice(options)
        note_output.append(next_state)
        rhythm_key=(rhythm_output[i-3],rhythm_output[i-2],rhythm_output[i-1])
        rhythm_options=rhythm_database.get(rhythm_key,[0.25,0.5,0.5,1.0,1.0,1.0,1.0,2.0,2.0,2.0])
        next_rhythm_state=random.choice(rhythm_options)
        rhythm_output.append(next_rhythm_state)

    return (note_output,rhythm_output)

def get_dataset(dataset_index=0):
    path="/home/bwerth/InteractiveProgramming-1/data{}".format(dataset_index)
    scores=[]
    for filename in os.listdir(path):
        scores.append(converter.parse("{}/{}".format(path,filename)))
    return scores


def generate_note_lists(dataset):
    melodyData = []
    for score in dataset:
        part = score.parts[0].getElementsByClass(stream.Measure) # Returns a list of Measures
        melodyData.append([]) # melodyData is a list of phrases, which contains a set of notes with no rests.
        for m in part: # For each measure!
            for n in m.notesAndRests:
                if(type(n) == note.Note):
                    melodyData[-1].append(n.name)# if it is a note, append the name of the note
                elif(type(n) == note.Rest):
                    melodyData.append([]) # A rest ends a musical phrase so we just start a new sublist here
                else: #the other possibility is that it is a chord...in which case, this grabs the top note
                    melodyData[-1].append(n[-1].name)
    return melodyData


def generate_rhythm_lists(dataset):
    rhythmData = []
    for score in dataset:
        part = score.parts[0].getElementsByClass(stream.Measure) # Returns a list of Measures
        rhythmData.append([]) # melodyData is a list of phrases, which contains a set of notes with no rests.
        for m in part: # For each measure
            for n in m.notesAndRests:
                if(type(n) == note.Note):
                    rhythmData[-1].append(n.quarterLength)# if it is a note, append the name of the note
                elif(type(n) == note.Rest):
                    rhythmData.append([]) # A rest ends a musical phrase so we just start a new sublist here
                else: #the other possibility is that it is a chord...in which case, this grabs the top note
                    rhythmData[-1].append(n[-1].quarterLength)
    return rhythmData


def generate_melody(list_of_notes, list_of_rhythms):
    octave = 4
    streams=stream.Stream()
    for indx,c in enumerate(list_of_notes):
        pitch=c+str(octave)
        note1=note.Note(pitch)
        note1.quarterLength=list_of_rhythms[indx]
        streams.append(note1)
    mf = midi.translate.streamToMidiFile(streams)
    mf.open('markov_melody.mid', 'wb')
    mf.write()
    mf.close()
    os.system('/usr/bin/xdg-open ~/InteractiveProgramming-1/markov_melody.mid')#        This line opens the MIDI file with the default program

def generate_song(length,dataset_index,note_seed,markov_order):
    scores=get_dataset(dataset_index)
    melody=generate_note_lists(scores)
    rhythm=generate_rhythm_lists(scores)

    if markov_order==1:
        note_doubles=doubles(melody)
        rhythm_doubles=doubles(rhythm)
        note_database=markov_table_1(note_doubles)
        rhythm_database=markov_table_1(rhythm_doubles)
        newsong=generate_string_1(note_seed, rhythm_seed,length,note_database,rhythm_database)
        list_of_notes=newsong[0]
        list_of_rhythms=newsong[1]
        generate_melody(list_of_notes, list_of_rhythms)

    elif markov_order==2:
        note_triples=triples(melody)
        rhythm_triples=triples(rhythm)
        note_database=markov_table_2(note_triples)
        rhythm_database=markov_table_2(rhythm_triples)
        newsong=generate_string_2(note_seed,length,note_database,rhythm_database)
        list_of_notes=newsong[0]
        list_of_rhythms=newsong[1]
        generate_melody(list_of_notes, list_of_rhythms)

    elif markov_order==3:
        note_quadrouples=quadrouples(melody)
        rhythm_quadrouples=quadrouples(rhythm)
        note_database=markov_table_3(note_quadrouples)
        rhythm_database=markov_table_3(rhythm_quadrouples)
        newsong=generate_string_3(note_seed,length,note_database,rhythm_database)
        list_of_notes=newsong[0]
        list_of_rhythms=newsong[1]
        generate_melody(list_of_notes, list_of_rhythms)
    else:
        print "Sorry, that markov order is not an option"

<<<<<<< HEAD
generate_song(50,0,["C","F","G"],[3.0,1.0,1.0],3)
=======
generate_song(50,0,"C",3)
>>>>>>> 7d290548ff76d17e25205269ffa101da36d72d41
