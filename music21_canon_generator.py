import music21
import os


score = music21.corpus.parse('bach/bwv321.xml')
soprano = score.getElementById('Soprano')
excerpt = soprano.flat.notesAndRests.stream()
outputScore = music21.stream.Score()

transformations = [(1.0, 'P1'),
                   (2.0, 'P1'),
                   (1.0, 'P5'),
                   (2.0, 'P5')
                  ]

for speed, transposition in transformations:
    part = excerpt.augmentOrDiminish(speed)
    part.transpose(transposition, inPlace=True)
    outputScore.insert(0, part)

mf = music21.midi.translate.streamToMidiFile(outputScore)
mf.open('canon_temp.mid', 'wb')
mf.write()
mf.close()
os.system('/usr/bin/xdg-open ~/InteractiveProgramming-1/canon_temp.mid')#		This line opens the MIDI file with the default program