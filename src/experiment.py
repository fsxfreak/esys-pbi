from multiprocessing import Process, Queue
import signal, time, sys

from time import sleep

import capture_bci
import capture_pupil
import display_stimuli

def main():
  stim_queue = Queue()
  bci_queue = Queue()
  pupil_queue = Queue()

  stimuli = Process(target=display_stimuli.begin, args=((stim_queue), ))
  bci = Process(target=capture_bci.begin, args=((bci_queue), ))
  pupil = Process(target=capture_puil.begin, args=((pupil_queue), ))

  stimuli.start()
  print('Waiting a bit for the stimuli to load...')
  time.sleep(1)
  print('Initializing sensors...')
  bci.start()
  pupil.start()

  bci_ready = False
  pupil_ready = False

  # Wait for the sensors to initialize before starting the experiment
  while True:
    bci_msg = bci_queue.get()
    pupil_msg = pupil_queue.get()
    print('bci_msg', bci_msg)
    print('pupil_msg', pupil_msg)

    if bci_msg == 'CONNECTED':
      bci_ready = True
    elif bci_msg == 'FAIL':
      stimuli.terminate()
      bci.terminate()
      pupil.terminate()
      sys.exit(-1)

    if pupil_msg == 'CONNECTED':
      pupil_ready = True
    elif pupil_msg == 'FAIL':
      stimuli.terminate()
      bci.terminate()
      pupil.terminate()
      sys.exit(-1)

    if bci_ready and pupil_ready:
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
  pupil.terminate()

  stimuli.join()
  bci.join()
  pupil.join()

if __name__ == '__main__':
  main()
