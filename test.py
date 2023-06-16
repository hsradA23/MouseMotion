import struct
import json
from torch import nn
import torch
file = open("/dev/input/mice", "rb")

class clf(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(clf, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        # Initialize the hidden and cell states
        h0 = torch.zeros(1, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(1, x.size(0), self.hidden_size).to(x.device)
        
        # Forward propagate through the LSTM layer
        out, _ = self.lstm(x, (h0, c0))
        
        # Reshape the output of the last LSTM step for classification
        out = out[:, -1, :]
        
        # Pass the output through the fully connected layer
        out = self.fc(out)
        
        return out

model = clf(2,256,26)
model.load_state_dict(torch.load('model.pt')) 
model.eval()




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

def get_pred(l):
    a = torch.FloatTensor(l)
    return torch.argmax(model(a.view(1,a.shape[0],2)))


print("Ready")
while True:
    (m1,m3,m2,x,y) = getMouseEvent()
    if( m1 == 0 and pm1 == 1):
        if(not recording):
            # print("Recording")
            recording = True
        else:
            # print("Stopped Recording")
            recording = False
            print(chr(97+get_pred(data).item()), end='', flush=True)
            data = []

    # Right click to break out of the program
    if( m2 == 0 and pm2 == 1):            
            break

    if(recording):
        data.append([x,y])

    pm1,pm2 = m1,m2
        

# Stop reading mouse
file.close() 
