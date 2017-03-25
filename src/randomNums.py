import numpy as np
import random
from pylsl import StreamInfo, StreamOutlet
import time


info = StreamInfo('bci', 'randomData', 2, 100, 'float32', 'myuid34234')
#info = StreamInfo('bci')
outlet = StreamOutlet(info)

print("about to go into for loop")

for timestamp in range(0,10):
    sample = random.randint(0,10)
    data = [sample, timestamp]
    #data = [sample]
    outlet.push_sample(data)
    print(data)
    time.sleep(0.01)

print("finished sending data")


    
