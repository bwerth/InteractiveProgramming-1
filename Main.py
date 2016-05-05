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

#The newclock class is used to limit the amount of time the title screen is present
class NewClock(Label):
    #The update function within the newclock class changes the current screen
    #to the menu screen when it is called.
    def update(self, *args):
        #The current screen of the testapp screen manager is defined as the menu screen
        TestApp.screen_manager.current = 'menu'

#The customdropdown class is empty because everything pertaining to the custom drop down class
#is defined in the corresponding kv file.
class CustomDropDown(DropDown):
    pass

#Everything important in the title screen is defined in the kv file, so this is also empty.
class TitleScreen(Screen):
    pass

#The menu screen class
class MenuScreen(Screen):
    #translateInput = ObjectProperty(None)
    #translateButton = ObjectProperty(None)
    #translateLabel = ObjectProperty(None)
    #top_layout = ObjectProperty(None)
    #dd_btn = ObjectProperty(None)
    #sets the dataset_index to zero
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
        res=[]# 										Create empty list to store the results in
        for lst in lst:#								This for loop is here because sometimes this function gets a list of lists
            if len(lst) < 2:#							if the list is shorter than 2, no doubles exist so pass
                pass
            for i in range(len(lst) - 1):#				otherwise, append all the doubles to the res list
                res.append((lst[i], lst[i+1]))
        return res

    def triples(self,lst):
        """ 
        Generates triples from a given list - for example [1,2,3,4,5] would become [(1,2,3),(2,3,4),(3,4,5)]
        """ 
        res=[]# 										Create empty list to store the results in
        for lst in lst:#								This for loop is here because sometimes this function gets a list of lists
            if len(lst) < 3:#							if the list is shorter than 2, no triples exist so pass
                pass
            for i in range(len(lst) - 2):
                res.append((lst[i], lst[i+1], lst[i+2]))# append all the triples to the res list
        return res

    def quadrouples(self,lst):
        """ 
        Generates quadrouples from a given list - for example [1,2,3,4,5] would become [(1,2,3,4),(2,3,4,5)]
        """ 
        res=[]# 										Create empty list to store the results in
        for lst in lst:#								This for loop is here because sometimes this function gets a list of lists
            if len(lst) < 4:#							if the list is shorter than 4, no quadrouples exist so pass
                pass
            for i in range(len(lst) - 3):
                res.append((lst[i], lst[i+1], lst[i+2], lst[i+3]))# append all the quadrouples to the res list
        return res


    def markov_table_1(self,doubles,database={}):
        for double in doubles:#							for each double in the list of doubles
            w1, w2 = double#							key is the first value in the double, value is the second
            key = w1
            if key in database:
                database[key].append(w2)#				add this to the database dictionary
            else:
                database[key] = [w2]
        return database

                
    def markov_table_2(self,triples,database={}):
        for triple in triples:#							for each triple in the list of triples
            w1, w2, w3 = triple#						key is the first two elements, value is the third
            key = (w1, w2)
            if key in database:
                database[key].append(w3)#				add this to the database dictionary
            else:
                database[key] = [w3]
        return database

    def markov_table_3(self,quadrouples,database={}):
        for quadrouple in quadrouples:#					for each quadrouple in the list of quadrouples
            w1, w2, w3, w4 = quadrouple#				first three elements are the key, 4th is the value
            key = (w1, w2, w3)
            if key in database:
                database[key].append(w4)#				add this to the database dictionary
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
        note_output.append(note_seed[0])#			add the note seed to the output
        rhythm_output.append(rhythm_seed[0])#		add the rhythm seed to the output

        for i in range(length-1):# 					for index in the range of length - seed length (1)
            i=i+1#									correct i to be the index for the future state
            key=note_output[i-1]#					the key is the previous state
            options=note_database.get(key,["C","D","E","F","G","A","B"])#	find this key in the dictionary, if it doesn't exist, return a list of notes
            next_state=random.choice(options)#		randomly choose one of these options
            note_output.append(next_state)#			add this to the output
            rhythm_key=rhythm_output[i-1]#						Do the same as above for rhythm
            rhythm_options=rhythm_database.get(rhythm_key)
            next_rhythm_state=random.choice(rhythm_options)   #,[0.25,0.5,0.5,1.0,1.0,1.0,1.0,2.0,2.0,2.0])
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
        note_output.append(note_seed[0])#				Add all the seeds to the output (note that because the GUI was created for only a single input, this note is being used for both previous states)
        note_output.append(note_seed[0])
        rhythm_output.append(rhythm_seed[0])
        rhythm_output.append(rhythm_seed[0])

        for i in range(length-2):#								Perform the same thing as in generate_string_1 except that the key is the two previous states
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
        note_output.append(note_seed[0])#  Add all the seeds to the output
        note_output.append(note_seed[0])
        note_output.append(note_seed[0])
        rhythm_output.append(rhythm_seed[0])
        rhythm_output.append(rhythm_seed[1])
        rhythm_output.append(rhythm_seed[2])

        for i in range(length-3):#													Perform the same thing as generate_string_2 except the key is the 3 previous states
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
        path="/home/bwerth/InteractiveProgramming-1/data{}".format(dataset_index)#		sets the directory to look for the folder
        scores=[]#																		empty list to store the scores in
        for filename in os.listdir(path):#												get a list of all files in the folder
            scores.append(converter.parse("{}/{}".format(path,filename)))#				convert all the files to music21 streams and append to the scores list
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
        octave = 4#										For now, the program is forcing all the notes into the 4th octave
        streams=stream.Stream()#						Create a music21 Stream
        for indx,c in enumerate(list_of_notes):#		iterate through the list of notes
            pitch=c+str(octave)#						pitch is the note plus the octave
            note1=note.Note(pitch)#						create a note with the given pitch
            note1.quarterLength=list_of_rhythms[indx]#	set the duration of the note to be the corresponding element from the list of rhythms
            streams.append(note1)#						append this note to the stream
        mf = midi.translate.streamToMidiFile(streams)#	Translate the stream to a midi file
        mf.open('markov_melody.mid', 'wb')#				Create a midi file to save to
        mf.write()#										save to this midi file
        mf.close()
        os.system('/usr/bin/xdg-open /home/bwerth/InteractiveProgramming-1/markov_melody.mid')#        This line opens the MIDI file with the default program

    def generate_song(self,length,dataset_index,note_seed,markov_order):
        scores=self.get_dataset(dataset_index)
        melody=self.generate_note_lists(scores)
        rhythm=self.generate_rhythm_lists(scores)

        if markov_order==1:#										If the user wants first order markov chains to be used, execute the code to do first order
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