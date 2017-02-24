from multiprocessing import Process, Queue
import signal, time

import capture_stream
import display_stimuli

def main():
  stimuli = Process(target=display_stimuli, args=())
  bci = Process(target=capture_stream, args=())
  stimuli.start()
  bci.start()

  time.sleep(5)
  
  stimuli.terminate()
  bci.terminate()

  stimuli.join()
  bci.join()

  input('press enter to terminate')
  cap.stop()
  ds.stop()

if __name__ == '__main__':
  main()
