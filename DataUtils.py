import midi
import pandas as pd
from pprint import pprint
from os import listdir
class MF_Utils:
    def __init__(self, filepath=None):
        self.filepath = filepath

    def set_file(self, filepath):
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

    def build_evt(self, evt_data):
        if len(evt_data) < 3:
            return None
        evt = None
        evt_type = evt_data[0]
        try:
            tick = int(evt_data[1])
            data1 = int(evt_data[2])
            data2=None
            if len(evt_data) > 3:
                data2 = int(evt_data[3])
        except ValueError:
            return None
        if evt_type == "n":
            if data2 is not None:
                evt = midi.NoteOnEvent(tick=tick, channel=0, data=[data1, data2])
            else:
                evt = midi.NoteOnEvent(tick=tick, channel=0, data=[data1, data2])
        if evt_type == "p":
            if data2 is not None:
                evt = midi.ProgramChangeEvent(tick=tick, channel=0, data=[data1, data2])
            else:
                evt = midi.ProgramChangeEvent(tick=tick, channel=0, data=[data1, data2])
        if evt_type == "c":
            if data2 is not None:
                evt = midi.ControlChangeEvent(tick=tick, channel=0, data=[data1, data2])
            else:
                evt = midi.ControlChangeEvent(tick=tick, channel=0, data=[data1, data2])
        return evt


    def string_to_track(self, corpus):
        track = midi.Track()
        evts = corpus.split(" ")
        for evt in evts:
            evt_data = evt.split("_")
            midi_event = self.build_evt(evt_data)
            if midi_event is not None:
                track.append(midi_event)
        track.append(midi.events.EndOfTrackEvent())
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

    def get_row_string(self, evt):
        if isinstance(evt, midi.events.NoteOnEvent):
            return "n"
        if isinstance(evt, midi.events.ControlChangeEvent):
            return "c"
        if isinstance(evt, midi.events.ProgramChangeEvent):
            return "p"
        return ""

    def create_evt_string(self, ty, t, d1, d2):
        evt_str = ty + "_" + t + "_" + d1
        if d2 is not "":
            evt_str = evt_str + "_" + d2
        return evt_str

    def create_df_from_track(self, track):
        track_info = {"tick":[], "data1": [], "data2": [], "note_on": [], "control": [], "program": []}
        for evt in track:
            if not self.desired_event(evt):
                continue
            track_info = self.set_row_type(track_info, evt)
            track_info["tick"].append(evt.tick)
            track_info["data1"].append(evt.data[0])
            try:
                track_info["data2"].append(evt.data[1])
            except:
                track_info["data2"].append(0)
        return pd.DataFrame(track_info)
    
    def create_text_corpus(self, track):
        corpus = ""
        for evt in track:
            if not self.desired_event(evt):
                continue
            evt_type = self.get_row_string(evt)
            tick = str(evt.tick)
            d1 = str(evt.data[0])
            if len(evt.data) > 1:
                d2 = str(evt.data[1])
            else:
                d2 = ""
            evt_string = self.create_evt_string(evt_type, tick, d1, d2)
            corpus = corpus + evt_string + " "
        return corpus
    
    def build_corpus_from_dir(self, dr):
        corpus = ""
        for fname in listdir(dr):
            fpath = dr + "/" + fname
            self.set_file(fpath)
            try:
                track = self.extract_single_track(track_index=1)
            except:
                track = self.extract_single_track(track_index=0)
            corpus += self.create_text_corpus(track)
        return corpus

    def fpath_to_mid(self, inpt, outpt):
        with open(inpt, "r") as f:
            text = f.read()
        # print(text)
        track = self.string_to_track(text)
        self.tracks_to_mid([track], outpt)
            

