import cmd
import sys
import os
import math

STR_SIZE = 128
MAX_ARRAY_SIZE = 1000




'''
    finds the nth occurence of character c in s, returns it.
'''
def find_nth_occurence(s, c, n=0):
    occ = 0
    for i in range(0, len(s)):        
        if s[i] == c:
            if occ == n:
                break
            elif occ < n:
                occ += 1
    
    if i == len(s):
        return -1
    else:
        return i


'''
    removes all whitespace off a string and returns it (not just leading).
    whitespace includes newlines
'''
def remove_ws(s):
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


'''
    removes all leading whitespace off a string and returns it.
    whitespace includes newlines
'''
def remove_leading_ws(s):
    while len(s) and s[0].isspace():
        s = s[1 : len(s)]

    return s


'''
    returns s with a header removed. headers are in the form of "[...]". ... could be any string. 
    also removes the block of whitespace after the header. if no header exists, no change is made.
    header must be at very start of string; s[0] == '[' 
'''
def remove_line_header(s):
    if s == "":
        return s

    if s[0] == '[':
        s = s[ find_nth_occurence(s, ']') + 2 : len(s) ]
    return remove_leading_ws(s)


'''
    reads a word off of the start of s, returns the word and s after word has been removed. 
    word defined as block of non-ws chars.
    removes all the leading whitespace and separating whitespace between the word and rest of string

    ex. s = ' [hello)-  there-3 how...   are u '

    then read_word(s) gives '[hello)-' and 'there-3 how...   are u '
    ws includes newlines.
'''
def read_word(s):
    s = remove_leading_ws(s)
    ret = remove_ws(s[ 0 : find_nth_occurence(s, ' ') + 1])
    s = s[len(ret) : len(s)]

    if ret[0] == '"':

        while True:
            nextWord, s = read_word(s)
            quoteIndex = find_nth_occurence(nextWord, '"')
            ret = ret + ' ' + nextWord
            if quoteIndex == -1:
                break
        
        nextWord = read_word(s)
    
    return ret, remove_leading_ws(s)


'''
    finds and reads the next vector off of the start of s.
    removes everything before and including the end of the vector; 
    before next closing paren ')', then 
    returns vector as a tuple (idx 0 = x component, idx 1 = y, idx 2 = z)
    and the modified s
'''
def read_vector(s):
    # ret = s[1 : len(s) - 1].split(',')
    ret = [ float(x) for x in s[ find_nth_occurence(s, '(') + 1 : find_nth_occurence(s, ')') ].split(',') ]
    s = s[find_nth_occurence(s, ')') + 1 : len(s)]
    return tuple(ret), remove_leading_ws(s)


'''
    reads a word off of the start of s (removes 1 word from s in the process), tries to parse as a bool
    is stupid; does not care if word is neither "true" nor "false"
    not case sensitive

    returns the boolean and the modified s without its leading word.
'''
def parse_bool(s):
    word, s = read_word(s)
    word = remove_ws(word)

    if word.upper() == 'TRUE':
        return True
    
    return False


'''
    formats a list of values into a normal workshop array (count <= 1000). no fancy tricks
'''
def format_list(l):
    ret = "Array("
    for e in l:
        ret += ("{elem},".format(elem=e))

    # trim last comma
    ret = ret[0:len(ret) - 1]
    ret += ")"

    return ret


'''
    formats a list of values into a large workshop array (count possibly > 1000)
    workshop array is formatted as an main array of sub arrays. each sub array contains
    values in order and is of size <= 1000. the sub arrays are also in order.

    ex. given a list [0, 1, 2, ... ], 
        values 0, 1, ... 999 will be in subarray 0, ie mainarray[0] = [0, 1, ..., 999]
        values 1000, 1001, ... 1999 in subarray 1, ie mainarray[1] = [1000, 1001, ... 1999]
        etc.

    the limit of values stored in this structure is 1 000 000 values
'''
def format_large_list(l):
    listOfLists = []

    while (len(l) > MAX_ARRAY_SIZE):
        listOfLists.append(l[0 : MAX_ARRAY_SIZE])
        l = l[MAX_ARRAY_SIZE : len(l)]

    listOfLists.append(l)

    return format_list([ format_list(subList) for subList in listOfLists ])


