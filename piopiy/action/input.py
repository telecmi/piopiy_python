from piopiy.underscore import isString, isURL, isObject


def input(action_url, option):
    if (isURL(action_url)):
        input = {
            "action": "input",
            "action_url": action_url
        }

        if isObject(option):
            input['max_digit'] = option.get('max_digit', 1)
            input['timeout'] = option.get('timeout', 5)
        return input

    else:
        raise NameError('invalid action_url in input')

def play_input(action_url,music_file,option):
    if (isURL(action_url) and isString(music_file)):
        input = {
            "action": "play_get_input",
            "action_url": action_url,
            "file_name": music_file
        }

        if isURL(music_file):
            input['file_url'] = music_file

        if isObject(option):
            input['max_digit'] = option.get('max_digit', 1)
            input['max_retry'] = option.get('max_retry', 3)
            input['timeout'] = option.get('timeout', 5)
        return input

    else:
        raise NameError('invalid action_url or music_file in input')