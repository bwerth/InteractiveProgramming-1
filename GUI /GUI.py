from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.label import Label
from kivy.clock import Clock
from music21 import *
import os
import random
import copy
from kivy.uix.image import Image

# Declare both screens as separate classes. Currently there is nothing in here, but there will be when we fill out the GUI.
class Logo(Image):
    def __init__(self, **kwargs):
        super(Logo, self).__init__(**kwargs)
        self.size = self.texture_size

class NewClock(Label):
    def update(self, *args):
        TestApp.screen_manager.current = 'menu'

class CustomDropDown(DropDown):
    for i in range(5):
        print i 

class TitleScreen(Screen):
    pass

class MenuScreen(Screen):
    translateInput = ObjectProperty(None)
    translateButton = ObjectProperty(None)
    translateLabel = ObjectProperty(None)
    top_layout = ObjectProperty(None)
    dd_btn = ObjectProperty(None)
    dataset_index = 0

    def __init__(self,*args,**kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)
        self.drop_down = CustomDropDown()
        mainbutton = Button(text='Hello', size_hint=(None, None))
        mainbutton.bind(on_release=self.drop_down.open)
        self.drop_down.bind(on_select=lambda instance, x: setattr(self.ddID, 'text', x))

    def get_datasetindex(self):
        if self.ddID == 'btn1':
            self.dataset_index = 0
        elif self.ddID == 'btn2':
            self.dataset_index = 1

    def doubles(self,lst):
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

    def triples(self,lst):
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

    def quadrouples(self,lst):
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


    def markov_table_1(self,doubles,database={}):
        for double in doubles:
            w1, w2 = double
            key = w1
            if key in database:
                database[key].append(w2)
            else:
                database[key] = [w2]
        return database

                
    def markov_table_2(self,triples,database={}):
        for triple in triples:
            w1, w2, w3 = triple
            key = (w1, w2)
            if key in database:
                database[key].append(w3)
            else:
                database[key] = [w3]
        return database

    def markov_table_3(self,quadrouples,database={}):
        for quadrouple in quadrouples:
            w1, w2, w3, w4 = quadrouple
            key = (w1, w2, w3)
            if key in database:
                database[key].append(w4)
            else:
                database[key] = [w4]
        return database

    def generate_string_1(self,note_seed,length,note_database,rhythm_database,rhythm_seed=[2.0]):
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
            print rhythm_options
            next_rhythm_state=random.choice(rhythm_options,[0.25,0.5,0.5,1.0,1.0,1.0,1.0,2.0,2.0,2.0])
            rhythm_output.append(next_rhythm_state)

        return (note_output,rhythm_output)

    def generate_string_2(self,note_seed,length,note_database,rhythm_database,rhythm_seed=[2.0,2.0]):
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

    def generate_string_3(self,note_seed,length,note_database,rhythm_database,rhythm_seed=[2.0,1.0,1.0]):
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

    def get_dataset(self,dataset_index=0):
        path="/home/bwerth/InteractiveProgramming-1/data{}".format(dataset_index)
        scores=[]
        for filename in os.listdir(path):
            scores.append(converter.parse("{}/{}".format(path,filename)))
        return scores


    def generate_note_lists(self,dataset):
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


    def generate_rhythm_lists(self,dataset):
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


    def generate_melody(self,list_of_notes, list_of_rhythms):
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

    def generate_song(self,length,dataset_index,note_seed,markov_order):
        scores=self.get_dataset(dataset_index)
        melody=self.generate_note_lists(scores)
        rhythm=self.generate_rhythm_lists(scores)

        if markov_order==1:
            note_doubles=self.doubles(melody)
            rhythm_doubles=self.doubles(rhythm)
            note_database=self.markov_table_1(note_doubles)
            rhythm_database=self.markov_table_1(rhythm_doubles)
            newsong=self.generate_string_1(note_seed,length,note_database,rhythm_database)
            list_of_notes=newsong[0]
            list_of_rhythms=newsong[1]
            self.generate_melody(list_of_notes, list_of_rhythms)

        elif markov_order==2:
            note_triples=self.triples(melody)
            rhythm_triples=self.triples(rhythm)
            note_database=self.markov_table_2(note_triples)
            rhythm_database=self.markov_table_2(rhythm_triples)
            newsong=self.generate_string_2(note_seed,length,note_database,rhythm_database)
            list_of_notes=newsong[0]
            list_of_rhythms=newsong[1]
            self.generate_melody(list_of_notes, list_of_rhythms)

        elif markov_order==3:
            note_quadrouples=self.quadrouples(melody)
            rhythm_quadrouples=self.quadrouples(rhythm)
            note_database=self.markov_table_3(note_quadrouples)
            rhythm_database=self.markov_table_3(rhythm_quadrouples)
            newsong=self.generate_string_3(note_seed,length,note_database,rhythm_database)
            list_of_notes=newsong[0]
            list_of_rhythms=newsong[1]
            self.generate_melody(list_of_notes, list_of_rhythms)
        else:
            print "Sorry, that markov order is not an option"

class SettingsScreen(Screen):
    pass



# Create the screen manager and add the two previously defined screens to it.

class TestApp(App):

    screen_manager = ScreenManager()

    def build(self):
        #self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(TitleScreen(name='title'))
        self.screen_manager.add_widget(MenuScreen(name='menu'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))
        clock = NewClock()
        Clock.schedule_once(clock.update, 4)
        return self.screen_manager

if __name__ == '__main__':
    TestApp().run()