'''
    formats a number into a string for compression.
    the string will be the sign followed by 7 digits.
    the 7 digits correspond to digits from 10^0 to 10^-6

    ex. -0.123456 -> "-0123456"
'''
def format_num(f):
    num = abs(int(1000 * round(f, 3)))
    
    return "{sign}{num:07}".format( 
        sign = ('-' if f < 0 else '+'),
        num = num
    )


'''
    formats a list of tuples (vectors) into a large (count possibly > 1000) 
    workshop array of string compressed vectors. strings are in reverse order;
    x component of first vector is at the end of the last string in the last array of strings,
    z component of last vector is at start of first string in first array of strings

    (array of strings because this is a large array (count possibly > 1000))
'''
def format_vectors(vectors):
    currStr = ""
    for vector in vectors:
        # put nums in backwards: mode will pop from top for efficiency
        for x in vector:
            # currStr = unadjusted_format_string(remove_ws(x)) + currStr
            currStr = format_num(x) + currStr
    
    stringArr = []

    while currStr != "":
        if len(currStr) > STR_SIZE:
            # chop STR_SIZE chars off the top of currStr and place it in the front of ret as a custom string
            stringArr.insert(0, "\nCustom String(\"{s}\")".format( s=currStr[ len(currStr) - STR_SIZE : len(currStr) ] ))
            currStr = currStr[ 0 : len(currStr) - STR_SIZE ]
        else:
            # put remainders into ret
            stringArr.insert(0, "\nCustom String(\"{s}\")".format(s=currStr[0:len(currStr)]))
            currStr = ""

    return format_large_list(stringArr)


'''
    converts a number to a team as in the inspector log format
'''
def num_to_team(n):
    match n:
        case 0:
            return "Team 1"
        case 1:
            return "Team 2"
        case 2:
            return "All Teams"
        case _:
            raise Exception("Invalid team number, {num} provided".format(num=n))


'''
    produces a subroutine given a string with a workshop array;
      - dataIdx is the index for where the bot's data will be stored,
        
      - part is the part in the data at dataIdx; 
        the data is split in parts bc of rule size limit, 
        each part appended together composes the bot's data at dataIdx 
'''
def to_subroutine(subNum, part, data):
    dataIdx = math.floor(subNum / 2)
    ret = "rule(\""+"data {idx}.{part} SUBROUTINE".format(idx=dataIdx, part=part) + "\") {"
    if (part == 0):
        ret += "event { Subroutine; " + "loadData{subNum}".format(subNum=subNum) + "; } actions{"
        ret += "Global.data[{idx}] = {data};".format(idx=dataIdx, data=data)
    else:
        ret += "event { Subroutine; " + "loadData{subNum}".format(subNum=subNum) + "; } actions{"
        ret += "Modify Global Variable At Index(data, {idx}, Append To Array, {data});".format(idx=dataIdx, data=data)

    ret += "}}"
    return ret


