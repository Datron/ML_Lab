import csv

# s find algorithm
with open('data.csv','r') as f:
    reader = csv.reader(f)
    dlist = list(reader)
    
h = [['0','0','0','0','0','0']]
print("Data input is:")
for l in dlist:
    print(l)
print("Training Data:")
for i in dlist:
    if i[-1] == "True":
        print(i)
        j = 0
        for x in i:
            if x != "True":
                if x != h[0][j] and h[0][j] == '0':
                    h[0][j] = x
                elif x != h[0][j] and h[0][j] != '0':
                    h[0][j] = '?'
                else:
                    pass
            j = j+1
print("Most specific hypothesis is:")
print(h)
