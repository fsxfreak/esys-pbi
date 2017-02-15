from pylsl import StreamInlet, resolve_stream

def main():
  streams = resolve_stream('name', 'psychopy')
  inlet = StreamInlet(streams[0])

  while True:
    sample, timestamp = inlet.pull_sample()
    print(timestamp, sample)

if __name__ == '__main__':
  main()
