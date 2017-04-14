from multiprocessing import Process, Queue, Event
import signal, time, sys

from time import sleep

import capture_bci
import capture_pupil
import display_stimuli
import graph_realtime

def stop():
  print('Stopping all programs.')

def sigint_handler(signal, frame):
  stop()

def main():
  signal.signal(signal.SIGINT, sigint_handler)

  stim_queue = Queue()
  bci_queue = Queue()
  pupil_queue = Queue()

  stimuli = Process(target=display_stimuli.begin, args=((stim_queue), ))
  bci = Process(target=capture_bci.begin, args=((bci_queue), ))
  pupil = Process(target=capture_puil.begin, args=((pupil_queue), ))
  graph = Process(target=graph_realtime.begin, args=((None), ))

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
      print('BCI connected, starting realtime graph...')
      graph.start()
    elif pupil_msg == 'CONNECTED':
      pupil_ready = True
    elif bci_msg == 'FAIL':
      stimuli.terminate()
      bci.terminate()
      pupil.terminate()
      graph.terminate()

      sys.exit(-1)
    elif pupil_msg == 'FAIL':
      stimuli.terminate()
      bci.terminate()
      pupil.terminate()
      graph.terminate()

      sys.exit(-1)

    # TODO wait for pupil_ready?
    if bci_ready:
      stim_queue.put('BEGIN')
      break

  # Wait for the stimuli to finish displaying before stopping sensor capture
  while True:
    try:
      stim_msg = stim_queue.get()
      print('stim', stim_msg)
    except InterruptedError:
      stop()
      break

    if (stim_msg == 'FINISHED'):
      stop()
      break

  print('Terminating from the main thread...')
  stimuli.terminate()
  bci.terminate()
  pupil.terminate()
  graph.terminate()

  stimuli.join()
  bci.join()
  pupil.join()
  graph.join()

if __name__ == '__main__':
  main()
