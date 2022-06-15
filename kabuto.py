# coding: utf-8
# Your code here!
n = int(input())
s = input().rstrip().split(' ')
red = int(s[0])
green = int(s[1])
blue = int(s[2])
count = 0
place_kabuto

#"R", "G", "B", "Y", "M", "C", "W"
def move(place_kabuto, dir):
    if dir=='R':
        if place_kabuto!=3:
            return 1
        else:
            return 0
    elif dir=='L':
        if place_kabuto!=-3:
            return -1
        else:
            return 0
    
#"R", "G", "B", "Y", "M", "C", "W"
def light(name, dir):
    global red,green,blue
    if name=='R':
        red+=move(dir)
    elif name=='G':
        green+=move(dir)
    elif name=='B':
        blue+=move(dir)
    elif name=='Y':
        red+=move(dir)
        green+=move(dir)
    elif name=='M':
        red+=move(dir)
        blue+=move(dir)
    elif name=='C':
        green+=move(dir)
       blue+=move(dir)
    elif name=='W':
        red+=move(dir)
        green+=move(dir)
        blue+=move(dir)

        
for i in range(n):
    s = input().rstrip().split(' ')
    direct = s[0]
    color = s[1]
    print(red,blue,green)
    light(color,direct)
    if red==blue and blue==green and green==red:
        print(red)
        break
    if i>=n-1:
        print('no')