from pylsl import StreamInlet, resolve_stream

running = True 
inlet = None

def load():
  streams = resolve_stream('name', 'psychopy')
  inlet = StreamInlet(streams[0])

def start():
  if inlet is None:
    print('load() the stream first.')
    raise TypeError

  while running:
    sample, timestamp = inlet.pull_sample()
    print(timestamp, sample)

def stop():
  running = False

def main():
  streams = resolve_stream('name', 'psychopy')
  inlet = StreamInlet(streams[0])

  while running:
    sample, timestamp = inlet.pull_sample()
    print(timestamp, sample)

if __name__ == '__main__':
  main()