'''
    bot class is just a collection of data for a bot w/ 
    ways to modify their data corresponding to the inspector log format
'''
class Bot:
    def __init__(self, number, hero, team):
        self.number = number
        self.hero = hero
        self.team = team
        self.throttles = []
        self.throttleTimings = []
        self.facings = []
        self.facingTimings = []
        self.weapon = []
        self.weaponTimings = []
        self.initButtonStates = [False] * 10
        self.buttonTimings = [[] for i in range(10)]
        self.initPos = (0, 0, 0)
        self.initFac = (0, 0, 0)
        self.frameCount = 0

    def __str__(self):
        ret = "{team} {hero} bot\n".format(team=self.team, hero=self.hero)
        
        ret += str(self.throttles) + "\n"
        ret += str(self.throttleTimings) + "\n"
        
        ret += str(self.facings) + "\n"
        ret += str(self.facingTimings) + "\n"
        
        ret += str(self.weapon) + "\n"
        ret += str(self.weaponTimings) + "\n"
        
        ret += 'buttons: \n'
        for buttonTiming in self.buttonTimings:
            ret += str(buttonTiming) + "\n"
        
        ret += "init buttons: " + str(list((1 if (state) else 0) for state in self.initButtonStates)) + "\n"
        ret += "ipos {pos} ifac {fac}".format(pos=self.initPos, fac=self.initFac)
        return ret

    def convert(self): 
        part1 = [ 'Hero({hero})'.format(hero = self.hero) ]      # 0
        part1.append( self.team )                                # 1
        part1.append( format_vectors(self.throttles) )           # 2
        part1.append( format_large_list(self.throttleTimings) )  # 3
        part1 = format_list(part1)

        part2 = [ format_vectors(self.facings) ]                 # 4
        part2.append( format_large_list(self.facingTimings) )    # 5

        part2.append( format_list(self.initButtonStates) )       # 6
        part2.append( format_list([ format_large_list(buttonTiming) for buttonTiming in self.buttonTimings ]) ) # 7
        part2.append( format_large_list(self.weapon) )           # 8
        part2.append( format_large_list(self.weaponTimings) )    # 9
        part2.append( str(self.initFac[0]) )                     # 10
        part2.append( str(self.initFac[1]) )                     # 11
        part2.append( str(self.initFac[2]) )                     # 12
        part2.append( str(self.initPos[0]) )                     # 13
        part2.append( str(self.initPos[1]) )                     # 14
        part2.append( str(self.initPos[2]) )                     # 15
        part2.append( str(self.frameCount) )                     # 16
        part2 = format_list(part2)

        return (part1, part2)

    def reset(self, firstThr, firstFac, firstWep, initButtonStates):
        self.throttles = [firstThr]
        self.throttleTimings = []
        self.facings = [firstFac]
        self.facingTimings = []
        self.weapon = [firstWep]
        self.weaponTimings = []
        self.initButtonStates = initButtonStates
        self.buttonTimings = [[] for i in range(10)]
    
    def cut(self, throttleIndex, facingIndex, weaponIndex, buttonIndices):
        self.throttles = self.throttles[0 : throttleIndex]
        self.throttleTimings = self.throttleTimings[0 : throttleIndex]
        self.facings = self.facings[0 : facingIndex]
        self.facingTimings = self.facingTimings[0 : facingIndex]
        self.weapon = self.weaponTimings[0 : weaponIndex]
        self.weaponTimings = self.weaponTimings[0 : weaponIndex]
        for i in range(0, len(self.buttonTimings)):
            self.buttonTimings[i] = self.buttonTimings[i][0 : buttonIndices[i]]
    
    def app(self, varName, value, index = 0):
        match varName:
            case "thr":
                self.throttles.append(value)
            case "thrT":
                self.throttleTimings.append(value)
            case "fac":
                self.facings.append(value)
            case "facT":
                self.facingTimings.append(value)
            case "wep":
                self.weapon.append(value)
            case "wepT":
                self.weaponTimings.append(value)
            case "butT":
                self.buttonTimings[index].append(value)
            case _:
                raise Exception("Invalid var name for append")
    
    def set_init_pos(self, pos):
        self.initPos = pos
    
    def set_init_fac(self, fac):
        self.initFac = fac

    def set_hero(self, hero):
        self.hero = hero


    def set_frame_count(self, count):
        self.frameCount = count


