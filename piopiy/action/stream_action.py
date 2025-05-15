from piopiy.underscore import isString, isURL
from .bridge import connect
from .input import input,play_input
from .stream import streamimg
from .play_stream import play_base64_audio
import json


class StreamAction:
    def __init__(self):
        self.action = []

    def playMusic(self, file_name_or_url):

        if isString(file_name_or_url):
            if isURL(file_name_or_url):
                self.action.append({
                    "action": "play",
                    "file_url": file_name_or_url
                })
            else:
                self.action.append({
                    "action": "play",
                    "file_name": file_name_or_url
                })
        else:
            raise NameError('filename is required to play')
        
    def speak(self, text):
        if isString(text):
            self.action.append({
                "action": "speak",
                "text": text
            })
        else:
            raise NameError('text is required to speak')
        
    def setValue(self, text):
        if isString(text):
            self.action.append({
                "action": "param",
                "text": text
            })
        else:
            raise NameError('text is required to set')

    def record(self):
        self.action.append({"action": "record"})

    def hangup(self):
        self.action.append({"action": "hangup"})

    def pause(self):
        return json.dumps({"action": "pause"})
    
    def interrupt(self):
        return json.dumps({"action": "break"})
    
    def resume(self):
        return json.dumps({"action": "resume"})
    
    def stop(self):
        return json.dumps({"action": "stop"})
    
    def call(self, to_or_array, piopiy_no, option='none'):
        bridge = connect(to_or_array, piopiy_no, option)
        self.action.append(bridge)

    def stream(self, ws_url, options='none'):
        stream = streamimg(ws_url, options)
        self.action.append(stream)


    def playStream(self,*,audio_base64, audio_type, sample_rate):
        play_stream = play_base64_audio(audio_base64, audio_type, sample_rate)
        return play_stream
        

    def PCMO(self):
        stream_pcmo = self.action
        self.clear()
        return json.dumps(stream_pcmo)
    
    def clear(self):
        self.action = []
