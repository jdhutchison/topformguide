def getValue(dict, key):
    if type(key).__name__ == 'str':
        if key in dict:
            return dict[key]
    else:
        for k in key:
            if k in dict:
                return dict[k]

    return None

def getTokenFromValue(dict, key, token, splitOn=None):
    value = getValue(dict, key)
    if value is not None:
        tokens = []
        if splitOn is not None:
            tokens = str(value).split(splitOn)
        else:
            tokens = str(value).split()
        if len(tokens) > token:
            value = tokens[token]

    return value

def getTokenFromValueAsNumber(dict, key, token, splitOn=None, defaultToZero=False,parseFunction=int):
    value = getTokenFromValue(dict, key, token, splitOn)
    if value is not None:
        return parseFunction(value)
    elif defaultToZero:
        return 0
    else:
        return None

def getTokenFromValueAsInt(dict, key, token, splitOn=None, defaultToZero=False):
    return getTokenFromValueAsNumber(dict, key, token, splitOn, defaultToZero, int)

def getValueFromAnyKey(dict, keys):
    for key in keys:
        if key in dict:
            return dict[key]

    return None