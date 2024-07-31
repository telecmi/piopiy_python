import re

def isNumber(no):
    return isinstance(no, int)


def isString(val):
    return isinstance(val, str)


def isArray(val):
    return isinstance(val, list)


def isObject(obj):
    return isinstance(obj, dict)

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