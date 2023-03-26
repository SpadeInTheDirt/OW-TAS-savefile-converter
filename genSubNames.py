startingSubNum = (128 - 24)


for i in range(0, 24):
    subNum = startingSubNum + i
    print("{sub}: loadData{idx}".format(sub=subNum, idx=i) )
    #print("{sub}: loadData{idx}_1".format(sub=(subNum+1), idx=i) )
