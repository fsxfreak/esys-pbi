from pylsl import StreamInlet, resolve_stream
import open_bci_v3 as bci

running = True 
inlet = None
board = None

details = []
data = []
NUM_CHANNELS = 8
bci_dataFile = ""
bci_stimulusFile = "" 


def load():
  streams = resolve_stream('name', 'psychopy')
  inlet = StreamInlet(streams[0])

  board = bci.OpenBCIBoard(port='/dev/ttyUSB0', filter_data=True, daisy=False)
  print (board.getNbEEGChannels(), "EEG channels and", 
      board.getNbAUXChannels(), "AUX channels at", 
      board.getSampleRate(), "Hz.")

def saveFile(data,details):
  for i in len(data):
    bci_dataFile = ' '.join(map(str,data(i)))
    f.write(bci_dataFile)
    f.write("\n")

    bci_stimulusFile = ' '.join(map(str(details)))
    f.write(bci_stimulusFile)
    f.write("\n")

def recordSample(details,sample,timestamp)
    details.append(( timestamp, sample))

def handleSample(sample):
  channels = sample.channel_data[0:NUM_CHANNELS]
  channels.append(str(datetime.now()))
  data.append(channels)

def start():
  if inlet is None:
    print('load() the stream first.')
    raise TypeError

  board.start_streaming(handleSample)

  while running:
    sample, timestamp = inlet.pull_sample()
    recordSample(details,sample,timestamp)
    print(timestamp, sample)

def stop():
  running = False
  saveFile(data,details)
  board.disconnect()

def main():
  load()
  start()


if __name__ == '__main__':
  main()
