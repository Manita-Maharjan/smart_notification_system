import re


def isValidPhone(value): 
    if value: 
        r = re.compile(r"[9][6-9]\d{8}$")
        if r.match(str(value)):
            return value
    return None

