import re
from music21 import stream, note, duration, pitch

def parse_note(note_str):
    match = re.match(r'([a-g])(\#\#|\#|\&\&|\&)?([0-9])/([0-9]+)', note_str)
    if match:
        pitch, accidental, octave, dur = match.groups()
        # Map the accidental names to music21 format
        accidental_map = {
            '##': 'double-sharp',
            '#': 'sharp',
            '&&': 'double-flat',  # Correct representation for double flat in music21
            '&': 'flat'
        }
        # Apply the mapping or leave accidental as None if not present
        accidental = accidental_map.get(accidental, None)
        return {
            'pitch': pitch.upper(),
            'accidental': accidental,
            'octave': int(octave) - 1,  # Convert to MIDI octave
            'duration': int(dur)
        }


def parse_omr_output(omr_content):
    notes_data = []
    measures = re.findall(r'\[(.*?)\]', omr_content, re.DOTALL)
    
    for measure in measures:
        elements = re.findall(r'(\{.*?\}|[a-g](\#\#|\#|\&\&|\&)?[0-9]/[0-9]+\.?)', measure)
        for elem in elements:
            if elem[0].startswith('{'):  # It's a chord
                chord_notes = re.findall(r'([a-g](\#\#|\#|\&\&|\&)?[0-9]/[0-9]+)', elem[0])
                for chord_note in chord_notes:
                    note_data = parse_note(chord_note[0])
                    notes_data.append(note_data)
            else:  # It's a single note
                note_data = parse_note(elem[0])
                notes_data.append(note_data)
    
    return notes_data

# Path to the .txt file containing the OMR output
file_path = 'C:/Users/Aatir Cheema/Desktop/sheet1.txt'

# Read the file and parse the content
with open(file_path, 'r') as file:
    omr_content = file.read()
    notes_data = parse_omr_output(omr_content)

# Create a music21 stream to hold the notes
s = stream.Stream()

# Populate the stream with notes from the parsed data
for note_data in notes_data:
    n = note.Note()
    n.pitch.step = note_data['pitch']
    n.pitch.octave = note_data['octave']
    if note_data['accidental']:
        n.pitch.accidental = pitch.Accidental(note_data['accidental'])
    n.duration = duration.Duration(4 / note_data['duration'])  # Convert note duration to a music21 Duration object
    s.append(n)

# Save to a MusicXML file
musicxml_output_path = 'C:/Users/Aatir Cheema/Desktop/sheet1.musicxml'

s.write('musicxml', fp=musicxml_output_path)

print(f'MusicXML file saved to {musicxml_output_path}')
