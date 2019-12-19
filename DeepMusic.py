import midi
import pandas as pd
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

    def desired_event(self, evt):
        if isinstance(evt, midi.events.NoteOnEvent):
            return True
        if isinstance(evt, midi.events.ControlChangeEvent):
            return True
        if isinstance(evt, midi.events.ProgramChangeEvent):
            return True
        return False

    def set_row_type(self, track_info, evt):
        if isinstance(evt, midi.events.NoteOnEvent):
            track_info["note_on"].append(1)
            track_info["control"].append(0)
            track_info["program"].append(0)
            return track_info
        elif isinstance(evt, midi.events.ControlChangeEvent):
            track_info["control"].append(1)
            track_info["note_on"].append(0)
            track_info["program"].append(0)
            return track_info
        elif isinstance(evt, midi.events.ProgramChangeEvent):
            track_info["program"].append(1)
            track_info["control"].append(0)
            track_info["note_on"].append(0)
            return track_info
        else:
            return None

    def create_df_from_track(self, track):
        track_info = {"tick":[], "data1": [], "data2": [], "note_on": [], "control": [], "program": []}
        for evt in track:
            if not self.desired_event(evt):
                continue
            track_info = self.set_row_type(track_info, evt)
            track_info["tick"].append(evt.tick)
            track_info["data1"].append(evt.data[0])
            try:
                track_info["data2"].append(evt.data[2])
            except:
                track_info["data2"].append(0)
        return pd.DataFrame(track_info)

mf = MF_Utils("midi_files/gerudo.mid")
track = mf.extract_single_track()
df = mf.create_df_from_track(track)
print(df)