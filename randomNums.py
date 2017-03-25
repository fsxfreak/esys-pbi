mport numpy as np
import random
from pylsl import StreamInfo, StreamOutlet


info  = StreamInfo('bci')
outlet = StreamOutlet(info)

for timestamp in range(0,1000):
    sample = random.randint(0,1000)
    data = [sample, timestamp]
    outlet.push_sample(data)
    time.sleep(0.01)

 print("sending data now")


    
