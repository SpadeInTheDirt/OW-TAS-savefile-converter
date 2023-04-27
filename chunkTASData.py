import math

# NEW FUNCTIONS    --------------------------------------------------

def find_first_occurence(s, c):
    i = 0
    while i < len(s) and s[i] != c:
        i += 1
    return i

def remove_line_header(s):
    return s[ find_first_occurence(s, ']') + 2
              : len(s) ]

def read_word(s):
    return s[ 0
              : find_first_occurence(s, ' ') + 1]

def is_all_ws(s):
    has_non_ws = False
    for c in s:
        if c != ' ' or c != '\n':
            has_non_ws = True
            break
    
    return has_non_ws

# LEGACY FUNCTIONS --------------------------------------------------

# this function is stupid; does not consider if commas/brackets occur in strings
def splitAtLevel(s):
    arr = []
    
    bracketLevel = 0
    elemStart = 0

    for i in range(0, len(s)):
        if s[i] == '(':
            bracketLevel += 1
        elif s[i] == ')':
            bracketLevel -= 1
        elif bracketLevel == 0 and s[i] == ',':
            # print(s[0 : i] + " " + "{i}".format(i=bracketLevel))
            arr.append(s[elemStart:i])
            elemStart = i + 1
    
    # get last elem
    arr.append(s[elemStart:len(s)])
    return arr

def printSubroutine(subNum, part, data):
    print("rule(\""+"data {idx}.{part} SUBROUTINE".format(idx=subNum, part=part) + "\") {")
    if (part == 0):
        print("event { Subroutine; " + "loadData{subNum}".format(subNum=subNum) + "; } actions{")
        print("Global.data[{idx}] = {data};".format(idx=subNum, data=data))
    else:
        print("event { Subroutine; " + "loadData{subNum}_{part}".format(subNum=subNum, part=part) + "; } actions{")
        print("Modify Global Variable At Index(data, {idx}, Append To Array, {data});".format(idx=subNum, data=data))

    print("}}")

def listToString(elems):
    ret = "Array("
    for i in elems:
        ret += ("{elem},".format(elem=i))

    # trim last comma
    ret = ret[0:len(ret) - 1]
    ret += ")"

    return ret

def removeWhiteSpace(s):
    i = 0
    while i < len(s):
        if s[i].isspace():
            if (i == len(s) - 1):
                s = s[0:i]
            else:
                s = s[0:i] + s[i + 1:len(s)]
        else:
            i += 1
           
    
    return s

def formatNumberString(s):
    s = removeWhiteSpace(s)
    isNeg = (s[0] == '-')
    if isNeg:
        s = s[1 : len(s)]

    decimalIdx = -1
    for i in range(0, len(s)):
        if s[i] == '.':
            decimalIdx = i
            break
    
    zeroes = "0000000"
    if (decimalIdx >= 0):
        s1 = s[0 : decimalIdx]
        s2 = s[decimalIdx + 1 : len(s)]

        s1 = zeroes[0 : 4 - len(s1)] + s1
        s2 = s2 + zeroes[0 : 3 - len(s2)] 

        s = s1 + s2
    else:
        s = zeroes[0 : 4 - len(s)] + s + zeroes[0 : 3]
    
    if isNeg:
        s = '-' + s
    else:
        s = '+' + s

    return s

def unadjustedFormatString(s):
    return formatNumberString("{i}".format(i=1000 * float(s)))

def compressToStrings(s):
    strSize = 128
    vectors = splitAtLevel(removeBracketLevel(s))
    
    currStr = ""
    for i in vectors:
        vector = splitAtLevel(removeBracketLevel(i))
        # put nums in backwards
        for x in vector:
            #currStr = unadjustedFormatString(removeWhiteSpace(x)) + currStr
            currStr = formatNumberString(removeWhiteSpace(x)) + currStr
    
    ret = ""

    while currStr != "":
        if len(currStr) > strSize:
            ret = "\nCustom String(\"{s}\"),".format(s=currStr[len(currStr) - strSize:len(currStr)]) + ret
            currStr = currStr[0:len(currStr) - strSize]
        else:
            ret = "\nCustom String(\"{s}\"),".format(s=currStr[0:len(currStr)]) + ret
            currStr = ""

    ret = "Array({elems})".format(elems=ret[0:len(ret) - 1])
    return ret

# MAIN PROGRAM     --------------------------------------------------


class bot:
    def __init__(self, hero, team):
        self.hero = hero
        self.team = team
    
    def reset(self, firstPos, firstFac, firstWep, initButtonStates):
        self.throttles = [[firstPos]]
        self.throttleTimings = [[]]
        self.facings = [[firstFac]]
        self.facingTimings = [[]]
        self.weapon = [[]]
        self.weaponTimings = [[]]
        

while True:
    try:
        line = remove_line_header(input())
        
        if line:
            print(remove_line_header(line))
    except EOFError:
        break

def multBy1000(s):
    return "{i}".format(i=1000 * float(s))
