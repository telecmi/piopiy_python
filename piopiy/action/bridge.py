from piopiy.underscore import isNumber, isArray, isObject


def connect(to_or_array, piopiy_no, option):
    if ((isNumber(piopiy_no)) and (isNumber(to_or_array) or isArray(to_or_array))):
        bridge = {'action': 'bridge', 'from': piopiy_no,
                  'connect': [], 'duration': 5400, 'timeout': 40, 'loop': 1}

        if isObject(option):

            bridge['duration'] = option.get('duration', 5400)
            bridge['timeout'] = option.get('timeout', 40)
            bridge['loop'] = option.get('loop', 1)

            if 'ring_type' in option and option['ring_type'] == 'group':
                bridge['ring_type'] = 'group'
         
        if (isNumber(to_or_array)):
            bridge['connect'].append({"type": "pstn", "number": to_or_array})
        else:
            for i in to_or_array:
                bridge['connect'].append({"type": "pstn", "number": i})

        return bridge

    else:
        raise NameError('invalid from or to number in bridge')
