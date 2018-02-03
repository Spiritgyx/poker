import itertools
carts=[]
cd=[]
cm=[]
file=open("input.txt", mode="r")
for st in file:
    m,k=st.split(",")
    m,k=int(m),int(k)
    cd.append(k)
    cm.append(m)
    carts.append([m,k])
file.close()
print("Массив достоинств: ", cd)
print("Массив карт: ", carts)
parax2 = 0
parax = 0
nomer=-1
set3=0
nomeraseta = []
#Первый раз проходим, parax2 = 1, count = 2
#Второй раз проходим, parax2 = 2, count = 2
#Третий раз проходим, parax2 = 3, count = 2
#Четвертый раз проходим, parax2 = 4, count = 2
combo = {0:None,1:None,2:[None,None],3:None,4:[None,None],5:None,6:[None,None],7:None,8:None,9:None}
#0:старшая карта 1:пара 2:две пары 3:сет 4:стрит 5:флеш 6:фулл хаус 7:каре 8:стрит флеш 9:флеш рояль
nepara = []
for i in cd:#проходим массив cd, i = достоинству карты, проходим его количество элементов раз
     count=cd.count(i)# количество повторений данного достоинства
     if count == 2:#пара
         combo[1] = i

     elif count == 3:#сет
         combo[3] = i
         for j in range(7):
             if cd[j] == combo[3]:
                 nomeraseta.append(j)

     elif count == 4:#каре
         combo[7] = i
#две пары
print("nomeraseta: ",nomeraseta)
for i in range(len(cd)):
    if cd[i] != combo[1]:
        nepara.append(cd[i])
print("nepara :", nepara)
for i in nepara:
    count = nepara.count(i)
    if count == 2:
        combo[2] = [combo[1], i]

nomeraneseta = []
neset = []
#Фулл хаус
for i in range(len(cd)):
    if cd[i] != combo[3]:
        neset.append(cd[i])
for i in neset:
    count = neset.count(i)
    if count == 2:
        combo[6] = [combo[3], i]
print("nomeraneseta: ", nomeraneseta)

#Флеш
for i in cm:
    count = cm.count(i)
    if count == 5:
        combo[5] = i
#стрит(пять последовательно расположенных карт)
strit = []#сюда входят достоинства из стрита
a = -1
nomera = []
for p in itertools.permutations(cd):
    for j in range(12):
        if ((p[0] == j) and (p[1] == j+1) and (p[2] == j+2) and (p[3] == j+3) and (p[4] == j+4)):
            print(p)
            if p[0] > a:
                a = p[0]
                combo[4] = [a, p[4]]
                for i in range(5):
                    strit.append(p[i])

print("strit",strit)

for i in range(len(cd)):
    if cd[i] == a:
        nomera.append(i)
    elif cd[i] == (a+1):
        nomera.append(i)
    elif cd[i] == (a+2):
        nomera.append(i)
    elif cd[i] == (a+3):
        nomera.append(i)
    elif cd[i] == (a+4):
        nomera.append(i)
print("nomera",nomera)
nestrik = []
for i in range(len(cd)):
    if cd[i] > (a+4):
        nestrik.append(cd[i])



nomerastrita = []
for i in range(5):
    for j in range(5):
        if cd[i] == strit[j]:
            nomerastrita.append(i)
print("nomerastrita", nomerastrita)

#стрит флеш

print(combo)
exit(0)

'''
carts=[]
cd=[]
cm=[]
file=open("input.txt", mode="r")
for st in file:
    m,k=st.split(",")
    m,k=int(m),int(k)
    cd.append(k)
    cm.append(m)
    carts.append([m,k])
file.close()
print(cd)
print(carts)
parax2 = 0
parax = 0
nomer=-1
set3=0
#Первый раз проходим, parax2 = 1, count = 2
#Второй раз проходим, parax2 = 2, count = 2
#Третий раз проходим, parax2 = 3, count = 2
#Четвертый раз проходим, parax2 = 4, count = 2
combo = {0:None,1:None,2:[None,None],3:None,4:None,5:None,6:[None,None],7:None,8:None,9:None}
for i in cd:#проходим массив ck, i = достоинству карты, проходим его количество элементов раз
     count=cd.count(i)# количество повторений данного достоинства
     parax2 += 1 if count == 2 else 0# Если два повторения данного достоинства(пара), то к parax2 прибавляется 1
     set3 += 1 if count == 3 else 0# Если три повторения данного достоинства(сет), то к set3 прибавляется 1
     if count == 1:# Если одно повторение данного достоинства, то
         if combo[0] is None:#
             combo[0] = i#
         elif combo[0] < i:#
             combo[0] = i#
     elif count == 2:#Если два повторения данного достоинства(пара), то
         if parax2 == 2:#Если пара обнаружлась повторно, то
             combo[1] = i#combo[1] присваевается значение достонства карты
         elif parax2 == 4:#Если две пары (любые), то
             combo[2]=[combo[1], i]#combo[2] =[combo[1](достоинство повторно обнаруженной пары)], i(последнее достоинство пары)
     elif count == 3:#
         if set3 == 3:#
             combo[3] = i#
     elif parax == 4:#
         combo[7] = i#
if (set3 == 3) and (parax2 == 2):
    combo[6]=[combo[3],combo[1]]

print(combo)
exit(0)

'''





'''
for i in range(7):
    if cd[0] == j:
        if cd[1] == j+1:
            if cd[2] == j+2:
                if cd[3] == j+3:
                    if cd[4] == j+4:
                        if cd[5] == j+5:
                            print("Стрит")
                        if cd[6] == j+6:
                            print("Стрит")
                    if cd[5] == j+4:
                        if cd[4] == j+5:
                            print("Стрит")
                        if cd[6] == j+6:
                            print("Стрит")
                    if cd[6] == j+4:
                        if cd[4] == j+5:
                            print("Стрит")
                        if cd[5] == j+6:
                            print("Стрит")
                if cd[4] == j+3:
                    if cd[3] == j+4:
                        if cd[5] == j+5:
                            print("Стрит")
                        if cd[6] == j+6:
                            print("Стрит")
                    if cd[5] == j+4:
                        if cd[3] == j+5:
                            print("Стрит")
                        if cd[6] == j+6:
                            print("Стрит")
                    if cd[6] == j+4:
                        if cd[3] == j+5:
                            print("Стрит")
                        if cd[5] == j+6:
                            print("Стрит")
                if cd[5] == j+3:
                    if cd[3] == j+4:
                        if cd[4] == j+5:
                            print("Стрит")
                        if cd[6] == j+6:
                            print("Стрит")
                    if cd[4] == j+4:
                        if cd[3] == j+5:
                            print("Стрит")
                        if cd[6] == j+6:
                            print("Стрит")
                    if cd[6] == j+4:
                        if cd[3] == j+5:
                            print("Стрит")
                        if cd[4] == j+6:
                            print("Стрит")
                if cd[6] == j+3:
                    if cd[3] == j+4:
                        if cd[4] == j+5:
                            print("Стрит")
                        if cd[5] == j+6:
                            print("Стрит")
                    if cd[4] == j+4:
                        if cd[3] == j+5:
                            print("Стрит")
                        if cd[5] == j+6:
                            print("Стрит")
                    if cd[5] == j+4:
                        if cd[3] == j+5:
                            print("Стрит")
                        if cd[4] == j+6:
                            print("Стрит")
'''
