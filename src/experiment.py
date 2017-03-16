from multiprocessing import Process, Queue, Event
import signal, time, sys

from time import sleep

import capture_bci
import display_stimuli

def main():
  stim_queue = Queue()
  bci_queue = Queue()

  stimuli = Process(target=display_stimuli.begin, args=((stim_queue), ))

  event = Event()
  bci = Process(target=capture_bci.begin, args=((bci_queue), (event)))


  stimuli.start()
  print('Waiting a bit for the stimuli to load...')
  time.sleep(1)
  print('Initializing sensors...')
  bci.start()

  bci_ready = False

  # Wait for the sensors to initialize before starting the experiment
  while True:
    bci_msg = bci_queue.get()
    print('bci_msg', bci_msg)

    if bci_msg == 'CONNECTED':
      bci_ready = True
    elif bci_msg == 'FAIL':
      stimuli.terminate()
      bci.terminate()
      sys.exit(-1)

    if bci_ready:
      stim_queue.put('BEGIN')
      break

  # Wait for the stimuli to finish displaying before stopping sensor capture
  while True:
    stim_msg = stim_queue.get()
    print('stim', stim_msg)

    if (stim_msg == 'FINISHED'):
      event.set()
      break

  print('Terminating from the main thread...')
  stimuli.terminate()
  #bci.terminate()

  stimuli.join()
  bci.join()

if __name__ == '__main__':
  main()
