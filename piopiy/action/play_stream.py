from piopiy.underscore import isString
import json
import base64

def play_base64_audio(audio_base64,audio_type,sample_rate):
    
    allowed_formats = {'raw', 'mp3', 'wav', 'ogg'}
    allowed_sample_rates = {8000, 16000}

    if audio_type not in allowed_formats:
        raise NameError('audio_type is required to play')
    if sample_rate not in allowed_sample_rates:
        raise NameError('sample_rate is required to play')

    if isString(audio_base64):
        if is_base64(audio_base64):
         return json.dumps({
               "type": "streamAudio",
               "data": {
               "audioDataType":audio_type,
               "sampleRate": sample_rate,
               "audioData": audio_base64    
               }
              })
        else:
            raise NameError('audio_base64 is not base64')
    else:
        raise NameError('audio_base64 is required to play')




def is_base64(s):
   
    try:
        # Try to decode the string
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False