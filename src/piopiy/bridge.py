from underscore import isString, isNumber, isArray, isObject


def connect(to, piopiy_no, option):
    if ((isNumber(piopiy_no)) and (isNumber(to) or isArray(to))):
        bridge = {'action': 'bridge', 'from': piopiy_no,
                  'connect': [], 'duration': 5400, 'timeout': 40, 'loop': 1}

        if isObject(option):

            for v in option:
                bridge[v] = option[v]
        if (isNumber(to)):
            bridge['connect'].append({"type": "pstn", "number": to})
        else:
            for i in to:
                bridge['connect'].append({"type": "pstn", "number": i})

        return bridge

    else:
        raise NameError('invalid from or to number in forward')
