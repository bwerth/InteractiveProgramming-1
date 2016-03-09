"""
This program takes a chord progression as input and randomly generates a melody.

@author: Joseph Lee and Bryan Werth

"""
import random
import music21
import copy

class Note(object):
  """
  This class defines a note.  Its attributes are the note name, the octave, and the duration.
  The note name is a string, octave is an integer (C4 is middle C), duration is the number of beats (duration of 4 is a whole note
  """
  note_list = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
  def  __init__(self,note = 'C',octave = 4,duration = 4):
    self.note = note
    self.octave = octave
    self.duration = duration
    
  def  __str__(self):
    return "{}{}".format(self.note,self.octave)
   
  """ 
  def name_interval(self,other):
    
    This method calculates the number of half steps separating two notes. Takes a note as input and produces an integer.
    
    notea = note_list.index(self.note)
    noteb = note_list.index(other.note)
    distance = abs(noteb-notea)
  """

  def producenote(self,interval):
    """
    This method produces the name of a note a given number of half steps higher than self
    """
    noteindex = self.note_list.index(self.note)
    if noteindex+interval>len(self.note_list)-1:
      newnoteindex = noteindex+interval-len(self.note_list)
      octave = self.octave + 1
    else:
      newnoteindex = noteindex+interval
      octave = self.octave
    newnote = Note(self.note_list[newnoteindex],octave,self.duration)
    return newnote
  
class Chord(object):
  """
  This class defines chords made up of notes.  Its attributes are bottomnote, chord name, and chord inversion
  """
  def __init__(self,bottomnote = Note(),chordname = '',inversion = 0):
    self.bottomnote = bottomnote
    self.chordname = chordname
    self.inversion = inversion
  
  def __str__(self):
    return "{} chord with a starting note of {} at an inversion of {}".format(self.chordname,self.bottomnote,self.inversion)
    
  def createchord(self):
    """
	  This method produces a list of note names that forms the chord given the parameters for the chord defined in the Chord class
 	  """
    chord = []
    interval1 = 0
    if self.inversion == 0:
      if self.chordname == 'minor':
       interval2,interval3 = 3,7
      elif self.chordname == 'diminished':
       interval2,interval3 = 3,6
      elif self.chordname == 'augmented':
       interval2,interval3 = 4,8
      else:
    	 interval2,interval3 = 4,7
    elif self.inversion == 1:
		  if self.chordname == 'minor':
			 interval1,interval2,interval3 = 3,7,12
		  elif self.chordname == 'augmented':
			 interval1,interval2,interval3 = 4,8,12
		  elif self.chordname == 'diminished':
			 interval1,interval2,interval3 = 3,6,12
		  else:
			 interval1,interval2,interval3 = 4,7,12
    elif self.inversion == 2:
		  if self.chordname == 'minor':
			 interval1,interval2,interval3 = 7,12,15
		  elif self.chordname == 'augmented':
			 interval1,interval2,interval3 = 8,12,16
		  elif self.chordname == 'diminished':
			 interval1,interval2,interval3 = 6,12,15
		  else:
			 interval1,interval2,interval3 = 7,12,16
    chord.append(self.bottomnote.producenote(interval1))
    chord.append(self.bottomnote.producenote(interval2))
    chord.append(self.bottomnote.producenote(interval3))
    return chord
    
class ChordProgression(object):
  """
  This class defines a chord progression made up of chords. Its attribute is a list of chords (loc)
  """
  def __init__(self,LoC = []):
    self.loc = LoC
  
  def __str__(self):
    loc = []
    for chord in self.loc:
      loc.append(str(chord))
    return '\n'.join(loc)
  
  def createchordprogression(self):
    """
    This method produces a list of lists of chord names. For each chord in the loc attribute, createchord is called with the result being added to a list
    """
    loc = []
    for chord in self.loc:
      loc.append(chord.createchord())
    return loc

  def createmelody(self):
    """
    This method produces a string melody given a chord progression
    """
    melody=[]
    listofchords = self.createchordprogression()
    for chord in listofchords:
      melody.append(str(random.choice(chord)))
    return melody


  #def createchordprogressionfromstring(self,chordstring,octave,duration):
    #notelist = chordstring.split(" ")
    #notelist = [chord.replace('m',' minor') for chord in chordlist]
    #notelist = [chord.replace('aug',' augmented') for chord in chordlist]
    #notelist = [chord.replace('dim',' diminished') for chord in chordlist]
    #notelist = [chord.split(" ") for chord in chordlist]
    #chordlist = []
    #newnote = Note(chordlist[0][0],octave,duration)
    #if chordlist[0][1]
    #newchord = Chord(newnote,chordlist[0][1],0)
    #chordlist.append(newchord)
    #for chord in chordlist:


def chordgenerator(chords):
  """
  This function accepts a list of lists describing chords and produces a list of chords, making this program more user friendly
  """
  loc=[]
  durations=[]
  for c in chords:
	 #chord has four parameters, for example ["C","major",4,2] would create a C major chord with bottom note C4 with a duration of two beats
    note=Note()
    chord=Chord()
    note.note=c[0]
    note.octave=c[2]
    note.duration=c[3]
    chord.chordname=c[1]
    chord.bottomnote=note
    loc.append(chord)
    durations.append(c[3])
  return (loc,durations)

chords=[["C","major",4,1],["F","major",4,1],["G","major",4,2],["A","minor",4,1],["E","minor",4,1],["F","major",4,2],["C","major",4,4]]	
chord_info = chordgenerator(chords)
loc=chord_info[0]
duration=chord_info[1]
chordprog = ChordProgression()
chordprog.loc = loc
durations=duration

voices=3
  # convert chords to notes and stuff into a stream

stream = {}

for v in range(voices):
	stream[v] = music21.stream.Stream()
# split each chord into a separate voice
for v in range(voices):
  melody1 = chordprog.createmelody()
  for index,notes in enumerate(melody1):
		pitch=notes
		note = music21.note.Note(pitch)
		note.quarterLength=durations[index]
		stream[v].append(note)


 # combine all voices to one big stream
streams = music21.stream.Stream()
for s in stream:
  streams.insert(0, copy.deepcopy(stream[s]))
mf = music21.midi.translate.streamToMidiFile(streams)
mf.open('test123.mid', 'wb')
mf.write()
mf.close()

if __name__ == "__main__":
    import doctest
    doctest.testmod()