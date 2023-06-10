import cmd

def compress_num(f):
    num = abs(int(1000 * round(f, 3)))
    
    return "{sign}{num:07}".format( 
        sign = ('-' if f < 0 else '+'),
        num = num
    )

while True:
    print(compress_num(float(input())))

k = [[] for x in range(0, 5)]
k[0].append(21)
print(k)

print(' '[1 : 1])
print('   '.split())
s = input()
ret = s[1 : len(s) - 1].split(',')

print(ret)
print(bool('False'))

class CommandProcessor(cmd.Cmd):
    def do_greet(self, line):
        print("hello")
    
    def do_EOF(self, line):
        return True

CommandProcessor().cmdloop()