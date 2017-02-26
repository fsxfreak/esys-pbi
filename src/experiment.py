from multiprocessing import Process, Queue
import signal, time, sys

import capture_stream
import display_stimuli

def main():
  stim_queue = Queue()
  bci_queue = Queue()

  stimuli = Process(target=display_stimuli.begin, args=((stim_queue), ))
  bci = Process(target=capture_stream.begin, args=((bci_queue), ))

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

    # TODO in future put more sensors here

    if bci_ready:
      stim_queue.put('BEGIN')
      break

  # Wait for the stimuli to finish displaying before stopping sensor capture
  while True:
    stim_msg = stim_queue.get()
    print('stim', stim_msg)

    if (stim_msg == 'FINISHED'):
      break

  print('Terminating from the main thread...')
  stimuli.terminate()
  bci.terminate()

  stimuli.join()
  bci.join()

if __name__ == '__main__':
  main()
