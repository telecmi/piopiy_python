from piopiy.underscore import isWs,isObject


def streamimg(ws_url,options):
    if isWs(ws_url):

        stream = {
            "action": "stream",
            "ws_url": ws_url
        }

        if isObject(options):
            stream['listen_mode'] = options.get('listen_mode', 'caller')
            stream['voice_quality'] = options.get('voice_quality', '8000')
            stream['stream_on_answer'] = options.get('stream_on_answer', False)

        return stream
    else:
        raise NameError('invalid ws_url in stream') 
