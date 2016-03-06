class Note(object):
  """
  This class defines a note.  Its attributes are the note name, the octave, and the duration.
  The note name is a string, octave is an integer (C4 is middle C), duration is the number of beats (duration of 4 is a whole note
  """
  note_list = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
  
  def  __init__(self,note = 'A',octave = 4,duration = 4):
    self.note = note
    self.octave = octave
    self.duration = duration
    
  def  __str__(self):
    return "{}{} duration {} beats".format(self.note,self.octave,self.duration)
    
  def name_interval(self,other):
    """
    This method calculates the number of half steps separating two notes. Takes a note as input and produces an integer.
    """
    notea = note_list.index(self.note)
    noteb = note_list.index(other.note)
    distance = abs(noteb-notea)
  
  def produce_note(self,interval):
    """
    This method produces the name of a note a given number of half steps higher than self
    """
    noteindex = note_list.index(self.note)
    if noteindex+interval>len(note_list)-1:
      newnoteindex = noteindex+interval-len(note_list)
    else:
      newnoteindex = noteindex+interval
    return note_list(newnoteindex)
  
class Chord(object):
  """
  This class defines chords made up of notes.  Its attributes are bottomnote, chord name, and chord inversion
  """
  def __init__(self,bottomnote = Note(),chordname = '',inversion = 0):
    self.bottomnote = bottomnote
    self.chordname = chordname
    self.inversion = inversion
  
  def __str__(self):
    return "{} chord with a starting note of {}, at an inversion of {}".format(self.bottomnote,self.chordname,self.inversion)
    
  def createchord(self):
    """
    This method produces a list of note names that forms the chord given the parameters for the chord defined in the Chord class
    """
    chord = []
    if self.chordname == 'minor':
      chord.append(bottomnote.note)
      chord.append(bottomnote.producenote(3))
      chord.append(bottomnote.producenote(4))
    elif self.chordname == 'diminished':
      chord.append(bottomnote.note)
      chord.append(bottomnote.producenote(3))
      chord.append(bottomnote.producenote(3))
    elif self.chordname == 'augmented':
      chord.append(bottomnote.note)
      chord.append(bottomnote.producenote(4))
      chord.append(bottomnote.producenote(4))
    else:
      chord.append(bottomnote.note)
      chord.append(bottomnote.producenote(4))
      chord.append(bottomnote.producenote(3))
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
      loc.append(chord)
    return loc
  
  def createchordprogression(self):
    """
    This method produces a list of lists of chord names. For each chord in the loc attribute, createchord is called with the result being added to a list
    """
    loc = []
    for chord in self.loc:
      loc.append(chord.createchord())
    return loc


if __name__ == "__main__":
    import doctest
    doctest.testmod()