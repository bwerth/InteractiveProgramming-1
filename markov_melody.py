from music21 import *
import os
import random

def triples(lst):
    """ 
    Generates triples from the given list
    """ 
    res=[]
    if len(lst) < 3:
        return
        
    for i in range(len(lst) - 2):
        res.append((lst[i], lst[i+1], lst[i+2]))
    return res
            
def markov_table(triples,database={}):
    for triple in triples:
        w1, w2, w3 = triple
        key = (w1, w2)
        if key in database:
            database[key].append(w3)
        else:
            database[key] = [w3]
    return database

def generate_string(seed,length,database):
    output=[]
    output.append(seed[0])
    output.append(seed[1])
    for i in range(length-2):
        i=i+2
        key=(output[i-2],output[i-1])
        options=database.get(key)
        next_state=random.choice(options)
        output.append(next_state)

    return output

def generate_list(corpus_name):
    full_list=[]
    score=corpus.parse(corpus_name)
    for part in score:
        note_list=[]
        try:
            part.stream
            part = part.flat.notesAndRests.stream()
            for note in part:
                note_list.append(note.name)
            full_list.append(note_list)
        except AttributeError:
            pass


    return full_list[0]#currently only returning one part



lst=generate_list('bwv66.6')
triples=triples(lst)
database=markov_table(triples)
string=generate_string(['F#','G#'],15,database)
print string