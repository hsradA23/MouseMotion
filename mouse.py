import struct
import json
file = open("/dev/input/mice", "rb")

def getMouseEvent():
    buf = file.read(3)
    button = buf[0]
    bLeft = button & 0x1
    bMiddle = (button & 0x4) > 0
    bRight = (button & 0x2) > 0
    x,y = struct.unpack("bb", buf[1:])
    #print("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight,x,y))
    return (bLeft,bMiddle,bRight,x,y)

recording = False
pm1 = 0
pm2 = 0
data = []

o = []
n = 0
badPerf = 'jkwxz'
letter = badPerf[0]
idx = 0
while True:
    (m1,m3,m2,x,y) = getMouseEvent()
    if( m1 == 0 and pm1 == 1):
        if(not recording):
            print("Recording")
            recording = True
        else:
            print("Stopped Recording",n+1)
            n = n+1
            recording = False
            o.append({'data':data, 'letter': letter})
            data = []
            if(n == 5):
                 idx += 1
                 if(idx == len(badPerf)): break
                 letter = badPerf[idx]
                 print(letter)
                 n=0
                 

    # Right click to break out of the program
    if( m2 == 0 and pm2 == 1):            
            break

    if(recording):
        data.append([x,y])

    pm1,pm2 = m1,m2
        

# Stop reading mouse
file.close() 

# Write to disc
ds = open('dataset2.json', "a")
ds.write(json.dumps(o))
ds.close()