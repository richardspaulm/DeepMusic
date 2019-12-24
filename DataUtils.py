import midi
import pandas as pd
from pprint import pprint
from os import listdir
from urllib.parse import urljoin
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
                evt = midi.NoteOnEvent(tick=tick, channel=0, data=[data1])
        if evt_type == "p":
            if data2 is not None:
                evt = midi.ProgramChangeEvent(tick=tick, channel=0, data=[data1 + 50, data2])
            else:
                evt = midi.ProgramChangeEvent(tick=tick, channel=0, data=[data1])
        if evt_type == "c":
            if data2 is not None:
                evt = midi.ControlChangeEvent(tick=tick, channel=0, data=[data1, data2])
            else:
                evt = midi.ControlChangeEvent(tick=tick, channel=0, data=[data1])
        print(evt)
        return evt


    def string_to_track(self, corpus):
        track = midi.Track()
        evts = corpus.split(" ")
        # evts = evts[1:].pop()
        for evt in evts:
            evt_data = evt.split("_")
            midi_event = self.build_evt(evt_data)
            if midi_event is not None:
                track.append(midi_event)
        track.append(midi.events.EndOfTrackEvent())
        return track

    def extract_single_track(self, track_index=1):
        track = midi.Track()
        try:
            evts = [midi_evt for midi_evt in midi.read_midifile(self.filepath)[track_index]]
        except IndexError:
            evts = [midi_evt for midi_evt in midi.read_midifile(self.filepath)[0]]
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

    def create_df_from_dir(self, dirname):
        full_df = None
        files = listdir(dirname)
        files = [f for f in files if f.endswith(".mid")]
        tracks = []
        for f in files:
            fpath = dirname + "/" + f
            mf.set_file(fpath)
            track = mf.extract_single_track()
            df = self.create_df_from_track(track)
            if full_df is None:
                full_df = df
            else:
                full_df = pd.concat([full_df, df])
        return full_df


    def create_df_from_track(self, track):
        track_info = {"tick":[], "data1": [], "data2": []}
        for evt in track:
            if not self.desired_event(evt):
                continue
            evt_type = self.get_row_string(evt)
            if evt_type is not "n":
                continue
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
            if evt_string == "p_8_0":
                print(evt)
                print(evt_string)
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

    def train_val_test_corpus(self, dr, w=True):
        train = ""
        val = ""
        test = ""
        fnames = listdir(dr)
        train_stop = int(len(fnames) * .67)
        remaining = len(fnames) - train_stop
        val_stop = int(remaining / 2) + train_stop
        for i in range(len(fnames)):
            fpath = dr + "/" + fnames[i]
            self.set_file(fpath)
            try:
                track = self.extract_single_track(track_index=1)
            except:
                track = self.extract_single_track(track_index=0)
                if i > val_stop:
                    test += self.create_text_corpus(track)
                elif i > train_stop:
                    val += self.create_text_corpus(track)
                else:
                    train += self.create_text_corpus(track)
        if w:
            with open("k2_train/train.txt", "w") as f:
                f.write(train)
            with open("k2_train/val.txt", "w") as f:
                f.write(val)
            with open("k2_train/test.txt", "w") as f:
                f.write(test)
        return (test, val, train)

    def fpath_to_mid(self, inpt, outpt):
        with open(inpt, "r") as f:
            text = f.read()
            text = text.split(' ', 1)[1]
            text = text.rsplit(' ', 1)[0]
        track = self.string_to_track(text)
        self.tracks_to_mid([track], outpt)

    def format_all_midis(self):
        for fname in listdir("mid_by_gen"):
            fpath = "mid_by_gen/" + fname
            try:
                self.fpath_to_mid(fpath, fname[:fname.index(".")] + ".mid")
            except:
                print("Error:", fpath)
    
    def csv_to_midi(self, fpath):
        track = midi.Track()
        track.append(midi.SequencerSpecificEvent(tick=0, data=[5, 15, 9, 70, 200]))
        track.append(midi.SequencerSpecificEvent(tick=0, data=[5, 15, 6, 71, 101, 110, 101, 114, 97, 108, 32, 77, 73, 68, 73]))
        track.append(midi.TrackNameEvent(tick=0, text='Acoustic Grand Piano High', data=[65, 99, 111, 117, 115, 116, 105, 99, 32, 71, 114, 97, 110, 100, 32, 80, 105, 97, 110, 111, 32, 72, 105, 103, 104]))
        track.append(midi.ProgramChangeEvent(tick=0, channel=0, data=[0]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[10, 64]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[10, 64]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[10, 64]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[7, 127]))
        track.append(midi.ControlChangeEvent(tick=3, channel=0, data=[100, 64]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[101, 64]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[100, 64]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[101, 64]))
        track.append(midi.ControlChangeEvent(tick=1, channel=0, data=[6, 12]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[6, 12]))
        track.append(midi.ControlChangeEvent(tick=1, channel=0, data=[38, 0]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[38, 0]))
        track.append(midi.NoteOnEvent(tick=5, channel=0, data=[67, 69]))
        df = pd.read_csv(fpath, index_col=0, names=["Tick", "Data1", "Data2","Evt_Type"], header=0)
        nrows = len(df.iloc[:, 0])
        for i in range(nrows):
            if df.Evt_Type[i] == "p":
                evt = midi.events.ProgramChangeEvent(tick=int(df.Tick[i]), data=[int(df.Data1[i]) + 50, int(df.Data2[i])])
                track.append(evt)
            if df.Evt_Type[i] == "c":
                evt = midi.events.ControlChangeEvent(tick=int(df.Tick[i]), data=[int(df.Data1[i]), int(df.Data2[i])])
                track.append(evt)
            if df.Evt_Type[i] == "n":
                evt = midi.events.NoteOnEvent(tick=int(df.Tick[i]), data=[int(df.Data1[i]), int(df.Data2[i])])
                track.append(evt)
        track.append(midi.events.EndOfTrackEvent())
        for t in track:
            print(t)
        self.tracks_to_mid([track], "output_test.mid")
    def notes_only_csv_to_mid(self, fpath):
        track = midi.Track()
        track.append(midi.SequencerSpecificEvent(tick=0, data=[5, 15, 9, 70, 200]))
        track.append(midi.SequencerSpecificEvent(tick=0, data=[5, 15, 6, 71, 101, 110, 101, 114, 97, 108, 32, 77, 73, 68, 73]))
        track.append(midi.TrackNameEvent(tick=0, text='Acoustic Grand Piano High', data=[65, 99, 111, 117, 115, 116, 105, 99, 32, 71, 114, 97, 110, 100, 32, 80, 105, 97, 110, 111, 32, 72, 105, 103, 104]))
        track.append(midi.ProgramChangeEvent(tick=0, channel=0, data=[0]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[10, 64]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[10, 64]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[10, 64]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[7, 127]))
        track.append(midi.ControlChangeEvent(tick=3, channel=0, data=[100, 64]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[101, 64]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[100, 64]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[101, 64]))
        track.append(midi.ControlChangeEvent(tick=1, channel=0, data=[6, 12]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[6, 12]))
        track.append(midi.ControlChangeEvent(tick=1, channel=0, data=[38, 0]))
        track.append(midi.ControlChangeEvent(tick=0, channel=0, data=[38, 0]))
        track.append(midi.NoteOnEvent(tick=5, channel=0, data=[67, 69]))
        df = pd.read_csv(fpath, index_col=0, names=["Tick", "Data1", "Data2","Evt_Type"], header=0)
        nrows = len(df.iloc[:, 0])
        oor = False
        for i in range(nrows):
            tick = int(abs(df.iloc[i, 0]))
            d1 = int(abs(df.iloc[i, 1]))
            d2 = int(abs(df.iloc[i, 2]))
            if tick > 256 or tick < 0 or d1 > 256 or d1 < 0 or d2 > 256 or d2 < 0:
                print("Note in position {} out of range".format(str(i)))
                break
            evt = midi.events.NoteOnEvent(tick=tick, data=[d1, d2])
            track.append(evt)

        track.append(midi.events.EndOfTrackEvent())
        for t in track:
            print(t)
        self.tracks_to_mid([track], "output_test.mid")    


mf = MF_Utils("midi_downloads/Portal_-_Still_Alive.mid")
mf.notes_only_csv_to_mid("mid_predictions.csv")

# df = mf.create_df_from_dir("midi_downloads")
# print(df.head(100))
# print(df.describe())
# df.to_csv("k3_train/full_midi.csv")