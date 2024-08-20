import re

def isNumber(no):
    return isinstance(no, int)


def isString(val):
    return isinstance(val, str)


def isArray(val):
    return isinstance(val, list)


def isObject(obj):
    return isinstance(obj, dict)

def isWs(url):
    websocket_regex = re.compile(r'^(ws|wss)://')
    return bool(websocket_regex.match(url))

def isURL(url):
    # Regular expression to validate URL format
    url_pattern = re.compile(
        r'^(https?|ftp)://'       # Scheme
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Domain name
        r'localhost|'              # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IPv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6
        r'(?::\d+)?'                # Optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(url_pattern, url) is not None

def isIND(piopiy_no):

    number = str(piopiy_no)
    # Remove any leading or trailing whitespace
    number = number.strip()
    
    # Regular expression to check for Indian mobile numbers starting with '91'
    pattern = re.compile(r'^91[6789]\d{9}$')
    
    # Match the number with the pattern
    return bool(pattern.match(number))