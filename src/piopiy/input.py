from underscore import isString, isNumber, isArray, isObject


def input(action_url, option):
    if (isString(action_url)):
        input = {
            "action": "input",
            "action_url": action_url
        }

        if isObject(option):

            for v in option:
                input[v] = option[v]

        return input

    else:
        raise NameError('invalid action_url in input')
