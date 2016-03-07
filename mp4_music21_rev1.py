import music21
import copy
import random

def realize_chord(chordstring, numofpitch=3, baseoctave=4, direction="ascending"):
  """
  given a chordstring like Am7, return a list of numofpitch pitches, starting in octave baseoctave, and ascending
  if direction == "descending", reverse the list of pitches before returning them
  """
  pitches = music21.harmony.ChordSymbol(chordstring).pitches
  num_iter = numofpitch/len(pitches)+1
  octave_correction = baseoctave - pitches[0].octave
  result = []
  actual_pitches = 0
  for i in range(num_iter):
    for p in pitches:
      if actual_pitches < numofpitch:
        newp = copy.deepcopy(p)
        newp.octave = newp.octave + octave_correction
        result.append(newp)
        actual_pitches += 1
      else:
        if direction == "ascending":
          return result
        else:
          result.reverse()
          return result
    octave_correction += 1

  if direction == "ascending":
    return result
  else:
    result.reverse()
    return result
 
  # define a chord progression as a string of all the chords
chords = "C G Am F C"
  # scale in which to interpret these chords
scale = music21.scale.MajorScale("C")
  # realize the chords in octave 4 (e.g. 4)
octave = 4
  # realize the chords using half notes (e.g. 1 for a whole note)
quarterLength = 2

chord_size=3

voices=2
  # convert chords to notes and stuff into a stream
splitted_chords = chords.split(" ")

stream = {}
splitted_chords = chords.split(" ")


for v in range(voices):
  stream[v] = music21.stream.Stream()
# split each chord into a separate voice
for c in splitted_chords:
  pitches = realize_chord(c, chord_size, octave, direction=random.choice(["ascending","descending"]))
  for v in range(voices):
    if v==voices-1 and c==splitted_chords[-1]:
  		pitch = realize_chord(c, 1, octave, direction="ascending")
		note = music21.note.Note(quarterLength)
		note.pitches=pitch
		stream[voices-1].append(note)
		print "hello"
    else:
      pitch=random.choice(pitches)
      note = music21.note.Note(pitch)
      note.quarterLength = quarterLength
      stream[v].append(note)



 # combine all voices to one big stream
streams = music21.stream.Stream()
for s in stream:
  streams.insert(0, copy.deepcopy(stream[s]))

streams.show("text")