import re


class Scanner:
    def __init__(self, data):
        self.data = data


PUNCTUATION = "|/\\;*()%:<>[]{}#$^&~='\"?,# "

# next : next -> next
# return the first token of the given string `s` after splitting `s` using give regexpr
def next(s):
    return re.split(r'[ \|/\\;*()%:<>[\]{}#$^&~=\'"?,# \s]\s*', s)[0]


# peek : scanner -> (or/c number string)
# Read the next token of input, leaving it on the input.
def peek(st):
    return peekHelper(st, False)


# pop : scanner -> (or/c number string)
# Read the next token of input, consuming from the input.
def pop(st):
    return peekHelper(st, True)


# peekHelper : scanner, boolean -> (or/c number string)
# Return the next token, either consuming it or not.
def peekHelper(s, consume):
    temp = s.data.lstrip()
    if not temp:
        return None
    elif temp[0] in PUNCTUATION:
        if consume: s.data = temp[1:]
        return temp[0]
    elif re.match('[+-]?[0-9.]*$', next(temp)):
        if consume: s.data = temp[len(next(temp)):]
        f = float(next(temp))
        return int(f) if f.is_integer() else f
    elif re.match('[a-zA-z]+', next(temp)):
        if consume: s.data = temp[len(next(temp)):]
        return next(temp)