class LogConverter(cmd.Cmd):
    bot = -1
    played_map = ""
    data = [None] * 48

    prompt = 'logcnvrt > '
    intro = 'Converting'

    def do_convert(self, arg=""):
        if not arg.isspace():
            botParts = [botPart.convert() for botPart in self.data if botPart]

            contents = ""
            subNum = 0
            for i in range(len(botParts)):
                contents += to_subroutine(subNum, 0, botParts[i][0])
                contents += "\n"
                contents += to_subroutine(subNum + 1, 1, botParts[i][1])
                contents += "\n"
                subNum += 2
            
            print(contents)
        
    def do_print(self, arg=""):
        print("Map: {map}".format(map=self.played_map))
        for bot in self.data:
            if bot:
                print(bot)

    def do_m(self, arg):
        self.played_map = arg
    
    def do_n(self, arg):
        args = arg.split()
        botnum = int(args[0])
        self.data[botnum] = Bot(botnum, args[1], num_to_team(int(args[2])))
        self.bot = int(args[0])

    def do_b(self, arg):
        args = arg.split()
        self.bot = int(args[0])

    def do_x(self, arg):
        self.data[self.bot] = None

    def do_r(self, arg):
        initThr, arg = read_vector(arg)
        initFac, arg = read_vector(arg)
        word, arg = read_word(arg)
        initWep = int(word)

        arg = arg[ find_nth_occurence(arg, '{') + 1 : find_nth_occurence(arg, '}') - 1 ]
        initButtonStates = [ parse_bool(x) for x in arg.split() ]

        self.data[self.bot].reset(initThr, initFac, initWep, initButtonStates)

    def do_c(self, arg):
        word, arg = read_word(arg)
        thrIdx = int(word)
        word, arg = read_word(arg)
        facIdx = int(word)
        word, arg = read_word(arg)
        wepIdx = int(word)
        arg = arg[find_nth_occurence(arg, '{') + 1 : find_nth_occurence(arg, '}') - 1]
        # print(arg.split())
        butIdxes = [ int(x) for x in arg.split() ]
        self.data[self.bot].cut(thrIdx, facIdx, wepIdx, butIdxes)

    def do_a(self, arg):
        var, arg = read_word(arg)
        if var == 'thr' or var == 'fac':
            # thr and fac given a vector
            val, arg = read_vector(arg)
            self.data[self.bot].app(var, val)
        elif var == 'butT':
            # butT given value and index
            args = arg.split()
            self.data[self.bot].app(var, int(args[0]), int(args[1]))
        else:
            # all other given just a number
            self.data[self.bot].app(var, int(arg))

    def do_p(self, arg):
        # print(arg)
        pos, arg = read_vector(arg)
        self.data[self.bot].set_init_pos(pos)

    def do_f(self, arg):
        fac, arg = read_vector(arg)
        self.data[self.bot].set_init_fac(fac)
    
    def do_h(self, arg):
        self.data[self.bot].set_hero(arg)

    def do_t(self, arg):
        count = int(arg)
        self.data[self.bot].set_frame_count(count)

    def do_EOF(self, arg=""):
        self.do_print()
        return True

'''
def processCommand(s):
    command, s = read_word(s)

    match command:
        case 'm':
            played_map = s
        case 'n':
            botNumber, s = read_word(s)
            botNumber = int(botNumber)
            
            data[botNUmber] = Bot(botNumber, hero, team)
        case 'b':
            print()
        case 'x':
            print()
        case 'r':
            print()
        case 'c':
            print()
        case 'a':
            print()
        case 'p':
            print()
        case 'f':
            print()
'''

converter = LogConverter()

if len(sys.argv) > 3:
    print("Wrong number of arguments! Provide one filename only.")
    quit(1)
elif len(sys.argv) >= 2:
    try:
        logfile = open(sys.argv[1])
    except IOError:
        print("Failed to open file!")
        quit(2)

    logfile.seek(0, os.SEEK_END)
    filesize = logfile.tell()
    logfile.seek(0, os.SEEK_SET)
else:
    converter.cmdloop()
    
while logfile.tell() != filesize:
    try:
        line = remove_line_header(logfile.readline())
        if line != "" and not line.isspace():
            #print(line[0 : len(line) - 1])
            converter.onecmd(line)
    except EOFError:
        break

logfile.close()

converter.do_convert()

