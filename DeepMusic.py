import midi
from pprint import pprint
class MF_Utils:
    def __init__(self, filepath):
        self.filepath = filepath

    def extract_track_events(self, track):
        return [midi_evt for midi_evt in track]

    def concat_all_track_evts(self, tracks):
        track = midi.Track()
        num_tracks = len(tracks)
        for i in range(num_tracks):
            evts = [midi_evt for midi_evt in tracks[i]]
            for evt in evts:
                if isinstance(evt, midi.events.EndOfTrackEvent):
                    if i == (num_tracks - 1):
                        track.append(evt)
                else:
                    track.append(evt)
        return track


    def extract_single_track(self, track_index=1):
        track = midi.Track()
        evts = [midi_evt for midi_evt in midi.read_midifile(self.filepath)[track_index]]
        for evt in evts:
            track.append(evt)
        return track

    def extract_all_tracks(self):
        t = []
        tracks = midi.read_midifile(self.filepath)
        for i in range(1, len(tracks)):
            t.append(self.extract_single_track(i))
        return t

    def tracks_to_mid(self, tracks, output):
        pattern = midi.Pattern()
        for track in tracks:
            pattern.append(track)
        midi.write_midifile(output, pattern)
    
    # def create_concat_mid(self, evt_lists, output):


mf = MF_Utils("midi_files/gerudo.mid")

# # tracks = [mf.extract_single_track(1)]
tracks = mf.extract_all_tracks()
tracks = mf.concat_all_track_evts(tracks)
mf.tracks_to_mid([tracks], "test.mid")

# mf2 = MF_Utils("test.mid")
# print(mf2.extract_single_track(0))