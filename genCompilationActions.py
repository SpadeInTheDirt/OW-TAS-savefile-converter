startingSubNum = 80
print("actions{")

for i in range(0, 24):
    subNum = startingSubNum + 2 * i
    print("Call Subroutine(loadData{idx});".format(idx=i) )
    #print("Call Subroutine(loadData{idx}_1);".format(idx=i) )

print("}")